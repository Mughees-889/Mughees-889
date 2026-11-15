import re
import urllib.request
import json
from datetime import datetime, timezone

README_PATH = "README.md"
GITHUB_USERNAME = "Mughees-889"  # <-- REPLACE THIS WITH YOUR EXACT USERNAME

def fetch_dynamic_content() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    req = urllib.request.Request(url, headers={"User-Agent": "Profile-Updater"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            events = json.loads(response.read().decode())
            if events:
                latest_repo = events[0]["repo"]["name"]
                event_type = events[0]["type"].replace("Event", "")
            else:
                latest_repo = "None yet"
                event_type = "Idle"
    except Exception as e:
        latest_repo = "Local Environment"
        event_type = "Offline Sync"

    return (
        f"- **Last Auto-Sync:** `{now}`\n"
        f"- **Latest Public Activity:** `{event_type}` in `{latest_repo}`\n"
        f"- **Telemetry Status:** `Operational`"
    )

def update_readme(new_content: str) -> None:
    with open(README_PATH, "r", encoding="utf-8") as file:
        readme = file.read()

    pattern = r"(<!-- START_SECTION:dynamic -->)(.*?)(<!-- END_SECTION:dynamic -->)"
    replacement = f"\\1\n{new_content}\n\\3"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

    if updated_readme != readme:
        with open(README_PATH, "w", encoding="utf-8") as file:
            file.write(updated_readme)

if __name__ == "__main__":
    content = fetch_dynamic_content()
    update_readme(content)
