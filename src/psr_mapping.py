# src/psr_mapping.py
import cv2
import json
import os
import shutil
from metadata_handling import extract_metadata, save_metadata

def detect_psr_regions(image, threshold=0.5):
    """
    Detects PSR regions in the image using a binary threshold.
    """
    _, binary_image = cv2.threshold(image, threshold * 255, 255, cv2.THRESH_BINARY)
    return binary_image

def overlay_on_map(psr_image, lunar_map):
    """
    Overlays the PSR regions onto a lunar map.
    """
    return cv2.addWeighted(lunar_map, 0.5, psr_image, 0.5, 0)

def map_psr_and_save(image_path, lunar_map_path, export_dir=None):
    """
    Maps PSR regions and saves the result.
    Optionally exports the PSR map and metadata if export_dir is specified.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    psr_regions = detect_psr_regions(image)
    lunar_map = cv2.imread(lunar_map_path, cv2.IMREAD_GRAYSCALE)
    
    overlayed_image = overlay_on_map(psr_regions, lunar_map)
    
    # Save processed PSR image locally
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_psr_mapped.png')
    cv2.imwrite(processed_image_path, overlayed_image)
    
    # Extract metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    # Export PSR map and metadata if an export directory is specified
    if export_dir:
        os.makedirs(export_dir, exist_ok=True)
        
        # Export metadata
        export_metadata_path = os.path.join(export_dir, "metadata.json")
        with open(export_metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        # Export PSR map
        psr_map_export_path = os.path.join(export_dir, "psr_mapped.png")
        cv2.imwrite(psr_map_export_path, overlayed_image)
    
    return processed_image_path
