from unittest import TestCase, skip
import json
import shapely
from shapely import Polygon, Point, Geometry, wkt
from shapely.ops import transform as sh_transform
from pyproj import Transformer
import os

import footprint_facility


#############################################################################
# Private Utilities to manipulate input test Footprint file
# - load
# - retrieve longitude/Latitude list according to the input
# - build shapely geometry
#############################################################################
def _load_samples():
    path = os.path.join(os.path.dirname(__file__),
                        'samples', 'footprints_basic.json')
    with open(path) as f:
        return json.load(f)['footprint']


def _split(txt, seps):
    """
    Split with list of separators
    """
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_odd_values(fp):
    # [1::2] odd indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[1::2]]


def get_even_values(fp):
    # [::2] even indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[::2]]


def get_longitudes(fp):
    func = get_even_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[1][:3:] == 'lon':
            func = get_odd_values
    return func(fp)


# Extract latitude coord list
def get_latitudes(fp):
    func = get_odd_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[0][:3:] == 'lat':
            func = get_even_values
    return func(fp)


def fp_to_geometry(footprint) -> Geometry:
    lon = get_longitudes(footprint)
    lat = get_latitudes(footprint)
    return Polygon([Point(xy) for xy in zip(lon, lat)])


def disk_on_globe(lon, lat, radius, func=None):
    """Generate a shapely.Polygon object representing a disk on the
    surface of the Earth, containing all points within RADIUS meters
    of latitude/longitude LAT/LON."""

    # Use local azimuth projection to manage distances in meter
    # then convert to lat/lon degrees
    local_azimuthal_projection = \
        "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)
    lat_lon_projection = "+proj=longlat +datum=WGS84 +no_defs"

    wgs84_to_aeqd = Transformer.from_crs(lat_lon_projection,
                                         local_azimuthal_projection)
    aeqd_to_wgs84 = Transformer.from_crs(local_azimuthal_projection,
                                         lat_lon_projection)

    center = Point(float(lon), float(lat))
    point_transformed = sh_transform(wgs84_to_aeqd.transform, center)
    buffer = point_transformed.buffer(radius)
    disk = sh_transform(aeqd_to_wgs84.transform, buffer)
    if func is None:
        return disk
    else:
        return func(disk)


