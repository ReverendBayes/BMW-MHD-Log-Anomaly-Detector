import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# ✅ Update this to match your actual CSV file name
csv_path = "data/2020-02-25 07_06_10 9E60B v1.54 Stage 1 93oct_98ron.csv"
df = pd.read_csv(csv_path)

# ✅ Feature engineering
df["AFR_spike"] = df["Lambda bank 1 (AFR)"] > 20
df["TPS_bug"] = df["Throttle Position (*)"] == 1599.99
df["Pedal_Throttle_Mismatch"] = (df["Accel Ped. Pos. (%)"] > 50) & (df["Throttle Position (*)"] < 40)
df["RPM_idle"] = df["RPM (rpm)"] < 900
df["RPM_hesitation"] = df["RPM (rpm)"].between(1600, 1800)

# ✅ Construct feature matrix for training
X = df[[
    "AFR_spike",
    "TPS_bug",
    "Pedal_Throttle_Mismatch",
    "RPM_idle",
    "RPM_hesitation"
]].astype(int)

# ✅ Train model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# ✅ Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/anomaly_model.pkl")
print("✅ Model saved to models/anomaly_model.pkl")
