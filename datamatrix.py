# import the necessary packages
from pylibdmtx.pylibdmtx import decode
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

# find the DataMatrix codes in the image and decode each of them
data_matrix_codes = decode(image)

# loop over the detected DataMatrix codes
for code in data_matrix_codes:
	# extract the bounding box location of the DataMatrix code and draw the
	# bounding box surrounding the code on the image
	(x, y, w, h) = code.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# the code data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	code_data = code.data.decode("utf-8")
	# draw the code data on the image
	cv2.putText(image, code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 255, 0), 2)
	# print the code data to the terminal
	print("[INFO] Found DataMatrix code: {}".format(code_data))

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
