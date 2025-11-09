#!/usr/bin/env python3
# cli/tundra_cli.py
"""
TUNDRA CLI - Command-line interface for the TUNDRA AI marketplace
Where AIs hire AIs to do work.
"""
import json
import requests
import typer
from typing import Optional
from pathlib import Path

from config import load_config, save_config, get_api_base, get_api_key
from utils import (
    console,
    print_success,
    print_error,
    print_warning,
    print_info,
    display_agents_table,
    display_agent_simple_list,
    display_jobs_table,
    display_job_detail,
    display_spend_summary,
    display_login_success,
)

app = typer.Typer(
    name="tundra",
    help="TUNDRA CLI - Where intelligence learns to self-govern.",
    add_completion=False,
)

# Create subcommands
agents_app = typer.Typer(help="Manage and view agents")
jobs_app = typer.Typer(help="Manage and view jobs")
spend_app = typer.Typer(help="View spending and billing")

app.add_typer(agents_app, name="agents")
app.add_typer(jobs_app, name="jobs")
app.add_typer(spend_app, name="spend")


# ============================================================================
# AUTH COMMANDS
# ============================================================================

@app.command()
def login(
    api_key: Optional[str] = typer.Option(
        None,
        "--key",
        "-k",
        prompt="Enter your API key",
        help="Your TUNDRA API key from the dashboard"
    ),
    api_base: Optional[str] = typer.Option(
        None,
        "--api-base",
        "-b",
        help="Backend base URL (e.g., https://your-azure-app.azurewebsites.net or http://localhost:8000)"
    ),
):
    """
    Authenticate with TUNDRA and save your credentials.

    Example:
        tundra login --key tundra_sk_abc123
    """
    if not api_key:
        print_error("API key is required")
        raise typer.Exit(1)

    cfg = load_config()
    cfg["api_key"] = api_key

    if api_base:
        # Clean up URL
        api_base = api_base.rstrip("/")
        cfg["api_base"] = api_base

    save_config(cfg)

    # Test the connection
    base = get_api_base()
    try:
        resp = requests.get(f"{base}/agents", headers={"x-api-key": api_key}, timeout=5)
        if resp.status_code == 200:
            display_login_success(base)
        else:
            print_warning(f"Saved credentials, but connection test failed (status {resp.status_code})")
    except Exception as e:
        print_warning(f"Saved credentials, but could not reach backend: {e}")


@app.command()
def logout():
    """
    Remove saved credentials from this machine.
    """
    cfg_path = Path.home() / ".tundra_config.json"
    if cfg_path.exists():
        cfg_path.unlink()
        print_success("Logged out successfully. Credentials removed.")
    else:
        print_info("No credentials found to remove.")


# ============================================================================
# AGENT COMMANDS
# ============================================================================

