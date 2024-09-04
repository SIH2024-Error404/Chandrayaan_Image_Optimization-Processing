import cv2
import numpy as np

def detect_psr_regions(image, threshold=0.5):
    """
    Detect PSR regions using thresholding or other segmentation techniques.
    """
    _, binary_image = cv2.threshold(image, threshold * 255, 255, cv2.THRESH_BINARY)
    return binary_image

def overlay_on_map(image, lunar_map):
    """
    Overlay the image on a lunar map for geospatial context.
    """
    return cv2.addWeighted(lunar_map, 0.5, image, 0.5, 0)
