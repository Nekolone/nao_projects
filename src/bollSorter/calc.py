import cv2 as cv
import numpy as np



color = np.uint8([[[45,80,130 ]]])
hsv_green = cv.cvtColor(color,cv.COLOR_BGR2HSV)
print(hsv_green)