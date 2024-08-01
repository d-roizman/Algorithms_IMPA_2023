# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:56:40 2023

@author: daniel roizman
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection


# 1 - copy 'point_in_polygon' and 'collor_point' algorithms (from class 1)
def point_in_polygon(point, vertices):
    x, y = point
    N = len(vertices)
    cont = 0

    y_max = max(vert[1] for vert in vertices)
    y_min = min(vert[1] for vert in vertices)
    x_max = max(vert[0] for vert in vertices)
    x_min = min(vert[0] for vert in vertices)
    
    if point in vertices: # points over vertices are outside
        cont = 0
                
    elif x_min <= x <= x_max and y_min <= y <= y_max:
    
        for i in range(N):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % N]
            
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


# 2 - copy the function to define the collor of the point
def collor_point(point, polygon):
    if point_in_polygon(point, polygon) == True:
        return 'go'
    else:
        return 'ro'

def plot_polygon(vertices): # vertices = tank_map
    if len(vertices) < 3:
        return "A polygon needs at least 3 vertices"
    


    fig, ax = plt.subplots()
    polygon = Polygon(vertices, closed=True, edgecolor='b', facecolor='none')
    ax.add_patch(polygon)

    plt.show()


# 3 - function that finds "best diagonal" to cut the polygon in two
def polygon_division(polygon):
    
    if len(polygon) < 4:
        return polygon
    else:
        N = len(polygon)

    # find first, second and third leftmost vertices
    leftmost_vertex = min(polygon, key = lambda t: (t[0], t[1]))
    ind = polygon.index(leftmost_vertex)
    vertex_before = polygon[(ind - 1) % N]
    vertex_after = polygon[(ind + 1) % N]

    # write the triangle that is formed by those 3 vertices
    triangle = [vertex_before, leftmost_vertex, vertex_after]
    x_ant, y_ant = vertex_before
    x, y = leftmost_vertex
    x_dep, y_dep = vertex_after

    # list polygons' points that lie inside that triangle, if any
    points_inside_triangle = []
    for point in polygon:
        if point not in triangle and point_in_polygon(point, triangle) == True:
            points_inside_triangle.append(point)

    # calculate area of triangles formed by 'vertex_before', 'vertex_after' and points in 'points_inside_triangle'
    if len(points_inside_triangle) > 0:
        max_area = 0
        for point in points_inside_triangle:
            area = 0.5 * abs(x_ant*(y - y_dep) + x*(y_dep - y_ant) + x_dep*(y - y_ant))
            if area > max_area:
                max_area = area
                max_point = point
        
        # we found our separating-diagonal!
        diagonal = [leftmost_vertex, max_point]
        index_pto_max = polygon.index(max_point)

        # now, identify the first polygon (created by our separating-diagonal), 'rotating' clockwise
        polygon_1 = [leftmost_vertex]
        next_point = max_point
        i = 0
        while next_point != leftmost_vertex:
            polygon_1.append(next_point)
            i += 1
            next_point = polygon[(index_pto_max - i) % N]
            
        # same thing for our second polygon, but now rotating counter-clockwise
        polygon_2 = [leftmost_vertex]
        next_point = max_point
        i = 0
        while next_point != leftmost_vertex:
            polygon_2.append(next_point)
            i += 1
            next_point = polygon[(index_pto_max + i) % N]
        
    else: # in this case, the diagonal just separates the triangle we found
        diagonal = [vertex_before, vertex_after]
        polygon_1 = [vertex_before, leftmost_vertex, vertex_after]
        polygon_2 = polygon
        polygon_2.remove(leftmost_vertex)
    
    return [polygon_1, polygon_2, diagonal]

# 4 - recursive function to triangulate our polygon (using previous 'polygon_division' function)

def triangulation (polygon): # retorna todas as diagonais e os triangulos formados

    if len(polygon) <= 3:
        return polygon

    diagonals = []
    triangles = []
    
    def recursion (polygon):
            
        pol_1, pol_2, diag = polygon_division (polygon)
        diagonals.append(diag)

        if len(pol_1) > 3 and len(pol_2) > 3:            
            return recursion(pol_1), recursion(pol_2)
        elif len(pol_1) > 3 and len(pol_2) == 3:
            triangles.append(pol_2)
            return recursion(pol_1)
        elif len(pol_2) > 3 and len(pol_1) == 3:
            triangles.append(pol_1)
            return recursion(pol_2)
        elif len(pol_2) == 3 and len(pol_1) == 3:
            triangles.append(pol_1)
            triangles.append(pol_2)
        else:
            pass
    
    recursion (polygon)
    
    unique_tuples = set()
    copy_triangles = triangulos
    new_triangles = []

    for sublist in copy_triangles:
        sublist_tuple = tuple(sublist)
        if sublist_tuple not in unique_tuples:
            new_triangles.append(sublist)
            unique_tuples.add(sublist_tuple)
    
    return diagonals, new_triangles

# 5 - Test
complicated_polygon = [
    (0, 0), (1, 3), (2, 0), (3, 3), (4, 0), 
    (4, 3.5), (2.5, 4), (2.5, 4.5), (3.5, 4.5), (3.5, 4),
    (4, 4), (3, 6), (2, 4), (1, 6), (1.2, 4), (0.2, 1.2), (0, 2)
    ]

# teste da funcao recursiva
diagonals, triangles = triangulation (complicated_polygon)

# definindo lista de linhas
diags = LineCollection(diagonals, linestyle='dashed', color='blue')
polygon_x = [point[0] for point in complicated_polygon]
polygon_y = [point[1] for point in complicated_polygon]

# Create a plot
fig, ax = plt.subplots(dpi=600)
ax.fill(polygon_x, polygon_y, facecolor='none', edgecolor='black')

# Add the line segments to the plot
ax.add_collection(diags)

# Set plot limits
ax.set_xlim(min(polygon_x) - 1, max(polygon_x) + 1)
ax.set_ylim(min(polygon_y) - 1, max(polygon_y) + 1)

plt.show()

# 6 - Another test

tank = 'tank.txt'
tank_map = []
with open(tank, 'r') as file:
    for line in file:
        x_str, y_str = line.strip().split(' ')
        x = float(x_str)
        y = -float(y_str)
        tank_map.append((round(x, 4), round(y, 4)))

fig, ax = plt.subplots(dpi=600)
polygon_patch = Polygon(tank_map, closed=True, fill=None, edgecolor='black')

diags = LineCollection(triangulation(tank_map.copy())[0], linestyle = 'dashed', color = 'blue')
ax.add_collection(diags)
ax.add_patch(polygon_patch)

ax.set_xlim(-50, 700)
ax.set_ylim(-420,-200)
plt.show()




