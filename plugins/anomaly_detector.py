import os
import joblib
import pandas as pd

class AnomalyDetectionPlugin:
    def __init__(self):
        super().__init__()
        model_path = os.path.join(os.path.dirname(__file__), "../models/anomaly_model.pkl")
        self.model = joblib.load(model_path)
        self.results = []

    def __call__(self, msg):
        try:
            rpm = float(msg.payload.get("RPM (rpm)", 0))
            afr = float(msg.payload.get("Lambda bank 1 (AFR)", 0))
            tps = float(msg.payload.get("Throttle Position (*)", 0))
            pedal = float(msg.payload.get("Accel Ped. Pos. (%)", 0))

            features = pd.DataFrame([{
                "AFR_spike": afr > 20 or pd.isna(afr),
                "TPS_bug": tps == 1599.99,
                "Pedal_Throttle_Mismatch": pedal > 50 and tps < 40,
                "RPM_idle": rpm < 900,
                "RPM_hesitation": 1600 <= rpm <= 1800
            }]).astype(int)

            prediction = self.model.predict(features)[0]
            if prediction == -1:
                timestamp = msg.timestamp if hasattr(msg, "timestamp") else "unknown"
                details = []

                if features["AFR_spike"].iloc[0]:
                    details.append(f"AFR spike: {afr} @ {timestamp}s")
                if features["TPS_bug"].iloc[0]:
                    details.append(f"TPS bug value 1599.99 @ {timestamp}s")
                if features["Pedal_Throttle_Mismatch"].iloc[0]:
                    details.append(f"Throttle mismatch (pedal={pedal}%, throttle={tps}%) @ {timestamp}s")
                if features["RPM_idle"].iloc[0]:
                    details.append(f"Idle RPM anomaly @ {timestamp}s")
                if features["RPM_hesitation"].iloc[0]:
                    details.append(f"Hesitation RPM anomaly @ {timestamp}s")

                for d in details:
                    print("⚠️", d)
        except Exception as e:
            print("❌ Plugin error:", e)