#############################################################################
# Test Class
#############################################################################
class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.footprints = _load_samples()
        footprint_facility.check_time(enable=True,
                                      incremental=False,
                                      summary_time=True)

    @classmethod
    def tearDownClass(cls):
        footprint_facility.show_summary()

    def setUp(self):
        pass

    def test_check_contains_pole_north(self):
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_contains_pole_south(self):
        geom = disk_on_globe(-160, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_antimeridian(self):
        geom = disk_on_globe(-179, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_no_antimeridian(self):
        geom = disk_on_globe(0, 0, 500*1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))

    def test_check_samples(self):
        """
        Pass through all the entries of the sample file that are marked as
        testable, then ensure they can be managed and reworked without failure.
        """
        for footprint in self.footprints:
            if footprint.get('testable', True):
                geom = fp_to_geometry(footprint)
                result = footprint_facility.check_cross_antimeridian(geom)
                self.assertEqual(result, footprint['antimeridian'],
                                 f"longitude singularity not properly "
                                 f"detected({footprint['name']}).")

    def test_rework_with_north_pole(self):
        """This footprint contains antimeridian and North Pole.
        """
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_with_south_pole(self):
        """This footprint contains antimeridian and South Pole.
        """
        geom = disk_on_globe(0, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_close_to_north_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the North Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_close_to_south_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the South Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, -81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_no_pole(self):
        """This footprint contains antimeridian and no pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)

    def test_rework_no_pole_no_antimeridian(self):
        """This footprint none of antimeridian and pole.
          No change of the footprint is required here.
        """
        geom = disk_on_globe(0, 0, 500 * 1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertEqual(geom, rwkd)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprint is not equivalents to input.")
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_no_antimeridian(self):
        """
        Index 15 is a S3B SLSTR footprint located over Atlantic sea.
        It does not intersect antimeridian nor pole.

        Product available in CDSE as:
        S3B_OL_2_LRR____20240311T111059_20240311T115453_20240311T134014_2634_090_308______PS2_O_NR_002
        product id: 247c85f8-a78c-4abf-9005-2171ad6d8455
        """
        index = 15
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_cross_antimeridian(self):
        """
        Index 17 is a S3B OLCI Level 1 ERR footprint located over Pacific sea.
        It intersects antimeridian but does not pass over the pole.

        Product available in CDSE as:
        S3B_OL_1_ERR____20240224T213352_20240224T221740_20240225T090115_2628_090_086______PS2_O_NT_003
        product id: 07a3fa27-787f-479c-9bb3-d267249ffad3
        """
        index = 17
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_south_pole_antimeridian_overlapping(self):
        """
        Index 18 is a very long S3A SLSTR WST footprint.
        It intersects antimeridian and passes over the South Pole.
        At the South Pole location the footprint overlaps.

        Product available in CDSE as:
        S3A_SL_2_WST____20240224T211727_20240224T225826_20240226T033733_6059_109_228______MAR_O_NT_003
        product id: 67a2b237-50dc-4967-98ce-bad0fbc04ad3
        """
        index = 18
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    @skip("Overlapping both north and south pole is still not supported")
    def test_rework_product_north_pole_antimeridian_overlapping(self):
        """
         Footprint with overlapping on the North Pole.It also passes other
         both North and South Pole.

         The fact the footprint cross both north and south pole fails with de
         manipulation and display.

         This product is an old historical product and this use case has not
         been retrieved in CDSE.
        """
        index = 10
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.
           index 16 footprint is S3A product type SR_2_LAN_LI from CDSE
           S3A_SR_2_LAN_LI_20240302T235923_20240303T001845_20240304T182116_1161_109_330______PS1_O_ST_005
        """
        index = 16
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiLineString)
        self.assertAlmostEqual(int(rwkd.length), 180, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_no_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.

           index 21 footprint is S3A product type SR_2_WAT from CDSE
           S3A_SR_2_WAT____20240312T172025_20240312T180447_20240314T075541_2661_110_083______MAR_O_ST_005
           cdse product id: f4b8547b-45ff-430c-839d-50a9be9c6105
        """
        index = 21
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.LineString)
        self.assertAlmostEqual(int(rwkd.length), 220, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_south_hemisphere_no_pole_antimeridian(self):
        """
        Footprint index 2 is a small simple footprint crossing antimeridan
        """
        footprint = self.footprints[2]
        geom = fp_to_geometry(footprint)
        self.assertEqual(footprint_facility.check_cross_antimeridian(geom),
                         footprint['antimeridian'])
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 18, delta=1)
        print(footprint_facility.to_geojson(rwkd))

    def testSimplifySimple(self):
        """
        Ensure an already simple polygon is not affected by the algorithm
        """
        index = 0
        geom = fp_to_geometry(self.footprints[index])

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)

        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifyAntimeridian(self):
        """
        Ensure an already simple polygon , crossing antimeridian
        is not affected by the algorithm
        """
        index = 3
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)
        print(rwkd)

        self.assertEqual(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_best_tolerance_for_single_geom(self):
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Surface change is limiting to 0.5% vs 100% of points could disappear
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.27, delta=0.01)

        # Point reduction 50% is controlling the surface (See document: 50%
        # is quickly reached)
        percentage_area_change = 1
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.028, delta=0.001)

    def test_best_tolerance_for_synergy(self):
        index = 22
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Synergy does not require tolerance: area surface never change,
        # and points are reduced from 292 to 5 with tolerance 0
        # The following parameter can not be reached  by the algorithm:
        #   This use cas is the most time-consuming
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

        # No area change for synergy
        percentage_area_change = 0
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))
        print(best_tolerance)
        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

    def testLongNoAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 211)
        self.assertAlmostEqual(origin_area, 2976.02, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2976.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 211)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2977.53, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3005.78, delta=0.01)
        self.assertEqual(stats['Points']['new'], 26)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3015.72, delta=0.01)
        self.assertEqual(stats['Points']['new'], 21)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3036.00, delta=0.01)
        self.assertEqual(stats['Points']['new'], 13)

    def testLongWithAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 17
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 216)
        self.assertAlmostEqual(origin_area, 2961.08, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2961.08, delta=0.01)
        self.assertEqual(stats['Points']['new'], 216)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2963.40, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2982.90, delta=0.01)
        self.assertEqual(stats['Points']['new'], 33)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2993.12, delta=0.01)
        self.assertEqual(stats['Points']['new'], 24)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3049.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 18)

    def testLongWithAntimeridianAndPole(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 18
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))
        print(footprint_facility.to_geojson(geom))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 272)
        self.assertAlmostEqual(origin_area, 10857.59, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10857.59, delta=0.01)
        self.assertEqual(stats['Points']['new'], 272)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10862.31, delta=0.01)
        self.assertEqual(stats['Points']['new'], 166)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10951.32, delta=0.01)
        self.assertEqual(stats['Points']['new'], 70)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10964.73, delta=0.01)
        self.assertEqual(stats['Points']['new'], 55)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 11229.99, delta=0.01)
        self.assertEqual(stats['Points']['new'], 39)

    def iter_among_simplify_tolerance(self, geometry, min: float, max: float,
                                      step: float):
        for tolerance in (map(lambda x: x/10000.0,
                              range(int(min*10000),
                                    int(max*10000),
                                    int(step*10000)))):
            print(self.simplify_bench(geometry, tolerance))

    @staticmethod
    def simplify_bench(geometry, tolerance=.1):
        origin_area = getattr(geometry, 'area', 0)
        origin_points_number = len(shapely.get_coordinates(geometry))

        reworked = footprint_facility.simplify(geometry, tolerance=tolerance)
        new_area = reworked.area
        variation_area = (new_area - origin_area)/origin_area
        new_points_number = len(shapely.get_coordinates(reworked))
        variation_point = ((new_points_number - origin_points_number) /
                           origin_points_number)
        return dict(value=tolerance,
                    Points=dict(
                        origin=origin_points_number,
                        new=new_points_number,
                        variation=variation_point),
                    Area=dict(
                        origin=origin_area,
                        new=new_area,
                        variation=variation_area))

    def testSimplifySynergyEurope(self):
        """
        Europe Syngery footprint has 297 point to be simplified
        :return:
        """
        index = 22
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("EUROPE" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 297)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifySynergyAustralia(self):
        """
        Australia Syngery footprint has 295 point to be simplified
        :return:
        """
        index = 23
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("AUSTRALASIA" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 295)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_print_geojson_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_geojson(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_print_wkt_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_wkt(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_S1A_WV_SLC__1SSV_no_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data.
        convex hull algortihm generates a polygon reducing points number
        from 470 to 53.
        """
        filename = ('S1A_WV_SLC__1SSV_20240408T072206_20240408T074451_053339_'
                    '0677B9_0282.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))

        geometry = shapely.MultiPolygon(polygons)
        self.assertEqual(
            len(shapely.get_coordinates(geometry)), 470)
        self.assertEqual(len(
            shapely.get_coordinates(geometry.convex_hull)), 53)

    def test_S1A_WV_SLC__1SSV_crossing_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data. This data crosses
        the antimridian.
        Convex hull algortihm generates a polygon reducing points number
        from 470 to 53. But This algorithm does not support antimeridian
        singularity, it shall be split into 2 polygons before execution.
        :return:
        """
        filename = ('S1A_WV_SLC__1SSV_20240405T060850_20240405T062741_053294_'
                    '0675E8_157E.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))
        geometry = shapely.MultiPolygon(polygons)

        east_geometry = geometry.intersection(shapely.box(-180, -90, 0, 90))
        west_geometry = geometry.intersection(shapely.box(0, -90, 180, 90))

        self.assertEqual(len(shapely.get_coordinates(geometry)), 390)
        self.assertEqual(
            len(shapely.get_coordinates(east_geometry.convex_hull)) +
            len(shapely.get_coordinates(west_geometry.convex_hull)), 49)

    def test_jan_07_06_2024_S1(self):
        """
        Issue reported by Jan Musiał <jmusial@cloudferro.com> 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_0695B3_"
        "DC42.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_"
                "0695B3_DC42.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                                '$filter=((Name%20eq%20%27'$product'%27))' |
            jq '.value[] | .Footprint' |
            tr -d '"' |
            tr -d "'" |
            cut -f 2 -d ';' |
            xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """

        product = ("MULTIPOLYGON (((-174.036011 66.098473, -170.292542 "
                   "70.167793, -180 71.02345651890965, "
                   "-180 66.64955743876074, -174.036011 66.098473)), "
                   "((180 66.64955743876074, 180 71.02345651890965, "
                   "178.781082 71.130898, 176.806686 66.944626, "
                   "180 66.64955743876074)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S2(self):
        """
        Issue reported by Jan Musiał <jmusial@cloudferro.com> 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_20240112T201221.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_"
                "20240112T201221.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                              '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("POLYGON ((-179.508117526313 -79.16127199879642, -180 "
                   "-79.01692999138557, -180 -79.19944296655834, "
                   "-180 -79.19959581716972, -180 -79.19972960600606, "
                   "-180 -79.19988578232916, -180 -79.20007346017209, "
                   "-180 -79.20013436682478, -180 -79.20024126342099, "
                   "-180 -79.20029258993124, -180 -79.20049921536173, "
                   "-180 -79.20054631332516, -180 -79.20066396817484, "
                   "-180 -79.20077375877023, -180 -79.2008843839914, "
                   "-180 -79.21714918681978, -180 -79.21715630792468, "
                   "-180 -79.2175551235766, -180 -79.21773293229286, "
                   "-180 -79.21778003784787, -180 -79.2177900670303, "
                   "-180 -79.21779114542757, -180 -79.21779351757006, "
                   "-180 -79.21780296489362, -180 -79.21780421542903, "
                   "-180 -79.21780998189048, -180 -79.21827514353097, "
                   "-180 -79.21830910412172, -180 -79.33237518158053, "
                   "-178.9375581912928 -79.33974790172739, "
                   "-179.5490821971551 -79.1659353807717, -179.5463891574934 "
                   "-79.16562951391516, -179.5464126641663 "
                   "-79.16562282940411, -179.508117526313 "
                   "-79.16127199879642))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S3(self):
        """
        Issue reported by Jan Musiał <jmusial@cloudferro.com> 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S3A_SL_2_LST____20240601T075148_20240601T075448_20240601T102247_0180_
            113_078_1080_PS1_O_NR_004.SEN3"

        Command line used:
        <code>
        #Sentinel-6
        product="S3A_SL_2_LST____20240601T075148_20240601T075448_"
                "20240601T102247_0180_113_078_1080_PS1_O_NR_004.SEN3"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 65.68414879114478, 179.764 65.842, "
                   "175.686 68.0499, 170.896 70.1128, 171.256 70.2301, "
                   "172.291 70.5293, 173.355 70.8266, 174.424 71.108, "
                   "175.533 71.393, 176.703 71.6691, 177.869 71.9409, "
                   "179.088 72.1986, 180 72.38208313539192, "
                   "180 65.68414879114478)), ((-180 72.38208313539192, "
                   "-179.649 72.4527, -178.36 72.6974, -177.039 72.9329, "
                   "-175.694 73.1682, -174.288 73.3878, -172.854 73.5962, "
                   "-171.396 73.7949, -169.91 73.9844, -168.382 74.1639, "
                   "-166.798 74.3324, -165.214 74.4841, -163.563 74.6311, "
                   "-161.917 74.7626, -160.247 74.8843, -158.545 74.996, "
                   "-156.815 75.0909, -155.079 75.1715, -153.303 75.2416, "
                   "-151.49 75.2841, -149.712 75.3291, -147.895 75.3655, "
                   "-146.1 75.3717, -145.923 72.801, -145.686 70.1856, "
                   "-145.411 67.5691, -145.11 64.9601, -145.109 64.9514, "
                   "-146.171 64.9259, -147.266 64.8952, -148.33 64.8479, "
                   "-149.397 64.7954, -150.451 64.7395, -151.517 64.6709, "
                   "-152.57 64.5974, -153.604 64.5188, -154.67 64.4338, "
                   "-155.683 64.3383, -156.721 64.2411, -157.73 64.1281, "
                   "-158.74 64.0097, -159.743 63.8851, -160.753 63.7556, "
                   "-161.729 63.6187, -162.7 63.475, -163.671 63.3246, "
                   "-164.625 63.169, -165.557 62.9984, -166.489 62.8312, "
                   "-167.416 62.6562, -168.325 62.4771, -169.236 62.2889, "
                   "-170.112 62.094, -170.979 61.896, -171.853 61.6965, "
                   "-172.713 61.4854, -173.554 61.2618, -173.86 61.1864, "
                   "-173.885 61.1901, -176.803 63.5458, "
                   "-180 65.68414879114478, -180 72.38208313539192)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S5P(self):
        """
        Issue reported by Jan Musiał <jmusial@cloudferro.com> 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_03_020100_"
        "20240601T035317.nc"

        Command line used:
        <code>
        #Sentinel-6
        product="S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_"
                "03_020100_20240601T035317.nc"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((-180 90, 0 90, 180 90, 180 "
                   "-41.86733642322825, 179.9763 -41.531116, 179.86395 "
                   "-40.08868, 179.74141 -38.645264, 179.60912 -37.200897, "
                   "179.46786 -35.75559, 179.31769 -34.30946, 179.15906 "
                   "-32.862434, 178.99269 -31.414688, 178.81853 -29.966076, "
                   "178.63658 -28.516865, 178.44719 -27.067, 178.25061 "
                   "-25.61658, 178.04707 -24.165606, 177.8364 -22.714108, "
                   "177.61887 -21.262264, 177.39426 -19.81008, 177.1631 "
                   "-18.357447, 176.925 -16.904694, 176.68001 -15.451712, "
                   "176.42805 -13.998643, 176.16916 -12.545524, 175.90312 "
                   "-11.092463, 175.63004 -9.639457, 175.3496 -8.186663, "
                   "175.06177 -6.734143, 174.76614 -5.281979, 174.46315 "
                   "-3.8302007, 174.15176 -2.378978, 173.8324 -0.9284125, "
                   "173.50458 0.5215158, 173.16786 1.9705427, 172.82219 "
                   "3.4187272, 172.46709 4.8658676, 172.10217 6.3118157, "
                   "171.7273 7.756614, 171.34175 9.199921, 170.94524 "
                   "10.641779, 170.53746 12.082073, 170.11725 13.520405, "
                   "169.68442 14.956774, 169.2385 16.391098, 168.77852 "
                   "17.823135, 168.3039 19.252695, 167.81377 20.679672, "
                   "167.30734 22.103739, 166.78372 23.524765, 166.24197 "
                   "24.942528, 165.68028 26.356531, 165.09837 27.766888, "
                   "164.4945 29.173054, 163.86742 30.57479, 163.21565 "
                   "31.971884, 162.53703 33.36365, 161.83011 34.749847, "
                   "161.09294 36.13012, 160.32303 37.503757, 159.51851 "
                   "38.87066, 158.67624 40.229736, 157.79373 41.58067, "
                   "156.86758 42.922604, 155.89424 44.254745, 154.87033 "
                   "45.576374, 153.79134 46.886234, 152.65265 48.1834, "
                   "151.44977 49.466858, 150.1766 50.734867, 148.82782 "
                   "51.986423, 147.3959 53.21909, 145.87462 54.431526, "
                   "144.25616 55.6216, 142.53186 56.786644, 140.6929 "
                   "57.92401, 138.73013 59.03079, 136.63399 60.103626, "
                   "134.3939 61.13849, 132.00021 62.131363, 129.44383 "
                   "63.077717, 126.71549 63.972107, 123.80851 64.80932, "
                   "120.71825 65.58352, 117.4435 66.28858, 113.9866 "
                   "66.91782, 110.35588 67.46508, 106.56541 67.92443, "
                   "102.63593 68.29027, 98.59393 68.55761, 94.47231 "
                   "68.723015, 90.30819 68.78379, 86.14067 68.73939, "
                   "82.00989 68.59008, 77.953156 68.338196, 74.004 67.98733, "
                   "70.19006 67.54217, 66.53354 67.00781, 63.048588 "
                   "66.390724, 59.74498 65.69689, 56.62577 64.93289, "
                   "53.69056 64.10463, 50.934845 63.218437, 48.35202 "
                   "62.279533, 45.933685 61.293293, 43.670315 60.264317, "
                   "41.552414 59.196846, 39.569862 58.094654, 37.71257 "
                   "56.961403, 35.971294 55.800068, 34.337177 54.613335, "
                   "32.801754 53.40378, 31.356928 52.17355, 29.996086 "
                   "50.924458, 28.712265 49.658478, 27.499353 48.377003, "
                   "26.351748 47.081535, 25.264315 45.773205, 23.509417 "
                   "46.187706, 22.387592 46.436874, 19.424397 47.043514, "
                   "18.469027 47.22568, 16.448671 47.595142, 15.751153 "
                   "47.719036, 13.117875 48.17936, 12.130072 48.35204, "
                   "9.9415 48.740776, 9.136205 48.886753, 7.1947713 "
                   "49.245853, 6.4209137 49.39178, 4.406008 49.77871, "
                   "3.5373578 49.94825, 1.0665072 50.43534, -0.1086481 "
                   "50.66653, -2.2045333 51.070694, -3.02813 51.2248, "
                   "-5.5050035 51.66518, -6.7307587 51.867783, -9.840376 "
                   "52.32859, -10.816945 52.456486, -11.346613 52.522366, "
                   "-11.343067 52.666473, -11.319423 54.106884, -11.315634 "
                   "55.54611, -11.333933 56.984184, -11.37619 58.420925, "
                   "-11.446254 59.856216, -11.548398 61.290066, -11.686891 "
                   "62.722286, -11.867555 64.152725, -12.096516 65.58102, "
                   "-12.384995 67.007065, -12.7416525 68.4305, -13.182033 "
                   "69.850876, -13.724232 71.26764, -14.393544 72.67994, "
                   "-15.221556 74.08696, -16.253458 75.48708, -17.554081 "
                   "76.87837, -19.21444 78.25778, -21.374022 79.62078, "
                   "-24.246838 80.96009, -28.17806 82.26377, -33.747017 "
                   "83.51025, -41.931393 84.65964, -54.259308 85.634834, "
                   "-72.295746 86.2957, -94.80977 86.46186, -115.950935 "
                   "86.07003, -131.49446 85.25663, -141.87256 84.19631, "
                   "-148.8116 83.00032, -153.60501 81.72725, -157.0416 "
                   "80.407684, -159.58424 79.058525, -161.51413 77.6892, "
                   "-163.01147 76.30584, -164.1911 74.91215, -165.13258 "
                   "73.51075, -165.89003 72.103264, -166.50316 70.69103, "
                   "-167.00111 69.27482, -167.40501 67.85531, -167.73248 "
                   "66.43314, -167.99614 65.00868, -168.20502 63.582, "
                   "-168.36803 62.153614, -168.49158 60.72353, -168.58104 "
                   "59.291912, -168.6403 57.859013, -168.6735 56.42478, "
                   "-168.6834 54.989403, -168.67216 53.55279, -168.64241 "
                   "52.11524, -168.59605 50.676617, -168.53398 49.23707, "
                   "-168.458 47.7965, -168.36926 46.35513, -168.26866 "
                   "44.912914, -168.15657 43.469837, -168.03493 42.02598, "
                   "-167.90309 40.58142, -167.76227 39.136147, -167.61287 "
                   "37.69012, -167.45518 36.243496, -167.28972 34.796215, "
                   "-167.11655 33.34833, -166.93604 31.899948, -166.7488 "
                   "30.450903, -166.55434 29.001495, -166.35318 27.551653, "
                   "-166.14563 26.10141, -165.93146 24.65076, -165.71072 "
                   "23.199873, -165.48364 21.748617, -165.25038 20.297253, "
                   "-165.01054 18.84571, -164.7642 17.394058, -164.51172 "
                   "15.942321, -164.25249 14.490606, -163.98685 13.039, "
                   "-163.71452 11.58754, -163.4353 10.136244, -163.1493 "
                   "8.685246, -162.85625 7.23458, -162.55586 5.7843776, "
                   "-162.24821 4.334724, -161.93277 2.885562, -161.60968 "
                   "1.4371812, -161.27832 -0.010504091, -160.93875 "
                   "-1.4573016, -160.59015 -2.9031165, -160.2327 -4.3478966, "
                   "-159.86583 -5.791431, -159.4894 -7.233785, -159.10248 "
                   "-8.674613, -158.70517 -10.113982, -158.29645 -11.551577, "
                   "-157.87637 -12.98747, -157.444 -14.421311, -156.99876 "
                   "-15.85309, -156.54001 -17.282581, -156.06744 -18.709654, "
                   "-155.57948 -20.13405, -155.07596 -21.555643, -154.5558 "
                   "-22.974205, -154.01758 -24.389427, -153.46085 "
                   "-25.801155, -152.8842 -27.209108, -152.28654 -28.612999, "
                   "-151.66628 -30.012564, -151.02205 -31.407356, -150.35246 "
                   "-32.79723, -149.65543 -34.181614, -148.9292 -35.56014, "
                   "-148.17175 -36.932407, -147.38063 -38.29769, -146.55342 "
                   "-39.6557, -145.68736 -41.00566, -144.7798 -42.347084, "
                   "-143.8269 -43.67897, -142.82521 -45.00064, -141.77133 "
                   "-46.31118, -140.66045 -47.60957, -139.4877 -48.894478, "
                   "-138.24828 -50.16494, -136.93637 -51.41941, -135.5458 "
                   "-52.656303, -134.0697 -53.87377, -132.5008 -55.069862, "
                   "-130.8311 -56.242336, -129.05223 -57.388638, -127.15525 "
                   "-58.506126, -125.13072 -59.59139, -122.968834 "
                   "-60.641064, -120.659386 -61.651016, -118.19338 "
                   "-62.61717, -115.5613 -63.534576, -112.755646 -64.39802, "
                   "-109.7707 -65.20218, -106.60273 -65.9407, -108.59956 "
                   "-66.93513, -109.949425 -67.55315, -113.80929 -69.11937, "
                   "-115.14966 -69.60426, -118.14668 -70.59907, -119.23415 "
                   "-70.933334, -123.59422 -72.15644, -125.33779 -72.600525, "
                   "-129.42595 -73.55694, -131.01332 -73.89894, -135.04094 "
                   "-74.698845, -136.73071 -75.00694, -141.37552 -75.7759, "
                   "-143.49399 -76.090675, -149.93294 -76.91839, -153.21971 "
                   "-77.26976, -159.44414 -77.81199, -162.01192 -77.991165, "
                   "-170.08966 -78.39724, -174.24023 -78.5178, "
                   "-180 -78.54299733461647, -180 -60.43489669869457, "
                   "-179.96748 -60.16659, -179.83322 -58.742584, -179.73184 "
                   "-57.316566, -179.65977 -55.888824, -179.6136 -54.45934, "
                   "-179.59041 -53.028225, -179.58913 -51.595722, -179.60602 "
                   "-50.161697, -179.64015 -48.726337, -179.69008 -47.2897, "
                   "-179.75443 -45.851803, -179.83203 -44.412685, -179.9221 "
                   "-42.972466, -180 -41.86733642322825, -180 90)), "
                   "((180 -78.54299733461647, 175.04135 -78.56469, 171.68889 "
                   "-78.500534, 169.88521 -78.44987, 170.11551 -78.31641, "
                   "172.13577 -76.97113, 173.73349 -75.609184, 175.0151 "
                   "-74.23472, 176.05489 -72.85067, 176.90472 -71.4589, "
                   "177.60373 -70.061005, 178.18103 -68.65796, 178.65848 "
                   "-67.25062, 179.05312 -65.83957, 179.37799 -64.42529, "
                   "179.6447 -63.00817, 179.86017 -61.588566, "
                   "180 -60.43489669869457, 180 -78.54299733461647)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S6(self):
        """
        Issue reported by Jan Musiał <jmusial@cloudferro.com> 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S6A_P4_2__LR______20240601T141934_20240601T151547_20240602T094057_"
        "3373_131_075_037_EUM__OPE_ST_F09.SEN6"

        Command line used:
        <code>
        #Sentinel-6
        product="S6A_P4_2__LR______20240601T141934_20240601T151547_"
                "20240602T094057_3373_131_075_037_EUM__OPE_ST_F09.SEN6"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 60.22980148474507, 168.417758 "
                   "56.243085, 155.691259 46.750119, 147.366563 36.111285, "
                   "141.341637 24.872868, 136.505741 13.306639, 132.205885 "
                   "1.583584, 127.965756 -10.173274, 123.326157 -21.849296, "
                   "116.541992 -35.271951, 108.459264 -46.166451, 96.228309 "
                   "-56.013986, 76.619961 -63.592298, 48.281191 -66.644914, "
                   "48.174683 -65.650602, 76.260516 -62.659132, 95.601983 "
                   "-55.234425, 107.656475 -45.570188, 115.649571 "
                   "-34.820747, 122.396845 -21.480001, 127.025064 -9.834011, "
                   "131.267059 1.927975, 135.583207 13.692556, 140.460574 "
                   "25.345868, 146.579813 36.728557, 155.094546 47.552574, "
                   "168.092904 57.188849, 180 61.27018968706418, "
                   "180 60.22980148474507)), ((-180 61.27018968706418, "
                   "-171.164341 64.298748, -145.987795 66.645419, "
                   "-145.894989 65.649735, -171.071535 63.303063, "
                   "-180 60.22980148474507, -180 61.27018968706418)))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))
