import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the image file
image_path = 'id-card.jpg'

# Perform OCR on the image
result = reader.readtext(image_path)

# Function to find the Huduma Namba
def extract_huduma_namba(results):
    for res in results:
        text = res[1]
        if 'ID NUMER' in text or 'id numer' in text:
            return text.split()[-1] 

# Extract and print the Huduma Namba
huduma_namba = extract_huduma_namba(result)
print("ID NUMER:", huduma_namba)
