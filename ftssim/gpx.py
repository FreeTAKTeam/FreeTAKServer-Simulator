import gpxpy.gpx
import uuid
from typing import Tuple
from ftssim import _common


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
        self.uid = str(uuid.uuid4())

    def _generate_steps_from_gpx(self) -> Tuple[list, list]:
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
        return _common.generate_smooth_route(points, self.speed_kph, self.max_time_step_secs)

    def play_gpx(self) -> None:
        """
        Start playing the gpx file into tak
        """
        points, waits = self._generate_steps_from_gpx()
        _common.iterate_and_send(points, waits, self.tak_server, self.tak_port, self.cot_type, self.callsign, self.uid)
