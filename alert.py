"""
Alert
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/8/2025
"""

import requests

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1421173634461859984/hRHsfdT0XDG6VJues-ihUWPSIEOSy0v4ZdlMPKjmfLZ7XckOO4Zecy-dyQzhyHiSNI5P"


def send_alert(message):
    data = {"content": message}
    
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        response.raise_for_status()
        print("Alert sent")
        return True
    except Exception as e:
        print(f"Alert failed: {e}")
        return False


def test_alert():
    send_alert("Test alert - system online")


if __name__ == "__main__":
    test_alert()
