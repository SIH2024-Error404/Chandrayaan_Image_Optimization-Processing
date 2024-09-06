# src/enhancement.py
import cv2
import numpy as np
from skimage import exposure
from metadata_handling import extract_metadata, save_metadata

def enhance_image(image):
    """
    Enhances the image using histogram equalization.
    """
    image_float = np.float32(image)
    
    if len(image_float.shape) == 3:
        image_gray = cv2.cvtColor(image_float, cv2.COLOR_BGR2GRAY)
        enhanced_gray = exposure.equalize_hist(image_gray)
        enhanced_image = cv2.merge([enhanced_gray]*3)
    else:
        enhanced_image = exposure.equalize_hist(image_float)
    
    enhanced_image = np.uint8(enhanced_image * 255)
    
    return enhanced_image

def apply_retinex(image):
    """
    Applies Retinex algorithm for image enhancement.
    """
    image = np.float32(image) + 1.0

    if len(image.shape) == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    scales = [15, 80, 250]
    result = np.zeros_like(image_gray)
    
    for scale in scales:
        blurred = cv2.GaussianBlur(image_gray, (5, 5), scale)
        log_image = np.log(image + 1.0)
        log_blurred = np.log(blurred + 1.0)
        result += log_image - log_blurred
    
    result = np.exp(result)
    result = np.uint8(result / np.max(result) * 255)
    
    return result

def enhance_and_save(image_path):
    """
    Enhances the image and saves the result.
    Also extracts and saves metadata.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    enhanced_image = enhance_image(image)
    
    # Save enhanced image
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_enhanced.png')
    cv2.imwrite(processed_image_path, enhanced_image)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
