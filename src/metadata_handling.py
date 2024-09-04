# src/metadata_handling.py
import json
import os

def extract_metadata(image_path):
    """
    Extracts metadata from the image file.
    """
    metadata = {
        "file_name": os.path.basename(image_path),
        "file_size": os.path.getsize(image_path),
        "creation_time": os.path.getctime(image_path),
        "modification_time": os.path.getmtime(image_path)
    }
    return metadata

def save_metadata(metadata, metadata_path):
    """
    Saves metadata to a JSON file.
    """
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
