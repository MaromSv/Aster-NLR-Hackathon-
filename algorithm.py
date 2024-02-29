import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial import cKDTree
from linalg import *


def getUserInput():
    # Define the adjacency matrix of the user shape
    user_adjacency = np.array([[0, 1, 0, 1],
                               [1, 0, 1, 0],
                               [0, 1, 0, 1],
                               [1, 0, 1, 0]])

    # Convert the adjacency matrix to edges
    user_edges = []
    for i in range(len(user_adjacency)):
        for j in range(i + 1, len(user_adjacency)):
            if user_adjacency[i][j] == 1:
                user_edges.append((i, j))

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
np.random.seed(5)


x_values = np.random.rand(num_points) * 10
y_values = np.random.rand(num_points) * 10

coordinates = list(zip(x_values, y_values))

tree = cKDTree(coordinates)


# Define the target point and distance threshold
target_point = (2, 5)
threshold = 1  # Adjust as needed

# Query the R-tree for points within the threshold distance of the target point
nearby_point_indices = tree.query_ball_point(target_point, threshold)

# Get the nearby points
nearby_points = [coordinates[i] for i in nearby_point_indices]

print(nearby_points)


coordinatePairs = combinations(coordinates, 2)

for coordates in coordinatePairs:
    coord_first = np.array([coordates[0][0], coordates[0][1]])
    coord_second = np.array([coordates[1][0], coordates[1][1]])
    distance = euclideanDistance(coord_first, coord_second)
    input_distances = getLengthsOfInput(user_vertices, user_edges)
    scale = distance / input_distances[0]  # Calculate the scale
    rot_matrix = get_rotation(
        user_vertices[1] - user_vertices[0], coord_second - coord_first, input_distances[0], distance)

    # input space
    next_edge = user_vertices[2] - user_vertices[1]
    const_edge = next_edge@rot_matrix * scale
    centroid = coord_second + const_edge

    print(user_vertices[0])
    print(user_vertices[1])
    print(user_vertices[2])

    print(coord_first)
    print(coord_second)
    print(centroid)
    break


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

# # Plot the closest match in a separate window
# plt.figure()
# plt.scatter(x_values, y_values, color='blue', marker='o', label='Random Points')
# plt.plot(best_match_points[:, 0], best_match_points[:, 1], color='green', linestyle='-', marker='o', label='Closest Match')
# plt.title('Closest Match to User Shape')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.grid(True)
# plt.legend()
# plt.show()


# # Function to compute the Hausdorff distance between two shapes
# def hausdorff_distance(shape1, shape2):
#     return max(np.min(np.linalg.norm(shape1 - point, axis=1)) for point in shape2)

# # Normalize shape vertices
# def normalize_shape(shape):
#     centroid = np.mean(shape, axis=0)
#     max_distance = np.max(np.linalg.norm(shape - centroid, axis=1))
#     return (shape - centroid) / max_distance
