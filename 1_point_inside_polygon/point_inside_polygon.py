# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 19:12:41 2023

@author: d-roizman
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import time as time

# 1 - Function to identify if a point in a 2-d plane is inside (or outside) a given simple closed curve

def point_in_polygon(point, vertices):
    x, y = point
    num_vertices = len(vertices)
    cont = 0

    y_max = max(vert[1] for vert in vertices)
    y_min = min(vert[1] for vert in vertices)
    x_max = max(vert[0] for vert in vertices)
    x_min = min(vert[0] for vert in vertices)
    
    if point in vertices: # points over vertices are outside
        cont = 0
                
    elif x_min <= x <= x_max and y_min <= y <= y_max:
    
        for i in range(num_vertices):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % num_vertices]
            
            # points over edges are outside
            if y == y1 == y2 :
                if min(x1, x2) <= x <= max(x1, x2):
                    return False # horizontal edge
     
            elif x == x1 == x2 :
                if min(y1, y2) <= y <= max(y1, y2):
                    return False # verical edge
            
            elif y > min(y1, y2):
                if y <= max(y1, y2):
                    if x <= max(x1, x2):
                        if y1 != y2:
                            x_intersec = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        if x1 == x2 or x < x_intersec:
                            cont += 1
                            
            if min(y1, y2) < y < max(y1, y2) and min(x1, x2) < x < max (x1, x2):
                angulo_aresta = (y2-y1)/(x2-x1)
                angulo_pto = (y2-y)/(x2-x)
                if angulo_aresta == angulo_pto:
                    return False # edge
 
    return cont % 2 == 1

# function to define the collor of the point
def collor_point(point, polygon):
    if point_in_polygon(point, polygon) == True:
        return 'go'
    else:
        return 'ro'


# 2 - Test

complicated_polygon = [
    (0, 0), (1, 2), (2, 0), (3, 3), (4, 0), 
    (4,3.5), (2.5,4), (2.5,4.5), (3.5,4.5), (3.5,4),
    (4, 4), (3, 6), (2, 4), (1, 6), (1.5, 4)
    ]

points = [
    (0.5, 2), (2, 2), (5, 5), (3, 5), (1.5, 1),
    (3, 6), (3, 4.5), (4, 2), (3, 1)
    ]

# Plotting
fig, ax = plt.subplots()
polygon_patch = Polygon(complicated_polygon, closed=True, fill=None, edgecolor='blue')
ax.add_patch(polygon_patch)
    
for point in points:
    ax.plot(*point, collor_point(point, complicated_polygon))

ax.set_xlim(-1, 8)
ax.set_ylim(-1, 8)
plt.show()

start = time.time()
for p in points:
    print(point_in_polygon(p, complicated_polygon))
end = time.time()
comput_time = end - start
print(f'total time was {comput_time:.6f} seconds')

# 3 - Another test

italy = 'Italy.txt'
italy_map = []
with open(italy, 'r') as file:
    for line in file:
        x_str, y_str = line.strip().split(',')
        x = float(x_str) / 100000
        y = -float(y_str) / 100000
        italy_map.append((round(x, 4), round(y, 4)))


fig, ax = plt.subplots()
polygon_patch = Polygon(italy_map, closed=True, fill=None, edgecolor='blue')
ax.add_patch(polygon_patch)

# plot points
points = [
    (5, -2), (6, -6), (5, -5), (3, -5), (1.5, -1),
    (3, -6), (3, -4.5), (4, -2), (3, -10)
    ]

[ax.plot(*point, collor_point(point, italy_map)) for point in points ]
ax.set_xlim(-1, 12)
ax.set_ylim(-12, 1)
plt.show()


