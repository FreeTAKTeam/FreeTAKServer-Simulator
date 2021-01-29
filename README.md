# FreeTAKServer-Simulator
Tool for Simulating moving objects in ATAK

### GPX
This tool currently will take a gpx file you have generated of a route and "play" it into ATAK. 
Taking the data in from the gpx file and filling in gaps where there may not be any location data between 2 points to allow 
for fluid movement in ATAK at a given speed.

#### Example
```python
from ftssim import gpx

player = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Walk", speed_kph=5, max_time_step_secs=4)
player.play_gpx()
```


### Wandering
Given a starting point and a few extra parameters this tool will make an object wander aimlessly 
in straigt lines then change direction (if you want to have an object just head in one straight line
set total_distance and distance_between_change to the same number)

#### Example
```python
wanderer = wander.Wander('192.168.3.2', total_distance_km=2, distance_between_change=1, callsign="lost_soul", speed_kph=5,
                         max_time_step_secs=4, start_lat=38.897125, start_lon=-77.036255)
```


Refer to gpx_example.py and wander_example.py for examples of running concurrently 


For an example, go [here](https://github.com/lennisthemenace/FreeTAKServer-Simulator-UI-Example)
