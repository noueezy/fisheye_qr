import numpy as np
import cv2
import math
import datetime
import time
import threading
from pyzbar.pyzbar import decode 

import unit_sphere as us
import omnidir_param as omnp
import centroid as ct
import undistort220 as u220
import nano_camera as nc


#魚眼パラメータロード
param = omnp.OmnidirParam()

th = nc.NanoCamera()
th.start()

while True:
    try:
        now = datetime.datetime.now()
        print("\ndatetime: {}".format(now))

        img = th.retrieve()

        #重心検出
        u, v = ct.detect_centroid(img)
        print(" centroid: {} {}".format(u, v))

        # 検出した重心を単位球面の座標に変換
        unit_sph_xyz = us.unit_sphere([[u, v]], param.K, param.D, param.xi[0,0])
        print(" unit sphere: {}".format(unit_sph_xyz))
        x = unit_sph_xyz[0][0]
        y = unit_sph_xyz[0][1]
        z = unit_sph_xyz[0][2]

        #単位球面の座標を極座標に変換
        r = math.sqrt(x*x + y*y + z*z)
        theta = math.acos(z/r)
        phi = math.atan2(y,x)
        print(" polar coord r:{} theta:{} phi:{}".format(r, theta, phi))
    
        ud = u220.Undistort220()
        R =  np.dot(u220.rot_y_axis(-theta), u220.rot_z_axis(-phi))
        dstimg = ud.undistort(img, R)
        d = decode(dstimg)

        if len(d) == 0:
            continue

        print(d[0].data.decode("utf-8"))

        strnow = "{0:%Y%m%d%H%M%S}".format(now)
        cv2.imwrite("{}_capture.jpg".format(strnow), img)

        cv2.circle(img=img, center=(int(u), int(v)), radius=4, color=(0,255, 0), thickness=-1)

        cropimg = ud.crop_area(img, R)
        cv2.imwrite("{}_undistort.jpg".format(strnow), dstimg)
        cv2.imwrite("{}_crop.jpg".format(strnow), cropimg)

    
    except KeyboardInterrupt:
        break

th.stop()
th.join()
