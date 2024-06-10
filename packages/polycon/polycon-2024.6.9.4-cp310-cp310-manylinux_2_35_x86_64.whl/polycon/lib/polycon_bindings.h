#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <polycon/PolyCon.h>

#ifndef POLYCON_SCALAR
#define POLYCON_SCALAR FP64
#endif

#ifndef POLYCON_DIM
#define POLYCON_DIM 02
#endif

#define CONCAT_5( A, B, C, D, E ) A ## B ## C ## D ## E
#define CC_DT_( NAME, D, T ) CONCAT_5( NAME, _, D, _, T )
#define CC_DT( NAME ) CC_DT_( NAME, POLYCON_DIM, POLYCON_SCALAR )

namespace py = pybind11;
using Array = py::array_t<POLYCON_SCALAR, py::array::c_style>;
using Point = PolyCon<POLYCON_SCALAR,POLYCON_DIM>::Point;

#define PolyCon_Py CC_DT( PolyCon_py )

struct PolyCon_py {
    PolyCon_py( Array a_dir, Array a_off, Array b_dir, Array b_off ) : pc(
            Span<Point>{ reinterpret_cast<Point *>( a_dir.mutable_data() ), PI( a_dir.shape( 0 ) ) },
            { a_off.mutable_data(), PI( a_off.shape( 0 ) ) },
            Span<Point>{ reinterpret_cast<Point *>( b_dir.mutable_data() ), PI( b_dir.shape( 0 ) ) },
            { b_off.mutable_data(), PI( b_off.shape( 0 ) ) }
    ) {
    }

    void write_vtk( const Str &filename ) {
        VtkOutput vo;
        pc.display_vtk( vo );
        vo.save( filename );
    }

    PolyCon<POLYCON_SCALAR,POLYCON_DIM> pc;
};

void fill_polycon_module( py::module_ &m, Str name ) {
    py::class_<PolyCon_py>( m, name.c_str(), py::module_local() )
        .def( py::init<Array, Array, Array, Array>() )
        .def( "write_vtk", &PolyCon_py::write_vtk );
}
