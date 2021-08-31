import qi, imutils, cv2
import numpy as np
from service import video, tts, memory, motion, alife, posture, atts



class Color:
    def __init__(self, name, lower_bound, upper_bound):
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        


class PictureColorDetector:
    def __init__(self, colors, size, camNum = 0):
        self.colors = colors
        self.size = size
        self.videoClient = video.subscribeCamera("myCam",camNum,2,13,10)


    def getColor(self):
        img = video.getImageRemote(self.videoClient)        
        video.releaseImage(self.videoClient)

        frame = np.reshape(img[6],(-1,img[0],3))
        frame = frame[:, 150:]
        frame = frame[:, :-150]
        # frame = imutils.resize(frame, width=640)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # mask = np.zeros((img[1],img[0]),dtype = int)
        mask = np.zeros((img[1],img[0]-300), np.uint8)
        for color in self.colors:
            mask = mask | cv2.inRange(hsv, color.lower_bound, color.upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        col = None
        detectedColors = []
        
        if len(cnts) == 0:
            return detectedColors
        c = max(cnts, key=cv2.contourArea)
        if cv2.contourArea(c) < self.size:
            return detectedColors        
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        detectedColors.append(self._pixelColor(hsv[center[1],center[0]]))
        return detectedColors


    def _pixelColor(self, pixel):
        for color in self.colors:
            if pixel[0] in range(color.lower_bound[0], color.upper_bound[0] + 1):
                return color.name
        raise Exception("Impossible Error, Pixel not identified")


    def __del__(self):
        video.unsubscribe(self.videoClient)