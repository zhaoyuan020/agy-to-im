import asyncio
from src.config import load_config
from pathlib import Path
import os
import httpx

async def main():
    cfg_path = Path("config.json")
    cfg = load_config(cfg_path)
    
    commands = [
        {"command": "start", "description": "Welcome message"},
        {"command": "help", "description": "Show help and all commands"},
        {"command": "status", "description": "Read-only system + chat summary"},
        {"command": "settings", "description": "Control panel with buttons"},
        {"command": "model", "description": "Pick a model (per-chat override)"},
        {"command": "mode", "description": "Pick a mode (Code or Plan)"},
        {"command": "reset", "description": "Fresh session for this chat"},
        {"command": "files", "description": "List recent uploads"}
    ]
    
    proxies = None
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    
    # Configure proxies matching httpx proxy dictionary format
    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy: proxies["http://"] = http_proxy
        if https_proxy: proxies["https://"] = https_proxy
        
    url = f"https://api.telegram.org/bot{cfg.telegram.bot_token}/setMyCommands"
    
    print(f"Setting commands... Proxies: {proxies}")
    async with httpx.AsyncClient(proxy=http_proxy if http_proxy else None) as client:
        r = await client.post(url, json={"commands": commands})
        print("Response:", r.json())

if __name__ == "__main__":
    asyncio.run(main())
