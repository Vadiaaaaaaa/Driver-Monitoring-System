import cv2
import numpy as np
import time


class HeadPose:
    def __init__(self, distraction_time_threshold=2.0):
        self.distraction_time_threshold = distraction_time_threshold
        self.distraction_start_time = None

        # 3D model points (approximate human face model)
        self.model_points = np.array([
            (0.0, 0.0, 0.0),          # Nose tip
            (0.0, -330.0, -65.0),     # Chin
            (-225.0, 170.0, -135.0),  # Left eye corner
            (225.0, 170.0, -135.0),   # Right eye corner
            (-150.0, -150.0, -125.0), # Left mouth corner
            (150.0, -150.0, -125.0)   # Right mouth corner
        ])

    def update(self, landmarks, frame_shape):
        h, w, _ = frame_shape

        # 2D image points from MediaPipe landmarks
        image_points = np.array([
            (landmarks[1].x * w, landmarks[1].y * h),     # Nose
            (landmarks[152].x * w, landmarks[152].y * h), # Chin
            (landmarks[33].x * w, landmarks[33].y * h),   # Left eye corner
            (landmarks[263].x * w, landmarks[263].y * h), # Right eye corner
            (landmarks[61].x * w, landmarks[61].y * h),   # Left mouth
            (landmarks[291].x * w, landmarks[291].y * h)  # Right mouth
        ], dtype="double")

        # Camera matrix
        focal_length = w
        center = (w / 2, h / 2)

        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1))

        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        rmat, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

        pitch, yaw, roll = angles

        distracted = False

        if abs(yaw) > 20:
            if self.distraction_start_time is None:
                self.distraction_start_time = time.time()
            else:
                elapsed = time.time() - self.distraction_start_time
                if elapsed >= self.distraction_time_threshold:
                    distracted = True
        else:
            self.distraction_start_time = None

        return {
            "yaw": yaw,
            "pitch": pitch,
            "roll": roll,
            "distracted": distracted
        }
