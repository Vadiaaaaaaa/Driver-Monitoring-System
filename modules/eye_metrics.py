import time
from scipy.spatial import distance


class EyeMetrics:
    def __init__(self, ear_threshold=0.25, drowsy_time_threshold=1.5):
        self.ear_threshold = ear_threshold
        self.drowsy_time_threshold = drowsy_time_threshold
        self.drowsy_start_time = None

        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def compute_ear(self, landmarks, eye_indices, frame_shape):
        h, w, _ = frame_shape
        
        points = []
        for idx in eye_indices:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            points.append((x, y))

        A = distance.euclidean(points[1], points[5])
        B = distance.euclidean(points[2], points[4])
        C = distance.euclidean(points[0], points[3])

        ear = (A + B) / (2.0 * C)
        return ear

    def update(self, face_landmarks, frame_shape):
        left_ear = self.compute_ear(face_landmarks, self.LEFT_EYE, frame_shape)
        right_ear = self.compute_ear(face_landmarks, self.RIGHT_EYE, frame_shape)
        avg_ear = (left_ear + right_ear) / 2.0

        drowsy = False

        if avg_ear < self.ear_threshold:
            if self.drowsy_start_time is None:
                self.drowsy_start_time = time.time()
            else:
                elapsed = time.time() - self.drowsy_start_time
                if elapsed >= self.drowsy_time_threshold:
                    drowsy = True
        else:
            self.drowsy_start_time = None

        return {
            "ear": avg_ear,
            "drowsy": drowsy
        }
