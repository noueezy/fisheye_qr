import cv2
import datetime
import time
import threading

# gstreamerコマンド スマホ画面上のQRコードを撮影するために露出を抑えている
GST_STR = 'nvarguscamerasrc exposuretimerange="2000000 2000000" gainrange="1 1" ispdigitalgainrange="1 1" wbmode=0\
    ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)21/1 \
    ! nvvidconv ! video/x-raw, width=(int)3264, height=(int)2464, format=(string)BGRx \
    ! videoconvert \
    ! appsink'

class NanoCamera(threading.Thread):

    def __init__(self):
        print('init')
        super(NanoCamera, self).__init__()
        self.stop_event = threading.Event()
        self.count = 0
        self.lock = threading.Lock()
        self.cap = cv2.VideoCapture(GST_STR, cv2.CAP_GSTREAMER)
        time.sleep(1)


    def stop(self):
        """
        撮影スレッドを停止する
        """
        self.stop_event.set()

    def run(self):
        """
        撮影スレッド
        """
        print('Running start')
        while not self.stop_event.is_set():
            self.lock.acquire()
            ret, self.img = self.cap.read()
            self.lock.release()
            if ret == False:
                raise ValueError('capture error')
            self.count += 1
        print('Running end')
    
    def retrieve(self):
        """
        撮影した最新の画像を取得
        """
        self.lock.acquire()
        img = self.img.copy()
        self.lock.release()
        return img

if __name__ == "__main__":
    th = NanoCamera()
    th.start()
    for i in range(5):
        print(i)
        now = datetime.datetime.now()
        imgpath = "{0:%Y%m%d%H%M%S}.jpg".format(now)
        print(imgpath)
        cv2.imwrite(imgpath, th.retrieve())
        time.sleep(1)
    th.stop()
    th.join()

