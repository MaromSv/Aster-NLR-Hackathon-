import numpy as np


def euclideanDistance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def euc_norm(point):
    return np.sqrt((point[0])**2 + (point[1])**2)


def get_transform(start_coord, end_coord):
    array = np.array([
        [end_coord[0]/start_coord[0], end_coord[0]/start_coord[1]],
        [end_coord[1]/start_coord[0], end_coord[1]/start_coord[1]]
    ])
    return array * 0.5


def vec_angle(a, b):
    dot = np.dot(a, b)      # Dot product between [x1, y1] and [x2, y2]
    det = a[0]*b[1] - a[1]*b[0]      # Determinant
    angle = np.arctan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return angle


def rot(a, b):
    a_nz = a / np.linalg.norm(a)
    b_nz = b / np.linalg.norm(b)
    angle = -vec_angle(a_nz, b_nz)

    cos = np.cos(angle)
    sin = np.sin(angle)
    return np.array([
        [cos, -sin],
        [sin, cos]
    ])


def get_rotation(a, b, a_norm, b_norm):
    a_nz = a / a_norm
    b_nz = b / b_norm

    angle = np.arccos(np.dot(a, b) / (a_norm * b_norm))
    cos = np.cos(angle)
    sin = np.sin(angle)

    # TODO: BROKEN FIX LATER!
    return np.array([
        [cos, -sin],
        [sin, cos]
    ])
