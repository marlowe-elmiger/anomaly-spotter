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


# testing
if __name__ == "__main__":
    extractor = FeatureExtractor()
    
    log_test = {
        'timestamp': 'Jun  9 06:06:20',
        'hostname': 'combo',
        'process': 'syslogd 1.4.1',
        'message': 'restart. error. warning'
    }
    
    features = extractor.extract(log_test)
    print(f"Features: {features}")