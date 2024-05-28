import easyocr
import cv2
import matplotlib.pyplot as plt

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # 'en' for English

# Function to display the image (optional)
def display_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.show()

# Function to extract text from the image
def extract_text(image_path):
    results = reader.readtext(image_path)
    extracted_text = []
    for (bbox, text, prob) in results:
        print(f"Detected text: {text} (Confidence: {prob:.2f})")
        extracted_text.append(text)
    return extracted_text

# Function to parse extracted text (assuming a specific format)
def parse_details(extracted_text):
    details = {}
    for text in extracted_text:
        if "FULL NAME:" in text:
            details['FULL NAME'] = text.split("DATE OF BIRTH:")[-1].strip()
        elif "DATE OF BIRTH:" in text:
            details['DATE OF BIRTH'] = text.split("DATE OF BIRTH:")[-1].strip()
        elif "PLACE OF BIRTH:" in text:
            details['PLACE OF BIRTH'] = text.split("PLACE OF BIRTH:")[-1].strip()
    return details

# Main function to scan and extract details from an employee ID image
def scan_employee_id(image_path):
    display_image(image_path)  # Display the image (optional)
    extracted_text = extract_text(image_path)
    details = parse_details(extracted_text)
    return details

if __name__ == "__main__":
    # Path to the employee ID image
    image_path = 'IMG_20240109_134142_484.jpg'  

    # Extract and print the details
    details = scan_employee_id(image_path)
    print("\nExtracted Employee Details:")
    for key, value in details.items():
        print(f"{key}: {value}")
