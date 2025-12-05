import streamlit as st
from PIL import Image
import numpy as np
import io
import json
import os
from datetime import datetime

# Import core modules
from src.preprocessing import load_image, apply_preprocessing
from src.ocr_engine import perform_ocr
from src.text_extraction import extract_target_line, TARGET_PATTERN

# --- UI Configuration ---
st.set_page_config(
    page_title="OCR Text Extraction Assessment",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Application Logic ---

def process_image(uploaded_file):
    """
    Runs the complete image processing and OCR pipeline.
    """
    if uploaded_file is None:
        st.error("Please upload an image file.")
        return

    # 1. Load Image
    original_image = load_image(uploaded_file)
    if original_image is None:
        st.error("Failed to load image. Is it a valid image file?")
        return

    # Display original image
    st.image(original_image, caption='Original Shipping Label Image', width=600)
    
    with st.spinner('Running OCR and Extraction Pipeline...'):
        start_time = datetime.now()
        
        # 2. Preprocessing
        processed_image = apply_preprocessing(original_image)
        if processed_image is None:
            st.error("Preprocessing step failed.")
            return

        # Display preprocessed image for debugging
        st.subheader("🔍 Preprocessed Image (for debugging)")
        st.image(processed_image, caption='Preprocessed Image (Grayscale + Thresholding)', width=600)

        # 3. Perform OCR
        raw_ocr_text = perform_ocr(processed_image)
        
        if raw_ocr_text is None or "ERROR" in raw_ocr_text:
            st.error(f"OCR Failed: {raw_ocr_text}")
            return

        # DEBUG: Show all lines from OCR
        st.subheader("🐛 Debug: OCR Lines Analysis")
        lines = raw_ocr_text.split('\n')
        st.write(f"Total lines detected: {len(lines)}")
        
        with st.expander("View all lines (click to expand)"):
            for i, line in enumerate(lines):
                st.text(f"Line {i}: '{line}' (length: {len(line.strip())})")
                # Check if line contains underscore and 1
                if '_' in line and '1' in line:
                    st.success(f"✓ Line {i} contains '_' and '1': {line}")

        # 4. Target Extraction
        extracted_line = extract_target_line(raw_ocr_text)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()


    # --- Display Results ---
    st.success(f"Processing Complete in {duration:.2f} seconds.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Extracted Target Text")
        if extracted_line:
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 8px; background-color: #f0fff0; border: 2px solid #38761d; font-size: 1.25rem; font-weight: bold; font-family: monospace;">
                {extracted_line}
            </div>
            """, unsafe_allow_html=True)
            
            # Create a mock JSON output structure as required in the assessment
            mock_json_output = {
                "timestamp": end_time.isoformat(),
                "file_name": uploaded_file.name,
                "target_pattern": TARGET_PATTERN,
                "extracted_text": extracted_line,
                "processing_time_seconds": duration,
                "confidence_score": "N/A (Tesseract requires advanced config to report line confidence)"
            }
            
            st.download_button(
                label="📥 Download JSON Result",
                data=json.dumps(mock_json_output, indent=4),
                file_name=f"{uploaded_file.name}_result.json",
                mime="application/json",
            )
            
        else:
            st.warning("⚠️ Target line containing '_1_' not found.")
            st.info("💡 Tip: Check the 'Debug: OCR Lines Analysis' section above to see what was detected.")

    with col2:
        st.subheader("📄 Raw OCR Output")
        st.text_area(
            "Full Text from OCR", 
            raw_ocr_text, 
            height=300
        )
        st.info("The extraction logic scans this raw text to find the line with the target pattern '_1_'.")


# --- Streamlit UI Layout ---
st.title("📦 AI/ML OCR Text Extraction System")
st.markdown("### Shipping Label Identifier Extractor")

st.sidebar.header("📤 Upload Image")
uploaded_file = st.sidebar.file_uploader(
    "Choose a shipping label image (.jpg, .png)", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.sidebar.success("✓ Image uploaded. Click Process to start!")
    
    # Advanced options
    with st.sidebar.expander("⚙️ Advanced Options"):
        show_preprocessed = st.checkbox("Show preprocessed image", value=True)
        show_debug = st.checkbox("Show debug information", value=True)
    
    if st.sidebar.button("⚙️ Process Image", type="primary"):
        process_image(uploaded_file)
    
else:
    st.info("👆 Upload an image of a shipping label to begin the OCR process.")
    
    st.markdown("""
    ### How to use:
    1. Upload a shipping label image using the sidebar
    2. Click the "Process Image" button
    3. View the extracted text containing the pattern `_1_`
    
    ### Expected format:
    The system will extract lines like: `163233702292313922_1_lWV`
    """)