"""
Live Log Parser Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/08/2025
"""

import subprocess
from log_parser import LogParser
from alert import send_alert
from anomaly_model import AnomalyModel
from feature_extractor import FeatureExtractor

class LiveLogParser:

    def __init__(self, model="trained_model.pkl"):
        self.parser = LogParser()
        self.extractor = FeatureExtractor()
        self.model = AnomalyModel()
        self.model.load(model)

    def monitor(self):
        print(f"\nMonitoring\n")
        

        # Look at the system's journal for logs. Should tail for current logs
        # and should ignore past logs
        process = subprocess.Popen(
            ['journalctl', '-f', '-n', '0', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Format the log from output, parse it, send alert if it's an anomaly
        try:
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                parsed = self.parser.parse(line)
                if not parsed:
                    continue

                features = self.extractor.extract(parsed)
                # Print information for terminal (for testing)
                print(f"\nTimestamp: {parsed['timestamp']}\nHost: {parsed['hostname']}\nProcess: {parsed['process']}\nMessage: {parsed['message']}")

                # ML prediction
                ml_prediction = self.model.predict([features])[0]

                # Keyword check for critical terms
                critical_keywords = ['critical', 'panic', 'fatal', 'emergency',
                                    'breach', 'attack', 'intrusion', 'malware',
                                    'out of memory', 'disk full', 'deadlock',
                                    'kernel panic', 'segmentation fault', 'core dumped']
                has_critical = any(kw in parsed['message'].lower() for kw in critical_keywords)

                # Alert if either condition is met
                if ml_prediction == -1 or has_critical:
                    if has_critical and ml_prediction == 1:
                        print(f"    (Keyword-based detection)")
                    send_alert("anomaly detected")

        except KeyboardInterrupt:
            print("\nNo longer monitoring.")
        finally:
            process.terminate()


if __name__ == "__main__":
    live_parser = LiveLogParser()
    live_parser.monitor()

