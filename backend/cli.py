#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tundra CLI - Command-line interface for Tundra A2A marketplace
"""
import click
import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import time

# Fix Windows encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Configuration
CONFIG_DIR = Path.home() / ".tundra"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_API_URL = "http://localhost:8000"


class TundraConfig:
    """Manage Tundra CLI configuration"""

    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"api_url": DEFAULT_API_URL, "api_key": None, "user_id": None}

    def save_config(self):
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def set_api_key(self, api_key, user_id):
        """Set API key in configuration"""
        self.config["api_key"] = api_key
        self.config["user_id"] = user_id
        self.save_config()

    def get_api_key(self):
        """Get API key from configuration"""
        return self.config.get("api_key")

    def get_user_id(self):
        """Get user ID from configuration"""
        return self.config.get("user_id")

    def get_api_url(self):
        """Get API URL from configuration"""
        return self.config.get("api_url", DEFAULT_API_URL)

    def set_api_url(self, url):
        """Set API URL in configuration"""
        self.config["api_url"] = url
        self.save_config()

    def clear(self):
        """Clear configuration"""
        self.config = {"api_url": DEFAULT_API_URL, "api_key": None, "user_id": None}
        self.save_config()


config = TundraConfig()


def get_headers():
    """Get headers with API key for requests"""
    api_key = config.get_api_key()
    if not api_key:
        click.echo("[ERROR] Not authenticated. Please run 'tundra login' or 'tundra register' first.", err=True)
        raise click.Abort()
    return {"X-API-Key": api_key, "Content-Type": "application/json"}


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Tundra CLI - A2A marketplace command-line interface"""
    pass


@cli.command()
def welcome():
    """Welcome to Tundra - Get started guide"""
    click.echo("\n" + "="*60)
    click.echo("     WELCOME TO TUNDRA CLI")
    click.echo("     A2A Marketplace Command-Line Interface")
    click.echo("="*60 + "\n")

    click.echo("GETTING STARTED:")
    click.echo("-" * 60)

    # Check if user is logged in
    if config.get_api_key():
        click.echo(f"[OK] You are logged in as: {config.get_user_id()}\n")
        click.echo("QUICK COMMANDS:")
        click.echo("  tundra whoami          - View your account & stats")
        click.echo("  tundra jobs            - List your recent jobs")
        click.echo("  tundra scrape <url>    - Scrape a website")
        click.echo("  tundra sentiment <txt> - Analyze sentiment")
    else:
        click.echo("[INFO] You are not logged in yet.\n")
        click.echo("TO GET STARTED:")
        click.echo("  1. Register: tundra register")
        click.echo("     - Enter username and password when prompted")
        click.echo("     - You'll be logged in automatically")
        click.echo("")
        click.echo("  2. Or Login:  tundra login")
        click.echo("     - If you already have an account\n")

    click.echo("\nALL COMMANDS:")
    click.echo("-" * 60)
    click.echo("Authentication:")
    click.echo("  tundra register        - Create new account")
    click.echo("  tundra login           - Login to existing account")
    click.echo("  tundra logout          - Logout and revoke API key")
    click.echo("  tundra whoami          - Show account info")

    click.echo("\nAgent Operations:")
    click.echo("  tundra scrape <url>    - Scrape website data")
    click.echo("  tundra sentiment <txt> - Analyze text sentiment")
    click.echo("  tundra execute <task>  - Execute custom task")
    click.echo("  tundra orchestrate <q> - Multi-agent workflow")

    click.echo("\nJob Management:")
    click.echo("  tundra jobs            - List your jobs")
    click.echo("  tundra job <task>      - Submit job to queue")
    click.echo("  tundra status <id>     - Check job status")

    click.echo("\nUtilities:")
    click.echo("  tundra health          - Check API status")
    click.echo("  tundra config-show     - Show configuration")
    click.echo("  tundra --help          - Full help")
    click.echo("  tundra --version       - Show version")

    click.echo("\n" + "="*60)
    click.echo("Need help? Run: tundra --help")
    click.echo("="*60 + "\n")


