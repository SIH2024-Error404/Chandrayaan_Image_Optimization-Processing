# src/export_handling.py
import json
import os
import shutil

def export_metadata(metadata, export_dir):

    os.makedirs(export_dir, exist_ok=True)
    metadata_path = os.path.join(export_dir, "metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def export_psr_map(image_path, export_dir):
    os.makedirs(export_dir, exist_ok=True)
    psr_map_export_path = os.path.join(export_dir, os.path.basename(image_path))
    shutil.copy(image_path, psr_map_export_path)

    return psr_map_export_path
