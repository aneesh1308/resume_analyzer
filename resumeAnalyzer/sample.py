import tempfile

import easyocr
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images


def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    extracted_text = []
    for result in results:
        words = result[1].split(' ')  # Split only when a space occurs
        extracted_text.extend(words)
    return extracted_text


pdf_path = r"C:\Users\Ani\OneDrive\Documents\pdfs\AneeshA R Resume.pdf"

images = convert_pdf_to_images(pdf_path)

for i, image in enumerate(images):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
        image.save(temp_image.name)

value = extract_text_from_image(temp_image.name)
print(len(value))
