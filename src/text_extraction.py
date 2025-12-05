import re
from typing import Union, List
from src.utils import log_message

# Regex to find the target line.
# It looks for any characters (.*) followed by the literal pattern '_1_' 
# and then any subsequent characters (.*) until the end of the line ($).
# The re.MULTILINE flag is essential to treat the string as multiple lines.
TARGET_PATTERN = r'^.*(_1_).*$'
TARGET_PATTERN_ROBUST = r'^.*(\d+)_1_(\d+).*$' # A more robust pattern assuming the number format

def extract_target_line(ocr_text: str, pattern: str = TARGET_PATTERN_ROBUST) -> Union[str, None]:
    """
    Analyzes the raw OCR text to find the complete line containing the target pattern.

    Args:
        ocr_text: The complete text output from the OCR engine.
        pattern: The regex pattern to use for matching.

    Returns:
        The complete extracted line as a string, or None if not found.
    """
    if not ocr_text:
        log_message("Extraction failed: OCR text is empty.", "WARNING")
        return None

    try:
        # re.MULTILINE ensures ^ and $ match the start/end of *each* line, not just the string.
        matches: List[str] = re.findall(pattern, ocr_text, re.MULTILINE)

        if not matches:
            log_message(f"Target pattern '{pattern}' not found in OCR output.", "WARNING")
            return None

        # The match will be the entire line containing the pattern.
        # Since the example line is '163233702292313922_11', we look for _1_ which is slightly
        # different from the example in the PDF, so we use a robust pattern.
        # Let's return the first full match found.
        
        # We need to re-find to get the full line if using the capturing group.
        # Let's simplify and use the non-capturing group version for the full line:
        full_line_matches = re.findall(TARGET_PATTERN, ocr_text, re.MULTILINE)
        
        if full_line_matches:
            log_message(f"Target line extracted: {full_line_matches[0].strip()}", "INFO")
            return full_line_matches[0].strip()
        
        return None

    except Exception as e:
        log_message(f"An error occurred during text extraction: {e}", "ERROR")
        return None