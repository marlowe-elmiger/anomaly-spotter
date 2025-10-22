
"""
Log Parser Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/22/2025


"""

# Supports regular expressions
import re

class LogParser:
    # parses Linux syslog messages and turns them into organized data
    
    
    def __init__(self):
        
        # regex pattern for parsing syslog layout
        # format- timestamp, hostname, process, then message
        self.pattern = re.compile(

            # timestamp
            r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+'

            # hostname  
            r'(\S+)\s+'

            # process name                       
            r'([^:]+):\s+' 

            # rest is the message                   
            r'(.+)'                           
        )
    
    # parses a single log line 
    def parse(self, log_line):


        # matches the log_line text with the regex pattern
        match = self.pattern.match(log_line)
        
        #if there is a match
        if match:
            #pairs the matched groups into a dictionary
            return {
                'timestamp': match.group(1),
                'hostname': match.group(2),
                'process': match.group(3),
                'message': match.group(4)
            }
        else:
            # couldnt parse
            return None  


# testing
if __name__ == "__main__":
    parser = LogParser()
    
    log_test = "Jun  9 06:06:20 combo syslogd 1.4.1: restart."
    result = parser.parse(log_test)
    print(f"\nTest:\n\n {result}\n")