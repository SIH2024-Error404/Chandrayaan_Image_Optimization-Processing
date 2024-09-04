import cv2
import numpy as np
import pywt

def apply_wavelet_denoising(image, wavelet='haar', level=2):
    """
    Apply wavelet transform for noise reduction.

    Args:
        image: Input image
        wavelet: Wavelet type (default: 'haar')
        level: Decomposition level (default: 2)

    Returns:
        Denoised image
    """

    # Convert the image to grayscale if it's color
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Decompose the image into approximation and detail coefficients
    coeffs = pywt.wavedec2(image, wavelet, level=level, mode='per')

    # Threshold the detail coefficients to remove noise
    coeffs_thresholded = [coeffs[0]]  # Keep the approximation coefficients untouched
    coeffs_thresholded += [tuple(pywt.threshold(detail, np.median(detail) / 2, mode='soft')
                                 for detail in level_details) for level_details in coeffs[1:]]

    # Reconstruct the image from the thresholded coefficients
    return pywt.waverec2(coeffs_thresholded, wavelet)

def deep_learning_denoising(image, model=None):
    """
    Apply deep learning-based denoising using a pre-trained model.

    Args:
        image: Input image (should be a grayscale image)
        model: Pre-trained deep learning model for denoising (optional)

    Returns:
        Denoised image
    """

    if len(image.shape) == 3:
        # Convert to grayscale if necessary
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if model is None:
        print("Deep learning model not available. Using default denoising.")
        return apply_wavelet_denoising(image)
    else:
        # Replace with model inference code if model is available
        return model.predict(image)
