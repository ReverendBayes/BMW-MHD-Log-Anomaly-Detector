# MHD Log Anomaly Detector

This tool analyzes MHD log files for data anomalies related to engine performance, AFR behavior, throttle behavior, and potential MHD logging bugs.

It has:
- An Isolation Forest-based anomaly detector for BMW MHD logs
- Engineered features specific to known BMW issues (TPS bug, throttle lag, AFR spikes)
- A test suite and training pipeline using real-world data

Clear diagnostic output with timestamps and signal values

---

## Features Detected

### 1. AFR Spikes
- Flags any Air-Fuel Ratio (AFR) values > 20
- Indicates lean conditions, failing sensors, or invalid data
- Useful for identifying lean conditions or sensor faults

### 2. Throttle Mismatch
- Flags mismatches between pedal input and throttle plate
- Flags when the **throttle body opening lags significantly behind pedal input**
- Example: Pedal at 100%, throttle at 30% → Indicates torque limiters, DME logic intervention, or throttle plate issues
- **NOTE: In specific contexts:**
  -  The ECU intentionally closes the throttle under full pedal to control boost pressure.
  -  This behavior is not an error — it’s part of torque targeting, especially on turbocharged engines with electronic throttle control (e.g., BMW N54/N55 platforms)

### 3. Hesitation RPM Zone
- Flags anomalies in the **1600–1800 RPM band**
- Captures airflow or throttle-related hesitations
- Often associated with poor throttle transitions, airflow delays, or DME logic stumbles

### 4. Idle AFR Instability
- Flags AFR swings during idle (RPM < 900)
- Used to catch idle air control valve issues, misfires, fuel delivery noise, or false sensor readings

### 5. Repeating AFR = 235.19
- Flags repeated AFR values of `235.19`, often seen due to MHD logging bugs or wideband sensor failures
- These are **excluded from anomaly scoring** but still printed to help identify sensor dropouts or log corruption
- Useful for diagnosing data quality issues
- **NOTE:**
  -  The 235.19 AFR value is a known placeholder in some MHD logs (common across N54/N55/S55 platforms).
  -  It likely reflects a logging bug or wideband sensor dropout.
  -  This check is primarily useful for BMWs using MHD.

---
From the current log file:
## ⚠️ Sample Output

⚠️ Throttle mismatch (pedal=51.4%, throttle=21.3%) @ 395.754s 

(Throttle mismatch events caught across multiple RPM bands)

⚠️ AFR spike: 235.19 @ 532.295s 
(AFR spikes up to 235.19 detected and flagged. AFR = 235.19 repeated over hundreds of lines → likely MHD logging bug or sensor dropout)

⚠️ Idle RPM anomaly @ 624.188s 
(Idle instability present with rapid AFR changes while below 900 RPM)

⚠️ Hesitation RPM anomaly @ 943.236s 
(Hesitation events correlate with RPM dip zones and throttle lag)


Flags print with timestamps for easy lookup.


It turns this:
![MHD Log Data](assets/MHD-Log-Data.png)

Into this:
![Output](assets/Output.png)


### What the Output Means:
Each line like:

⚠️ Throttle mismatch (pedal=51.4%, throttle=21.3%) @ 395.754s

⚠️ Hesitation RPM anomaly @ 395.754s

Means:

The model noticed that the pedal position is high, but the throttle isn’t opening accordingly

