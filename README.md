# FreeTAKServer-Simulator
Tool for Simulating Users in ATAK

This tool currently will take a gpx file you have generated of a route and "play" it into ATAK. 
Taking the data in from the gpx file and filling in gaps where there may not be any location data between 2 points to allow 
for fluid movement in ATAK at a given speed. 

## Example

```
from ftssim import gpx

player = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Walk", speed_kph=5, max_time_step_secs=4)
player.play_gpx()
```
Refer to test.py for an example of playing multiple routes back at the same time


For en example, go [here]("https://github.com/lennisthemenace/FreeTAKServer-Simulator-UI-Example")
