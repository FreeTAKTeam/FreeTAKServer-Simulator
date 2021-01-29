from ftssim import wander
from threading import Thread

wanderer = wander.Wander('192.168.3.2', total_distance_km=2, distance_between_change=1, callsign="lost_soul", speed_kph=40,
                         max_time_step_secs=5, start_lat=38.897125, start_lon=-77.036255)
wanderer1 = wander.Wander('192.168.3.2', total_distance_km=2, distance_between_change=1, callsign="lost_soul_1", speed_kph=5,
                          max_time_step_secs=5, start_lat=38.897125, start_lon=-77.036255)

t1 = Thread(target=wanderer.start_wandering)
t2 = Thread(target=wanderer1.start_wandering)


t1.start()
t2.start()

