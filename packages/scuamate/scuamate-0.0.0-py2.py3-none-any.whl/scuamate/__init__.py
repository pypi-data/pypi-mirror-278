#__init__.py

__doc__ = '''
`SCUAMATE`: **S**ome **C**loud **U**tilites to **A**dvance **M**onitoring of **A**nimals and **T**heir **E**cosystems
(or, **S**ome **C**loud **U**tilities for **A**nimals, **MATE**).
A Python package containing utilities to help run, maintain, check, and back
up the cloud infrastructure for next-generation wildlife monitoring projects
(originally develope at CSIRO for SpaceCows and the National Koala Monitoring Program)
'''

from .core import *
from . import az
from . import gc
from . import gsattrack
from .version import __version__
