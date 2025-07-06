# Blurring image
import numpy as np
import cv2
from matplotlib import pyplot as plt


def blur(imgPath):
    img = cv2.imread("image.jpg")                                   # Loading the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                      # BRG to RGB

    k = 20                                                          # kernel size(Intensity of Blur)
    pad = k // 2                                                    # padding size
    kernel = np.ones((k, k), dtype=np.float32) / (k * k)

    blurred_img = np.zeros_like(img)

    for c in range(3):                                              # for each channel
        padded = np.pad(img[:, :, c], pad_width=pad, mode="edge")   # padding added
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                region = padded[i:i+k, j:j+k]
                blurred_img[i, j, c] = np.sum(region * kernel)

    return blurred_img