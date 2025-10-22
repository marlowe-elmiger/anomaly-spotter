
"""
Log Parser Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/22/2025


"""


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

    # Transforms a list of raw log lines into a list of parsed ones. Does this all in one go.
    def parse_all(self, log_lines):

        # Empty list to store the results
        parsed = []

        for log in log_lines:

            # parses individual log in list
            result = self.parse(log)
            if result:

                # If successful, stores the parsed log in the list
                parsed.append(result)
        
        # returns list of all parsed logs
        return parsed

# testing
if __name__ == "__main__":

    from log_gatherer import LogGatherer
    
    print("\nTESTING:")

     # Get some logs
    gatherer = LogGatherer()
    unparsed_logs = gatherer.read_logs(max_lines=5)

    # Parse them
    parser = LogParser()

    print("\nParsing first 5 logs:")
    for i, log in enumerate(unparsed_logs, 1):
        parsed = parser.parse(log)
        print(f"\n{i}. {log}...")
        if parsed:
            print(f"   Parsed:")
            print(f"     Timestamp: {parsed['timestamp']}")
            print(f"     Hostname:  {parsed['hostname']}")
            print(f"     Process:   {parsed['process']}")
            print(f"     Message:   {parsed['message']}...")
        else:
            print(f"   Failed to parse")


    print("\nTesting parse_all() function\n")

    all_logs = gatherer.read_logs(max_lines=500)
    parsed_logs = parser.parse_all(all_logs)

    print(f"\nTotal logs: {len(all_logs)}")
    print(f"Parsed successfully: {len(parsed_logs)}\n\n")

    print("Last log stored:\n")
    print(parsed_logs[499])