import uuid
import time
from ftssim import _common


class Wander:
    def __init__(self, tak_server: str, total_distance_km: int, distance_between_change: int, start_lat: float,
                 start_lon: float, callsign: str, tak_port: int = 8087, speed_kph: int = 5, max_time_step_secs: int = 4,
                 cot_identity: str = "friend", cot_dimension: str = "land-unit", cot_stale: int = 1,
                 cot_type: str = "a-f-G-U-C"):
        """
        Constructs all the necessary attributes for a wandering object.

        Parameters
        ----------
            tak_server : str
                address for the tak server to set CoT to
            total_distance_km : int
                total distance in kilometers to wander
            distance_between_change : int
                distance in km between direction changes
            start_lat : float
                the starting point latitude
            start_lon : float
                the starting point longitude
            callsign : str
                callsign for user in ATAK
            tak_port : int
                port that takserver is listening on
            speed_kph : int
                speed the gpx will play back at in kph
            max_time_step_secs : int
                max time in seconds allows for a gap between CoT messages (the smaller the number the more
                fluid the movement)
            cot_identity : str
                Cot identity e.g friend
            cot_dimension : str
                Cot dimension e.g land-unit
            cot_stale : int
                Time in minuets for the object to become stale in ATAK
            cot_type : str
                CoT identifier string to use
        """
        self.callsign = callsign
        self.lat = start_lat
        self.lon = start_lon
        self.total_distance_km = total_distance_km
        self.distance_between_change = distance_between_change
        self.tak_port = tak_port
        self.tak_server = tak_server
        self.cot_identity = cot_identity
        self.cot_dimension = cot_dimension
        self.cot_stale = cot_stale
        self.cot_type = cot_type
        self.speed_kph = speed_kph
        self.max_time_step_secs = max_time_step_secs
        self.uid = str(uuid.uuid4())

    def start_wandering(self) -> None:
        """
        Start aimlessly wandering object
        """
        points = [(self.lat, self.lon)]
        km_count = 0
        next_lat = self.lat
        next_lon = self.lon
        while km_count < self.total_distance_km:
            next_lat, next_lon = _common.move_from_location_in_random_direction(next_lat, next_lon,
                                                                                self.distance_between_change)
            points.insert(km_count + 1, (next_lat, next_lon))
            km_count += self.distance_between_change
        points, waits = _common.generate_smooth_route(points, self.speed_kph, self.max_time_step_secs)
        _common.iterate_and_send(points, waits, self.tak_server, self.tak_port, self.cot_type, self.callsign, self.uid,
                                 self.cot_identity, self.cot_dimension, self.cot_stale)

    def loiter_for_time(self, loiter_time_secs: int) -> None:
        """
        Loiter in the area

        Parameters
        ----------
            loiter_time_secs : int
                Time in seconds for object to loiter in area
        """
        centre_lat = self.lat
        centre_lon = self.lon
        points = []
        waits = []
        num_points = loiter_time_secs / self.max_time_step_secs
        point_counter = 0
        while point_counter < num_points:
            points.insert(point_counter, (centre_lat, centre_lon))
            waits.insert(point_counter, self.max_time_step_secs)

            next_lat, next_lon = _common.move_from_location_in_random_direction(centre_lat, centre_lon, 0.005)
            points.insert(point_counter + 1, (next_lat, next_lon))
            waits.insert(point_counter + 1, self.max_time_step_secs)

            point_counter += 2

        _common.iterate_and_send(points, waits, self.tak_server, self.tak_port, self.cot_type, self.callsign, self.uid,
                                 self.cot_identity, self.cot_dimension, self.cot_stale)

    def circle_point(self, radius: int, clockwise: bool = True) -> None:
        """
        Loiter in the area

        Parameters
        ----------
            radius : int
                Radius in Meters from starting point to circle
            clockwise : bool
                Bool value to denote direction (default is clockwise)
        """
        centre_lat = self.lat
        centre_lon = self.lon
        points = []
        point_counter = 0
        clock_bearing = 0
        anti_clock_bearing = 359
        if clockwise:
            while clock_bearing <= 359:
                next_lat, next_lon = _common.move_from_location(centre_lat, centre_lon, (radius/1000), clock_bearing)
                points.insert(point_counter, (next_lat, next_lon))
                clock_bearing += 9.9
                point_counter += 1
        else:
            while anti_clock_bearing >= 0:
                next_lat, next_lon = _common.move_from_location(centre_lat, centre_lon, (radius/1000), anti_clock_bearing)
                points.insert(point_counter, (next_lat, next_lon))
                anti_clock_bearing -= 9.9
                point_counter += 1
        points, waits = _common.generate_smooth_route(points, self.speed_kph, self.max_time_step_secs)
        _common.iterate_and_send(points, waits, self.tak_server, self.tak_port, self.cot_type, self.callsign, self.uid,
                                 self.cot_identity, self.cot_dimension, self.cot_stale)
