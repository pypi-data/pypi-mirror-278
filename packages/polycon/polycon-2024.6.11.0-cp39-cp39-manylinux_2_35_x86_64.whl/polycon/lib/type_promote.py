
kind_value = { '': 0, 'i': 1, 'f': 2 }
def best_kind( a, b ):
    if kind_value[ a ] >= kind_value[ b ]:
        return a
    else:
        return b

type_map = { 'f4': 'FP32', 'f8': 'FP64' }
def make_type( kind, size ):
    return type_map[ kind + str( size ) ]
    
def type_promote( *types, **kw_args ):
    kind = ''
    size = 4
    for type in types:
        kind = best_kind( kind, type.kind )
        size = max( size, type.itemsize )

    if 'ensure_scalar' in kw_args and kw_args[ 'ensure_scalar' ]:
        kind = 'f' # TODO: rational, ...
        
    return make_type( kind, size )
