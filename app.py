import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

# Set page config
st.set_page_config(page_title="Advanced OCR App", layout="wide")

st.title("Advanced Image to Text OCR")
st.markdown("Upload an image to extract text with advanced options.")

# Sidebar for controls
st.sidebar.header("Settings")

# Language Selection
langs = st.sidebar.multiselect("Select Languages", ['en', 'hi', 'fr', 'es', 'de'], default=['en'])

# Preprocessing Options
st.sidebar.subheader("Preprocessing")
use_grayscale = st.sidebar.checkbox("Convert to Grayscale", value=True)

# Rescaling
rescale_factor = st.sidebar.slider("Rescale Image (Upscale for small text)", 1.0, 3.0, 1.0, 0.5)

# Denoising
use_denoising = st.sidebar.checkbox("Apply Noise Removal (Denoising)", value=False)

# Thresholding Types
threshold_type = st.sidebar.selectbox("Thresholding Method", ["None", "Simple Binary", "Adaptive Gaussian"])

threshold_value = 128
if threshold_type == "Simple Binary":
    threshold_value = st.sidebar.slider("Threshold Value", 0, 255, 128)

use_dilation = st.sidebar.checkbox("Apply Dilation (Thicken Text)", value=False)

st.sidebar.subheader("Advanced Accuracy")
use_clahe = st.sidebar.checkbox("Use CLAHE (Auto-Contrast)", value=False)
use_deskew = st.sidebar.checkbox("Auto-Deskew (Fix Rotation)", value=False)
use_sharpen = st.sidebar.checkbox("Apply Sharpening Filter", value=False)

st.sidebar.subheader("OCR Settings")
use_paragraph = st.sidebar.checkbox("Paragraph Mode (Groups Text)", value=False)

@st.cache_resource
def load_reader(languages):
    return easyocr.Reader(languages)

