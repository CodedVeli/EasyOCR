import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the image file
image_path = 'unnamed.jpg'  

# Perform OCR on the image
results = reader.readtext(image_path)

# Initialize variables to store extracted information
id_number = None
full_names = []

# Improved extraction logic
for result in results:
    text = result[1].strip()
    # Check for ID number
    if len(text) == 8 and text.isdigit():
        id_number = text
    # Check for full names (basic heuristic: more than one word and mostly alphabetic)
    elif len(text.split()) > 1 and all(char.isalpha() or char.isspace() for char in text):
        full_names.append(text)

# Assume the longest alphabetic segment is the name (basic heuristic)
if full_names:
    full_names = max(full_names, key=len)
else:
    full_names = None

# Print the extracted information
print("ID Number:", id_number)
print("Full Names:", full_names)

# Optionally, print all results for debugging
for result in results:
    print(result)
