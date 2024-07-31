# Ray Cast Algorithm

This repository contains a Python function `point_in_polygon` that determines, using the Ray-Cast Algorithm if a given point lies inside a polygon on a 2D plane. 
Basically, the function "counts" how many times a horizontal ray that passes throught a point crosses the polygon. Its correctness may be proved using the Jordan Curve Theorem. 
It essentially states that a closed curve divides a plane into an "inside" and "outside."
It takes, as input, a point and the vertices of the polygon as inputs and returns a boolean indicating whether the point is inside the polygon.

## Algorithm Explanation

The `point_in_polygon` function uses the ray-casting method to determine the point's position relative to the polygon. Here's a detailed explanation of the algorithm:

1. **Inputs**:
   - `point`: A tuple `(x, y)` representing the coordinates of the point.
   - `vertices`: A list of tuples `[(x1, y1), (x2, y2), ..., (xn, yn)]` representing the vertices of the polygon.

2. **Initialization**:
   - Extract the x and y coordinates of the point.
   - Calculate the number of vertices in the polygon.
   - Initialize a counter `cont` to keep track of intersections.
   - Determine the minimum and maximum x and y values of the polygon's vertices.

3. **Edge Cases**:
   - If the point is one of the vertices, it is considered outside the polygon.
   - If the point lies within the bounding box defined by the minimum and maximum x and y values of the vertices, proceed to the main algorithm.

4. **Ray-Casting**:
   - For each edge of the polygon, determine if a horizontal ray starting from the point intersects the edge.
   - If the point lies on an edge, it is considered outside the polygon.
   - Calculate the intersection of the ray with the edge and count the number of intersections.

5. **Result**:
   - If the number of intersections is odd, the point is inside the polygon.
   - If the number of intersections is even, the point is outside the polygon.

## Reference

This implementation is inspired by the algorithm discussed in [PNPOLY - Point Inclusion in Polygon Test](https://wrfranklin.org/Research/Short_Notes/pnpoly.html);

Good Explanation of the [Jordan Curve Theorem](https://en.wikipedia.org/wiki/Jordan_curve_theorem).
