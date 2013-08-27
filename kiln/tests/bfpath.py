import sys
import os

# Ensure that the bfiles extension directory is on the package search path
# so that modules in its tests directory can be found.
extpath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bfiles'))
try:
    sys.path.index(extpath)
except ValueError:
    sys.path.append(extpath)
