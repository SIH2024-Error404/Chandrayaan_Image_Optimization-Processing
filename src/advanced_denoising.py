# src/advanced_denoising.py
import cv2
import numpy as np
import os
import pywt
from metadata_handling import extract_metadata, save_metadata

def apply_wavelet_denoising(image, wavelet='db4', level=2):

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform wavelet decomposition
    coeffs = pywt.wavedec2(image, wavelet, level=level, mode='per')

    # Apply thresholding to each detail coefficient
    coeffs_thresholded = [coeffs[0]]  # Approximation coefficients
    for details in coeffs[1:]:
        coeffs_thresholded.append(tuple(pywt.threshold(detail, np.median(detail) / 2, mode='soft') for detail in details))
    
    # Perform wavelet reconstruction
    return pywt.waverec2(coeffs_thresholded, wavelet, mode='per')

def deep_learning_denoising(image, model=None):
    
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if model is None:
        print("Deep learning model not available. Using default denoising.")
        return apply_wavelet_denoising(image)
    else:
        return model.predict(image)

def denoise_and_save(image_path, model=None):
    
    if not image_path:
        raise ValueError("Image path is None or invalid")

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image file not found at path: {image_path}")

    denoised_image = deep_learning_denoising(image, model)
    
    
    processed_image_path = image_path.replace('raw', 'processed').replace(os.path.splitext(image_path)[1], '_denoised.png')
    cv2.imwrite(processed_image_path, denoised_image)
    
   
    metadata = extract_metadata(image_path)
    metadata_path = image_path.replace('raw', 'metadata').replace(os.path.splitext(image_path)[1], '_metadata.json')
    save_metadata(metadata, metadata_path)
    
    return processed_image_path
