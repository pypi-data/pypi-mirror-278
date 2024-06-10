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

        if a_dirs.ndim <= 1:
            if b_dirs.ndim <= 1:
                nbdim = 0
            else:
                nbdim = b_dirs.shape[ 1 ]
        else:
            assert( a_dirs.shape[ 1 ] == b_dirs.shape[ 1 ] )
            nbdim = a_dirs.shape[ 1 ]

        # module import
        sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
        module = __import__( "polycon_bindings_{:02}_{}".format( nbdim, dtype ) )
        self.pc = module.PolyCon( a_dirs, a_offs, b_dirs, b_offs )

    def go( self ):
        return self.pc.go()
    