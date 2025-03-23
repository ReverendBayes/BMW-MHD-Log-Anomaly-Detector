import pandas as pd
from plugins.anomaly_detector import AnomalyDetectionPlugin

# ✅ Match the actual name of your real driving log file
csv_path = "data/2020-02-25 07_06_10 9E60B v1.54 Stage 1 93oct_98ron.csv"
df = pd.read_csv(csv_path)

# ✅ Mock msg object compatible with MHD-style plugin
class Msg:
    def __init__(self, row):
        self.payload = row
        self.timestamp = row["Time"]

# ✅ Initialize and run plugin
plugin = AnomalyDetectionPlugin()
for _, row in df.iterrows():
    plugin(Msg(row))
