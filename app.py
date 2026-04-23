"""
app.py — VELOUR Instagram DM Bot
"""

import os
import json
import requests
import traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

from responses import get_response

app = Flask(__name__)


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[WEBHOOK] Verification successful")
        return challenge, 200
    else:
        print("[WEBHOOK] Verification FAILED")
        return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True)
    print(f"[RAW] {json.dumps(data)}")

    if not data or data.get("object") != "instagram":
        return "OK", 200

    try:
        for entry in data.get("entry", []):
            messaging_events = entry.get("messaging", [])

            if not messaging_events:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for msg in messages:
                        sender_id = msg.get("from", {}).get("id") or msg.get("from")
                        message_text = msg.get("text", {})
                        if isinstance(message_text, dict):
                            message_text = message_text.get("body", "")
                        if sender_id and message_text:
                            print(f"[MESSAGE] From {sender_id}: {message_text!r}")
                            reply = get_response(message_text)
                            send_reply(sender_id, reply)
                continue

            for event in messaging_events:
                if event.get("message", {}).get("is_echo"):
                    continue

                sender_id    = event.get("sender", {}).get("id")
                message_text = event.get("message", {}).get("text")

                if not sender_id or not message_text:
                    continue

                print(f"[MESSAGE] From {sender_id}: {message_text!r}")
                reply = get_response(message_text)
                send_reply(sender_id, reply)

    except Exception as e:
        print(f"[ERROR] {e}")
        traceback.print_exc()

    return "OK", 200


def send_reply(recipient_id: str, message_text: str):
    url = "https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message":   {"text": message_text}
    }
    params = {"access_token": ACCESS_TOKEN}

    try:
        response = requests.post(url, json=payload, params=params, timeout=10)
        response.raise_for_status()
        print(f"[SENT] Reply delivered to {recipient_id}")
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Meta API: {e.response.status_code} — {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network: {e}")


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "bot":    "VELOUR Instagram DM Bot",
        "mode":   "keyword-matching"
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)