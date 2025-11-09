# cli/config.py
import os
import json

CONFIG_PATH = os.path.expanduser("~/.tundra_config.json")


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}


def save_config(data: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)


def get_api_base() -> str:
    cfg = load_config()
    # env wins, then config, then fallback
    return os.getenv("TUNDRA_API", cfg.get("api_base", "http://localhost:8000"))


def get_api_key() -> str | None:
    cfg = load_config()
    return os.getenv("TUNDRA_API_KEY", cfg.get("api_key"))
