import cv2
import numpy as np

class OmnidirParam:
    """
    OpenCV魚眼カメラパラメータ読み込み
    """
    def __init__(self, parampath='omnidirectionalCalibrate.xml'):
        fs = cv2.FileStorage(parampath, cv2.FileStorage_READ)
        self.K = fs.getNode('K').mat()
        self.D = fs.getNode('D').mat()
        self.xi = fs.getNode('Xi').mat()