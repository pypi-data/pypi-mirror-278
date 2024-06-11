import typing as typ
import cv2
import numpy as np
from loopfinder import utils


def canny_masker(
    img: np.ndarray,
    min_sharpness=100,
):
    return cv2.Canny(img, min_sharpness, min_sharpness + 10)


def mini_canny_masker(
    img: np.ndarray, min_sharpness: int = 100, processing_size=(128, 128)
) -> np.ndarray:
    small_img = cv2.resize(img, processing_size)
    edges = canny_masker(small_img, min_sharpness=min_sharpness)
    return cv2.resize(edges, img.shape[::-1], interpolation=cv2.INTER_NEAREST)


def find_loop(img: np.ndarray) -> typ.Optional[typ.Tuple[int, int]]:
    """
    return values are x, y pixel coordinates of the loop tip.
    returns None if there is no foreground visible.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    mask = mini_canny_masker(gray)
    utils.save_img("mask", mask)
    for y in range(len(mask) - 1, 0, -1):  # starting at the bottom, go upwards
        row = mask[y]
        if any(row):
            nonzero_indexes = np.nonzero(row)[0]
            leftmost = nonzero_indexes[0]
            rightmost = nonzero_indexes[-1]
            x = (rightmost + leftmost) // 2
            return x, y
    return None
