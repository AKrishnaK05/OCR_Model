# Advanced Image to Text OCR Model

A powerful, Streamlit-based Web Application for Optical Character Recognition (OCR) built with EasyOCR and OpenCV. This tool allows users to upload images, apply advanced preprocessing filters, and extract text in multiple languages.

## 🚀 Features

- **Multi-language Support**: Extract text in English, Hindi, French, Spanish, and German.
- **Advanced Preprocessing**:
  - **Rescaling**: Upscale images for better detection of small text.
  - **Denoising**: Remove noise for clearer character recognition.
  - **Thresholding**: Simple Binary and Adaptive Gaussian methods for better contrast.
  - **Dilation**: Thicken text to improve OCR accuracy.
- **Layout Analysis**: Custom logic to sort detected text boxes into a natural reading order (Paragraph Mode).
- **Visualization**: Side-by-side comparison of processed images and annotated detection results.
- **Export**: Download extracted text as a `.txt` file.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **OCR Engine**: [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- **Image Processing**: [OpenCV](https://opencv.org/) & [Pillow](https://python-pillow.org/)
- **Numerical Ops**: [NumPy](https://numpy.org/)

## 📦 Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd OCR_Model
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment

This app is ready to be deployed on **Streamlit Cloud** or **Hugging Face Spaces**. Make sure to include the `requirements.txt` file in your repository.

---

Built with ❤️ for LPU PEP.
