# src/export.py
import os
from metadata_handling import extract_metadata, export_metadata
from psr_mapping import export_psr_map

def export_results(image_path, psr_image, export_dir):
    """
    Exports metadata and PSR mapped image.
    """
    # Extract and export metadata
    metadata = extract_metadata(image_path)
    metadata_export_path = export_dir + '/' + os.path.basename(image_path).replace('.png', '_metadata.csv')
    export_metadata(metadata, metadata_export_path)

    # Export PSR mapped image
    psr_image_export_path = export_dir + '/' + os.path.basename(image_path).replace('.png', '_psr_mapped_export.png')
    export_psr_map(psr_image, psr_image_export_path)