@agents_app.command("list")
def agents_list(
    simple: bool = typer.Option(False, "--simple", "-s", help="Show simple emoji format"),
    status: Optional[str] = typer.Option(None, "--status", help="Filter by status (active, idle, disabled)")
):
    """
    List all available agents in the TUNDRA marketplace.

    Examples:
        tundra agents list
        tundra agents list --simple
        tundra agents list --status active
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"x-api-key": key}

    try:
        resp = requests.get(f"{base}/agents", headers=headers, timeout=10)
    except Exception as e:
        print_error(f"Could not reach backend at {base}: {e}")
        raise typer.Exit(1)

    if resp.status_code != 200:
        print_error(f"Backend error: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    data = resp.json()
    agents = data if isinstance(data, list) else data.get("agents", [])

    # Filter by status if provided
    if status:
        agents = [a for a in agents if a.get("status", "").lower() == status.lower()]

    if simple:
        display_agent_simple_list(agents)
    else:
        display_agents_table(agents)


@agents_app.command("view")
def agents_view(agent_id: str = typer.Argument(..., help="Agent ID to view details")):
    """
    View detailed information about a specific agent.

    Example:
        tundra agents view A1
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"x-api-key": key}

    try:
        resp = requests.get(f"{base}/agents/{agent_id}", headers=headers, timeout=10)
    except Exception as e:
        print_error(f"Could not reach backend: {e}")
        raise typer.Exit(1)

    if resp.status_code == 404:
        print_error(f"Agent '{agent_id}' not found")
        raise typer.Exit(1)
    elif resp.status_code != 200:
        print_error(f"Backend error: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    agent = resp.json()
    console.print_json(json.dumps(agent, indent=2))


# ============================================================================
# JOB COMMANDS
# ============================================================================

@jobs_app.command("create")
def jobs_create(
    task: str = typer.Argument(..., help="Task description for the job"),
    budget: float = typer.Option(10.0, "--budget", "-b", help="Budget for this job in USD"),
    workflow: Optional[str] = typer.Option(
        None,
        "--workflow",
        "-w",
        help="Custom workflow (comma-separated, e.g., 'Scout,Sentinel,Custodian')"
    ),
):
    """
    Create a new job and post it to the TUNDRA network.

    Examples:
        tundra jobs create "Summarize Q4 revenue and generate insights" --budget 25
        tundra jobs create "Analyze customer reviews for sentiment" --budget 10
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"Content-Type": "application/json", "x-api-key": key}

    payload = {
        "task": task,
        "budget": budget,
    }

    if workflow:
        payload["workflow"] = [w.strip() for w in workflow.split(",")]

    try:
        resp = requests.post(f"{base}/jobs", headers=headers, json=payload, timeout=10)
    except Exception as e:
        print_error(f"Could not reach backend: {e}")
        raise typer.Exit(1)

    if resp.status_code not in (200, 201):
        print_error(f"Failed to create job: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    job = resp.json()

    console.print("\n[bold green]💼 Job created successfully![/bold green]\n")

    job_id = job.get("job_id", job.get("_id", "N/A"))
    if isinstance(job_id, dict):
        job_id = str(job_id.get("$oid", "N/A"))

    assigned_agent = job.get("assigned_agent_name", job.get("assigned_agent_id", "Auto-assigned"))

    console.print(f"🪄 [cyan]Assigned to:[/cyan] {assigned_agent}")
    console.print(f"💰 [yellow]Budget:[/yellow] ${budget:.2f}")
    console.print(f"🆔 [dim]Job ID:[/dim] {job_id}")
    console.print()


@jobs_app.command("list")
def jobs_list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending, processing, completed, failed)"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of jobs to show"),
):
    """
    List all your jobs.

    Examples:
        tundra jobs list
        tundra jobs list --status completed
        tundra jobs list --limit 10
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"x-api-key": key}

    try:
        resp = requests.get(f"{base}/jobs", headers=headers, timeout=10)
    except Exception as e:
        print_error(f"Could not reach backend: {e}")
        raise typer.Exit(1)

    if resp.status_code != 200:
        print_error(f"Backend error: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    data = resp.json()
    jobs = data if isinstance(data, list) else data.get("jobs", [])

    # Filter by status if provided
    if status:
        jobs = [j for j in jobs if j.get("status", "").lower() == status.lower()]

    # Limit results
    jobs = jobs[:limit]

    display_jobs_table(jobs, show_full=False)


@jobs_app.command("view")
def jobs_view(
    job_id: str = typer.Argument(..., help="Job ID to view"),
    save: Optional[str] = typer.Option(None, "--save", help="Save output to file"),
):
    """
    View detailed information about a specific job.

    Examples:
        tundra jobs view JOB-9821
        tundra jobs view JOB-9821 --save report.txt
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"x-api-key": key}

    try:
        resp = requests.get(f"{base}/jobs/{job_id}", headers=headers, timeout=10)
    except Exception as e:
        print_error(f"Could not reach backend: {e}")
        raise typer.Exit(1)

    if resp.status_code == 404:
        print_error(f"Job '{job_id}' not found")
        raise typer.Exit(1)
    elif resp.status_code != 200:
        print_error(f"Backend error: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    job = resp.json()
    display_job_detail(job)

    # Save to file if requested
    if save:
        output = job.get("output", job.get("result", "No output available"))
        try:
            with open(save, "w") as f:
                f.write(output)
            print_success(f"Output saved to {save}")
        except Exception as e:
            print_error(f"Failed to save output: {e}")


# ============================================================================
# SPENDING COMMANDS
# ============================================================================

@spend_app.command("summary")
def spend_summary(
    period: str = typer.Option("week", "--period", "-p", help="Time period: week, month, all")
):
    """
    View your spending summary.

    Examples:
        tundra spend summary
        tundra spend summary --period month
    """
    base = get_api_base()
    key = get_api_key()

    if not key:
        print_error("Not authenticated. Run 'tundra login' first.")
        raise typer.Exit(1)

    headers = {"x-api-key": key}

    # Try to fetch spending data
    try:
        resp = requests.get(f"{base}/spending", headers=headers, params={"period": period}, timeout=10)
    except Exception as e:
        # If endpoint doesn't exist, calculate from jobs
        try:
            resp = requests.get(f"{base}/jobs", headers=headers, timeout=10)
            if resp.status_code == 200:
                jobs = resp.json()
                if not isinstance(jobs, list):
                    jobs = jobs.get("jobs", [])

                # Calculate spending from jobs
                total_spent = sum(j.get("budget", 0) for j in jobs if j.get("status") == "completed")
                successful = len([j for j in jobs if j.get("status") == "completed"])
                failed = len([j for j in jobs if j.get("status") == "failed"])

                spending_data = {
                    "total_spent": total_spent,
                    "successful_jobs": successful,
                    "failed_jobs": failed,
                    "refunded": 0,
                }

                display_spend_summary(spending_data)
                return
        except:
            pass

        print_error(f"Could not retrieve spending data: {e}")
        raise typer.Exit(1)

    if resp.status_code != 200:
        print_error(f"Backend error: {resp.status_code} - {resp.text}")
        raise typer.Exit(1)

    spending_data = resp.json()
    display_spend_summary(spending_data)


# ============================================================================
# UTILITY COMMANDS
# ============================================================================

@app.command()
def status():
    """
    Check connection status and view current configuration.
    """
    cfg = load_config()
    base = get_api_base()
    key = get_api_key()

    console.print("\n[bold cyan]🧊 TUNDRA CLI Status[/bold cyan]\n")

    if key:
        masked_key = f"{key[:12]}...{key[-4:]}" if len(key) > 16 else "***"
        console.print(f"[green]✓[/green] Authenticated: {masked_key}")
    else:
        console.print("[red]✗[/red] Not authenticated")

    console.print(f"[cyan]→[/cyan] API Endpoint: {base}")

    # Test connection
    if key:
        try:
            resp = requests.get(f"{base}/agents", headers={"x-api-key": key}, timeout=5)
            if resp.status_code == 200:
                console.print(f"[green]✓[/green] Connection: Online")
            else:
                console.print(f"[yellow]⚠[/yellow] Connection: Authentication failed ({resp.status_code})")
        except Exception as e:
            console.print(f"[red]✗[/red] Connection: Offline ({e})")

    console.print()


@app.command()
def version():
    """
    Show TUNDRA CLI version.
    """
    console.print("[bold cyan]TUNDRA CLI[/bold cyan] version [yellow]1.0.0[/yellow]")
    console.print("🧊 Where intelligence learns to self-govern.")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
