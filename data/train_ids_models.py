import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
import requests
import zipfile
import io
import torch
from torch.utils.data import DataLoader, TensorDataset

# Config
MODEL_DIR = "models/"
DATA_DIR = "data/"
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00203/NSL-KDD.zip"

def generate_synthetic_data(num_samples=5000):
    """Generates synthetic data if dataset download fails."""
    print("[*] Generating synthetic training data for demonstration...")
    # 10 features as defined in our preprocessor
    data = np.random.rand(num_samples, 10)
    binary_labels = (data[:, 0] > 0.7).astype(int) 
    
    # Create an anomaly (Zero-Day) dataset
    anomaly_data = np.random.rand(500, 10) * 2 # Out of distribution
    
    attack_types = ["Normal", "DoS", "Probe", "Brute Force", "R2L", "U2R"]
    multi_labels = []
    for i in range(num_samples):
        if binary_labels[i] == 0:
            multi_labels.append("Normal")
        else:
            multi_labels.append(np.random.choice(attack_types[1:]))
            
    return data, binary_labels, np.array(multi_labels), anomaly_data

def train_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    X, y_binary, y_multi, anomaly_data = generate_synthetic_data()

    # 🔹 Model 1: Binary Classifier
    print("[*] Training Model 1: Binary Classifier (Normal vs Attack)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2)
    rf_binary = RandomForestClassifier(n_estimators=100)
    rf_binary.fit(X_train, y_train)
    joblib.dump(rf_binary, os.path.join(MODEL_DIR, "binary_model.pkl"))

    # 🔹 Model 2: Multi-Class Classifier
    print("[*] Training Model 2: Multi-Class Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_multi, test_size=0.2)
    rf_multi = RandomForestClassifier(n_estimators=100)
    rf_multi.fit(X_train, y_train)
    joblib.dump(rf_multi, os.path.join(MODEL_DIR, "multi_class_model.pkl"))

    # 🔹 Model 3: Deep Learning (Autoencoder)
    print("[*] Training Model 3: Deep Learning Autoencoder (Zero-Day Detection)...")
    
    # Import the Autoencoder class
    # Add root to sys.path so we can import
    import sys
    backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    from app.services.dl_engine import Autoencoder
    
    # Train only on 'Normal' data to learn baseline
    normal_indices = np.where(y_binary == 0)[0]
    X_normal = X[normal_indices]
    
    # Convert to Tensor
    tensor_x = torch.Tensor(X_normal)
    dataset = TensorDataset(tensor_x) # create your datset
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    model = Autoencoder(input_dim=10)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.MSELoss()
    
    model.train()
    for epoch in range(10): # 10 Epochs
        for batch in dataloader:
            optimizer.zero_grad()
            output = model(batch[0])
            loss = criterion(output, batch[0])
            loss.backward()
            optimizer.step()
            
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "autoencoder.pth"))
    print("[*] Deep Learning Model Saved.")

    # Save initial scalers/transformers
    from app.services.preprocessor import Preprocessor
    prep = Preprocessor(model_dir=MODEL_DIR)
    prep.save_transformers()
    
    print("[*] All models saved to /models directory.")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    train_models()
