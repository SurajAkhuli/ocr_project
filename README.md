# 📦 AI/ML OCR Text Extraction System

## Project Overview

This project implements an automated OCR-based text extraction system designed to process shipping label and waybill images. The primary objective is to extract complete text lines containing the pattern `_1_` from various shipping labels with high accuracy.

**Core Functionality:**
- Performs optical character recognition (OCR) on shipping label images
- Applies advanced image preprocessing for enhanced text detection
- Extracts target text lines matching the pattern `_1_`
- Provides a user-friendly Streamlit interface for testing and demonstration

**Target Output Format:** `163233702292313922_1_lWV`

---

## Technical Approach

### OCR Engine
- **Primary Tool:** Tesseract OCR (open-source)
- **Configuration:** PSM 6 (single uniform block of text) with OEM 3 (default engine mode)
- **Language:** English (eng)

### Image Preprocessing Pipeline

The preprocessing module implements a multi-stage approach to enhance text recognition:

1. **Grayscale Conversion:** Reduces image complexity while preserving text features
2. **Gaussian Blur (5x5 kernel):** Removes high-frequency noise that can interfere with OCR
3. **Otsu's Adaptive Thresholding:** Binarizes the image to handle uneven lighting and shadows
4. **Optional Morphological Operations:** Available for fine-tuning text thickness if needed

### Text Extraction Logic

The extraction module uses regex pattern matching to identify target lines:

- **Primary Pattern:** `^.*(_1_).*$` - Captures any line containing the literal pattern `_1_`
- **Robust Pattern:** `^.*(\d+)_1_(\d+).*$` - Matches numeric patterns around `_1_`
- **Multi-line Processing:** Uses `re.MULTILINE` flag to scan each line independently

---

## Installation Instructions

### Prerequisites

1. **Python 3.8+** must be installed on your system
2. **Tesseract OCR** must be installed:
   - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
   - **macOS:** `brew install tesseract`
   - **Windows:** Download installer from [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Setup Steps

```bash
# Clone the repository
git clone <repository-url>
cd surajakhuli-ocr_project

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Windows-Specific Configuration

If you're on Windows, you may need to specify the Tesseract executable path in `src/ocr_engine.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## Usage Guide

### Running the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Upload Image:** Click "Choose a shipping label image" in the sidebar
2. **Configure Options:** Expand "Advanced Options" to toggle debug views
3. **Process:** Click the "⚙️ Process Image" button
4. **View Results:**
   - Extracted target text is displayed in a highlighted box
   - Raw OCR output is shown for reference
   - Debug section shows all detected lines for troubleshooting

### Output Formats

- **On-screen Display:** Visual presentation of extracted text
- **JSON Download:** Structured output including:
  - Timestamp
  - File name
  - Target pattern
  - Extracted text
  - Processing time

---

## Project Structure

```
surajakhuli-ocr_project/
├── app.py                    # Streamlit web application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── src/                      # Core source code
    ├── __init__.py           # Package initializer
    ├── ocr_engine.py         # Tesseract OCR integration
    ├── preprocessing.py      # Image preprocessing pipeline
    ├── text_extraction.py    # Target pattern extraction logic
    └── utils.py              # Logging and utility functions
```

---

## Dependencies

```
opencv-python       # Image processing and manipulation
numpy              # Numerical operations
pytesseract        # Python wrapper for Tesseract OCR
streamlit          # Web application framework
Pillow             # Image file handling
```

---

## Key Features

### ✅ Implemented

- Complete modular architecture with separation of concerns
- Robust image preprocessing pipeline (grayscale, blur, thresholding)
- Tesseract OCR integration with optimized configuration
- Regex-based pattern matching for target text extraction
- Interactive Streamlit UI with real-time processing
- Debug mode showing line-by-line OCR analysis
- JSON export functionality for results
- Comprehensive logging system for debugging
- Error handling for common failure scenarios

### ⏳ Remaining Work

Due to limited time availability alongside my internship commitments:

- **Dataset Testing:** Complete accuracy evaluation on full test dataset with metrics reporting
- **Results Documentation:** OCR screenshots and JSON outputs for all test images
- **Fine-tuning:** Parameter optimization for edge cases and varying image qualities

---

## Challenges & Solutions

### Challenge 1: Pattern Variation
**Issue:** Target patterns appear in various formats across different labels  
**Solution:** Implemented two regex patterns (basic and robust) to handle format variations

### Challenge 2: Image Quality
**Issue:** Some images have noise, shadows, or uneven lighting  
**Solution:** Multi-stage preprocessing with Gaussian blur and Otsu's thresholding

### Challenge 3: Character Recognition
**Issue:** Partially erased or degraded characters in some images  
**Solution:** Configured Tesseract with PSM 6 mode for structured text detection

### Challenge 4: Debugging OCR Failures
**Issue:** Difficulty identifying why certain lines weren't detected  
**Solution:** Added comprehensive debug mode showing all detected lines with character analysis

---

## Future Improvements

1. **Deep Learning Integration**
   - Implement CRAFT or EasyOCR for improved text detection
   - Fine-tune models on shipping label dataset

2. **Enhanced Preprocessing**
   - Automatic image rotation correction
   - Perspective transformation for skewed images
   - Adaptive binarization based on local image regions

3. **Post-Processing**
   - Spell-checking and correction for common OCR errors
   - Confidence-based filtering of results
   - Pattern validation against expected formats

4. **Production Features**
   - Batch processing API
   - Database integration for result storage
   - Real-time monitoring and logging dashboard

5. **Accuracy Improvements**
   - Ensemble approach combining multiple OCR engines
   - Custom character recognition for problematic symbols
   - Machine learning-based pattern correction

---

## Performance Metrics

**Target Requirement:** ≥75% accuracy on `_1_` pattern extraction

**Current Status:** Architecture complete, accuracy evaluation pending full dataset testing

---

## Development Notes

**Note:** Due to limited time availability alongside my internship, the system could not be fully tested on the complete test dataset. However, the codebase reflects a complete architecture with modular design, robust preprocessing pipeline, Tesseract OCR integration, and regex-based extraction logic. The core functionality is implemented and operational. Given additional time, I am fully capable of completing the accuracy testing, generating all required documentation, and fine-tuning the system for optimal performance.

---

## Troubleshooting

### Common Issues

**Tesseract Not Found Error**
```
Solution: Ensure Tesseract is installed and path is correctly set in ocr_engine.py
```

**Image Upload Fails**
```
Solution: Check image format (must be .jpg, .jpeg, or .png) and file size
```

**No Text Extracted**
```
Solution: Check debug section to see raw OCR output, may need preprocessing adjustment
```

**Pattern Not Found**
```
Solution: Verify the pattern exists in the image using the debug view showing all lines
```

---

## Contact & Support

For questions, clarifications, or issues:
- **Email-id:** surajakhuli6@gmail.com
- **Project Issues:** Submit via GitHub Issues

---

## License

This project is submitted as part of the AI/ML Developer Assessment Task.

---

## Acknowledgments

- Tesseract OCR for providing open-source OCR capabilities
- OpenCV community for image processing tools
- Streamlit for the intuitive web framework

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Author:** Suraj Akhuli
