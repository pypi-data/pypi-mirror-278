# import the necessary packages
import cv2

def get_blurry_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm_value = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm_value