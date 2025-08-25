import os
import time
import requests

# Multiple GroupMe bot IDs
# Prefer env var GROUPME_BOT_IDS (comma or semicolon separated),
# falls back to hard-coded list below.
_env_ids = os.environ.get("GROUPME_BOT_IDS", "")
if _env_ids.strip():
    BOT_IDS = [i.strip() for i in _env_ids.replace(";", ",").split(",") if i.strip()]
else:
    BOT_IDS = [
        "986d3ab45206ddc9093759719e",  # test1
        "bc4d141a6e0dac0a1c9a16bdfd",  # test2
        "5c9c8df74d756ba431e36c32a1",  # test3
    ]

# Message you want to send
MESSAGE_TEXT = "Hello from Python! Here's an image 🚀"

# Image URL (must be a GroupMe-hosted image URL)
IMAGE_URL = "https://i.groupme.com/960x960.jpeg.986b60bbdbd04e89862847a0aa9f75f2"

def send_bot_message(bot_id, text, image_url=None):
    """Send a message (with optional image) using a GroupMe bot."""
    url = "https://api.groupme.com/v3/bots/post"
    payload = {"bot_id": bot_id, "text": text}
    if image_url:
        payload["attachments"] = [{"type": "image", "url": image_url}]
    # Try up to 3 times on transient server errors
    for attempt in range(1, 4):
        response = requests.post(url, json=payload, timeout=15)
        print()
        if response.status_code == 202:
            print("✅ Sent via bot", bot_id)
            return True
        print()
        # Retry on 5xx
        if 500 <= response.status_code < 600 and attempt < 3:
            time.sleep(1.5 * attempt)
            continue
        print(f"❌ Failed via bot {bot_id} ({response.status_code}): {response.text}")
        return False

def main():
    if not BOT_IDS:
        raise SystemExit("No bot IDs configured. Set GROUPME_BOT_IDS or edit BOT_IDS in sender.py.")
    for bot_id in BOT_IDS:
        send_bot_message(bot_id, MESSAGE_TEXT, IMAGE_URL)

if __name__ == "__main__":
    main()
