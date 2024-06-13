# -*- coding: utf-8 -*-
import cv2
import numpy as np


def is_inside(point: tuple, shape: list) -> bool:
    """
    Checks if a given point lies inside or on the boundary of a shape.

    This function uses the OpenCV function cv2.pointPolygonTest to determine whether the point is inside the shape,
    on the boundary, or outside the shape.

    Parameters:
        point (tuple): A tuple representing the (x, y) coordinates of the point.
        shape (list): A list of tuples representing the vertices of the shape in the format [(x1, y1), (x2, y2), ...].

    Returns:
        bool: True if the point is inside or on the boundary of the shape, False otherwise.

    Note:
        The pointPolygonTest function returns +1 if the point is inside the contour, -1 if it is outside, and 0 if
        it is on the contour.

    Example:
        >>> is_inside((50, 50), [(0, 0), (100, 0), (100, 100), (0, 100)])
        Returns True if the point (50, 50) is inside the square [(0, 0), (100, 0), (100, 100), (0, 100)].
    """
    ctn = np.array(shape)
    ctn = ctn.reshape((-1, 1, 2))

    # When measureDist=false , the return value is +1, -1, and 0, respectively. Otherwise, the return value is a
    # signed distance between the point and the nearest contour edge.
    result = cv2.pointPolygonTest(ctn, point, measureDist=False)

    return result >= 0
