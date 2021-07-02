import cv2
import numpy as np


img = cv2.imread("C:\\Users\\tsi_nao\\Desktop\\nao_projects\\src\\vision\\camImage.png", cv2.IMREAD_COLOR)

cv2.imshow("Input Image", img)
cv2.waitKey(0)

detector = cv2.SimpleBlobDetector_create()
keyppoint_info = detector.detect(img)
blank_img = np.zeros((1,1))
blobs = cv2.drawKeypoints(img, keyppoint_info, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("displaying blobs", blobs)
cv2.waitKey(0)
cv2.destroyAllWindows()
