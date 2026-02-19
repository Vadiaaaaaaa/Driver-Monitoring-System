import time


class BlinkDetector:
    def __init__(self, ear_threshold=0.25):
        self.ear_threshold = ear_threshold
        self.eye_closed = False
        self.blink_count = 0
        self.start_time = time.time()

    def update(self, ear):
        current_time = time.time()

        # Detect blink event
        if ear < self.ear_threshold and not self.eye_closed:
            self.eye_closed = True

        elif ear >= self.ear_threshold and self.eye_closed:
            self.eye_closed = False
            self.blink_count += 1

        # Calculate blink rate per minute
        elapsed_minutes = (current_time - self.start_time) / 60.0
        blink_rate = 0

        if elapsed_minutes > 0:
            blink_rate = self.blink_count / elapsed_minutes

        return {
            "blink_count": self.blink_count,
            "blink_rate": blink_rate
        }
