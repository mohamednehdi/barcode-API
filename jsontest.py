from flask import Flask, render_template, request, jsonify
import os
import cv2
from pyzbar import pyzbar
from pylibdmtx.pylibdmtx import decode

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ensure_upload_directory():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def detect_barcodes(image_path):
    image = cv2.imread(image_path)
    barcodes = pyzbar.decode(image)
    detected_barcodes = []

    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        detected_barcodes.append({"data": barcodeData, "type": barcodeType})

    data_matrix_codes = decode(image)
    for code in data_matrix_codes:
        code_data = code.data.decode("utf-8")
        detected_barcodes.append({"data": code_data, "type": "DataMatrix"})

    return detected_barcodes

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        ensure_upload_directory()
        file = request.files['file']
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            detected_barcodes = detect_barcodes(filename)
            if request.accept_mimetypes.accept_json:
                return jsonify(detected_barcodes)
            else:
                return render_template("result.html", filename=file.filename, detected_barcodes=detected_barcodes)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
