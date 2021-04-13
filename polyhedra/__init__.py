import os

__title__ = 'polyhedra'
__version__ = '0.4.0'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

from .tools import *
from .Solid import Solid
from .ConvexSolid import ConvexSolid
from .PlatonicSolid import PlatonicSolid
from .ArchimedeanSolid import ArchimedeanSolid
