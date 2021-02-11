import numpy as np
import math
import omnidir_param
#import ply

def unit_sphere_point(pi, K, D, Xi):

    #カメラマトリックス
    f = [K[0,0], K[1,1]]
    c = [K[0,2], K[1,2]]
    s = K[0,1]

    #ディストーション
    k = [D[0,0], D[0,1]]
    p = [D[0,2], D[0,3]]

    pp = [ (pi[0]*f[1]-c[0]*f[1]-s*(pi[1]-c[1]))/(f[0]*f[1]), (pi[1]-c[1])/f[1]]
    pu = pp.copy()

    for i in range(0,20):
        r2 = pu[0]*pu[0] + pu[1]*pu[1]
        r4 = r2*r2
        pu[0] = (pp[0] - 2*p[0]*pu[0]*pu[1] - p[1]*(r2+2*pu[0]*pu[0])) / (1 + k[0]*r2 + k[1]*r4)
        pu[1] = (pp[1] - 2*p[1]*pu[0]*pu[1] - p[0]*(r2+2*pu[1]*pu[1])) / (1 + k[0]*r2 + k[1]*r4) 

    r2 = pu[0]*pu[0] + pu[1]*pu[1]
    a = (r2 + 1)
    b = 2 * Xi*r2
    cc = r2*Xi*Xi-1
    Zs = (-b + math.sqrt(b*b - 4*a*cc))/(2*a)
    Xw = [pu[0]*(Zs + Xi), pu[1]*(Zs + Xi), Zs]

    return Xw

def unit_sphere(distorted, K, D, Xi):
    sphere_xyz = [unit_sphere_point(pi, K, D, Xi) for pi in distorted]
    return sphere_xyz
