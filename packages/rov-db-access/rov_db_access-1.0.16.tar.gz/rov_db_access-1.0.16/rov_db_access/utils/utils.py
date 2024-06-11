from typing import Optional

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape, from_shape
from shapely import wkt, get_srid


def wkt_to_wkbelement(wkt_str: str) -> WKBElement:
    shapely_geometry = wkt.loads(wkt_str)
    if shapely_geometry.geom_type == "MultiPolygon":
        shapely_geometry = list(shapely_geometry.geoms)[0]
    return from_shape(shapely_geometry, srid=4326)


def ewkt_to_wkbelement(ewkt: str) -> WKBElement:
    wkt_str = ewkt[ewkt.find(";") + 1: -1]
    shapely_geometry = wkt.loads(wkt_str)
    if shapely_geometry.geom_type == "MultiPolygon":
        shapely_geometry = list(shapely_geometry.geoms)[0]
    return from_shape(shapely_geometry, srid=4326)


def wkbelement_to_ewkt(ewkt: WKBElement) -> str:
    geometry = to_shape(ewkt)
    srid = get_srid(geometry)
    if srid == 0:
        srid = 4326
    srid_str = '='.join(['SRID', srid])
    wkt_str = geometry.wkt
    ewkt = ';'.join([srid_str, wkt_str])
    return ewkt


def wkbelement_to_wkt(ewkt: Optional[WKBElement]) -> Optional[str]:
    if ewkt is None:
        return None
    return to_shape(ewkt).wkt

def add_srid_to_raw_wkt(wkt_str: str, srid: int = 4326) -> str:
    srid_str = f'SRID={srid};'
    return srid_str + wkt_str
