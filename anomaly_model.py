"""
Anomaly Model Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/3/2025


"""
# used for serialization
import pickle
from sklearn.ensemble import IsolationForest


class AnomalyModel:

    def __init__(self, contamination=0.02):


        self.contamination = contamination
        self.model = None
    
    
    def train(self, features):

        # creates and trains isolation forest
        self.model = IsolationForest(
            contamination=self.contamination,
            # for reproducibility (can be any number really)
            random_state=0  
        )
        
        self.model.fit(features)
        print(f"Model trained on {len(features)} samples")
    
    # This function will predict if the features indicate an anomaly or not
    def predict(self, features):
        
         if self.model is None:
            raise ValueError("Model not trained yet.")
        
         #  will return 1 for normal and -1 for anomaly
         return self.model.predict(features)
    
    # This function saves the trained model to a file
    def save(self, filepath):
        if self.model is None:
            raise ValueError("No model")
        
        # Opens the file in binary write mode and saves the model using pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {filepath}")
    
    # This function loads trained model from file
    def load(self, filepath):

        # Opens the file in binary read mode and loads the model from pickle
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {filepath}")


# testing
if __name__ == "__main__":
    from log_gatherer import LogGatherer
    from log_parser import LogParser
    from feature_extractor import FeatureExtractor
    

    
    
    print("Preparing training data...")
    gatherer = LogGatherer()
    parser = LogParser()
    extractor = FeatureExtractor()
    
    logs = gatherer.read_logs(max_lines=100000)
    parsed = parser.parse_all(logs)
    features = extractor.extract_all(parsed)
    print(f"Extracted features from {len(features)} logs\n")
    
    
    print("Training model...")
    detector = AnomalyModel(contamination=0.0125)
    detector.train(features)
   
    
    
    print("\nRunning predictions...")
    predictions = detector.predict(features)
    
    
    
    
    print("\n 30 Sample anomalies:")
    shown = 0
    for pred, log in zip(predictions, parsed):
        if pred == -1:
            shown += 1
            print(f"  {shown}. [{log['process']}] {log['message']}")
            if shown >= 30:
                break



    detector.save("trained_model.pkl")
    new_detector = AnomalyModel()
    new_detector.load("trained_model.pkl")
    
    
    