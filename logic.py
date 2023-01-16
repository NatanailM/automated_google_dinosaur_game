import cv2
from PIL import ImageGrab
import numpy as np


class Object:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.location = None

    def match(self, scr):
        res = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        start_loc = max_loc
        end_loc = (start_loc[0] + self.width, start_loc[1] + self.height)

        if max_val > 0.8:
            self.location = (start_loc, end_loc)
            return True
        else:
            self.location = None
            return False


def record_screen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
