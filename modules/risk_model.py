class RiskModel:
    def __init__(self):
        # Normal behavioral baselines
        self.normal_blink_rate = 15  # avg blinks/min
        self.normal_ear = 0.35       # approximate open-eye EAR

    def compute(self, eye_data, head_data, blink_rate):
        ear = eye_data["ear"]
        yaw = head_data["yaw"]

        # ---------------- Eye Risk ----------------
        # Lower EAR increases risk
        eye_risk = max(0, (self.normal_ear - ear) / self.normal_ear)

        # ---------------- Head Pose Risk ----------------
        # Large yaw increases risk
        head_risk = min(abs(yaw) / 45.0, 1.0)

        # ---------------- Blink Risk ----------------
        # Too high or too low blink rate increases risk
        blink_risk = min(abs(blink_rate - self.normal_blink_rate) / 30.0, 1.0)

        # ---------------- Weighted Fusion ----------------
        risk_score = (
            0.4 * eye_risk +
            0.4 * head_risk +
            0.2 * blink_risk
        )

        # Clamp
        risk_score = min(risk_score, 1.0)

        if risk_score < 0.3:
            state = "ATTENTIVE"
        elif risk_score < 0.6:
            state = "DISTRACTED"
        else:
            state = "HIGH RISK"

        return {
            "risk_score": risk_score,
            "state": state
        }
