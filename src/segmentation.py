# src/segmentation.py
import cv2
import numpy as np

def segment_image(image_path, output_path):
    """
    Segments the image using a simple thresholding method.
    Saves the segmented image to the specified path.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise FileNotFoundError(f"Image at path {image_path} not found or cannot be read.")
    
    # Apply a simple threshold for segmentation
    _, segmented_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    
    # Save the segmented image
    cv2.imwrite(output_path, segmented_image)

    return output_path
