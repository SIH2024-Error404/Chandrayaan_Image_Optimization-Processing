import cv2
import numpy as np

def reduce_noise(image):
    """
    Apply noise reduction using Gaussian blur or other techniques.
    """
    return cv2.GaussianBlur(image, (5, 5), 0)

def adjust_contrast(image, alpha=1.0, beta=0):
    """
    Adjust the contrast of an image.
    
    Parameters:
    - alpha: Contrast control (1.0 = no change)
    - beta: Brightness control (0 = no change)
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def crop_and_align(image, x, y, width, height):
    """
    Crop the image to the specified bounding box.
    
    Parameters:
    - x, y: Top-left corner of the crop box
    - width, height: Dimensions of the crop box
    """
    return image[y:y+height, x:x+width]
