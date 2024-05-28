import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the image file
image_path = 'id-card.jpg'  # Update this path to the correct image path

# Perform OCR on the image
result = reader.readtext(image_path)

# Function to extract ID number and full names
def extract_info(results):
    id_number = None
    full_names = None
    for res in results:
        text = res[1]
        if 'ID NUMBER' in text or 'ID No.' in text:
            id_number = text.split()[-1]  # Assuming the ID number is the last part of the string
        if 'FULL NAMES' in text:
            full_names = text.split('FULL NAMES')[-1].strip()
        # Check for the case without labels
        if not full_names and not id_number:
            if any(char.isdigit() for char in text):
                potential_id = text.replace(' ', '')
                if potential_id.isdigit() and len(potential_id) >= 7:
                    id_number = potential_id
            else:
                full_names = text

    return id_number, full_names

# Extract and print the ID number and full names
id_number, full_names = extract_info(result)
print("ID Number:", id_number)
print("Full Names:", full_names)

# Display the results for debugging
for detection in result:
    print(detection)
