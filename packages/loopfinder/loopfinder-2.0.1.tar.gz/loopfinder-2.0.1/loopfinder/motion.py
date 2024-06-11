###############################################################################
# This file is part of the lib-maxiv-loopfinder project.
#
# Copyright Lund University
#
# Distributed under the GNU GPLv3 license. See LICENSE file for more info.
###############################################################################
import logging
import math
import typing as typ
import numpy as np
import dataclasses

from loopfinder.vision import find_loop

logger = logging.getLogger("loopfinder")


@dataclasses.dataclass
class Step:
    """
    A step for the goniometer to perform before
    the next call to `CentringSequence.step()`.

    Attributes:
        rotate: Rotate by this many degrees.
            Works either clockwise or anticlockwise
            as long as you are consistent.
        x_to_center: move the sample so this x position is in the center.
        y_to_center: move the sample so this y position is in the center.
    """

    rotate: typ.Optional[float] = None
    x_to_center: typ.Optional[float] = None
    y_to_center: typ.Optional[float] = None

    def finished(self) -> bool:
        """
        An empty step means you are finished.
        """
        return all(
            getattr(self, field.name) is None for field in dataclasses.fields(self)
        )


class CentringNavigator:
    def __init__(self, target_coordinates: typ.Tuple[int, int], tolerance: int):
        self.found_in_2d = False
        self.target_coordinates = target_coordinates
        self.tolerance = tolerance

    def distance_to_target(self, x: int, y: int) -> float:
        tx, ty = self.target_coordinates
        return math.sqrt((x - tx) ** 2 + (y - ty) ** 2)

    def centered(self, x, y) -> bool:
        return self.distance_to_target(x, y) < self.tolerance

    def next_step(self, img: np.ndarray) -> Step:
        """
        Args:
            img: the current image from the diffractometer camera in RGB/BGR
        Returns:
            A Step object which instructs you what motors should be moved and how much
            before calling next_step again with a new image. When step.finished() is
            True, then the centring is finished.
        """
        loop_pos = find_loop(img)
        if loop_pos:
            if self.distance_to_target(*loop_pos) < self.tolerance:
                if self.found_in_2d:
                    logger.debug("loop centring finished!")
                    return Step()
                self.found_in_2d = True
                logger.debug(
                    "the loop is now found in two dimensions, rotating 90 degrees."
                )
                return Step(rotate=90)
            else:
                logger.debug(
                    "Loop is off-center, translating {} to beam".format(loop_pos)
                )
                self.found_in_2d = False
                x, y = loop_pos
                return Step(x_to_center=x, y_to_center=y)
        else:  # no foreground is visible
            logger.debug(
                "I see nothing. fishing for loop, rot70 and moving half a screen down"
            )
            self.found_in_2d = False
            return Step(
                rotate=70, x_to_center=img.shape[1] // 2, y_to_center=img.shape[0]
            )
