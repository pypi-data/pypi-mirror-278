// cppimport

#define POLYCON_DIM 02
#define POLYCON_SCALAR FP64
#include "polycon_bindings.h"

PYBIND11_MODULE(polycon_bindings_02_FP64, m) {
    py::class_<PolyCon_py>( m, "PolyCon" )
        .def( py::init<Array, Array, Array, Array>() )
        .def( "go", &PolyCon_py::go );
}

/*

*/
