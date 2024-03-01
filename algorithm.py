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





# plotUserInput(user_vertices, user_edges)
# # Generate random points

#TODO: Get input from UI
user_vertices, user_edges = getUserInput()
def findConstellation(starsx, starsy, ids, threshhold):

    coordinates = list(zip(starsx, starsy))

    # Combine coordinates with IDs
    coordinates_with_ids = list(zip(starsx, starsy, ids))

    #Effecient Data Structure
    tree = cKDTree(coordinates)

    # Generate combinations of coordinate pairs with IDs
    coordinatePairs = combinations(coordinates_with_ids, 2)

    best_length = float("inf")

    possible_constelations = []
    for coordates in coordinatePairs:
        possible_constelation = []
        possible_constelation_ids = []
        coord_first = np.array([coordates[0][0], coordates[0][1]])
        coord_second = np.array([coordates[1][0], coordates[1][1]])
        possible_constelation.append(coord_first)
        possible_constelation.append(coord_second)
        possible_constelation_ids.append(coordates[0][2])
        possible_constelation_ids.append(coordates[1][2])

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
            nearby_point_indices = tree.query_ball_point(centroid, threshhold)

            
            # Get the nearby points
            nearby_points = np.array([coordinates[i] for i in nearby_point_indices])

            # print(nearby_points)
            # print(centroid)

            # Compute their distances
            distances = np.array([euclideanDistance(point, centroid) for point in nearby_points])

            # Sort the nearby point indices based on distances
            sorted_indices = np.argsort(distances)
            sorted_nearby_point_indices = [nearby_point_indices[i] for i in sorted_indices]

            # Now you have sorted indices corresponding to the nearby points
            # You can access the sorted nearby points using these indices
            sorted_nearby_points = nearby_points[sorted_indices]

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

            if distance > threshhold:
                break  # Point is too far away
            else:
                totalDistance += distance
                if (totalDistance > best_length):
                    break
                possible_constelation.append(nearest_point)
                possible_constelation_ids.append(sorted_nearby_point_indices[0])

            if counter == len(user_vertices) - 1:
                possible_constelations.append(
                    (possible_constelation, totalDistance, possible_constelation_ids))
                best_length = totalDistance


    # print(len(possible_constelations))
    possible_constelations


    sorted_posible_constelations = sorted(
        possible_constelations, key=lambda x: x[1])

    # First value will have minimum total distance
    final_constellation = possible_constelations[0]
    return final_constellation




# num_points = 50
# np.random.seed(1)
# ids = np.arange(num_points)
# starsx = np.random.rand(num_points) * 10
# starsy = np.random.rand(num_points) * 10

# final_constellation_with_ids = findConstellation(starsx, starsy, ids, 1)
# final_constellation = final_constellation_with_ids[0]
# final_constellation_ids = final_constellation_with_ids[1]

# print(final_constellation)
# # print(final_constellation_ids)


# # Split the coordinates into x and y arrays
# x_constellation = [coord[0] for coord in final_constellation]
# y_constellation = [coord[1] for coord in final_constellation]

# # Plot the closest match in a separate window
# plt.figure()
# plt.scatter(starsx, starsy, color='blue',
#             marker='o', label='Random Points', alpha=0.5, s=3)
# for edge in user_edges:
#     plt.plot([x_constellation[edge[0]], x_constellation[edge[1]]],
#              [y_constellation[edge[0]], y_constellation[edge[1]]], 'b-')
# plt.plot([x_constellation[0], x_constellation[1]], [
#          y_constellation[0], y_constellation[1]], color='black',  label='First edge')
# plt.title('Closest Match to User Shape')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(True)
# plt.legend()
# plt.show()
