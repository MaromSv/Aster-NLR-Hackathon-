import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial import cKDTree
from linalg import *


def getUserInput():
    # Define the adjacency matrix of the user shape

    # Convert the adjacency matrix to edges
    user_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

    # Define the vertices of the user shape
    user_vertices = np.array([(1, 1), (1, 2), (2, 2), (2, 1)])

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

# # Generate random points
num_points = 50
np.random.seed(12)


x_values = np.random.rand(num_points) * 10
y_values = np.random.rand(num_points) * 10

coordinates = list(zip(x_values, y_values))

tree = cKDTree(coordinates)


threshold = 0.5

coordinatePairs = combinations(coordinates, 2)

possible_constelations = []
for coordates in coordinatePairs:
    possible_constelation = []
    coord_first = np.array([coordates[0][0], coordates[0][1]])
    coord_second = np.array([coordates[1][0], coordates[1][1]])
    possible_constelation.append(coord_first)
    possible_constelation.append(coord_second)

    distance = euclideanDistance(coord_first, coord_second)

    input_distances = getLengthsOfInput(user_vertices, user_edges)
    scale = distance / input_distances[0]  # Calculate the scale
    rot_matrix = get_rotation(
        user_vertices[1] - user_vertices[0], coord_second - coord_first, input_distances[0], distance)
    for i, vertex in enumerate(user_vertices[2:]):
        coord_first = coord_second
        counter = i + 2

        # input space
        next_edge = user_vertices[counter] - user_vertices[counter - 1]
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
            for coordinate in possible_constelation:
                if not np.array_equal(point, coordinate):
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
            possible_constelation.append(nearest_point)
            coord_second = np.array(nearest_point)

        if counter == len(user_vertices) - 1:
            possible_constelations.append(possible_constelation)


print(len(possible_constelations))
print(possible_constelations)

# TODO: Find best of the possible constelations

# # Find the closest match among the random points
# best_match_distance = float('inf')
# best_match_points = None

# # Generate all possible combinations of vertices for the candidate shapes
# candidate_vertex_combinations = combinations(zip(x_values, y_values), len(user_vertices))

# # Normalize user shape vertices
# user_normalized = normalize_shape(user_vertices)

# for candidate_vertices in candidate_vertex_combinations:
#     candidate_shape = np.array(list(candidate_vertices))
#     # Normalize candidate shape vertices
#     candidate_normalized = normalize_shape(candidate_shape)
#     # Connect the last vertex back to the first one to close the shape
#     candidate_shape = np.vstack((candidate_shape, candidate_shape[0]))
#     # Calculate Hausdorff distance between normalized shapes
#     distance = hausdorff_distance(user_normalized, candidate_normalized)
#     if distance < best_match_distance:
#         best_match_distance = distance
#         best_match_points = candidate_shape


final_constellation = possible_constelations[0]
print(final_constellation)

rot_matrix = get_rotation(
    user_vertices[1] - user_vertices[0], final_constellation[1] - final_constellation[0], input_distances[0], distance)


# Extract coordinates from the data
constellation_coordinates = []
for item in final_constellation:
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
            marker='o', label='Random Points')
plt.plot(x_constellation, y_constellation, color='green',
         linestyle='-', marker='o', label='Closest Match')
plt.plot([x_constellation[0], x_constellation[1]], [
         y_constellation[0], y_constellation[1]], color='black',  label='First edge')
plt.title('Closest Match to User Shape')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
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
