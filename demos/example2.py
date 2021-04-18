## Solid Example 2
## The convex hull of some points.

import polyhedra as ph

# Some points
pts = [
    (-1,1,2),
    (1,-1,2),
    (1,1,-2),
    (-2,1,1),
    (2,-1,1),
    (2,1,-1),
    (-1,2,1),
    (1,-2,1),
    (1,2,-1)
]

# Create a solid as the convex hull of these points
ch = ph.ConvexSolid.hull("example2", pts)

# Generate the STL file
ch.build().gen_file()
