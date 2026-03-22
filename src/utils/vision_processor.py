try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def extract_data_from_image(image_path):
    if not TESSERACT_AVAILABLE:
        raise ImportError("pytesseract and Pillow are required for OCR functionality. Install with: pip install pytesseract Pillow")
    text = pytesseract.image_to_string(Image.open(image_path))
    return text
