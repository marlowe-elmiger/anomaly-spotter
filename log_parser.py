
"""
Log Parser Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/22/2025


"""


class LogParser:
    # parses Linux syslog messages and turns them into organized data
    
    # For this function, i'll have to add regex patterns 
    def __init__(self):
        pass
    
    # This function will be for implementing the parsing logic
    def parse(self, log_line):
        # will return dictionary with timestamp, hostname, process, and message
        return None


# testing
if __name__ == "__main__":
    parser = LogParser()
    
    log_test = "Jun  9 06:06:20 combo syslogd 1.4.1: restart."
    result = parser.parse(log_test)
    print(f"Test: {result}")