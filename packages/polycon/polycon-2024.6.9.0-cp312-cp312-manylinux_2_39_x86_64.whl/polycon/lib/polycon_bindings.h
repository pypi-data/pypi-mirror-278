#include "../../../cpp/polycon/PolyCon.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#ifndef POLYCON_SCALAR
#define POLYCON_SCALAR FP64
#endif

#ifndef POLYCON_DIM
#define POLYCON_DIM 02
#endif

namespace py = pybind11;
using Array = py::array_t<POLYCON_SCALAR, py::array::c_style>;
using Point = PolyCon<POLYCON_SCALAR,POLYCON_DIM>::Point;

struct PolyCon_py {
    PolyCon_py( Array a_dir, Array a_off, Array b_dir, Array b_off ) : pc(
            Span<Point>{ reinterpret_cast<Point *>( a_dir.mutable_data() ), PI( a_dir.shape( 0 ) ) },
            { a_off.mutable_data(), PI( a_off.shape( 0 ) ) },
            Span<Point>{ reinterpret_cast<Point *>( b_dir.mutable_data() ), PI( b_dir.shape( 0 ) ) },
            { b_off.mutable_data(), PI( b_off.shape( 0 ) ) }
    ) {
    }

    PI go() { return pc.nb_bnds(); }

    PolyCon<POLYCON_SCALAR,POLYCON_DIM> pc;
};
