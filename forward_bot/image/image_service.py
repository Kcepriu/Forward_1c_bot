import cv2
from pyzbar import pyzbar
import numpy as np


class ImageQR:
    def __init__(self, filename=None, byte_string=None):
        if filename:
            self.img = cv2.imread(filename)
        elif byte_string:
            np_arr = np.frombuffer(byte_string, np.uint8)
            self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        else:
            self.img = None

        (self.h, self.w, self.d) = self.img.shape

    def decode_barcodes(self):
        barcodes = pyzbar.decode(self.img)

        if barcodes:
            barcode = barcodes[0]
            barcode_data = barcode.data.decode("utf-8")
            return barcode_data
        else:
            return None
