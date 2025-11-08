"""
Alert
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/5/2025
"""

import requests

WEBHOOK_URL = https://discordapp.com/api/webhooks/1421173634461859984/hRHsfdT0XDG6VJues-ihUWPSIEOSy0v4ZdlMPKjmfLZ7XckOO4Zecy-dyQzhyHiSNI5P

def send_alert(message):
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)
