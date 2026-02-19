import cv2
import time
import uuid
import requests
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from modules.eye_metrics import EyeMetrics
from modules.head_pose import HeadPose
from modules.blink_detector import BlinkDetector
from modules.risk_model import RiskModel

# -----------------------------
# CONFIGURATION
# -----------------------------

API_URL = "http://127.0.0.1:8000/metrics"

DEVICE_ID = "vehicle_001"
SESSION_ID = str(uuid.uuid4())

SEND_INTERVAL = 1.0  # seconds between POSTs
last_sent_time = 0

# -----------------------------
# MediaPipe Setup
# -----------------------------

base_options = python.BaseOptions(model_asset_path="face_landmarker.task")

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

face_landmarker = vision.FaceLandmarker.create_from_options(options)

# -----------------------------
# Initialize Modules
# -----------------------------

eye_metrics = EyeMetrics()
head_pose = HeadPose()
blink_detector = BlinkDetector()
risk_model = RiskModel()

# -----------------------------
# Webcam Setup
# -----------------------------

cap = cv2.VideoCapture(0)
fps_start_time = time.time()

print(f"Session Started: {SESSION_ID}")
print(f"Device ID: {DEVICE_ID}")

# -----------------------------
# Main Loop
# -----------------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    timestamp = int(time.time() * 1000)
    result = face_landmarker.detect_for_video(mp_image, timestamp)

    state = "NO FACE"
    risk_score = 0
    avg_ear = 0
    blink_rate = 0
    yaw = 0
    pitch = 0

    if result.face_landmarks:
        for face_landmarks in result.face_landmarks:

            # ---- Eye ----
            eye_data = eye_metrics.update(face_landmarks, frame.shape)
            avg_ear = eye_data["ear"]

            # ---- Blink ----
            blink_data = blink_detector.update(avg_ear)
            blink_rate = blink_data["blink_rate"]

            # ---- Head Pose ----
            head_data = head_pose.update(face_landmarks, frame.shape)
            yaw = head_data["yaw"]
            pitch = head_data["pitch"]

            # ---- Risk ----
            risk_data = risk_model.compute(eye_data, head_data, blink_rate)
            risk_score = risk_data["risk_score"]
            state = risk_data["state"]

    # -----------------------------
    # Throttled Network Send
    # -----------------------------

    current_time = time.time()

    if current_time - last_sent_time >= SEND_INTERVAL:

        payload = {
            "device_id": DEVICE_ID,
            "session_id": SESSION_ID,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "ear": float(avg_ear),
            "yaw": float(yaw),
            "pitch": float(pitch),
            "blink_rate": float(blink_rate),
            "risk_score": float(risk_score),
            "state": state
        }

        try:
            requests.post(API_URL, json=payload, timeout=1)
        except:
            pass

        last_sent_time = current_time

    # -----------------------------
    # Display
    # -----------------------------

    cv2.putText(frame, f"Device: {DEVICE_ID}", (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"State: {state}", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(frame, f"Risk: {risk_score:.2f}", (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("AI Driver Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
