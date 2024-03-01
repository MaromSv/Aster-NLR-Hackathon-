import numpy as np
# THIWS FILE IS USELESS DO NOT USE!!!!!


def vec_angle(a, b):
    dot = np.dot(a, b)      # Dot product between [x1, y1] and [x2, y2]
    det = a[0]*b[1] - a[1]*b[0]      # Determinant
    angle = np.arctan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return angle


def rot(a, b):
    a_nz = a / np.linalg.norm(a)
    b_nz = b / np.linalg.norm(b)
    angle = vec_angle(a_nz, b_nz)
    print(np.rad2deg(angle))
    cos = np.cos(angle)
    sin = np.sin(angle)
    return np.array([
        [cos, sin],
        [-sin, cos]
    ])


def get_rotation(a, b):
    a_nz = a / np.linalg.norm(a)
    b_nz = b / np.linalg.norm(b)

    angle = np.arccos(np.dot(a_nz, b_nz) /
                      (np.linalg.norm(a) * np.linalg.norm(b)))
    print(np.rad2deg(angle))
    cos = np.cos(angle)
    sin = np.sin(angle)

    # TODO: BROKEN FIX LATER!
    return np.array([
        [cos, -sin],
        [sin, cos]
    ])


a = np.array([0, 1, 0])
b = np.array([1, 2, 0])
print(rot(a, b))
print(get_rotation(a, b))
