from .footprint_facility import (rework_to_polygon_geometry,
                                 rework_to_linestring_geometry,
                                 check_cross_antimeridian,
                                 simplify, find_best_tolerance_for,
                                 check_time, show_summary,
                                 to_wkt, to_geojson)
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

__all__ = ['rework_to_polygon_geometry', 'rework_to_linestring_geometry',
           'check_cross_antimeridian', 'simplify', 'find_best_tolerance_for',
           'check_time', 'show_summary',
           'to_geojson', 'to_wkt']
