# src/preprocessing.py
import cv2
import numpy as np
from metadata_handling import extract_metadata, save_metadata

def reduce_noise(image):
    """
    Applies Gaussian blur to reduce noise in the image.
    """
    return cv2.GaussianBlur(image, (5, 5), 0)

def adjust_contrast(image, alpha=1.0, beta=0):
    """
    Adjusts the contrast of the image.
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def crop_and_align(image, x, y, width, height):
    """
    Crops and aligns the image based on the given coordinates.
    """
    return image[y:y+height, x:x+width]

def preprocess_and_save(image_path):
    """
    Preprocesses the image by reducing noise, adjusting contrast, and saving it.
    Also extracts and saves metadata.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Preprocess image
    processed_image = reduce_noise(image)
    processed_image = adjust_contrast(processed_image)
    
    # Save processed image
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_processed.png')
    cv2.imwrite(processed_image_path, processed_image)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
