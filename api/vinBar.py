import numpy as np
import cv2
import easyocr
import re
import requests
import barcode
from barcode.writer import ImageWriter
import os


def extractVin(image_file):
    # Convert the uploaded file to a NumPy array
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    
    # Decode the image from the buffer
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        print("❌ Failed to decode image from uploaded file.")
        return "Invalid"

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)

    # Combine detected text
    all_text = " ".join([text[1] for text in result])
    print("📄 OCR Text:\n", all_text)

    # VIN pattern (17 characters, excluding I, O, Q)
    vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
    matches = re.findall(vin_pattern, all_text.upper())

    if matches:
        vin = matches[0]
        print("\n✅ Chassis Number Found:", vin)
        return vin
    else:
        print("\n⚠️ No valid chassis number found.")
        return "Invalid"


def generateBarCode(txt):
    os.makedirs("static/barcodes", exist_ok=True)
    barcode_class = barcode.get_barcode_class('code128')
    chassis_barcode = barcode_class(txt, writer=ImageWriter())
    filename = chassis_barcode.save("static/barcodes/" + txt + "_barcode")
    return "barcodes/" + txt + "_barcode"