@cli.command()
def register():
    """Register a new user with username and password"""
    try:
        username = click.prompt("Username")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

        api_url = config.get_api_url()
        response = requests.post(
            f"{api_url}/auth/register",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            config.set_api_key(data["api_key"], data["user_id"])
            click.echo(f"\n[OK] Registration successful!")
            click.echo(f"User: Username: {data['user_id']}")
            click.echo(f"\n You are now logged in and ready to use Tundra!")
        elif response.status_code == 400:
            click.echo(f"\n[ERROR] {response.json()['detail']}", err=True)
            click.echo(f"Tip: Use 'tundra login' if you already have an account.", err=True)
        else:
            click.echo(f"\n[ERROR] Registration failed: {response.text}", err=True)
    except requests.exceptions.ConnectionError:
        click.echo(f"\n[ERROR] Cannot connect to Tundra API at {config.get_api_url()}", err=True)
        click.echo(f"Tip: Make sure the backend is running with: uvicorn main:app --reload", err=True)
    except Exception as e:
        click.echo(f"\n[ERROR] Error: {str(e)}", err=True)


@cli.command()
def login():
    """Login with username and password"""
    try:
        username = click.prompt("Username")
        password = click.prompt("Password", hide_input=True)

        api_url = config.get_api_url()
        response = requests.post(
            f"{api_url}/auth/login",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            config.set_api_key(data["api_key"], data["user_id"])
            click.echo(f"\n[OK] Login successful!")
            click.echo(f"User: Welcome back, {data['user_id']}!")
        elif response.status_code == 401:
            click.echo(f"\n[ERROR] Invalid username or password", err=True)
        else:
            click.echo(f"\n[ERROR] Login failed: {response.text}", err=True)
    except requests.exceptions.ConnectionError:
        click.echo(f"\n[ERROR] Cannot connect to Tundra API at {config.get_api_url()}", err=True)
        click.echo(f"Tip: Make sure the backend is running with: uvicorn main:app --reload", err=True)
    except Exception as e:
        click.echo(f"\n[ERROR] Error: {str(e)}", err=True)


@cli.command()
def logout():
    """Logout and revoke API key"""
    try:
        api_url = config.get_api_url()
        headers = get_headers()
        response = requests.delete(f"{api_url}/auth/revoke", headers=headers)

        if response.status_code == 200:
            user_id = config.get_user_id()
            config.clear()
            click.echo(f"[OK] Logged out successfully!")
            click.echo(f"🔒 API key for user '{user_id}' has been revoked.")
        else:
            click.echo(f"[ERROR] Logout failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
def whoami():
    """Show current user information and stats"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        response = requests.get(f"{api_url}/me", headers=headers)

        if response.status_code == 200:
            data = response.json()
            click.echo(f"\nUser: User: {data['user_id']}")
            click.echo(f"Joined: Joined: {data.get('created_at', 'N/A')}")

            if data.get('api_key_last_used'):
                click.echo(f"Last Active: Last Active: {data['api_key_last_used']}")

            click.echo(f"\nStats: Your Stats:")
            stats = data.get('stats', {})
            click.echo(f"   Total Jobs: {stats.get('total_jobs', 0)}")
            click.echo(f"   Pending: {stats.get('pending_jobs', 0)}")
            click.echo(f"   Completed: {stats.get('completed_jobs', 0)}")
        else:
            click.echo(f"[ERROR] Failed to get user info: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.option('--limit', default=10, help='Number of jobs to show')
def jobs(limit):
    """List your recent jobs"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        response = requests.get(f"{api_url}/jobs?limit={limit}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            jobs_list = data.get('jobs', [])

            if not jobs_list:
                click.echo("\n[EMPTY] No jobs yet. Submit your first job with 'tundra job <task>'")
                return

            click.echo(f"\nJobs: Your Recent Jobs ({len(jobs_list)} shown):\n")

            for i, job in enumerate(jobs_list, 1):
                status_emoji = {
                    'pending': '[PENDING]',
                    'completed': '[OK]',
                    'failed': '[ERROR]'
                }.get(job.get('status'), '[RUNNING]')

                click.echo(f"{i}. {status_emoji} {job.get('task', 'N/A')}")
                click.echo(f"   Job ID: {job.get('job_id', 'N/A')}")
                click.echo(f"   Status: {job.get('status', 'N/A')}")
                click.echo(f"   Created: {job.get('created_at', 'N/A')}")
                if job.get('agent_used'):
                    click.echo(f"   Agent: {job.get('agent_used')}")
                click.echo()

            click.echo(f"Tip: View job details: tundra status <job_id>")
        else:
            click.echo(f"[ERROR] Failed to get jobs: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('job_id')
def status(job_id):
    """Get status and results of a specific job"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        response = requests.get(f"{api_url}/jobs/{job_id}", headers=headers)

        if response.status_code == 200:
            job = response.json()

            status_emoji = {
                'pending': '[PENDING]',
                'completed': '[OK]',
                'failed': '[ERROR]'
            }.get(job.get('status'), '[RUNNING]')

            click.echo(f"\n{status_emoji} Job Status: {job.get('status', 'N/A')}")
            click.echo(f"\nJobs: Job Details:")
            click.echo(f"   ID: {job.get('job_id', 'N/A')}")
            click.echo(f"   Task: {job.get('task', 'N/A')}")
            click.echo(f"   Created: {job.get('created_at', 'N/A')}")

            if job.get('agent_used'):
                click.echo(f"   Agent: {job.get('agent_used')}")

            if job.get('finished_at'):
                click.echo(f"   Finished: {job.get('finished_at')}")

            if job.get('reasoning'):
                click.echo(f"\nTip: Reasoning: {job.get('reasoning')}")

            if job.get('output'):
                click.echo(f"\nOutput: Output:")
                click.echo(json.dumps(job['output'], indent=2))

        elif response.status_code == 404:
            click.echo(f"\n[ERROR] Job not found. Check the job ID.", err=True)
        else:
            click.echo(f"\n[ERROR] Failed to get job status: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('task')
@click.option('--url', help='URL to scrape or analyze')
@click.option('--wait', is_flag=True, help='Wait for job completion and show results')
def job(task, url, wait):
    """Submit a job to the Tundra agent queue"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        payload = {"task": task}
        if url:
            payload["url"] = url

        response = requests.post(f"{api_url}/submit_job", headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            click.echo(f"[OK] Job submitted successfully!")
            click.echo(f"ID: Job ID: {data['job_id']}")
            click.echo(f"Stats: Status: {data['status']}")

            if wait:
                click.echo(f"\n[PENDING] Waiting for job completion...")
                job_id = data['job_id']
                # Note: You'll need to implement a /job/{job_id} endpoint to check status
                click.echo(f"Tip: Use 'tundra status {job_id}' to check job status")
        else:
            click.echo(f"[ERROR] Job submission failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('task')
@click.option('--url', help='URL to scrape or analyze')
@click.option('--text', help='Text to analyze')
@click.option('--goal', help='Goal or objective for the task')
def execute(task, url, text, goal):
    """Execute a task immediately (synchronous)"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        payload = {}
        if url:
            payload["url"] = url
        if text:
            payload["text"] = text

        request_data = {
            "task_type": task,
            "payload": payload,
            "goal": goal or task
        }

        click.echo(f" Executing task: {task}")
        response = requests.post(f"{api_url}/execute", headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            click.echo(f"\n[OK] Task completed successfully!")
            click.echo(f"\nStats: Tundra Agent Decision:")
            click.echo(f"   Agent: {data['selected_agent']}")
            click.echo(f"   Task Type: {data['task_type']}")
            click.echo(f"   Reasoning: {data['tundra_agent_decision'].get('reasoning', 'N/A')}")

            click.echo(f"\nOutput: Result:")
            click.echo(json.dumps(data['result'], indent=2))

            if data.get('events'):
                click.echo(f"\nJobs: Events ({len(data['events'])} total):")
                for i, event in enumerate(data['events'][:5], 1):
                    click.echo(f"   {i}. {event.get('type', 'N/A')}: {event.get('message', 'N/A')}")
        else:
            click.echo(f"[ERROR] Execution failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('url')
@click.option('--goal', help='What data to extract from the page')
def scrape(url, goal):
    """Scrape data from a URL using the WebScraper agent"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        request_data = {
            "task_type": "web_scrape",
            "payload": {"url": url},
            "goal": goal or f"Scrape data from {url}"
        }

        click.echo(f" Scraping URL: {url}")
        if goal:
            click.echo(f" Goal: {goal}")

        response = requests.post(f"{api_url}/execute", headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            click.echo(f"\n[OK] Scraping completed!")

            click.echo(f"\nOutput: Extracted Data:")
            click.echo(json.dumps(data['result'], indent=2))
        else:
            click.echo(f"[ERROR] Scraping failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('text')
def sentiment(text):
    """Analyze sentiment of text"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        request_data = {
            "task_type": "sentiment_analysis",
            "payload": {"text": text},
            "goal": f"Analyze sentiment of: {text[:50]}..."
        }

        click.echo(f"🔍 Analyzing sentiment...")

        response = requests.post(f"{api_url}/execute", headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            result = data['result']

            click.echo(f"\n[OK] Sentiment Analysis Complete!")
            click.echo(f"\nStats: Sentiment: {result.get('sentiment', 'N/A')}")
            click.echo(f"📈 Score: {result.get('score', 'N/A')}")

            if result.get('details'):
                click.echo(f"\nOutput: Details:")
                click.echo(json.dumps(result['details'], indent=2))
        else:
            click.echo(f"[ERROR] Sentiment analysis failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('query')
def orchestrate(query):
    """Execute a complex query with multi-agent orchestration"""
    try:
        headers = get_headers()
        api_url = config.get_api_url()

        click.echo(f"🎭 Orchestrating agents for query: {query}")

        response = requests.post(
            f"{api_url}/orchestrate?user_query={query}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()

            click.echo(f"\n[OK] Orchestration Complete!")
            click.echo(f"\nStats: Tundra Decision:")
            click.echo(f"   Agent: {data['tundra_decision'].get('agent', 'N/A')}")
            click.echo(f"   Task Type: {data['tundra_decision'].get('task_type', 'N/A')}")
            click.echo(f"   Reasoning: {data['tundra_decision'].get('reasoning', 'N/A')}")

            click.echo(f"\n Agents Used: {data['total_agents_used']}")

            click.echo(f"\nJobs: Orchestration Log:")
            for step in data['orchestration_log']:
                click.echo(f"\n   Step {step['step']}: {step['agent']}")
                click.echo(f"   Action: {step['action']}")

            click.echo(f"\nOutput: Final Result:")
            click.echo(json.dumps(data['final_result'], indent=2))
        else:
            click.echo(f"[ERROR] Orchestration failed: {response.text}", err=True)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


@cli.command()
@click.argument('url')
def config_set_url(url):
    """Set the API URL for the Tundra backend"""
    config.set_api_url(url)
    click.echo(f"[OK] API URL set to: {url}")


@cli.command()
def config_show():
    """Show current configuration"""
    click.echo("⚙️  Tundra Configuration:")
    click.echo(f"\n API URL: {config.get_api_url()}")
    click.echo(f"Jobs: User ID: {config.get_user_id() or 'Not set'}")

    api_key = config.get_api_key()
    if api_key:
        click.echo(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}")
    else:
        click.echo(f"🔑 API Key: Not set")

    click.echo(f"\n📁 Config file: {config.config_file}")


@cli.command()
def health():
    """Check if the Tundra API is running"""
    try:
        api_url = config.get_api_url()
        response = requests.get(f"{api_url}/health")

        if response.status_code == 200:
            click.echo(f"[OK] Tundra API is healthy!")
            click.echo(f" API URL: {api_url}")
            click.echo(f"Stats: Status: {response.json()}")
        else:
            click.echo(f"⚠️  API returned status code: {response.status_code}", err=True)
    except requests.exceptions.ConnectionError:
        click.echo(f"[ERROR] Cannot connect to Tundra API at {config.get_api_url()}", err=True)
        click.echo(f"Tip: Make sure the backend is running with: uvicorn main:app --reload", err=True)
    except Exception as e:
        click.echo(f"[ERROR] Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
