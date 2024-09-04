import numpy as np
import cv2
def calculate_snr(image, noise):
    """
    Calculate the Signal-to-Noise Ratio (SNR) of the image.
    
    Parameters:
    - image: Enhanced image
    - noise: Noise component or reference image
    """
    signal = np.mean(image)
    noise_std = np.std(noise)
    return 20 * np.log10(signal / noise_std)

def extract_features(image):
    """
    Extract key features such as crater edges and ridges.
    """
    # Example: Canny edge detection
    edges = cv2.Canny(image, 100, 200)
    return edges

def compare_images(original, enhanced):
    """
    Compare raw and enhanced images side-by-side.
    """
    return np.hstack((original, enhanced))
