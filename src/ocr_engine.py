import pytesseract
from PIL import Image
import numpy as np
import io
from typing import Union
from src.utils import log_message

# Configuration for Tesseract (adjust path if needed, especially on Windows)
# Example for Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Tesseract Configuration for Document Processing
# PSM 6: Assume a single uniform block of text. This is often best for structured documents.
# OEM 3: Default, based on what is available (best performance).
TESSERACT_CONFIG = r'--psm 6 --oem 3'

def perform_ocr(processed_image: np.ndarray) -> Union[str, None]:
    """
    Performs OCR on the preprocessed image using Tesseract.

    Args:
        processed_image: The image ready for OCR (typically binarized/thresholded).

    Returns:
        The raw text output from Tesseract or None on failure.
    """
    if processed_image is None:
        log_message("OCR failed: Input image is None.", "ERROR")
        return None

    try:
        # Convert OpenCV image (NumPy array) to a Pillow Image object
        # Tesseract wrapper works well with Pillow objects.
        pil_image = Image.fromarray(processed_image)

        log_message("Starting Tesseract OCR.", "INFO")
        
        # Perform OCR
        raw_text = pytesseract.image_to_string(
            pil_image, 
            config=TESSERACT_CONFIG, 
            lang='eng'
        )

        log_message("Tesseract OCR completed.", "INFO")
        return raw_text.strip()
    
    except pytesseract.TesseractNotFoundError:
        log_message("Tesseract not found. Please ensure it is installed and configured.", "CRITICAL")
        return "ERROR: Tesseract OCR is not installed or the path is incorrect."
    except Exception as e:
        log_message(f"An error occurred during OCR: {e}", "ERROR")
        return None
