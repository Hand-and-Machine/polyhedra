import numpy as np
from .Solid import *
from .tools import *

class ConvexSolid(Solid):

    def __init__(self, name):

        super().__init__(name)

    ## Determine whether the ConvexSolid contains a given point
    def contains(self, p):

        return all([not(f.is_visible(p)) for f in self.faces])

    ## Add a vertex to the hull of this ConvexSolid
    def add_hull_vertex(self, vertex):

        if self.contains(vertex):
            return self

        cs = ConvexSolid(self.name)

        pv = np.asarray(vertex)
        visible_faces = [f for f in self.faces if f.is_visible(vertex)]
        horizon = Solid.boundary(visible_faces)
        horiz_length = len(horizon)

        for i in range(horiz_length):
            id1 = horizon[i]
            id2 = horizon[(i + 1) % horiz_length]
            v1 = self.vertices[id1]
            v2 = self.vertices[id2]
            adj_face = self.faces_with_edge(id1, id2)[1]
            if not adj_face.is_visible(pv, strict=False):
                cs.add_face([v1, v2, vertex])
            else:
                visible_faces.append(adj_face)
                new_vertices = []
                for id in adj_face.vertex_ids:
                    new_vertices.append(adj_face.get_coords(id))
                    if id == id2: new_vertices.append(pv)
                cs.add_face(new_vertices)

        for f in self.faces:
            if f not in visible_faces: cs.add_face(f.all_coords())

        self.overwrite(cs)
        return self

    ## Construct a tetrahedral ConvexSolid with 4 given (noncoplanar) vertices
    def tetrahedron(name, p1, p2, p3, p4):

        cs = ConvexSolid(name)
        
        pv1 = np.asarray(p1)
        pv2 = np.asarray(p2)
        pv3 = np.asarray(p3)
        pv4 = np.asarray(p4)
        cv = (pv1 + pv2 + pv3 + pv4)/4

        sv1 = pv1 - pv2
        sv2 = pv3 - pv2
        test_normal = np.cross(sv2, sv1)
        proj_sign = np.dot(test_normal, p4 - cv)

        if proj_sign > 0:
            cs.add_face([pv1, pv3, pv2])
            cs.add_face([pv2, pv3, pv4])
            cs.add_face([pv1, pv2, pv4])
            cs.add_face([pv1, pv4, pv3])
        else:
            cs.add_face([pv1, pv2, pv3])
            cs.add_face([pv2, pv4, pv3])
            cs.add_face([pv1, pv4, pv2])
            cs.add_face([pv1, pv3, pv4])

        return cs

    ## Construct a ConvexSolid as a convex hull of a given set of points
    def hull(name, pts, error=1e-7):

        pv1 = np.asarray(pts[0])
        pv2 = np.asarray(pts[1])
        pv3 = np.asarray(pts[2])
        cv = (pv1 + pv2 + pv3) / 3
        nv = np.cross(pv2-pv1, pv3-pv2)
        nv = nv / np.linalg.norm(nv)
        proj = 0
        id4 = 3
        pv4 = np.asarray(pts[id4])
        while abs(np.dot(nv, pv4-cv)) < error:
            id4 += 1
            pv4 = np.asarray(pts[id4])
        remaining_pts = [pts[i] for i in range(len(pts)) if i not in [0,1,2,id4]]

        cs = ConvexSolid.tetrahedron(name, pv1, pv2, pv3, pv4)
        for p in remaining_pts:
            cs.add_hull_vertex(p)

        return cs
