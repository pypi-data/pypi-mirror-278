// cppimport

#define POLYCON_DIM 7
#define POLYCON_SCALAR FP64
#include "polycon_bindings.h"

PYBIND11_MODULE(polycon_bindings_07_FP64, m) {
    fill_polycon_module( m, "PolyCon_07_FP64" );
}

/*
<%
import sys, os
sys.path.append( os.getcwd() + '/polycon/lib' )
from cppimport_cfg import cppimport_cfg
setup_pybind11( cfg )
cppimport_cfg( cfg )
%>
*/
