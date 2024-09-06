import json
import os
from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(image_path):

    def get_exif_data(image_path):
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return {}
            return {TAGS.get(tag, tag): value for tag, value in exif_data.items() if tag in TAGS}
    
    with Image.open(image_path) as img:
        width, height = img.size
        format = img.format
        color_mode = img.mode
        orientation = "Portrait" if height > width else "Landscape"
        exif_data = get_exif_data(image_path)
        gps_info = exif_data.get("GPSInfo", "N/A")
    
    metadata = {
        "file_name": os.path.basename(image_path),
        "file_size": os.path.getsize(image_path),
        "creation_time": os.path.getctime(image_path),
        "modification_time": os.path.getmtime(image_path),
        "width": width,
        "height": height,
        "format": format,
        "color_mode": color_mode,
        "orientation": orientation,
    }
    return metadata

def save_metadata(metadata, metadata_path):

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
