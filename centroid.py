import numpy as np
import cv2

def detect_centroid(img):
    
    # グレースケール変換→2値化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)

    # 明るい領域の輪郭を検出
    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    maxCont = contours[0]
    for c in contours:
        if len(maxCont) < len(c):
            maxCont = c

    # 重心を計算
    mu = cv2.moments(maxCont)
    x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    return x, y

