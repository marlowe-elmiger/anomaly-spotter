"""
Alert
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/5/2025
"""

import requests

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1421172625173905478/CL8QgyVAdeHtBUAAtKHZ_THzsbtiYeOb8uBvPohvcu4QAmEFFuoEkP0nFBTzrEWV7oVM"

def send_alert(message):
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)
