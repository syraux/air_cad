import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(
        self,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ):
        base_options = python.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        self.detector = vision.HandLandmarker.create_from_options(options)


    def process_frame(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(mp_image)

        landmarks_data = []

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                current_hand = []
                for lm in hand_landmarks:
                    current_hand.append({
                        "x": int(lm.x * w),
                        "y": int(lm.y * h),
                        "z": lm.z
                    })
                landmarks_data.append(current_hand)

        return result, landmarks_data

    def draw_landmarks(self, frame, result):
        # Optional: visualization left minimal on purpose
        pass
