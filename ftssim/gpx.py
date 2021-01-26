import gpxpy.gpx
import geopy.distance
import time
from takpak.takcot import takcot
from takpak.mkcot import mkcot
import uuid
from typing import Tuple


class GpxPlayer:
    def __init__(self, tak_server: str, filename: str, callsign: str, tak_port: int = 8087, speed_kph: int = 5,
                 max_time_step_secs: int = 4, cot_type: str = "a-f-G-U-C"):
        """
        Constructs all the necessary attributes for the gpx object.

        Parameters
        ----------
            tak_server : str
                address for the tak server to set CoT to
            filename : str
                filename/path to gpx file to play
            callsign : str
                callsign for user in ATAK
            tak_port : int
                port that takserver is listening on
            speed_kph : int
                speed the gpx will play back at in kph
            max_time_step_secs : int
                max time in seconds allows for a gap between CoT messages (the smaller the number the more
                fluid the movement)
            cot_type : str
                CoT identifier string to use
        """
        self.filename = filename
        self.callsign = callsign
        self.tak_port = tak_port
        self.tak_server = tak_server
        self.cot_type = cot_type
        self.speed_kph = speed_kph
        self.max_time_step_secs = max_time_step_secs
        self.uid = uuid.uuid4()

    @staticmethod
    def _get_midway_coords(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
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

    def _generate_steps(self) -> Tuple[list, list]:
        """
         Ingest the gpx file and create the lists of coordinates and time needed to wait between each
         point for the given speed

        Returns
        -------
            Tuple[list, list]
        """
        gpx_file = open(self.filename, 'r')
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        waits = []
        pnt = 0
        while pnt < len(points) - 1:
            pnt_1 = pnt + 1
            dst = geopy.distance.distance(points[pnt], points[pnt_1]).km
            time_seconds = (dst / self.speed_kph) * 60 * 60
            if time_seconds > self.max_time_step_secs:
                points.insert(pnt_1, self._get_midway_coords(points[pnt][0], points[pnt][1], points[pnt_1][0], points[pnt_1][1]))
            else:
                waits.insert(pnt, time_seconds)
                pnt += 1
        return points, waits

    def play_gpx(self) -> None:
        """
        Start playing the gpx file into tak
        """
        takserver = takcot()
        takserver.open(self.tak_server, self.tak_port)
        points, waits = self._generate_steps()
        locator = 0
        takserver.flush()
        for location in points:
            takserver.send(mkcot.mkcot(cot_identity="friend",
                                       cot_stale=1,
                                       cot_dimension="land-unit",
                                       cot_typesuffix=str(self.cot_type),
                                       cot_callsign=str(self.callsign),
                                       cot_id=str(self.uid),
                                       cot_lat=round(location[0], 5), cot_lon=round(location[1], 5)))
            takserver.flush()
            try:
                time.sleep(waits[locator])
            except(IndexError):
                continue
            locator += 1
        takserver.close()
