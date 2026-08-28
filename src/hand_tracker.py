import ctypes
import os
from typing import Any

import cv2
import mediapipe as mp
from mediapipe.python import solution_base


WRIST_LANDMARK_INDEX = 0


def get_short_path(path: str) -> str:
    if os.name != "nt":
        return path

    buffer = ctypes.create_unicode_buffer(260)
    result = ctypes.windll.kernel32.GetShortPathNameW(path, buffer, 260)

    if result == 0:
        return path

    return buffer.value


def fix_mediapipe_resource_path() -> None:
    solution_base.__file__ = get_short_path(solution_base.__file__)


class HandTracker:
    def __init__(self) -> None:
        fix_mediapipe_resource_path()

        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.hand_connections = mp.solutions.hands.HAND_CONNECTIONS

    def process_frame(self, frame: Any) -> tuple[Any, Any | None]:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return frame, None

        hand_landmarks = results.multi_hand_landmarks[0]
        self.drawing_utils.draw_landmarks(
            frame,
            hand_landmarks,
            self.hand_connections,
        )

        return frame, hand_landmarks

    def get_hand_x(self, hand_landmarks: Any | None) -> float | None:
        if hand_landmarks is None:
            return None

        wrist = hand_landmarks.landmark[WRIST_LANDMARK_INDEX]
        return max(0.0, min(1.0, wrist.x))

    def close(self) -> None:
        self.hands.close()
