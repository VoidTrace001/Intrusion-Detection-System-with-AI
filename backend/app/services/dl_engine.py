import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import os
import numpy as np

class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim),
            nn.Sigmoid()  # Assuming input features are normalized 0-1
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class DLDetector:
    def __init__(self, model_dir="models/"):
        self.model_dir = model_dir
        self.input_dim = 10  # Must match the Preprocessor output
        self.threshold = 0.1 # Dynamic threshold for anomaly detection
        self.model = Autoencoder(self.input_dim)
        self.load_model()

    def load_model(self):
        try:
            path = os.path.join(self.model_dir, "autoencoder.pth")
            if os.path.exists(path):
                self.model.load_state_dict(torch.load(path))
                self.model.eval()
                # Load threshold if saved separately, or re-calculate
                print("[*] Deep Learning Anomaly Detector Loaded.")
            else:
                print("[!] Deep Learning model not found. Run training script.")
        except Exception as e:
            print(f"[!] Failed to load DL model: {e}")

    def detect_anomaly(self, vector):
        """
        Returns True if the reconstruction error exceeds the threshold.
        High Error = Anomaly (Zero-Day Attack).
        """
        with torch.no_grad():
            tensor_in = torch.FloatTensor(vector)
            reconstructed = self.model(tensor_in)
            loss = nn.MSELoss()(reconstructed, tensor_in)
            
            # If reconstruction error is high, it's an anomaly (Zero-Day)
            is_anomaly = loss.item() > self.threshold
            return is_anomaly, loss.item()

    def train(self, data_loader, epochs=10):
        optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        criterion = nn.MSELoss()
        
        self.model.train()
        for epoch in range(epochs):
            for batch in data_loader:
                optimizer.zero_grad()
                output = self.model(batch)
                loss = criterion(output, batch)
                loss.backward()
                optimizer.step()
        
        torch.save(self.model.state_dict(), os.path.join(self.model_dir, "autoencoder.pth"))
        print("[*] Deep Learning Model Saved.")
