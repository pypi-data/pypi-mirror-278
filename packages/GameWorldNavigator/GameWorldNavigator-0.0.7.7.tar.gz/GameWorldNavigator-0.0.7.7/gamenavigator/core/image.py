from pathlib import Path

import cv2
from cv2.typing import MatLike


class Image:
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._cv2_image = cv2.imread(filename)

    @property
    def cv2_image(self) -> MatLike:
        return self._cv2_image

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def image_name(self) -> str:
        return Path(self._filename).name

    def set_filename(self, filename: str):
        self._filename = filename
        self._cv2_image = cv2.imread(filename)
