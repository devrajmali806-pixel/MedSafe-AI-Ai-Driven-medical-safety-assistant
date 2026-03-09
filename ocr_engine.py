import pytesseract
import cv2
import numpy as np

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text(image):

    # Convert image to numpy array
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR text extraction
    text = pytesseract.image_to_string(gray)

    return text