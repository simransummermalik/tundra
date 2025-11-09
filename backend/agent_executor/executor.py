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
import sys


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
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            page.set_default_navigation_timeout(60000)
            page.set_default_timeout(60000)

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_load_state("load")
            page.wait_for_selector("body", state="attached", timeout=10000)
            page.wait_for_timeout(1500)

            content = page.content()
            browser.close()

            return BeautifulSoup(content, "html.parser")

    async def scrape_page(self, url: str):
        loop = asyncio.get_running_loop()
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
            temperature=0,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)

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

    def __init__(self, name: str):
        super().__init__(name)

        self.llm_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-05-01-preview"
        )

    async def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received sentiment analysis request"))

        payload = request.payload or {}
        text = payload.get("text") or (request.goal or "")

        symbol = payload.get("symbol")
        goal_lower = (request.goal or "").lower()
        if not symbol:
            if "tesla" in goal_lower:
                symbol = "TSLA"
            elif "apple" in goal_lower:
                symbol = "AAPL"
            elif "google" in goal_lower or "alphabet" in goal_lower:
                symbol = "GOOGL"
            elif "amazon" in goal_lower:
                symbol = "AMZN"
            elif "microsoft" in goal_lower:
                symbol = "MSFT"
            elif "nvidia" in goal_lower:
                symbol = "NVDA"

        if not symbol:
            queue.push(Event(type="status_update", message="Detecting ticker symbol from question"))
            sysp = (
                "You extract US stock ticker symbols. Return JSON with one field: "
                "{'symbol': '<TICKER>'} using the primary US exchange ticker. If uncertain, return {'symbol': null}."
            )
            resp = self.llm_client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": sysp},
                    {"role": "user", "content": request.goal or text}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            detected = json.loads(resp.choices[0].message.content)
            if detected.get("symbol"):
                symbol = detected.get("symbol").upper()
                queue.push(Event(type="status_update", message=f"Detected symbol: {symbol}"))
            else:
                queue.push(Event(type="status_update", message="No symbol detected; analyzing without live market data"))

        scraped = None
        url = payload.get("url")
        if not url and symbol:
            url = f"https://finance.yahoo.com/quote/{symbol}"

        if url:
            queue.push(Event(type="delegation", message="Delegated to WebScraperAgent", metadata={"url": url, "symbol": symbol}))
            print(f"[{self.name}] delegating to WebScraperAgent url={url} symbol={symbol}")
            ws = WebScraperExecutor(name="WebScraperAgent")
            ws_req = RequestContext(task_type="web_scrape", payload={"url": url}, goal=f"Collect current market data for {symbol or url}")
            scraped = await ws.execute(ws_req, queue)
            queue.push(Event(type="status_update", message="Received market data from WebScraperAgent"))

        analysis_input = {
            "user_question": text,
            "symbol": symbol,
            "scrape_result": scraped
        }
        data_summary = json.dumps(analysis_input, indent=2)

        system_prompt = """You are an expert financial analyst specializing in stock sentiment analysis.

Analyze the user's question and any provided market data to determine:
1. Overall sentiment (strongly_positive, positive, neutral, negative, strongly_negative)
2. Confidence score (0.0 to 1.0)
3. Investment recommendation (buy/sell/hold with reasoning)
4. What additional data would improve the analysis

Return a JSON object with this structure:
{
  "sentiment": "positive|negative|neutral|strongly_positive|strongly_negative",
  "confidence_score": 0.85,
  "recommendation": "Buy/Sell/Hold with detailed reasoning",
  "reasoning": "Detailed analysis",
  "key_factors": ["factor 1", "factor 2"],
  "needs_additional_data": true/false,
  "requested_data": ["specific data needed"],
  "risk_level": "low|medium|high",
  "time_horizon": "short-term|medium-term|long-term"
}"""

        user_prompt = f"""Input for analysis:

{data_summary}
"""

        response = self.llm_client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )

        ai_result = json.loads(response.choices[0].message.content)

        result = {
            "sentiment": ai_result.get("sentiment", "neutral"),
            "confidence_score": ai_result.get("confidence_score", 0.5),
            "recommendation": ai_result.get("recommendation", "No recommendation"),
            "reasoning": ai_result.get("reasoning", ""),
            "key_factors": ai_result.get("key_factors", []),
            "needs_additional_data": ai_result.get("needs_additional_data", True),
            "requested_data": ai_result.get("requested_data", []),
            "risk_level": ai_result.get("risk_level", "unknown"),
            "time_horizon": ai_result.get("time_horizon", "unknown"),
            "symbol": symbol,
            "scrape_used": bool(scraped),
            "analyzed_at": datetime.now(timezone.utc).isoformat()
        }

        queue.push(Event(type="result", message="Sentiment analysis completed", metadata=result))
        request.mark_completed()
        return result
