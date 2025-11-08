# cli/tundra_cli.py
import json
import requests
import typer

from config import load_config, save_config, get_api_base, get_api_key

app = typer.Typer(help="TUNDRA CLI – talk to your backend on Vultr.")


@app.command()
def login(
    api_key: str = typer.Argument(..., help="Your TUNDRA API key"),
    api_base: str = typer.Option(
        None,
        "--api-base",
        "-b",
        help="Backend base URL, e.g. http://123.45.67.89:8000",
    ),
):
    """
    Save your API key (and optional API base) for later commands.
    """
    cfg = load_config()
    cfg["api_key"] = api_key
    if api_base:
        cfg["api_base"] = api_base
    save_config(cfg)
    typer.secho("✅ Saved CLI config.", fg=typer.colors.GREEN)


@app.command()
def agents():
    """
    List all agents from the TUNDRA backend.
    """
    base = get_api_base()
    key = get_api_key()
    headers = {}
    if key:
        headers["x-api-key"] = key

    url = f"{base}/agents"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        typer.secho(f"❌ Could not reach backend at {base}: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    if resp.status_code != 200:
        typer.secho(f"❌ Backend error: {resp.status_code} {resp.text}", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command()
def jobs():
    """
    List all jobs from the TUNDRA backend.
    """
    base = get_api_base()
    key = get_api_key()
    headers = {}
    if key:
        headers["x-api-key"] = key

    resp = requests.get(f"{base}/jobs", headers=headers, timeout=10)
    if resp.status_code != 200:
        typer.secho(f"❌ Backend error: {resp.status_code} {resp.text}", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command()
def create_job(task: str, budget: float = 10.0):
    """
    Create a new job via the backend (not directly in Mongo).
    """
    base = get_api_base()
    key = get_api_key()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["x-api-key"] = key

    payload = {
        "task": task,
        "budget": budget,
    }

    resp = requests.post(f"{base}/jobs", headers=headers, json=payload, timeout=10)
    if resp.status_code not in (200, 201):
        typer.secho(f"❌ Backend error: {resp.status_code} {resp.text}", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("✅ Job created:", fg=typer.colors.GREEN)
    typer.echo(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    app()
