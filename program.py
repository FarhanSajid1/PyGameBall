import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

for file in os.listdir('.'):
    if file.endswith('.png'):
        if 'E' not in file:
            img = plt.imread(file)
            plt.imshow(img)
            plt.show()