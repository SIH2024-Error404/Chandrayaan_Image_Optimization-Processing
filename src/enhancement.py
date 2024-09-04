import cv2
import numpy as np
from skimage import exposure

def enhance_image(image):
    """
    Enhance the contrast of an image using histogram equalization.

    Parameters:
    - image: Input image (as a NumPy array)

    Returns:
    - Enhanced image (as a NumPy array)
    """
    # Convert image to float
    image_float = np.float32(image)
    
    # Apply histogram equalization
    if len(image_float.shape) == 3:  # Color image
        # Convert to grayscale for histogram equalization
        image_gray = cv2.cvtColor(image_float, cv2.COLOR_BGR2GRAY)
        enhanced_gray = exposure.equalize_hist(image_gray)
        # Convert back to BGR with enhanced contrast
        enhanced_image = cv2.merge([enhanced_gray]*3)
    else:  # Grayscale image
        enhanced_image = exposure.equalize_hist(image_float)
    
    # Convert back to 8-bit image
    enhanced_image = np.uint8(enhanced_image * 255)
    
    return enhanced_image

def apply_retinex(image):
    """
    Enhance the image using Multi-Scale Retinex (MSR).

    Parameters:
    - image: Input image (as a NumPy array)

    Returns:
    - Enhanced image (as a NumPy array)
    """
    # Convert image to float
    image = np.float32(image) + 1.0

    # Convert to grayscale if the image is in color
    if len(image.shape) == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    # Apply Gaussian blur at multiple scales
    scales = [15, 80, 250]
    result = np.zeros_like(image_gray)
    
    for scale in scales:
        blurred = cv2.GaussianBlur(image_gray, (0, 0), scale)
        log_image = np.log(image + 1.0)
        log_blurred = np.log(blurred + 1.0)
        result += log_image - log_blurred
    
    # Normalize and convert to 8-bit image
    result = np.exp(result)
    result = np.uint8(result / np.max(result) * 255)
    
    return result
