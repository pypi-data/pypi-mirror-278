// cppimport

#define POLYCON_DIM 9
#define POLYCON_SCALAR FP64
#include "polycon_bindings.h"

PYBIND11_MODULE(polycon_bindings_09_FP64, m) {
    fill_polycon_module( m, "PolyCon_09_FP64" );
}

/*

*/
