import numpy as np
from .ConvexSolid import *
from .tools import *
from .location import __location__

class ArchimedeanSolid(ConvexSolid):

    solid_map = {
        1: "unit-truncated-tetrahedron",
        2: "unit-cuboctahedron",
        3: "unit-truncated-cube",
        4: "unit-truncated-octahedron",
        5: "unit-rhombicuboctahedron",
        6: "unit-truncated-cuboctahedron",
        7: "unit-snub-cube",
        8: "unit-icosidodecahedron",
        9: "unit-truncated-dodecahedron",
        10: "unit-truncated-icosahedron",
        11: "unit-rhombicosidodecahedron",
        12: "unit-truncated-icosidodecahedron",
        13: "unit-snub-dodecahedron"
    }

    def __init__(self, name, id, sidelength):
        super().__init__(name)

        solidname = ArchimedeanSolid.solid_map[id]
        file = os.path.join(__location__, "data/archimedean-solids/" + solidname)
        self.overwrite(Solid.load(file, name))
        self.origin_dilate(sidelength)
