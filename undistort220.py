import cv2
import numpy as np
import math
import omnidir_param


def rot_x_axis(rad_x):
    rotvec = np.array([rad_x, 0.0, 0.0])
    Rx, jac = cv2.Rodrigues(rotvec)
    return Rx

def rot_y_axis(rad_y):
    rotvec = np.array([0.0, rad_y, 0.0])
    Ry, jac = cv2.Rodrigues(rotvec)
    return Ry

def rot_z_axis(rad_z):
    rotvec = np.array([0.0, 0.0, rad_z])
    Rz, jac = cv2.Rodrigues(rotvec)
    return Rz


class Undistort220:

    def __init__(self):
        self.param = omnidir_param.OmnidirParam()
        self.DST_WIDTH = 512
        self.DST_HEIGHT = 512
        self.DST_CHANNEL = 3
        self.newKPers = np.array([
            [ self.DST_HEIGHT/2/math.tan(math.radians(25.0)), 1.0, self.DST_WIDTH/2 ],
            [ 1.0, self.DST_HEIGHT/2/math.tan(math.radians(25.0)), self.DST_HEIGHT/2 ],
            [ 0.0, 0.0, 1]
        ])
        self.grid = 50


    def undistort(self, srcimg, R):
       
        dstimg = np.zeros((self.DST_WIDTH, self.DST_HEIGHT, self.DST_CHANNEL))
        size = (self.DST_WIDTH, self.DST_HEIGHT)

        dstimg = cv2.omnidir.undistortImage(srcimg, self.param.K, self.param.D, self.param.xi, \
        cv2.omnidir.RECTIFY_PERSPECTIVE, dstimg, self.newKPers, size, R)
        return dstimg

    def crop_area(self, srcimg, R):
        # 点の描画        
        pointimg = self.__write_crop_point(srcimg, R)
        #枠の描画
        dstimg = self.__write_crop_frame(pointimg, R)
        return dstimg

    def __write_crop_point(self, srcimg, R):
        fp_pixel = self.newKPers[0,0]
        h_width = self.DST_WIDTH/2
        h_height = self.DST_HEIGHT/2
        dif_w = self.DST_WIDTH/self.grid
        dif_h = self.DST_HEIGHT/self.grid
        rvec = np.array([0.0, 0.0, 0.0])
        tvec = np.array([0.0, 0.0, 0.0])

        tmp = [[-h_width + w * dif_w, -h_height + h * dif_h, fp_pixel] for w in range(0, self.grid+1) for h in range(0, self.grid+1)]
        objectPoints = [ np.dot(op, R) for op in tmp ]

        imagePoints, jacobian = cv2.omnidir.projectPoints(np.array([objectPoints]), rvec, tvec, self.param.K, self.param.xi[0,0], self.param.D)
        pts = np.array(imagePoints[0], np.int32)
        dstimg = srcimg.copy()
        for ip in pts:
            cv2.circle(img=dstimg, center=(int(ip[0]), int(ip[1])), radius=1, color=(0,0,255), thickness=-1)
        return dstimg

    def __write_crop_frame(self, srcimg, R):
        fp_pixel = self.newKPers[0,0]
        h_width = self.DST_WIDTH/2
        h_height = self.DST_HEIGHT/2
        dif_w = self.DST_WIDTH/self.grid
        dif_h = self.DST_HEIGHT/self.grid
        rvec = np.array([0.0, 0.0, 0.0])
        tvec = np.array([0.0, 0.0, 0.0])

        tmp0 = [[-h_width, -h_height + i * dif_h, fp_pixel] for i in range(0, self.grid+1)]
        tmp1 = [[-h_width + i * dif_w, h_height, fp_pixel] for i in range(0, self.grid+1)]
        tmp2 = [[h_width, h_height - i * dif_h, fp_pixel] for i in range(0, self.grid+1)]
        tmp3 = [[h_width - i * dif_w, -h_height, fp_pixel] for i in range(0, self.grid+1)]
        tmp = tmp0 + tmp1 + tmp2 + tmp3

        objectPoints = [np.dot(op, R) for op in tmp]        
        imagePoints, jacobian = cv2.omnidir.projectPoints(np.array([objectPoints]), rvec, tvec, self.param.K, self.param.xi[0,0], self.param.D)
        pts = np.array(imagePoints[0], np.int32)
        pts = pts.reshape((-1,1,2))
        dstimg = srcimg.copy()
        dstimg = cv2.polylines(dstimg, [pts], True, (0, 255, 0), 2)
        return dstimg


