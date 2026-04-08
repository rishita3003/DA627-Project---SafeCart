import easyocr
import cv2

# Initialize once (important)
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return "Image not readable"

    results = reader.readtext(img)

    # Combine detected text
    extracted_text = " ".join([res[1] for res in results])

    return extracted_text
