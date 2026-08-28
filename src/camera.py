from typing import Any

import cv2


class Camera:
    def __init__(self, index: int = 0) -> None:
        self.index = index
        self.capture: cv2.VideoCapture | None = None

    def open(self) -> None:
        self.capture = cv2.VideoCapture(self.index)

        if not self.is_opened():
            self.release()
            raise RuntimeError(f"Kamera acilamadi. Kamera indeksi: {self.index}")

    def read_frame(self) -> tuple[bool, Any]:
        if not self.is_opened() or self.capture is None:
            return False, None

        return self.capture.read()

    def is_opened(self) -> bool:
        return self.capture is not None and self.capture.isOpened()

    def release(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None
