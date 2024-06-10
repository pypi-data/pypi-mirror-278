// cppimport

#define POLYCON_DIM 5
#define POLYCON_SCALAR FP64
#include "polycon_bindings.h"

PYBIND11_MODULE(polycon_bindings_05_FP64, m) {
    fill_polycon_module( m, "PolyCon_05_FP64" );
}

/*

*/
