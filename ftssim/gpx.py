import gpxpy.gpx
import geopy.distance
import time
from takpak.takcot import takcot
from takpak.mkcot import mkcot
import uuid


class GpxPlayer:
    def __init__(self, tak_server, filename, callsign, tak_port=8087, speed_kph=5, max_time_step_secs=4, cot_type="a-f-G-U-C"):
        self.filename = filename
        self.callsign = callsign
        self.tak_port = tak_port
        self.tak_server = tak_server
        self.cot_type = cot_type
        self.speed_kph = speed_kph
        self.max_time_step_secs = max_time_step_secs
        self.uid = uuid.uuid4()

    @staticmethod
    def get_midway_coords(lat1, lon1, lat2, lon2):
        midlat = (lat1 + lat2) / 2
        midlong = (lon1 + lon2) / 2
        return midlat, midlong

    def generate_steps(self):
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
                points.insert(pnt_1, self.get_midway_coords(points[pnt][0], points[pnt][1], points[pnt_1][0], points[pnt_1][1]))
            else:
                waits.insert(pnt, time_seconds)
                pnt += 1
        return points, waits

    def play_gpx(self, ):
        takserver = takcot()
        takserver.open(self.tak_server, self.tak_port)
        points, waits = self.generate_steps()
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
