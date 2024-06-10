from .type_promote import type_promote
import numpy
import sys
import os

class PolyCon:
    def __init__( self, a_dirs, a_offs, b_dirs, b_offs ):
        # arg types
        a_dirs = numpy.asarray( a_dirs )
        a_offs = numpy.asarray( a_offs )
        b_dirs = numpy.asarray( b_dirs )
        b_offs = numpy.asarray( b_offs )

        # compile time parameters
        dtype = type_promote( a_dirs.dtype, a_offs.dtype, b_dirs.dtype, b_offs.dtype, ensure_scalar = True )

        if a_dirs.ndim > 1:
            if b_dirs.ndim > 1:
                assert( a_dirs.shape[ 1 ] == b_dirs.shape[ 1 ] )
            nbdim = a_dirs.shape[ 1 ]
        else:
            if b_dirs.ndim > 1:
                nbdim = b_dirs.shape[ 1 ]
            else:
                nbdim = 0

        # module import
        sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
        module = __import__( "polycon_bindings_{:02}_{}".format( nbdim, dtype ) )
        classv = getattr( module, "PolyCon_{:02}_{}".format( nbdim, dtype ) )
        self.pc = classv( a_dirs, a_offs, b_dirs, b_offs )

    def write_vtk( self, filename ):
         self.pc.write_vtk( filename )
    