from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import werkzeug

app = Flask(__name__)
CORS(app)

@app.route('/extract_info', methods=['POST'])
def extract_info():
    if 'img-id' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Save the image file
    imagefile = request.files['img-id']
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

    first_name = None
    middle_name = None
    sir_name = None
    if full_names:
        full_names = max(full_names, key=len)
        names = full_names.split()
        if len(names) == 3:
            first_name, middle_name, sir_name = names
        elif len(names) == 2:
            first_name, middle_name, sir_name = None
    else:
        full_names = None

    # Return the extracted information
    return jsonify({"ID_Number": id_number, "First_Name": first_name, "Middle_Name": middle_name, "Sir_Name": sir_name})

if __name__ == '__main__':
    app.run(debug=True)