import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file
from pyzbar import pyzbar
from pylibdmtx.pylibdmtx import decode
import io
from PIL import Image
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:4200", supports_credentials=True)

def detect_barcodes(image):
    barcodes = pyzbar.decode(image)
    barcode_info = []

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        barcode_info.append({"type": barcodeType, "data": barcodeData})
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    data_matrix_codes = decode(image)
    for code in data_matrix_codes:
        (x, y, w, h) = code.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        code_data = code.data.decode("utf-8")
        cv2.putText(image, code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        barcode_info.append({"type": "DataMatrix", "data": code_data})
        print("[INFO] Found DataMatrix code: {}".format(code_data))

    return image, barcode_info

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and (file.filename.endswith('.jpg') or file.filename.endswith('.png')):
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image = np.array(image)
        processed_image, barcode_info = detect_barcodes(image)
        _, buffer = cv2.imencode('.jpg', processed_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return jsonify({'image': image_base64, 'barcodes': barcode_info})
    return jsonify({'error': 'Invalid file format. Only JPEG and PNG are supported.'}), 400

if __name__ == "__main__":
    app.run(debug=True)
