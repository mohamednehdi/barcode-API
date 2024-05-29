import cv2
from pyzbar import pyzbar
from pylibdmtx.pylibdmtx import decode

def detect_barcodes(image_path):
    # Load the input image
    image = cv2.imread(image_path)

    # Find QR codes and normal barcodes
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # Find DataMatrix codes
    data_matrix_codes = decode(image)
    for code in data_matrix_codes:
        (x, y, w, h) = code.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        code_data = code.data.decode("utf-8")
        cv2.putText(image, code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] Found DataMatrix code: {}".format(code_data))

    # Show the output image
    cv2.imshow("Detected Codes", image)
    cv2.waitKey(0)

if __name__ == "__main__":
    image_path = "C:/Users/Mega-PC/Documents/barcode test/images/Image_1.png"  # Replace with the actual path to your image
    detect_barcodes(image_path)