# Main App Logic
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load and preprocess image
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image, dtype=np.uint8)
    
    # Preprocessing Chain
    processed_img = img_array.copy()
    
    # 1. Rescaling
    if rescale_factor > 1.0:
        processed_img = cv2.resize(processed_img, None, fx=rescale_factor, fy=rescale_factor, interpolation=cv2.INTER_CUBIC)

    # 2. Grayscale
    if use_grayscale:
        if len(processed_img.shape) == 3:
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
    
    # 3. Denoising
    if use_denoising:
        # fastNlMeansDenoising is good but slow. simple medianBlur is faster.
        # Let's use helpful median blur for OCR
        processed_img = cv2.medianBlur(processed_img, 3) 
        
    # 4. Thresholding
    if threshold_type == "Simple Binary":
        # Ensure we work on grayscale
        if len(processed_img.shape) == 3:
             processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
        _, processed_img = cv2.threshold(processed_img, threshold_value, 255, cv2.THRESH_BINARY)
    elif threshold_type == "Adaptive Gaussian":
         if len(processed_img.shape) == 3:
             processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
         processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
    # 5. Dilation
    if use_dilation:
        kernel = np.ones((2,2), np.uint8)
        processed_img = cv2.dilate(processed_img, kernel, iterations=1)

    # 6. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    if use_clahe:
        # Convert to grayscale if not already
        if len(processed_img.shape) == 3:
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        processed_img = clahe.apply(processed_img)

    # 7. Auto-Deskew
    if use_deskew:
        if len(processed_img.shape) == 3:
            gray_skew = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
        else:
            gray_skew = processed_img
        
        # Binary threshold for contour detection
        _, thresh = cv2.threshold(gray_skew, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle logic
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        (h, w) = processed_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        processed_img = cv2.warpAffine(processed_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # 8. Sharpening
    if use_sharpen:
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        processed_img = cv2.filter2D(processed_img, -1, kernel)

    # Visualization
    col1, col2 = st.columns(2)

    
    with col1:
        st.subheader("Original/Processed Image")
        has_preprocessing = (
            use_grayscale
            or use_denoising
            or use_dilation
            or threshold_type != "None"
            or rescale_factor > 1.0
        )
        display_img = processed_img if has_preprocessing else image
        st.image(display_img, caption="Image for OCR", use_container_width=True)

    with col2:
        st.subheader("OCR Results")
        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                try:
                    reader = load_reader(langs)
                    
                    # EasyOCR with paragraph=True groups text but changes return format
                    if use_paragraph:
                        # Improved Paragraph Mode using Smart Sorting (Manual Grouping) instead of EasyOCR's built-in
                        # EasyOCR's paragraph=True is too aggressive for layouts. We will use standard detection + Custom Layout Analysis.
                        results = reader.readtext(processed_img)
                        
                        # Helper to sort boxes into lines
                        boxes = []
                        for res in results:
                            bbox = res[0]
                            # bbox points: tl, tr, br, bl
                            tl, tr, br, bl = bbox
                            
                            # Center Y and Height
                            center_y = (tl[1] + bl[1]) / 2
                            height = abs(bl[1] - tl[1])
                            tl_x = tl[0]
                            
                            boxes.append({'res': res, 'center_y': center_y, 'height': height, 'tl_x': tl_x})
                            
                        # Sort initially by Y to process top-down
                        boxes.sort(key=lambda b: b['center_y'])
                        
                        lines = []
                        current_line = []
                        
                        for box in boxes:
                            if not current_line:
                                current_line.append(box)
                                continue
                            
                            # Extremely robust grouping:
                            # Use the average height of the current line to determine a grouping threshold
                            line_heights = [b['height'] for b in current_line]
                            avg_height = sum(line_heights) / len(line_heights)
                            
                            # Group if the new box's center is within 70% of a line height from the previous box's center
                            last_box = current_line[-1]
                            y_dist = abs(box['center_y'] - last_box['center_y'])
                            
                            if y_dist < (avg_height * 0.7):
                                current_line.append(box)
                            else:
                                lines.append(current_line)
                                current_line = [box]
                        
                        if current_line:
                            lines.append(current_line)
                            
                        # Sort each line by X-coordinate (Left to Right)
                        sorted_results = []
                        for line in lines:
                            line.sort(key=lambda b: b['tl_x'])
                            for b in line:
                                sorted_results.append(b['res'])
                        
                        results = sorted_results
                        extracted_text_list = [text for (_, text, _) in results]
                        annotated_img = np.array(image)
                        
                        # Visualization with Reading Order Index
                        for idx, (bbox, text, _) in enumerate(results):
                            (tl, tr, br, bl) = bbox
                            tl = (int(tl[0]), int(tl[1]))
                            br = (int(br[0]), int(br[1]))
                            
                            color = (0, 255, 0)
                            cv2.rectangle(annotated_img, tl, br, color, 2)
                            # Show Index ID to verify order
                            cv2.putText(annotated_img, f"{idx+1}", (tl[0], tl[1] - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                    else:
                        results = reader.readtext(processed_img)
                        # Standard Sort (Top-Down with 30px leeway)
                        results.sort(key=lambda r: (int(r[0][0][1] / 30), r[0][0][0]))
                        
                        extracted_text_list = [text for (_, text, _) in results]
                        annotated_img = np.array(image)
                        
                        for (bbox, text, _) in results:
                            (tl, tr, br, bl) = bbox
                            tl = (int(tl[0]), int(tl[1]))
                            br = (int(br[0]), int(br[1]))
                            cv2.rectangle(annotated_img, tl, br, (0, 255, 0), 2)
                            cv2.putText(annotated_img, text, (tl[0], tl[1] - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    st.image(annotated_img, caption="Detected Text", use_container_width=True)
                    
                    final_text = "\n".join(extracted_text_list)
                    st.text_area("Extracted Text", final_text, height=200)
                    
                    st.download_button("Download Text", final_text, file_name="extracted_text.txt")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
