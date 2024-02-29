import numpy as np
import math as math

vertices1 = [[0,1], [1,1], [1, 0], [1, 2], [2, 1]]
edges1 = [[0,1], [1, 2], [1, 3], [1, 4]]
shape1 = [vertices1,edges1]
vertices2 = [[0,1], [1,1], [1,0], [1, 2], [3, 1]]
edges2 = [[0,1], [1,2], [1, 3], [1, 4]]
shape2 = [vertices2,edges2]
shapes = [shape1,shape2]
input = [shape1]
vertecesinput = shape1[0]
edgesinput = shape1[1]
lengthsinput = []
anglesinput = []
vectorsinput = []
magnitudesinput = []
ratiosinput = []

i = 0
while i < len(edgesinput):
    vertex1input = vertecesinput[edgesinput[i][0]]
    vertex2input = vertecesinput[edgesinput[i][1]]
    lengthsinput.append(math.sqrt((vertex1input[0] - vertex2input[0])**2 + (vertex1input[1] - vertex2input[1])**2))
    vectorsinput.append([vertex1input[0] - vertex2input[0], vertex1input[1] - vertex2input[1]])
    magnitudesinput.append(math.sqrt(vectorsinput[i][0]**2 + vectorsinput[i][1]**2))
    i = i + 1
i = 1
while i < len(lengthsinput):
    ratiosinput.append(lengthsinput[i]/lengthsinput[0])
    i = i + 1

scores = []

i = 0
while i < len(shapes):
    verteces = shapes[i][0]
    edges = shapes[i][1]
    lengths = []
    angles = []
    ratios = []

    j = 0
    while j < len(edges):
        vertex1 = verteces[edges[j][0]]
        vertex2 = verteces[edges[j][1]]
        lengths.append(math.sqrt((vertex1[0] - vertex2[0])**2 + (vertex1[1] - vertex2[1])**2))
        vector = [vertex1[0] - vertex2[0], vertex1[1] - vertex2[1]]
        dotproduct = vector[0] * vectorsinput[j][0] + vector[1] * vectorsinput[j][1]
        magnitudevector = math.sqrt(vector[0]**2 + vector[1]**2)
        angles.append(np.arccos(dotproduct / (magnitudevector * magnitudesinput[j])))
        j = j + 1
    j = 1
    while j < len(lengths):
        ratios.append(lengths[j]/lengths[0])
        j = j + 1
    score = 0
    j = 0
    while j < len(angles):
        score = score + (angles[j] * (180/math.pi))**2
        j = j + 1
    j = 0
    while j < len(ratios):
        score = score + (((ratios[j] - ratiosinput[j])/ratiosinput[j])*50)**2
        j = j + 1
    scores.append(score)
    i = i + 1

winningscore = [scores[-1]]
indexwinner = 0
i = 0
while i < len(scores):
    if scores[i] < winningscore:
        winningscore = scores[i]
        indexwinner = i
    i = i + 1
winner = shapes[indexwinner]
print('winner:') 
print(winner)
print(scores)