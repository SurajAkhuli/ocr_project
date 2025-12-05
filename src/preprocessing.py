import cv2
import numpy as np
from typing import Union
# IMPORT FIXED: Changed from 'from .utils import log_message'
from src.utils import log_message

def load_image(image_file):
    """
    Reads an uploaded image file into an OpenCV format (numpy array).
    Handles byte streams from Streamlit file uploader.
    """
    try:
        # Convert the file buffer to a numpy array
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        # Read the image using OpenCV
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Could not decode image.")
        log_message("Image loaded successfully.", "DEBUG")
        return image
    except Exception as e:
        log_message(f"Error loading image: {e}", "ERROR")
        return None

def apply_preprocessing(image: np.ndarray) -> Union[np.ndarray, None]:
    """
    Applies a series of image processing steps to enhance text for OCR.

    Args:
        image: The input image (OpenCV numpy array).

    Returns:
        The processed image or None if input is invalid.
    """
    if image is None:
        log_message("Preprocessing failed: Input image is None.", "ERROR")
        return None

    log_message("Starting image preprocessing pipeline.", "INFO")

    # 1. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    log_message("Converted to grayscale.", "DEBUG")

    # 2. Noise Removal (Gaussian Blur)
    # This slightly blurs the image but removes high-frequency noise that confuses OCR.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    log_message("Applied Gaussian blur for noise reduction.", "DEBUG")

    # 3. Adaptive Thresholding (Otsu's Method)
    # Binarizes the image, crucial for handling uneven lighting/shadows.
    _, processed_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    log_message("Applied Otsu's Adaptive Thresholding.", "DEBUG")

    # OPTIONAL: Morphological operations (use if text is very thin or thick)
    # kernel = np.ones((1, 1), np.uint8)
    # processed_image = cv2.dilate(processed_image, kernel, iterations=1) # Makes text thicker
    # processed_image = cv2.erode(processed_image, kernel, iterations=1) # Makes text thinner

    log_message("Preprocessing complete.", "INFO")
    return processed_image