The RPM is in the 1600–1800 “hesitation” range, and something else was off (e.g., low throttle delta, AFR oddity, etc.


---

### Machine Learning Pipeline

This tool uses a machine learning model trained on binary diagnostic features extracted from real-world MHD logs.

The model is based on [`IsolationForest`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) from `scikit-learn`, trained to detect rare patterns such as AFR spikes, torque limiting behavior, and RPM anomalies.

The training pipeline:

- Loads MHD logs from `.csv`
- Engineers binary features:
  - `AFR_spike`
  - `TPS_bug`
  - `Pedal_Throttle_Mismatch`
  - `RPM_idle`
  - `RPM_hesitation`
- Trains an unsupervised Isolation Forest model with contamination set to 0.05
- Saves the model to `models/anomaly_model.pkl`

**Training Code:** [`models/train_model.py`](models/train_model.py)

At runtime, this model is loaded and applied to incoming logs using the plugin system in [`plugins/anomaly_detector.py`](plugins/anomaly_detector.py), where it flags any predictions of `-1` (anomalies) and explains them in detail.

---

## How to Use

1. Place your `.csv` MHD log in the project directory  
2. Run:  
   `python analyze_log.py`  
3. Anomalies will print to console. You can redirect output or integrate JSON logging as needed.

---

## Dependencies
- scikit-learn==1.3.0
- joblib==1.3.2
- numpy==1.26.4
- pandas==2.2.0

Optional: for future UI
- streamlit==1.32.0
  
---

## Future Plans
# MHD Log Anomaly Detector

This tool analyzes MHD log files for data anomalies related to engine performance, AFR behavior, throttle behavior, and potential MHD logging bugs.

It has:
- An Isolation Forest-based anomaly detector for BMW MHD logs
- Engineered features specific to known BMW issues (TPS bug, throttle lag, AFR spikes)
- A test suite and training pipeline using real-world data

Clear diagnostic output with timestamps and signal values

---

## Features Detected

### 1. AFR Spikes
- Flags any Air-Fuel Ratio (AFR) values > 20
- Indicates lean conditions, failing sensors, or invalid data
- Useful for identifying lean conditions or sensor faults

### 2. Throttle Mismatch
- Flags mismatches between pedal input and throttle plate
- Flags when the **throttle body opening lags significantly behind pedal input**
- Example: Pedal at 100%, throttle at 30% → Indicates torque limiters, DME logic intervention, or throttle plate issues
- **NOTE: In specific contexts:**
  -  The ECU intentionally closes the throttle under full pedal to control boost pressure.
  -  This behavior is not an error — it’s part of torque targeting, especially on turbocharged engines with electronic throttle control (e.g., BMW N54/N55 platforms)

### 3. Hesitation RPM Zone
- Flags anomalies in the **1600–1800 RPM band**
- Captures airflow or throttle-related hesitations
- Often associated with poor throttle transitions, airflow delays, or DME logic stumbles

### 4. Idle AFR Instability
- Flags AFR swings during idle (RPM < 900)
- Used to catch idle air control valve issues, misfires, fuel delivery noise, or false sensor readings

---
From the current log file:
## ⚠️ Sample Output

⚠️ Throttle mismatch (pedal=51.4%, throttle=21.3%) @ 395.754s 

(Throttle mismatch events caught across multiple RPM bands)

⚠️ AFR spike: 235.19 @ 532.295s 
(AFR spikes up to 235.19 detected and flagged. AFR = 235.19 repeated over hundreds of lines → likely MHD logging bug or sensor dropout)

⚠️ Idle RPM anomaly @ 624.188s 
(Idle instability present with rapid AFR changes while below 900 RPM)

⚠️ Hesitation RPM anomaly @ 943.236s 
(Hesitation events correlate with RPM dip zones and throttle lag)


Flags print with timestamps for easy lookup.


It turns this:
![MHD Log Data](assets/MHD-Log-Data.png)

Into this:
![Output](assets/Output.png)


### What the Output Means:
Each line like:

⚠️ Throttle mismatch (pedal=51.4%, throttle=21.3%) @ 395.754s

⚠️ Hesitation RPM anomaly @ 395.754s

Means:

The model noticed that the pedal position is high, but the throttle isn’t opening accordingly

The RPM is in the 1600–1800 “hesitation” range, and something else was off (e.g., low throttle delta, AFR oddity, etc.


---

### Machine Learning Pipeline

This tool uses a machine learning model trained on binary diagnostic features extracted from real-world MHD logs.

The model is based on [`IsolationForest`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) from `scikit-learn`, trained to detect rare patterns such as AFR spikes, torque limiting behavior, and RPM anomalies.

The training pipeline:

- Loads MHD logs from `.csv`
- Engineers binary features:
  - `AFR_spike`
  - `TPS_bug`
  - `Pedal_Throttle_Mismatch`
  - `RPM_idle`
  - `RPM_hesitation`
- Trains an unsupervised Isolation Forest model with contamination set to 0.05
- Saves the model to `models/anomaly_model.pkl`

**Training Code:** [`models/train_model.py`](models/train_model.py)

At runtime, this model is loaded and applied to incoming logs using the plugin system in [`plugins/anomaly_detector.py`](plugins/anomaly_detector.py), where it flags any predictions of `-1` (anomalies) and explains them in detail.

---

## How to Use

1. Place your `.csv` MHD log in the project directory  
2. Run:  
   `python analyze_log.py`  
3. Anomalies will print to console. You can redirect output or integrate JSON logging as needed.

---

## Dependencies
- scikit-learn==1.3.0
- joblib==1.3.2
- numpy==1.26.4
- pandas==2.2.0

Optional: for future UI
- streamlit==1.32.0
  
---

## Future Plans

- Group related anomaly clusters for readability. Add deduplication logic so the same anomaly isn’t logged every 0.1s unless a threshold is passed.  
- Add a `--verbose` flag to enable full line-by-line output; default output could shift to a summary-style log.  
- Build a Streamlit UI front-end for easier review, especially for non-technical users.  
- Extend detection logic to cover boost control and airflow-related anomalies.  
- Group anomalies into logical sequences (e.g., “throttle dip → AFR spike → hesitation”).  
- Add visualization support (e.g., throttle vs. pedal plots, AFR over time, RPM heatmaps).  
- Improve sensor bug detection — e.g., flag repeated static values as potential sensor dropout or MHD logging issues.

---

### Context-Aware Upgrades

- **Context-aware throttle analysis using RPM and boost pressure**  
  - Current throttle mismatch detection is based on pedal vs. throttle position alone.  
  - In turbocharged engines, it's normal for the ECU to **intentionally close the throttle** at full pedal to manage boost (torque management logic).  
  - Adding RPM and/or boost pressure would reduce false positives by distinguishing **expected** vs. **unexpected** throttle closures.  
  - Helps isolate real issues like DME logic faults, throttle lag, or airflow bottlenecks.

- **Support for ignition timing and cylinder-level timing corrections**  
  - Logging ignition timing and corrections can reveal critical issues like:  
    - Knock-induced ignition retard  
    - Cylinder-specific inconsistencies  
    - Unsafe or overly aggressive tuning strategies  
  - These events are often **invisible to the driver** but crucial for engine health.

- **Misfire detection and idle quality analysis**  
  - Many drivers report idle issues as “random pops” or slight surging.  
  - Analyzing AFR noise, RPM fluctuation, and ignition corrections can help detect:  
    - Soft misfires  
    - Fuel delivery imbalance  
    - Inconsistent combustion  
  - Especially valuable for diagnosing idle complaints after a tune.

- **Tune validation tooling**  
  - Tuners often request WOT logs from ~1500 RPM to redline in 3rd gear.  
  - Detector could auto-verify if a log is “clean,” meaning:  
    - Throttle was at 100%  
    - RPM range is valid  
    - No ECU intervention occurred  
  - Automating this helps users avoid wasting tuning time on invalid logs.

