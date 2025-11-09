# cli/utils.py
"""
Utility functions for TUNDRA CLI - formatting, display helpers, etc.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from typing import Dict, List, Any

console = Console()


def print_success(message: str):
    """Print a success message with checkmark"""
    console.print(f" {message}", style="bold green")


def print_error(message: str):
    """Print an error message with X mark"""
    console.print(f"L {message}", style="bold red")


def print_warning(message: str):
    """Print a warning message"""
    console.print(f"   {message}", style="bold yellow")


def print_info(message: str):
    """Print an info message"""
    console.print(f"9  {message}", style="bold blue")


def format_status(status: str) -> str:
    """Format status with emoji and color"""
    status_map = {
        "active": ("=â", "green"),
        "idle": ("ª", "white"),
        "disabled": ("=4", "red"),
        "pending": ("=á", "yellow"),
        "processing": ("=5", "blue"),
        "completed": ("", "green"),
        "failed": ("L", "red"),
        "disputed": (" ", "yellow"),
    }
    emoji, color = status_map.get(status.lower(), ("Ï", "white"))
    return f"[{color}]{emoji} {status}[/{color}]"


def display_agents_table(agents: List[Dict[str, Any]]):
    """Display agents in a beautiful table format"""
    if not agents:
        print_warning("No agents found")
        return

    table = Table(title="> TUNDRA Agents", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Capabilities", style="magenta")
    table.add_column("Success Rate", justify="right", style="green")
    table.add_column("Latency", justify="right")
    table.add_column("Price", justify="right", style="yellow")
    table.add_column("Status")

    for agent in agents:
        capabilities = ", ".join(agent.get("capabilities", [])[:2])
        if len(agent.get("capabilities", [])) > 2:
            capabilities += "..."

        success_rate = f"{agent.get('success_rate', 0):.0f}%"
        latency = f"{agent.get('average_latency_ms', 0)}ms"

        pricing = agent.get("pricing", {})
        price = f"${pricing.get('base_rate', 0):.2f}/{pricing.get('unit', 'task')}"

        status = format_status(agent.get("status", "unknown"))

        table.add_row(
            agent.get("name", "Unknown"),
            capabilities,
            success_rate,
            latency,
            price,
            status
        )

    console.print(table)


def display_jobs_table(jobs: List[Dict[str, Any]], show_full: bool = False):
    """Display jobs in a table format"""
    if not jobs:
        print_warning("No jobs found")
        return

    table = Table(title="=¼ Jobs", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Task", style="white", max_width=40)
    table.add_column("Status")
    table.add_column("Agent", style="cyan")
    table.add_column("Budget", justify="right", style="yellow")

    if show_full:
        table.add_column("Created", style="dim")

    for job in jobs:
        job_id = job.get("job_id", job.get("_id", "N/A"))
        if isinstance(job_id, dict):
            job_id = str(job_id.get("$oid", "N/A"))

        task = job.get("task", "No description")
        if len(task) > 40 and not show_full:
            task = task[:37] + "..."

        status = format_status(job.get("status", "unknown"))
        agent = job.get("assigned_agent_name", job.get("assigned_agent_id", "-"))
        budget = f"${job.get('budget', 0):.2f}"

        row_data = [job_id, task, status, agent, budget]

        if show_full:
            created = job.get("created_at", "")
            if created:
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            row_data.append(created)

        table.add_row(*row_data)

    console.print(table)


def display_job_detail(job: Dict[str, Any]):
    """Display detailed job information"""
    job_id = job.get("job_id", job.get("_id", "N/A"))
    if isinstance(job_id, dict):
        job_id = str(job_id.get("$oid", "N/A"))

    # Create a formatted panel with job details
    details = []
    details.append(f"[bold cyan]Task:[/bold cyan] {job.get('task', 'N/A')}")
    details.append(f"[bold cyan]Status:[/bold cyan] {format_status(job.get('status', 'unknown'))}")
    details.append(f"[bold cyan]Agent:[/bold cyan] {job.get('assigned_agent_name', job.get('assigned_agent_id', 'Unassigned'))}")
    details.append(f"[bold cyan]Budget:[/bold cyan] ${job.get('budget', 0):.2f}")

    created = job.get("created_at", "N/A")
    if created and created != "N/A":
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            created = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
    details.append(f"[bold cyan]Created:[/bold cyan] {created}")

    workflow = job.get("workflow", [])
    if workflow:
        details.append(f"[bold cyan]Workflow:[/bold cyan] {' ’ '.join(workflow)}")

    # Add output if available
    output = job.get("output", job.get("result"))
    if output:
        details.append("")
        details.append("[bold cyan]Output:[/bold cyan]")
        details.append(f"[white]{output}[/white]")

    panel = Panel(
        "\n".join(details),
        title=f"=¼ Job Details: {job_id}",
        border_style="cyan"
    )
    console.print(panel)


def display_spend_summary(data: Dict[str, Any]):
    """Display spending summary"""
    total_spent = data.get("total_spent", 0)
    successful_jobs = data.get("successful_jobs", 0)
    failed_jobs = data.get("failed_jobs", 0)
    refunded = data.get("refunded", 0)

    summary = []
    summary.append(f"[bold yellow]=° Total Spent:[/bold yellow] ${total_spent:.2f}")
    summary.append(f"[bold green] Successful Jobs:[/bold green] {successful_jobs}")

    if failed_jobs > 0:
        summary.append(f"[bold red]   Failed Jobs:[/bold red] {failed_jobs}")
    if refunded > 0:
        summary.append(f"[bold blue]©  Refunded:[/bold blue] ${refunded:.2f}")

    panel = Panel(
        "\n".join(summary),
        title="=Ê Spending Summary",
        border_style="yellow"
    )
    console.print(panel)


def display_login_success(api_base: str):
    """Display successful login message"""
    # Extract region from URL if possible
    region = "Cloud"
    if "azure" in api_base.lower():
        region = "Azure"
    elif "vultr" in api_base.lower():
        region = "Vultr"

    message = f"Logged in successfully. Connected to TUNDRA {region}."
    print_success(message)


def display_agent_simple_list(agents: List[Dict[str, Any]]):
    """Display agents in simple emoji format (for quick view)"""
    if not agents:
        print_warning("No agents found")
        return

    console.print("\n[bold cyan]> Your Agents:[/bold cyan]\n")

    for agent in agents:
        name = agent.get("name", "Unknown")
        capabilities = agent.get("capabilities", [])
        cap_desc = capabilities[0] if capabilities else "General AI"
        success_rate = agent.get("success_rate", 0)
        status = agent.get("status", "unknown")

        status_emoji = "=â" if status == "active" else "ª" if status == "idle" else "=4"

        console.print(f"  {status_emoji} [cyan]{name:15}[/cyan]  {cap_desc:25} (success rate: {success_rate:.0f}%) [{status}]")

    console.print()
