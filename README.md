# AI Driver Monitoring System

Real-Time Fatigue and Distraction Detection with Analytics Dashboard

## Overview

This project implements a real-time AI-based Driver Monitoring System (DMS) that detects driver fatigue and distraction using computer vision and behavioral modeling.

The system processes live webcam input, extracts facial landmarks using MediaPipe Face Mesh, computes eye metrics and head pose, and classifies driver state using a multi-factor risk fusion model. Logged session data is visualized through a cloud-deployed analytics dashboard.

---

## System Architecture

### Edge Layer (Real-Time Engine)

* Face landmark detection (468-point mesh via MediaPipe)
* Eye Aspect Ratio (EAR) computation
* Head pose estimation (yaw, pitch)
* Blink detection with duration validation
* Temporal risk modeling and state classification
* Session-based telemetry logging

### Analytics Layer (Dashboard)

* Session and device-level filtering
* Risk trend visualization
* Blink rate analysis
* Head pose distribution
* Driver state breakdown
* Cloud deployment via Streamlit

---

## Key Features

### Real-Time Face Landmark Detection

* Uses MediaPipe Face Mesh for high-resolution facial landmark extraction
* Processes live webcam input at approximately 20–30 FPS

### Drowsiness Detection (EAR-Based)

* Implements Eye Aspect Ratio (EAR) computation
* Applies exponential smoothing to reduce jitter
* Detects sustained eye closure (>1.5 seconds)
* Prevents false positives from normal blinks

### Blink Detection

* Time-based blink validation (minimum closure duration)
* Computes blink rate per minute
* Identifies abnormal blink patterns

### Head Pose-Based Distraction Detection

* Estimates yaw angle from facial landmarks
* Triggers distraction only when head deviation is sustained (>2 seconds)
* Ignores transient head movements

### Multi-Factor Risk Fusion Model

Combines:

* Eye closure duration
* Head pose deviation
* Blink rate abnormality

Produces behavioral states:

* ATTENTIVE
* DISTRACTED
* HIGH RISK

### Interactive Analytics Dashboard

* Device-level filtering
* Session-level filtering
* Risk score over time
* Blink rate trends
* Head yaw distribution
* Driver state distribution

---

## Technologies Used

* Python
* OpenCV
* MediaPipe (Face Mesh)
* NumPy / SciPy
* FastAPI (Telemetry Backend – optional)
* SQLAlchemy
* Streamlit
* Matplotlib
* Git and GitHub

---

## Project Structure

```
Driver-Monitoring-System/
│
├── engine.py
├── modules/
│   ├── eye_metrics.py
│   ├── head_pose.py
│   ├── blink_detector.py
│   ├── risk_model.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── session_logs.csv
│
├── backend/  (optional API layer)
│
└── README.md
```

---

## How It Works

1. Webcam captures real-time video.
2. MediaPipe extracts facial landmarks.
3. Eye Aspect Ratio (EAR) is computed per frame.
4. Head yaw and pitch are estimated.
5. Blink detection validates sustained eye closure.
6. A temporal risk model computes driver state.
7. Metrics are logged per session.
8. Dashboard visualizes behavioral trends.

---

## Engineering Highlights

* Implemented temporal gating to eliminate false blink-triggered alerts.
* Applied exponential smoothing to reduce landmark noise.
* Designed modular architecture separating perception, behavior modeling, and analytics.
* Built a multi-signal risk fusion model instead of single-threshold logic.
* Structured system for extensibility and future ML integration.

---

## Future Improvements

* Deep learning-based driver state classifier
* Adaptive EAR calibration per user
* Cloud database integration (PostgreSQL / Supabase)
* Real-time WebSocket streaming dashboard
* Edge device deployment (Jetson / Raspberry Pi)

