// cppimport

#define POLYCON_DIM 1
#define POLYCON_SCALAR FP64
#include "polycon_bindings.h"

PYBIND11_MODULE(polycon_bindings_01_FP64, m) {
    fill_polycon_module( m, "PolyCon_01_FP64" );
}

/*

*/
