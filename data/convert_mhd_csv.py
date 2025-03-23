import csv

"""
Convert a real MHD CSV log to a simplified trace format.

This script reads a .csv log file and writes a formatted text trace
to 'data/mhd_trace.txt', preserving engine parameters in a readable format.

Intended for inspection or further parsing in downstream tools.
"""

input_file = "data/2020-02-25 07_06_10 9E60B v1.csv"  # <- Rename your CSV to match this
output_file = "data/mhd_trace.txt"

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    reader = csv.DictReader(f_in)
    for row in reader:
        msg = f"[MHD] ENG: RPM={row['RPM (rpm)']}, AFR={row['Lambda bank 1 (AFR)']}, Throttle={row['Throttle Position (*)']}, VANOS_IN_act={row['VANOS IN act. (*)']}, VANOS_IN_req={row['VANOS IN req. (*)']}\n"
        f_out.write(msg)

print("✅ MHD log formatted and written to mhd_trace.txt")
