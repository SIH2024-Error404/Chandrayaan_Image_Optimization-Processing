# src/advanced_denoising.py
import cv2
import numpy as np
import pywt
from metadata_handling import extract_metadata, save_metadata

def apply_wavelet_denoising(image, wavelet='haar', level=2):
    """
    Applies wavelet denoising to the image.
    """
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    coeffs = pywt.wavedec2(image, wavelet, level=level, mode='per')
    coeffs_thresholded = [coeffs[0]]
    coeffs_thresholded += [tuple(pywt.threshold(detail, np.median(detail) / 2, mode='soft')
                                 for detail in level_details) for level_details in coeffs[1:]]
    return pywt.waverec2(coeffs_thresholded, wavelet)

def deep_learning_denoising(image, model=None):
    """
    Applies deep learning-based denoising to the image.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if model is None:
        print("Deep learning model not available. Using default denoising.")
        return apply_wavelet_denoising(image)
    else:
        return model.predict(image)

def denoise_and_save(image_path, model=None):
    """
    Denoises the image and saves the result.
    Also extracts and saves metadata.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    denoised_image = deep_learning_denoising(image, model)
    
    # Save denoised image
    processed_image_path = image_path.replace('raw', 'processed').replace('.png', '_denoised.png')
    cv2.imwrite(processed_image_path, denoised_image)
    
    # Extract and save metadata
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace('.png', '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
