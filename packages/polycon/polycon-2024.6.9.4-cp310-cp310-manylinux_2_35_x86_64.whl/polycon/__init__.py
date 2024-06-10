# compile .cpp files if necessary
try:
    import cppimport.import_hook
except:
    pass

# exports
from .lib.PolyCon import PolyCon
