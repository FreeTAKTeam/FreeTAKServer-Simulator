from ftssim import gpx
from threading import Thread

player = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Walk", speed_kph=5, max_time_step_secs=4)
player2 = gpx.GpxPlayer('192.168.3.2', 'test.gpx', "A2_Walk", speed_kph=5, max_time_step_secs=4)
player3 = gpx.GpxPlayer('192.168.3.2', 'test.gpx', "A2_Jog", speed_kph=10, max_time_step_secs=4)
player4 = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Jog", speed_kph=10, max_time_step_secs=4)

t1 = Thread(target=player.play_gpx)
t2 = Thread(target=player2.play_gpx)
t3 = Thread(target=player3.play_gpx)
t4 = Thread(target=player4.play_gpx)

t1.start()
t4.start()
t2.start()
t3.start()
