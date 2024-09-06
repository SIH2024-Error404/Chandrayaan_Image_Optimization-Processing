# src/preprocessing.py
import cv2
import numpy as np
import os
from metadata_handling import extract_metadata, save_metadata

def reduce_noise(image):

    return cv2.GaussianBlur(image, (5, 5), 0)

def adjust_contrast(image, alpha=2.0, beta=70):

    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def crop_and_align(image, x, y, width, height):

    return image[y:y+height, x:x+width]

def preprocess_and_save(image_path):


    if not image_path:
        raise ValueError("Image path is None or invalid")

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image file not found at path: {image_path}")

    # Example preprocessing (convert to grayscale as a placeholder)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocess image
    processed_image = reduce_noise(gray_image)
    processed_image = adjust_contrast(processed_image)
    
    # Ensure directory exists
    processed_image_dir = os.path.dirname(image_path).replace('raw', 'processed')
    metadata_dir = os.path.dirname(image_path).replace('raw', 'metadata')
    os.makedirs(processed_image_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Save processed image
    processed_image_path = os.path.join(processed_image_dir, os.path.basename(image_path).replace('.png', '_processed.png'))
    cv2.imwrite(processed_image_path, processed_image)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = os.path.join(metadata_dir, os.path.basename(image_path).replace('.png', '_metadata.json'))
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
