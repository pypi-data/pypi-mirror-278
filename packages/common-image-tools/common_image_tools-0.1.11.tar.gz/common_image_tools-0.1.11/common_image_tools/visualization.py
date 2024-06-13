# -*- coding: utf-8 -*-
import cv2


def draw_points_shape(img, roi_points, color):
    for v in range(1, len(roi_points)):
        cv2.line(img, roi_points[v], roi_points[v - 1], color, 2)

    cv2.line(img, roi_points[0], roi_points[-1], color, 2)

    return img
