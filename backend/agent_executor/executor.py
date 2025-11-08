import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from context import RequestContext
from event_queue import EventQueue, Event


class AgentExecutor:

    def __init__(self, name: str):
        self.name = name

    def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received request: {request.task_type}"))
        queue.push(Event(type="status_update", message="Agent logic not yet implemented"))
        return {"status": "not_implemented"}


class WebScraperExecutor(AgentExecutor):

    async def scrape_page(self, url: str):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")

    def extract_prices(self, soup: BeautifulSoup):
        price_tags = soup.select("[class*='price'], [id*='price'], [class*='plan']")
        prices = []

        for tag in price_tags:
            text = tag.get_text(strip=True)
            if any(char.isdigit() for char in text):
                prices.append(text)

        unique_prices = list(set(prices))
        return unique_prices if unique_prices else ["No pricing info found"]

    async def run(self, request: RequestContext, queue: EventQueue):
        url = request.payload.get("url", "unknown")
        queue.push(Event(type="message", message=f"Starting web scrape for {url}"))
        queue.push(Event(type="status_update", message="Connecting to website..."))

        soup = await self.scrape_page(url)
        queue.push(Event(type="status_update", message="Extracting pricing information..."))
        prices = self.extract_prices(soup)

        result = {
            "url": url,
            "prices": prices,
            "scraped_at": datetime.now(timezone.utc).isoformat()
        }

        queue.push(Event(type="result", message=f"Scraping completed successfully for {url}", metadata=result))
        request.mark_completed()
        return result

    def execute(self, request: RequestContext, queue: EventQueue):
        import asyncio
        return asyncio.run(self.run(request, queue))
