import datetime
import os
import sys
import time

import requests

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")


def send_daily_message():
    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: TG_BOT_TOKEN or TG_CHAT_ID not set in environment.")
        sys.exit(1)

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}"

    now = datetime.datetime.now(datetime.timezone.utc)
    day_number = now.timetuple().tm_yday
    message = f"Day {day_number}."

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    max_retries = 3
    retry_delay_seconds = 10
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.post(f"{api_url}/sendMessage", json=payload, timeout=10)
        except requests.RequestException as e:
            last_error = e
            print(f"Attempt {attempt}/{max_retries} failed (network error): {type(e).__name__}")
            if attempt < max_retries:
                time.sleep(retry_delay_seconds)
            continue

        try:
            data = r.json()
        except ValueError:
            last_error = f"Non-JSON response, status {r.status_code}: {r.text[:200]}"
            print(f"Attempt {attempt}/{max_retries} failed: {last_error}")
            if attempt < max_retries:
                time.sleep(retry_delay_seconds)
            continue

        if data.get("ok"):
            print(f"OK: message sent, message_id={data['result']['message_id']}")
            return

        # Telegram actively rejected the request (bad token, bad chat_id, etc.)
        # No point retrying: it will fail the same way every time.
        print("ERROR: Telegram API rejected the message.")
        print(f"  Status code: {r.status_code}")
        print(f"  error_code: {data.get('error_code')}")
        print(f"  description: {data.get('description')}")
        sys.exit(1)

    print(f"ERROR: all {max_retries} attempts failed. Last error: {last_error}")
    sys.exit(1)


if __name__ == "__main__":
    send_daily_message()
