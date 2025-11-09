# db/routing_agent.py
"""
Routing AI - The "Scout" that finds the best agent for a job
"""

import os
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API (free tier)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class RoutingAgent:
    """
    The Scout AI that analyzes incoming jobs and matches them to the best agent
    """

    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def find_best_agent(
        self,
        task_description: str,
        task_type: Optional[str],
        available_agents: List[Dict]
    ) -> Dict:
        """
        Use LLM to analyze the task and pick the best agent from MongoDB

        Args:
            task_description: What the user wants done
            task_type: Optional hint like "web_scrape"
            available_agents: List of agents from MongoDB with their capabilities

        Returns:
            Dict with selected agent and reasoning
        """

        # Build prompt for Gemini
        agent_list = "\n".join([
            f"- Agent ID: {agent.get('_id')}\n"
            f"  Name: {agent.get('name')}\n"
            f"  Capabilities: {', '.join(agent.get('capabilities', []))}\n"
            f"  Success Rate: {agent.get('success_rate', 0)}%\n"
            f"  Avg Latency: {agent.get('average_latency_ms', 0)}ms\n"
            f"  Region: {agent.get('region')}\n"
            f"  Status: {agent.get('status')}\n"
            for agent in available_agents
        ])

        prompt = f"""You are TUNDRA's Routing AI. Your job is to match tasks to the best available AI agent.

TASK DETAILS:
- Task Type: {task_type or 'unspecified'}
- Description: {task_description}

AVAILABLE AGENTS:
{agent_list}

INSTRUCTIONS:
1. Analyze the task requirements
2. Match capabilities to the task (e.g., "web_scrape" needs web scraping capability)
3. Consider success rate, latency, and agent status
4. Pick the BEST agent for this specific job
5. If no agent matches, return "no_match"

RESPOND IN THIS EXACT JSON FORMAT (no markdown):
{{
  "agent_id": "the MongoDB _id of the selected agent OR no_match",
  "agent_name": "name of the agent OR null",
  "confidence": 0.95,
  "reasoning": "Why this agent is best suited for the task"
}}
"""

        # Call Gemini
        response = self.model.generate_content(prompt)
        result_text = response.text.strip()

        # Parse JSON response
        import json
        # Remove markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]

        result = json.loads(result_text.strip())
        return result


    def validate_task_type(self, task_type: str, agent_capabilities: List[str]) -> bool:
        """
        Simple capability matching (before LLM call to filter candidates)
        """
        task_to_capability = {
            "web_scrape": ["web_scraping", "data_extraction", "scraping"],
            "summarize": ["text_summarization", "summarization", "nlp"],
            "validate": ["data_validation", "compliance", "validation"],
            "code_review": ["code_review", "security_analysis", "code_analysis"],
            "image_analysis": ["image_classification", "computer_vision", "ocr"],
        }

        required_caps = task_to_capability.get(task_type, [])
        if not required_caps:
            return True  # If unknown task type, let LLM decide

        # Check if agent has any of the required capabilities
        agent_caps_lower = [cap.lower().replace(" ", "_") for cap in agent_capabilities]
        return any(req_cap in agent_caps_lower for req_cap in required_caps)
