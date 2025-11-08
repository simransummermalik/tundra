import time
import random
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue, Event

class AgentExecutor:

    def __init__(self, name: str):
        self.name = name

    def execute(self, request: RequestContext, queue: EventQueue):
        queue.push(Event(type="message", message=f"{self.name} received request: {request.task_type}"))
        queue.push(Event(type="status_update", message="Agent logic not yet implemented"))
        return {"status": "not_implemented"}

class WebScraperExecutor(AgentExecutor):

    def execute(self, request: RequestContext, queue: EventQueue):
        url = request.payload.get("url", "unknown")
        queue.push(Event(type="message", message=f"Starting web scrape for {url}"))

        queue.push(Event(type="status_update", message="Connecting to website..."))
        time.sleep(1.5)

        queue.push(Event(type="status_update", message="Extracting pricing information..."))
        time.sleep(2)

        result = {
            "prices": [
                {"tier": "basic", "price": random.randint(20, 35)},
                {"tier": "pro", "price": random.randint(45, 60)}
            ],
            "currency": "USD",
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        queue.push(Event(type="result", message=f"Scraping completed successfully for {url}", metadata=result))
        request.mark_completed()
        return result
