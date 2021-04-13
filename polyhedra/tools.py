import numpy as np

def stringify_vec(vec):
    s = ""
    for x in vec: s += str(x) + " "
    return s

def distance(p1, p2):
    pv1 = np.asarray(p1)
    pv2 = np.asarray(p2)
    return np.linalg.norm(pv1 - pv2)

def multireplace(arr, x, sub_arr):
    new_arr = []
    for entry in arr:
        if (entry == x).all():
            new_arr += sub_arr
        else:
            new_arr += [entry]
    return new_arr

def rotate_about_line(point, base_pt, vec, theta):
    pv = np.asarray(point)
    bpv = np.asarray(base_pt)
    lv = np.asarray(vec)
    diffv = pv - bpv
    diffproj = lv * np.dot(diffv, lv) / np.linalg.norm(lv)**2
    projv = bpv + diffproj
    rv1 = pv - projv
    rv2 = np.cross(lv, rv1)
    rv2 = rv2 * np.linalg.norm(rv1) / np.linalg.norm(rv2)
    new_pv = projv + rv1 * np.cos(theta) + rv2 * np.sin(theta)
    return new_pv
