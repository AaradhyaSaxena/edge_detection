import numpy as np
import matplotlib.pyplot as plt
import cv2

## adjust dimensions of image
def pre_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape
    h = h - h%5
    w = w - w%5
    img = img[0:h,0:w]
    
    return img

