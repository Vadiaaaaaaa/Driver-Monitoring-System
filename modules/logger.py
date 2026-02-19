import csv
import os
from datetime import datetime


class SessionLogger:
    def __init__(self, filename="data/session_logs.csv"):
        self.filename = filename

        # If file doesn't exist OR is empty → write headers
        if (not os.path.exists(self.filename)) or os.path.getsize(self.filename) == 0:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timestamp",
                    "ear",
                    "yaw",
                    "pitch",
                    "blink_rate",
                    "risk_score",
                    "state"
                ])

    def log(self, ear, yaw, pitch, blink_rate, risk_score, state):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().isoformat(),
                ear,
                yaw,
                pitch,
                blink_rate,
                risk_score,
                state
            ])
