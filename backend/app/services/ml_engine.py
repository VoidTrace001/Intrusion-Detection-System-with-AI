import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class MLEngine:
    def __init__(self, model_dir="models/"):
        self.model_dir = model_dir
        self.binary_model = None
        self.multi_class_model = None
        self.load_models()

    def load_models(self):
        """3️⃣ Machine Learning Engine: Load binary and multi-class models."""
        try:
            self.binary_model = joblib.load(os.path.join(self.model_dir, "binary_model.pkl"))
            self.multi_class_model = joblib.load(os.path.join(self.model_dir, "multi_class_model.pkl"))
            print("[*] Successfully loaded ML models.")
        except FileNotFoundError:
            print("[!] ML models not found. Please run data/train_ids_models.py first.")
            # Placeholder/Dummy models for initial execution if models are missing
            self.binary_model = None
            self.multi_class_model = None

    def predict(self, features_vector):
        """
        4️⃣ Real-Time Detection System:
        Predict using binary model first, then multi-class if an attack is detected.
        """
        # Default results
        prediction = "Normal"
        confidence = 0.95
        attack_type = "Normal"
        risk_score = 0.0

        if self.binary_model is None:
            # Fallback for demo if model not trained yet (Simulated prediction)
            import random
            is_attack = random.random() > 0.8
            if is_attack:
                prediction = "Attack"
                confidence = random.uniform(0.7, 0.99)
                attack_type = random.choice(["DoS", "Probe", "Brute Force", "R2L", "U2R"])
            else:
                prediction = "Normal"
                confidence = random.uniform(0.95, 0.99)
                attack_type = "Normal"
            
            return {
                "prediction": prediction,
                "confidence": round(confidence, 4),
                "attack_type": attack_type
            }

        # REAL INFERENCE (If models exist)
        binary_pred = self.binary_model.predict(features_vector)[0]
        binary_prob = self.binary_model.predict_proba(features_vector)[0]
        
        if binary_pred == 1: # 1 = Attack in binary classification
            prediction = "Attack"
            confidence = max(binary_prob)
            
            # Use multi-class classifier to identify attack type
            multi_pred = self.multi_class_model.predict(features_vector)[0]
            multi_prob = self.multi_class_model.predict_proba(features_vector)[0]
            attack_type = multi_pred
            confidence = max(multi_prob)
        else:
            prediction = "Normal"
            confidence = max(binary_prob)
            attack_type = "Normal"

        return {
            "prediction": prediction,
            "confidence": round(float(confidence), 4),
            "attack_type": attack_type
        }

# Example Usage
if __name__ == "__main__":
    ml = MLEngine()
    dummy_input = np.zeros((1, 10)) # Matches preprocessor's output vector size
    result = ml.predict(dummy_input)
    print(f"Prediction result: {result}")
