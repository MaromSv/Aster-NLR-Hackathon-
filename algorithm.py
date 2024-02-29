import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial import cKDTree
from linalg import *


def getUserInput():
    # Define the adjacency matrix of the user shape

    # Convert the adjacency matrix to edges
    user_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]

    # Define the vertices of the user shape
    user_vertices = np.array(
        [(1, 1), (3, 3), (5, 1), (4, 1), (4, -2), (2, -2), (2, 1)])

    # user_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
    #               (5, 6), (6, 7), (7, 8), (8, 9), (9, 0)]

    # user_vertices = np.array([(31, -95),
    #                           (-31, -95),
    #                           (-81, -59),
    #                           (-100, 0),
    #                           (-81, 59),
    #                           (-31, 95),
    #                           (31, 95),
    #                           (81, 59),
    #                           (100, 0),
    #                           (81, -59)])

    return user_vertices, user_edges


def euclideanDistance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def getLengthsOfInput(user_vertices, user_edges):
    lengths_of_input = []
    for edge in user_edges:
        lengths_of_input.append(euclideanDistance(
            user_vertices[edge[0]], user_vertices[edge[1]]))
    return lengths_of_input


def plotUserInput(user_vertices, user_edges):

    # Plotting
    plt.figure()
    # Plotting vertices
    plt.plot(user_vertices[:, 0], user_vertices[:, 1], 'bo')
    # Plotting edges
    for edge in user_edges:
        plt.plot(user_vertices[edge, 0], user_vertices[edge, 1], 'b-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('User Shape')
    plt.grid(True)
    plt.axis('equal')
    plt.show()


user_vertices, user_edges = getUserInput()
# plotUserInput(user_vertices, user_edges)
# # Generate random points
num_points = 500
np.random.seed(5)


x_values = np.random.rand(num_points) * 10
y_values = np.random.rand(num_points) * 10

coordinates = list(zip(x_values, y_values))

tree = cKDTree(coordinates)


threshold = 0.5

coordinatePairs = combinations(coordinates, 2)

best_length = float("inf")

possible_constelations = []
for coordates in coordinatePairs:
    possible_constelation = []
    coord_first = np.array([coordates[0][0], coordates[0][1]])
    coord_second = np.array([coordates[1][0], coordates[1][1]])
    possible_constelation.append(coord_first)
    possible_constelation.append(coord_second)

    distance = euclideanDistance(coord_first, coord_second)
    pair_vector = coord_second - coord_first

    input_distances = getLengthsOfInput(user_vertices, user_edges)
    scale = distance / input_distances[0]  # Calculate the scale
    rot_matrix = rot(
        user_vertices[1] - user_vertices[0], pair_vector)

    totalDistance = 0
    for i, vertex in enumerate(user_vertices[2:]):
        counter = i + 2

        # input space
        next_edge = user_vertices[counter] - user_vertices[1]
        const_edge = next_edge@rot_matrix * scale
        centroid = coord_second + const_edge

        # Query the kd-tree for the nearest neighbor to the target point
        nearby_point_indices = tree.query_ball_point(centroid, threshold)

        # Get the nearby points
        nearby_points = [np.array(coordinates[i])
                         for i in nearby_point_indices]

        # Compute their distances
        distances = [euclideanDistance(point, centroid)
                     for point in nearby_points]

        # Sort the list
        sorted_indices = np.argsort(distances)
        sorted_nearby_points = [nearby_points[i] for i in sorted_indices]

        new_sorted_nearby_points = []
        for index, point in enumerate(sorted_nearby_points):
            overlap = False
            for coordinate in possible_constelation:
                if euclideanDistance(point, coordinate) < 0.001:
                    overlap = True
            if not overlap:
                new_sorted_nearby_points.append(point)

        # print("constellation", possible_constelation)
        # print("nearby point", new_sorted_nearby_points)
        if len(new_sorted_nearby_points) == 0:
            break

        nearest_point = new_sorted_nearby_points[0]
        distance = euclideanDistance(nearest_point, centroid)

        if distance > threshold:
            break  # Point is too far away
        else:
            totalDistance += distance
            if (totalDistance > best_length):
                break
            possible_constelation.append(nearest_point)

        if counter == len(user_vertices) - 1:
            possible_constelations.append(
                (possible_constelation, totalDistance))
            best_length = totalDistance


print(len(possible_constelations))
possible_constelations


sorted_posible_constelations = sorted(
    possible_constelations, key=lambda x: x[1])

# First value will have minimum total distance
final_constellation = possible_constelations[0]
print(final_constellation)

# Extract coordinates from the data
constellation_coordinates = []
for item in final_constellation[0]:
    if isinstance(item, tuple):
        constellation_coordinates.append(item)
    else:
        constellation_coordinates.append(item.tolist())

# Split the coordinates into x and y arrays
x_constellation = [coord[0] for coord in constellation_coordinates]
y_constellation = [coord[1] for coord in constellation_coordinates]

# Plot the closest match in a separate window
plt.figure()
plt.scatter(x_values, y_values, color='blue',
            marker='o', label='Random Points', alpha=0.5, s=3)
for edge in user_edges:
    plt.plot([x_constellation[edge[0]], x_constellation[edge[1]]],
             [y_constellation[edge[0]], y_constellation[edge[1]]], 'b-')
plt.plot([x_constellation[0], x_constellation[1]], [
         y_constellation[0], y_constellation[1]], color='black',  label='First edge')
plt.title('Closest Match to User Shape')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend()
plt.show()


# # Function to compute the Hausdorff distance between two shapes
# def hausdorff_distance(shape1, shape2):
#     return max(np.min(np.linalg.norm(shape1 - point, axis=1)) for point in shape2)

# # Normalize shape vertices
# def normalize_shape(shape):
#     centroid = np.mean(shape, axis=0)
#     max_distance = np.max(np.linalg.norm(shape - centroid, axis=1))
#     return (shape - centroid) / max_distance
