from ftssim import gpx
from threading import Thread

player = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Walk", speed_kph=5, max_time_step_secs=4)
player2 = gpx.GpxPlayer('192.168.3.2', 'test.gpx', "A2_Walk", speed_kph=5, max_time_step_secs=4, repeated_objects=5)


t1 = Thread(target=player.play_gpx)
t2 = Thread(target=player2.play_gpx)

t1.start()
t2.start()
player2.play_gpx_multiple()