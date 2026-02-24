# Advanced Image to Text OCR Model

A powerful, Streamlit-based Web Application for Optical Character Recognition (OCR) built with EasyOCR and OpenCV.

## 🔗 Live Demo
**Access the app here: [ocrmodel-dh22ahgtyxqhesfhkvzhqp.streamlit.app](https://ocrmodel-dh22ahgtyxqhesfhkvzhqp.streamlit.app/)**

## 🚀 Features

- **Multi-language Support**: Extract text in English, Hindi, French, Spanish, and German.
- **Advanced Accuracy Suite**:
  - **Auto-Deskew**: Automatically fix image rotation.
  - **CLAHE**: Intelligent contrast enhancement for better results in poor lighting.
  - **Sharpening**: Enhance character edges for clearer recognition.
  - **Rescaling**: Upscale small text.
- **Layout Analysis**: Smart Paragraph Mode to preserve natural reading order.
- **Visualization**: Comparison view of processed images vs. annotated results.
- **Export**: Download results as a `.txt` file.

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
