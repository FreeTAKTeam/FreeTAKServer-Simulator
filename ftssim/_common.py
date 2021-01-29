import geopy.distance
from typing import Tuple, Callable
from takpak.takcot import takcot
from takpak.mkcot import mkcot
import random
import time


def move_from_location(lat: float, lon: float, distance_km: float, bearing: float) -> Tuple[float, float]:
    """
    Get the coordinates at a given distance away in a set bearing

    Parameters
    ----------
        lat : float
            starting latitude
        lon : float
            starting latitude
        distance_km : float
            distance to move in kilometers (1 and above)
        bearing : float
            the bearing to head in (0-360)

    Returns
    -------
        Tuple[float, float]

    """
    start_point = geopy.Point(lat, lon)
    d = geopy.distance.distance(kilometers=distance_km)
    end_point = d.destination(point=start_point, bearing=bearing)

    return end_point.latitude, end_point.longitude


def move_from_location_in_random_direction(lat: float, lon: float, distance_km: float) -> Tuple[float, float]:
    """
    Get the coordinates at a given distance away in a random bearing

    Parameters
    ----------
        lat : float
            starting latitude
        lon : float
            starting latitude
        distance_km : float
            distance to move in kilometers (1 and above)

    Returns
    -------
        Tuple[float, float]

    """
    bearing = round(random.uniform(0, 360), 1)
    new_lat, new_lon = move_from_location(lat, lon, distance_km, bearing)

    return new_lat, new_lon


def get_midway_coords(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
    """
    Get the coordinates half way between to coordinates

    Parameters
    ----------
        lat1 : float
            first latitude
        lat2 : float
            second latitude
        lon1 : float
            first longitude
        lon2 : float
            second longitude

    Returns
    -------
        Tuple[float, float]

    """
    midlat = (lat1 + lat2) / 2
    midlong = (lon1 + lon2) / 2

    return midlat, midlong


def generate_smooth_route(points: list, speed_kph: int, max_time_step_secs: int) -> Tuple[list, list]:
    """
    Takes a list of coordinates and adds more points to the list to create a smooth journey

    Parameters
    ----------
        points : list
            list of coordinate points
        speed_kph : int
            the speed the object needs to travel at
        max_time_step_secs : int
            the maximum gap between calling in in seconds

    Returns
    -------
        Tuple[list, list]

    """
    waits = []
    pnt = 0
    while pnt < len(points) - 1:
        pnt_1 = pnt + 1
        dst = geopy.distance.distance(points[pnt], points[pnt_1]).km
        time_seconds = (dst / speed_kph) * 60 * 60
        if time_seconds > max_time_step_secs:
            points.insert(pnt_1,
                          get_midway_coords(points[pnt][0], points[pnt][1], points[pnt_1][0], points[pnt_1][1]))
        else:
            waits.insert(pnt, time_seconds)
            pnt += 1

    return points, waits


def iterate_and_send(points: list, waits: list, tak_server: str, tak_port: int, cot_type: str, callsign: str, uid: str):
    """
    Iterates through list of coordinate points and wait times and sends them to a TAKServer

    Parameters
    ----------
        points : list
            list of coordinate points
        waits : list
            list of times in seconds to wait between locations
        tak_server : str
            the address of the target TAKServer
        tak_port : int
            the port for the target TAKServer
        cot_type : str
            cot type string e.g a-f-G-U-C
        callsign : str
            the callsign of the object
        uid : str
            the uid for the object
    """
    takserver = takcot()
    takserver.open(tak_server, tak_port)
    locator = 0
    takserver.flush()
    for location in points:
        takserver.send(mkcot.mkcot(cot_identity="friend",
                                   cot_stale=1,
                                   cot_dimension="land-unit",
                                   cot_typesuffix=str(cot_type),
                                   cot_callsign=str(callsign),
                                   cot_id=str(uid),
                                   cot_lat=round(location[0], 5), cot_lon=round(location[1], 5)))
        takserver.flush()
        try:
            time.sleep(waits[locator])
        except IndexError:
            break
        locator += 1
    takserver.close()


def offset_route(points: list, distance_km: float) -> list:
    """
    Iterates through list of coordinate points and wait times and sends them to a TAKServer

    Parameters
    ----------
        points : list
            list of coordinate points
        distance_km : float
            distance in km to offset a route by

    Returns
    -------
        List

    """
    new_points = []
    bearing = round(random.uniform(0, 360), 1)
    pnt = 0
    for point in points:
        new_lat, new_lon = move_from_location(point[0], point[1], distance_km, bearing)
        new_points.insert(pnt, (new_lat, new_lon))
        pnt += 1
    return new_points


def iterate_wrapper(points, waits, tak_server, tak_port, cot_type, callsign, uid) -> Callable:
    """
    Iterates through list of coordinate points and wait times and sends them to a TAKServer

    Parameters
    ----------
        points : list
            list of coordinate points
        waits : list
            list of times in seconds to wait between locations
        tak_server : str
            the address of the target TAKServer
        tak_port : int
            the port for the target TAKServer
        cot_type : str
            cot type string e.g a-f-G-U-C
        callsign : str
            the callsign of the object
        uid : str
            the uid for the object


    Returns
    -------
        Callable

    """
    def wrapper():
        iterate_and_send(points, waits, tak_server, tak_port, cot_type, callsign, uid)
    return wrapper
