#
#   Test if all shapely methods are implemented
#   This makes it easier to update PGPD to new shapely versions
#
import pytest
import shapely

import pgpd

skips = {
    '_geometry': ('SetPrecisionMode',),
    'creation': (
        'box',
        'collections_1d',
        'empty',
        'from_wkt',
        'geometrycollections',
        'linearrings',
        'linestrings',
        'multilinestrings',
        'multipoints',
        'multipolygons',
        'points',
        'polygons',
        'simple_geometries_1d',
    ),
    'measurement': (),
    'predicates': (),
    'set_operations': (),
    'constructive': (
        'BufferCapStyle',
        'BufferJoinStyle',
    ),
    'linear': (),
    'coordinates': ('get_coordinates',),
    'strtree': (
        'Any',
        'BaseGeometry',
        'BinaryPredicate',
        'Iterable',
        'Union',
    ),
}

global_skips = (
    'Geometry',
    'GeometryType',
    'geos_version',
    'IntEnum',
    'lib',
    'multithreading_enabled',
    'np',
    'ParamEnum',
    'requires_geos',
    'warnings',
    'UnsupportedGEOSVersionError',
)


@pytest.mark.parametrize('module', skips.keys())
def test_for_missing_methods(module):
    skip = skips[module]
    mod = getattr(shapely, module)

    for func in dir(mod):
        if func.startswith('_'):
            continue
        if func in global_skips:
            continue
        if func in skip:
            continue

        if func not in dir(pgpd.GeosSeriesAccessor):
            raise NotImplementedError(f'{module}.{func}')
