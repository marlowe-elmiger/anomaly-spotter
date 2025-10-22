"""
Feature Extraction Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/22/2025


"""

class FeatureExtractor:
    
    
    def __init__(self):
        # keywords that might possibly signal anomalies
        self.error_keywords = []
    
    # This function will be the nitty gritty of the feature extraction
    def extract(self, parsed_log):
    
        return []


# testing
if __name__ == "__main__":
    extractor = FeatureExtractor()
    
    log_test = {
    }
    
    features = extractor.extract(log_test)
    print(f"Features: {features}")