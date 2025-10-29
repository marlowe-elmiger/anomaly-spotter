"""
Feature Extraction Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/28/2025


"""

class FeatureExtractor:
    
    
    def __init__(self):
        # keywords that might possibly signal anomalies


        # keywords organized by category: errors, warnings, security, system health, network issues, and unexpected behavior
        self.error_keywords = [
            # errors 
            'error', 'failed', 'failure', 'panic', 'fatal', 'crash', 
            'abort', 'unhandled', 'stack trace', 'core dumped', 'cannot', 'exception',
            
            # warnings 
            'warning', 'degraded', 'high latency', 'resource low', 'timeout', 
            'retry', 'recovering', 'unavailable', 'missed', 'dropped', 'overload',
            
            # security 
            'unauthorized', 'forbidden', 'denied', 'intrusion', 'attack', 
            'malware', 'breach', 'invalid login', 'suspicious', 'tamper detected',
            'exploit', 'brute force', 'vulnerability'
            
            # system health
            'out of memory', 'disk full', 'cpu high', 'deadlock', 'service down', 
            'unresponsive', 'halted', 'segmentation fault', 'out of space', 'kernel panic'
            
            # network problems
            'connection refused', 'connection reset', 'network unreachable', 
            'packet loss',
            
            # unexpected behavior 
            'unexpected', 'unknown', 'not found', 'corrupt', 'mismatch', 
            'overflow', 'invalid'
        ]
        
    
    # This function will be the nitty gritty of the feature extraction
    def extract(self, parsed_log):
    
        message = parsed_log['message'].lower()
        
        features = []
        
        # finds message length
        features.append(len(message))
        
        # finds number of words
        features.append(len(message.split()))
        
        # checks for error keywords 
        for keyword in self.error_keywords:
            features.append(1 if keyword in message else 0)
        
        # returns features in a vector format
        return features

    
    
    def extract_all(self, parsed_logs):
        
        # Will store all the feature vectors we extract
        feature_list = []
        
        for log in parsed_logs:
            # extracts features from each individual log
            features = self.extract(log)

            # adds feature vector to the list
            feature_list.append(features)
        
        # returns all features
        return feature_list

# testing
if __name__ == "__main__":

    from log_gatherer import LogGatherer
    from log_parser import LogParser

    gatherer = LogGatherer()
    parser = LogParser()
    extractor = FeatureExtractor()
    
    test_log = {
        'timestamp': 'Jun  9 06:06:20',
        'hostname': 'combo',
        'process': 'syslogd 1.4.1',
        'message': 'restart.'
    }
    
    all_logs = gatherer.read_logs(max_lines=500)
    all_parsed = parser.parse_all(all_logs)
    all_features = extractor.extract_all(all_parsed)
    
    print(f"\nExtracted features from {len(all_features)} logs")
    
    print(f"\nExample: {all_features[499]}")