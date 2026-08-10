#!/usr/bin/env python3
"""
alert_response.py

Minimal SOC response automation script.
"""

import json
import os
import sys
import urllib.request

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
HIGH_SEVERITY_THRESHOLD = 12


def send_slack_alert(message: str) -> None:
    """Post a message to Slack via incoming webhook."""
    if not SLACK_WEBHOOK_URL:
        print("[!] SLACK_WEBHOOK_URL is not set.", file=sys.stderr)
        return
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[!] Failed to send Slack alert: {e}", file=sys.stderr)


def isolate_host(hostname: str) -> None:
    """Placeholder for a real response action."""
    print(f"[MOCK ACTION] Would isolate host: {hostname}")


def handle_alert(alert: dict) -> None:
    level = alert.get("rule", {}).get("level", 0)
    description = alert.get("rule", {}).get("description", "Unknown rule")
    hostname = alert.get("agent", {}).get("name", "unknown-host")

    if level >= HIGH_SEVERITY_THRESHOLD:
        message = f":rotating_light: *{description}* fired on `{hostname}` (level {level})"
        print(message)
        send_slack_alert(message)
        isolate_host(hostname)
    else:
        print(f"[info] Alert below threshold, logging only: {description} (level {level})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 alert_response.py <alert.json>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        sample_alert = json.load(f)

    handle_alert(sample_alert)
