from flask import Flask, request, jsonify
import easyocr
import werkzeug

app = Flask(__name__)

@app.route('/extract_info', methods=['POST'])
def extract_info():
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Save the image file
    imagefile = request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    imagefile.save(filename)

    # Perform OCR on the image
    results = reader.readtext(filename)

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

    if full_names:
        full_names = max(full_names, key=len)
    else:
        full_names = None

    # Return the extracted information
    return jsonify({"ID Number": id_number, "Full Names": full_names})

if __name__ == '__main__':
    app.run(debug=True)