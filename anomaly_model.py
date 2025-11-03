"""
Anomaly Model Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 11/3/2025


"""

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


# testing
if __name__ == "__main__":
    detector = AnomalyModel()
    print("done")