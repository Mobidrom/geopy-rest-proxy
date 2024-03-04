from auth import get_user
from fastapi import APIRouter, Depends
from geojson import Feature, FeatureCollection, Point
from geopy import Location
from geopy.geocoders import Photon

router = APIRouter()


def loc_to_geojson(
    loc: Location | list[Location], geocoder: str | None = "Unknown"
) -> FeatureCollection | FeatureCollection:
    if isinstance(loc, Location):
        ret_point = Point(loc.point)
        prop_adress = {"address": loc.address}
        prop_geocoder = {"geocoder": geocoder}
        prop_raw = {"raw": loc.raw}
        ret_feature = Feature(geometry=ret_point, properties=[prop_adress, prop_geocoder, prop_raw])
        ret_feature_col = FeatureCollection(ret_feature)

    if isinstance(loc, list):
        feature_list = [Feature]
        for entry in loc:
            ret_point = Point(entry.point)
            prop_adress = {"address": entry.address}
            prop_geocoder = {"geocoder": geocoder}
            prop_raw = {"raw": entry.raw}
            ret_feature = Feature(geometry=ret_point, properties=[prop_adress, prop_geocoder, prop_raw])
            feature_list.append(ret_feature)
            print(feature_list)
        ret_feature_col = FeatureCollection(feature_list)

    return ret_feature_col


@router.get("/")
async def get_testroute(user: dict = Depends(get_user)):
    return user


@router.get("/api")
async def geocode(
    q: str,
    limit: int | None = None,
    lang: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    geocoder: str | None = "photon",
    raw: bool | None = False,
):
    if limit == 1:
        exactly_one = True
    else:
        exactly_one = False
    match geocoder:
        case "photon":
            upstream_geocoder = Photon()
            location = upstream_geocoder.geocode(
                query=q, exactly_one=exactly_one, language=lang, limit=limit, location_bias=(lat, lon)
            )
            ret_geojson = loc_to_geojson(location, geocoder)
    return ret_geojson


@router.get("/reverse")
async def reverse(lon: float, lat: float, geocoder: str | None = "photon", limit: int | None = None):
    if limit == 1:
        exactly_one = True
        print("Foobar")
    else:
        exactly_one = False
    match geocoder:
        case "photon":
            upstream_geocoder = Photon()
            location = upstream_geocoder.reverse((lat, lon), exactly_one=exactly_one, limit=limit)
            ret_geojson = loc_to_geojson(location, geocoder)
    return ret_geojson
