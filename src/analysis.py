# src/analysis.py
import numpy as np
import cv2
import os
from metadata_handling import extract_metadata, save_metadata

def extract_features(image):
    """
    Extracts features from the image (e.g., edges).
    """
    edges = cv2.Canny(image, 100, 200)
    return edges

def compare_images(original, enhanced):
    """
    Compares the original image with the enhanced image.
    """
    return np.hstack((original, enhanced))

def analyze_and_save(image_path, enhanced_image_path):
    """
    Analyzes the image and saves the results.
    Also extracts and saves metadata.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    enhanced_image = cv2.imread(enhanced_image_path, cv2.IMREAD_GRAYSCALE)

    # Extract features from the original image
    features = extract_features(image)

    # Save analysis results
    base_name = os.path.basename(image_path)
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_features.png')
    cv2.imwrite(processed_image_path, features)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path, metadata_path
