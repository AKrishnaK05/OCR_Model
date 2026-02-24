# 🔍 Advanced Image-to-Text OCR Model

A state-of-the-art **Optical Character Recognition (OCR)** web application built with Python. This tool leverages deep learning and advanced computer vision to extract text from images with extreme precision, even in challenging conditions like poor lighting, perspective distortion, or low contrast.

## 🔗 Live Application
**[Experience the Demo Here](https://ocrmodel-dh22ahgtyxqhesfhkvzhqp.streamlit.app/)**

---

## ✨ Key Features

### 🎯 Advanced Accuracy Suite
*   **Auto-Deskewing**: Automatically detects text tilt and rotates the image to align it horizontally.
*   **CLAHE (Contrast Enhancement)**: Locally optimizes contrast to make text "pop," especially helpful for photos taken in shadows or uneven light.
*   **Edge Sharpening**: Digitally enhances character boundaries to help the OCR engine distinguish similar shapes (e.g., 'O' vs '0').
*   **Adaptive Thresholding**: Handles varying background colors and textures intelligently.

### 🧠 Intelligent Layout Analysis
*   **Paragraph Mode**: Uses custom geometric logic to group detected text into natural paragraphs, preserving the original reading order.
*   **Multi-Language Engine**: native support for English, Hindi, French, Spanish, and German.

### 🛠️ Developer-First Experience
*   **Robust Image Handling**: Built-in protection against unsupported data types (stable 1-bit, grayscale, and RGB support).
*   **Instant Export**: One-click download of extracted text as a `.txt` file.
*   **Interactive UI**: Side-by-side comparison of processed images and annotated results.

---

## � How It Works

The platform follows a sophisticated **Vision Pipeline**:
1.  **Image Normalization**: Automatically converts any uploaded file (PNG, JPG, JPEG) into a high-fidelity 8-bit RGB format.
2.  **Preprocessing Chain**: Applies selected filters (Rescaling -> Grayscale -> Denoising -> Deskew/CLAHE -> Sharpness) in a specific order to maximize character legibility.
3.  **Neural Recognition**: Utilizes **EasyOCR** (powered by PyTorch) to perform deep-learning recognition on the optimized image.
4.  **Spatial Sorting**: Runs a coordinate-based sorting algorithm to ensure the digital text matches the human reading order.

---

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Vision Engine**: [OpenCV](https://opencv.org/) & [Pillow](https://python-pillow.org/)
- **OCR Engine**: [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Deep Learning)
- **Data Backbone**: [NumPy](https://numpy.org/)

---

## 📦 Local Development

1. **Clone & Enter**:
   ```bash
   git clone <your-repo-url>
   cd OCR_Model
   ```

2. **Environment Setup**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Core Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch**:
   ```bash
   streamlit run app.py
   ```

---
