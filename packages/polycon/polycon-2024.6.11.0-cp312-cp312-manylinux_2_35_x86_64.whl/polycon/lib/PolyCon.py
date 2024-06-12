from .type_promote import type_promote
import numpy
import sys
import os

class PolyCon:
    def __init__( self, a_dirs, a_offs = None, b_dirs = None, b_offs = None ):
        """ a => affine functions, b => boundarys """

        if 'polycon_bindings_' in repr( type( a_dirs ) ):
            self.pc = a_dirs
            return

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

    @staticmethod
    def from_function_samples( function, points, eps = 1e-6, b_dirs = [], b_offs = [] ):
        a_dirs = []
        a_offs = []
        for p in points:
            p = numpy.asarray( p )
            v = function( p )
            g = []
            for d in range( p.size ):
                o = p.copy()
                o[ d ] += eps
                w = function( o )
                g.append( ( w - v ) / eps )
            
            a_offs.append( numpy.dot( g, p ) - v )
            a_dirs.append( g )

        return PolyCon( a_dirs, a_offs, b_dirs, b_offs )


    def ndim( self ):
        return self.pc.ndim()

    def value_and_gradient( self, x_or_xs ):
        """ return nan if not in a cell """
        # TODO: optimize
        p = numpy.asarray( x_or_xs )
        if p.ndim == 2:
            values = []
            grads = []
            for x in p:
                r = self.value_and_gradient( x )
                values.append( r[ 0 ] )
                grads.append( r[ 1 ] )
            return values, grads
        
        return self.pc.value_and_gradient( p )

    def value( self, x_or_xs ):
        return self.value_and_gradient( x_or_xs )[ 0 ]

    def legendre_transform( self ):
        return PolyCon( self.pc.legendre_transform() )

    def __add__( self, that ):
        if isinstance( that, PolyCon ):
            return PolyCon( self.pc.add_polycon( that.pc ) )
        return PolyCon( self.pc.add_scalar( that ) )

    def __radd__( self, that ):
        return self.__add__( that )

    def __sub__( self, that ):
        return PolyCon( self.pc.add_scalar( - that ) )

    def __mul__( self, that ):
        assert( that >= 0 )
        return PolyCon( self.pc.mul_scalar( that ) )

    def __rmul__( self, that ):
        return self.__mul__( that )

    def __repr__( self, floatfmt="+.5f" ):
        def as_tab( v ):
            import tabulate
            return "  " + tabulate.tabulate( v, tablefmt= "plain", floatfmt = floatfmt ).replace( '\n', '\n  ' )

        f, b = self.as_fb_arrays()
        res  = "Affine functions:\n"
        res += as_tab( f )
        res += "\nBoundaries:\n"
        res += as_tab( b )
        return res

    def normalized( self ):
        """ return the same PolyCon, with 
            * normalized boundaries,
            * sorted rows for boundaries and affine functions
        """
        return PolyCon( self.pc.normalized() )

    def as_fbdo_arrays( self ):
        """ return two arrays, one for the affine function, one for the boundary ones
            For instance with `f, b = pc.as_fb_array()`
               `f[ :, 0:nb_dims ]` => affine function directions (gradients)
               `f[ :, nb_dims ]` => affine function offsets
               `b[ :, 0:nb_dims ]` => boundary directions
               `b[ :, nb_dims ]` => boundary offsets
        """
        return self.pc.as_fbdo_arrays()

    def as_fb_arrays( self ):
        """ return four arrays for the affine function and the boundary ones, with directions and offset
            For instance with `f_dir, f_off, b_dir, b_off = pc.as_fb_array()`
               `f_dir` => affine function directions (gradients)
               `f_off` => affine function offsets
               `b_dir` => boundary directions
               `b_off` => boundary offsets
        """
        return self.pc.as_fb_arrays()

    def write_vtk( self, filename ):
        """ write a vtk file """
        self.pc.write_vtk( filename )
    
    def edge_points( self ):
        """ return an array with the coordinates + type of the vertice
            array[ num_edge, num_vertex, 0 : ndim ] => vertex coords
            array[ num_edge, num_vertex, ndim + 0 ] => vertex height
            array[ num_edge, num_vertex, ndim + 1 ] => nb interior cuts
            array[ num_edge, num_vertex, ndim + 2 ] => nb boundary cuts
            array[ num_edge, num_vertex, ndim + 3 ] => nb infinity cuts
        """
        return self.pc.edge_points()
    
    def plot( self, color = 'b', show = True ):
        """ use matplotlib """
        from matplotlib import pyplot 

        if self.ndim() != 1:
            raise NotImplemented

        edges = self.pc.edge_points().tolist()
        for e in edges:
            e.sort()
        edges.sort()

        def app( xs, ys, edge, c ):
            xs.append( ( 1 - c ) * edge[ 0 ][ 0 ] + c * edge[ 1 ][ 0 ] )
            ys.append( ( 1 - c ) * edge[ 0 ][ 1 ] + c * edge[ 1 ][ 1 ] )

        def is_inf( vertex ):
            return vertex[ 4 ] != 0
        
        # regular lines
        xs = []
        ys = []
        app( xs, ys, edges[ 0 ], is_inf( edges[ 0 ][ 0 ] ) / 3 )
        for e in edges:
            app( xs, ys, e, 1 - is_inf( e[ 1 ] ) / 3 )

        pyplot.plot( xs, ys, color = color )

        # dotted lines
        for e in edges:
            xd = []
            yd = []
            if is_inf( e[ 0 ] ):
                app( xd, yd, e, 0.0 )
                app( xd, yd, e, 1/3 )

            if is_inf( e[ 1 ] ):
                app( xd, yd, e, 2/3 )
                app( xd, yd, e, 1.0 )

            pyplot.plot( xd, yd, linestyle = "dotted", color = color )

        if show:
            pyplot.show()
