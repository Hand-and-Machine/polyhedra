This folder contains Python scripts I've written to generate 3D geometrical forms as STL files by directly writing the contents of the STL files. I'm sure something similar has been done before by someone else, so I may be reinventing the wheel... but hey, I'm learning a lot by doing this!

Here's a list of the code files with descriptions of their functions:
- `tools.py` contains a bunch of functions that are useful for geometrical constructions in 3D.
- `Solid.py` defines the basic classes `Triangle`, `Face` and `Solid` that are used to build solids and generate STL files.
- `ConvexSolid.py` implements a (rather inefficient) convex hull algorithm and some other tools for dealing with convex solids.
- `PlatonicSolid.py` and `ArchimedeanSolid.py` can be used to load pre-constructed Platonic and Archimedean solids.

Here's a table of contents if you want to read about any of the above in greater detail:

- [3D Construction Tools](#3d-construction-tools)
- [The Solid Class](#the-solid-class)
  + [Supplementary Triangle and Face Classes](#supplementary-triangle-and-face-classes)
  + [Adding Vertices, Edges, and Faces](#adding-vertices-edges-and-faces)
  + [Solid Manipulation](#solid-manipulation)
  + [STL File Generation](#stl-file-generation)
- [Special Solids](#special-solids)
  + [Common Solids](#common-solids)
  + [Uniform Solids](#uniform-solids)

## 3D Construction Tools

Here's a list of tools for 3D construction defined in `tools.py`:

- `stringify_vec(vec)` converts a vector (or other list of numbers) into a string in which the numbers are separated by spaces. Used to generate ASCII STL files.
- `distance(p1, p2)` calculates the distance between two points represented as lists of numbers.
- `multireplace(arr, x, sub_arr)` is more of an array-manipulation tool than a geometrical one - it finds all instances of the element `x` in the array `arr` and replaces them with the elements of the array `sub_arr`. For example, `multireplace([1,2,3,2],2,[4,5])` should return `[1,4,5,3,4,5]`.
- `rotate_about_line(point, base_pt, vec, theta)` returns the image of the point `point` rotated `theta` radians about the line defined by the point `base_pt` and the vector `vec`. Direction of rotation is determined by the right-hand rule.

## The Solid Class

### Supplementary Triangle and Face Classes

Two supplementary classes are used to define the `Solid` class: the `Triangle` and `Face` classes.

The `Triangle` class is used only to construct STL files. A `Triangle` is defined by three points, which are passed as arguments to its constructor. The order in which these points are listed is important! In an STL file, triangles are stored as *facets*, which are like flat triangles that are only visible from one side and invisible from the other side. A `Triangle` will be visible on the side from which its points appear in counterclockwise order. Aside from its constructor, the `Triangle` class only has one method: `to_stl()`, which converts it to ASCII text in the STL file format.

The `Face` class is also very simple, and is just used to help organize the `Solid` class. Its most important method is `Solid.vertices`, which stores its vertices. However, it does not store the actual coordinates of each vertex, but rather the *ids* of each vertex, which are integers. In a `Solid` object, vertices are stored in the list `Solid.vertices`, and each vertex is assigned an id equal to its index in this list, so the entries of `Face.vertices` refer to these ids rather than the points themselves. Also, the order in which these points are listed is important: when the `Solid` is converted to STL, each `Face` will only appear from the side on which its vertices appear in counterclockwise order.

### Adding Vertices, Edges, and Faces

Information about the vertices, edges, and faces of each `Solid` are stored redundantly for ease of manipulation:

- `Solid.vertices` is a list of the vertices of the `Solid`, defined by floating point coordinates.
- `Solid.edges` stores information about which pairs of vertices are connected to each other by edges. It is a list of sets, where `Solid.edges[i]` is the set of ids of vertices connected to the vertex with id `i`, or `Solid.vertices[i]`. In other words, `Solid.vertices[i]` and `Solid.vertices[j]` are joined by an edge if and only if `j in Solid.edges[i]`.
- `Solid.faces` is a list of `Face` objects representing the faces of the `Solid`.

Vertices, edges, and faces can be added using the methods `Solid.add_vertex(v)`, `Solid.add_edge(v_id, w_id)`, and `Solid.add_face(pts)` where `v` is a point defined by coordinates, `v_id` and `w_id` are the ids of two points already in the `Solid`, and `pts` is a list of points defined by coordinates. The method `Solid.add_vertex(v)` automatically protects against accidentally storing the same vertex multiple times by checking whether `Solid.vertices` already contains `v` before appending it to the list again. `Solid.add_vertex(v)` also returns the id of `v`, or its index in `Solid.vertices`, whether a duplicate was found or not. `Solid.add_edge` naturally protects against accidental duplication because it consists of sets rather than lists. Also, `Solid.add_face` automatically adds the necessary edges and vertices in addition to constructing a new face for the `Solid`, so there is no need to manually add a polygon's points and edges in addition to calling `Solid.add_face(pts)`.

One potential problem with using floating-point numbers to specify points in coordinate space in Python is that two numerical calculations which, in theory, should yield the same exact point, sometimes give slightly different results due to minute calculation errors. For example, two mathematically identical calculations might produce the results `(0.0, 0.0, 1.0)` and `(0.0, 0.0, 1.0000000003)`. This would cause the duplication fail-safe built into `Solid.add_vertex(v)` to fail, because these two points would register as unequal even though they should be the same. However, this is remedied by checking not only whether `v` is *identical* to any preexisting vertex in `Solid.vertices`, but whether it is *very close* to any of them. If `v` is sufficiently close to another vertex in `Solid.vertices`, it registers as a duplicate. The default threshhold for recognizing a vertex as a duplicate is a distance of `1E-7`, but this threshhold is stored in `Solid.error` and can be overridden.

This failsafe against accidental vertex duplication is helpful, but it has drawbacks - for example, it makes the program buggy when dealing with very small or finely-detailed solids. For this reason, these classes are not appropriate for approximating smoothly curved surfaces.

### Solid Manipulation

The `Solid` class also has a few built-in higher-level functions for manipulating its geometry. (They're designed to work only for convex solids, and might not work properly for concave/stellated solids.) These include:

- `Solid.translate(trans)` rigidly translates the `Solid` (vertexwise) in the direction of the given vector `trans`.
- `Solid.overwrite(solid)` completely overwrites the `Solid` with a copy of the given solid `solid`.
- `Solid.copy()` returns a deep copy of the `Solid` object.
- `Solid.conway_kis(distance)` returns the solid formed by turning each face into a pyramid, which is accomplished  by locating the center of each face and pushing it outward (or inward, for negative values of `distance`) in the direction normal to the face. Corresponds to the Conway "kis" operator.
- `Solid.conway_truncate(proportion)` returns the solid formed by cutting off (truncating) all of the vertices of the `Solid` (the depth of the cut is determined by the argument `proportion`, where a value of, say, `0.5` cuts half of the depth of the maximum cut which would not collide with any other vertices). Corresponds to the Conway "truncate" operator.
- `Solid.conway_expand(distance) returns the solid formed by pushing each face a distance `distance` away from the center, and automatically filling in the empty spaces with polygons.
- `Solid.conway_snub(distance, twist)` is analogous to `Solid.conway_expand`, but in addition to being pushed away from the center, each face is also rotated counterclockwise by `twist` radians.
- `Solid.conway_dual()` attempts to form the dual solid of a given solid by placing a point at the center of each face and connecting the points corresponding to the faces surrounding each vertex into a single face. 
    + For many solids, this results in "faces" with vertices that do not all lie in the same plane. These sorts of solids can be built and converted to STL files unproblematically, but they may not respond predictably when further transformations are applied to them. It is recommended to use `Solid.smooth_faces` to fix these degenerate faces.
- `Solid.smooth_faces(coef, n)` attempts to "smooth out" degenerate faces of a solid ("faces" whose vertices are not actually coplanar) using an iterative method that converges to a topologically equivalent solid with nondegenerate faces. The larger the value of `n`, the greater the number of iterations, and the smoother the solid will be - but not many iterations are usually necessary. 
    + This operation preserves symmetry!

There are a lot more methods I'd like to write to manipulate `Solid` objects with. Here's a tentative to-do list:

- Rotating the polyhedron in 3-space
- Edge-truncation (as opposed to vertex truncation)
- Most/all of the remaining Conway polyhedron operations

### STL File Generation

When you initialize a `Solid` object, you must pass a `name` to its constructor. When you generate an STL file for the `Solid`, `name` will be the name of the file. To generate the file, first call `Solid.build()`, which turns all of the `Face` objects into `Triangle` objects that are stored in `Solid.triangles`, and then call `Solid.gen_file()`, which turns these `Triangle` objects into an STL file and saves it. BEWARE: `Solid.gen_file()` will overwrite previously created STL files with the same name.

## Special Solids

### Uniform Solids

Right now, the only uniform solids implemented in `stl-Uniform.py` are the Platonic solids and the Archimedean solids. The Platonic solids are generated by the constructor `PlatonicSolid(name, id, sidelength)`, where `name` is the desired name, `id` is one of 5 integers corresponding to the Platonic solids, and `sidelength` is the desired side length of the solid (all sides have equal length on a uniform solid). The ids are as follows:

- `1` -> regular tetrahedron
- `2` -> regular octahedron
- `3` -> cube
- `4` -> regular dodecahedron
- `5` -> regular icosahedron

The Archimedean solids can be generated analogously using the constructor `ArchimedeanSolid(name, id, sidelength)`. I've finally finished working out how to build each of these, so they're all supported now!

- `1` -> truncated tetrahedron
- `2` -> cuboctahedron
- `3` -> truncated cube
- `4` -> truncated octahedron
- `5` -> rhombicuboctahedron
- `6` -> truncated cuboctahedron
- `7` -> snub cube
- `8` -> icosidodecahedron
- `9` -> truncated dodecahedron
- `10` -> truncated icosahedron
- `11` -> rhombicosidodecahedron
- `12` -> truncated icosidodecahedron
- `13` -> snub dodecahedron

I hope to add more soon - right prisms, pyramids, maybe eventually the rest of the Johnson Solids.
