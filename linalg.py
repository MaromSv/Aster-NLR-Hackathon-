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


def get_rotation(a, b, a_norm, b_norm):
    cos = np.dot(a, b) / (a_norm * b_norm)
    sin = np.sqrt(1 - cos*cos)

    # can be improved
    return np.array([
        [cos, -sin],
        [sin, cos]
    ])
