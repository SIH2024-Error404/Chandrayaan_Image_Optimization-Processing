# src/psr_mapping.py
import cv2
import numpy as np
from metadata_handling import extract_metadata, save_metadata

def detect_psr_regions(image, threshold=0.5):
    """
    Detects PSR regions in the image using a binary threshold.
    """
    _, binary_image = cv2.threshold(image, threshold * 255, 255, cv2.THRESH_BINARY)
    return binary_image

def overlay_on_map(image, lunar_map):
    """
    Overlays the PSR regions onto a lunar map.
    """
    return cv2.addWeighted(lunar_map, 0.5, image, 0.5, 0)

def map_psr_and_save(image_path, lunar_map_path):
    """
    Maps PSR regions and saves the result.
    Also extracts and saves metadata.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    psr_regions = detect_psr_regions(image)
    lunar_map = cv2.imread(lunar_map_path, cv2.IMREAD_GRAYSCALE)
    
    overlayed_image = overlay_on_map(psr_regions, lunar_map)
    
    # Save processed PSR image
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_psr_mapped.png')
    cv2.imwrite(processed_image_path, overlayed_image)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
