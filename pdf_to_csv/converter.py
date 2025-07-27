from pytesseract import image_to_string

def extract_text_from_area(image, coords):
    left, top, right, bottom = map(int, coords)
    cropped = image.crop((left, top, right, bottom))
    text = image_to_string(cropped)
    return text