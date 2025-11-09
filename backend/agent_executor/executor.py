from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue, Event
from openai import AzureOpenAI
import asyncio
import os
import json
import re
from concurrent.futures import ThreadPoolExecutor


class AgentExecutor:

    def __init__(self, name: str):
        self.name = name

    def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received request: {request.task_type}"))
        queue.push(Event(type="status_update", message="Agent logic not yet implemented"))
        return {"status": "not_implemented"}


class WebScraperExecutor(AgentExecutor):

    def __init__(self, name: str):
        super().__init__(name)
        self.llm_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-05-01-preview"
        )
        self.executor = ThreadPoolExecutor(max_workers=3)

    def _scrape_page_sync(self, url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            content = page.content()
            browser.close()

            return BeautifulSoup(content, "html.parser")

    async def scrape_page(self, url: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._scrape_page_sync, url)

    def clean_text(self, soup: BeautifulSoup):
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript']):
            tag.decompose()

        main_content = soup.find('main') or soup.find('article') or soup.find('body') or soup

        text = main_content.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text

    def extract_data_with_llm(self, soup: BeautifulSoup, user_goal: str, url: str):
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "No title"

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""

        text_content = self.clean_text(soup)
        text_content = text_content[:12000] if len(text_content) > 12000 else text_content

        system_prompt = (
            "You are an expert web data extraction assistant. Extract specific information from webpage content based on the user's goal.\n\n"
            "IMPORTANT RULES:\n"
            "1. Extract actual data values, not placeholders\n"
            "2. For prices: include currency symbol and exact amount\n"
            "3. For stocks: extract current price, change, volume, market cap, etc.\n"
            "4. Return clean, structured JSON with relevant fields\n"
            "5. If data is unavailable, return specific error message\n\n"
            "Example outputs:\n"
            "Stock: {\"symbol\":\"TSLA\",\"price\":\"$245.67\",\"change\":\"-2.3%\",\"volume\":\"125M\",\"market_cap\":\"$780B\"}\n"
            "Pricing: {\"plan\":\"Pro\",\"price\":\"$20/month\",\"features\":[\"feature1\",\"feature2\"]}\n"
            "Product: {\"name\":\"Product X\",\"price\":\"$99.99\",\"rating\":\"4.5/5\",\"availability\":\"In Stock\"}\n\n"
            "Extract real values from the content provided."
        )

        context_parts = [f"URL: {url}", f"Title: {title_text}"]
        if description:
            context_parts.append(f"Description: {description}")

        context_parts.append(f"Page Content:\n{text_content}")

        user_prompt = f"User's Goal: {user_goal}\n\n" + "\n\n".join(context_parts)

        response = self.llm_client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )

        llm_response = response.choices[0].message.content.strip()

        if llm_response.startswith("```json"):
            llm_response = llm_response[7:]
        if llm_response.startswith("```"):
            llm_response = llm_response[3:]
        if llm_response.endswith("```"):
            llm_response = llm_response[:-3]

        extracted_data = json.loads(llm_response.strip())
        return extracted_data

    async def execute(self, request: RequestContext, queue: EventQueue):
        url = request.payload.get("url", "unknown")
        user_goal = request.goal or "Extract relevant information from this webpage"

        queue.push(Event(type="message", message=f"Starting intelligent web scrape for: {url}"))
        queue.push(Event(type="status_update", message=f"User goal: {user_goal}"))
        queue.push(Event(type="status_update", message="Connecting to website..."))

        soup = await self.scrape_page(url)

        queue.push(Event(type="status_update", message="Page retrieved successfully"))
        queue.push(Event(type="status_update", message="Analyzing content with LLM..."))

        extracted_data = self.extract_data_with_llm(soup, user_goal, url)

        result = {
            "url": url,
            "user_goal": user_goal,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "extracted_data": extracted_data
        }

        queue.push(Event(type="result", message=f"Scraping completed successfully for {url}", metadata=result))
        request.mark_completed()
        return result


class SummarizerExecutor(AgentExecutor):

    def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received summarization request"))

        data = request.payload.get("data", "")
        max_length = request.payload.get("max_length", 200)

        if not data:
            result = {"error": "No data provided to summarize"}
        else:
            summary = data[:max_length] + "..." if len(data) > max_length else data
            result = {
                "summary": summary,
                "original_length": len(data),
                "summarized_length": len(summary),
                "summarized_at": datetime.now(timezone.utc).isoformat()
            }

        queue.push(Event(type="result", message="Summarization completed", metadata=result))
        request.mark_completed()
        return result


class SentimentExecutor(AgentExecutor):

    def analyze_sentiment(self, text: str):
        positive_keywords = ["gain", "profit", "growth", "success", "increase", "up", "bullish", "surge"]
        negative_keywords = ["loss", "decline", "fall", "drop", "crash", "down", "bearish", "plunge"]

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)

        if positive_count > negative_count:
            sentiment = "positive"
            score = min(1.0, positive_count / (positive_count + negative_count + 1))
        elif negative_count > positive_count:
            sentiment = "negative"
            score = min(1.0, negative_count / (positive_count + negative_count + 1))
        else:
            sentiment = "neutral"
            score = 0.5

        return {
            "sentiment": sentiment,
            "confidence_score": round(score, 2),
            "positive_indicators": positive_count,
            "negative_indicators": negative_count
        }

    def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received sentiment analysis request"))

        text = request.payload.get("text", "")

        if not text:
            result = {"error": "No text provided for sentiment analysis"}
        else:
            sentiment_result = self.analyze_sentiment(text)
            result = {
                **sentiment_result,
                "analyzed_at": datetime.now(timezone.utc).isoformat()
            }

        queue.push(Event(type="result", message="Sentiment analysis completed", metadata=result))
        request.mark_completed()
        return result
