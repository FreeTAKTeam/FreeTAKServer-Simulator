from ftssim import wander
from threading import Thread

wanderer = wander.Wander('192.168.3.2', total_distance_km=1, distance_between_change=1, callsign="lost_soul",
                         speed_kph=120, max_time_step_secs=5, start_lat=38.897125, start_lon=-77.036255)
wanderer1 = wander.Wander('192.168.3.2', total_distance_km=2, distance_between_change=1, callsign="lost_soul_1",
                          speed_kph=5, max_time_step_secs=5, start_lat=38.897125, start_lon=-77.036255)

# Setup A thread for each wanderer
wanderer_tread = Thread(target=wanderer.start_wandering)
wanderer1_thread = Thread(target=wanderer1.start_wandering)

# Start each thread
wanderer_tread.start()
wanderer1_thread.start()


def print_info(wnd, thread):
    print(f"""
    _________________________________________________
    + {wnd.callsign} is Running + 
    + Process ID: {thread.native_id} + 
    + UID: {wnd.uid} + 
    + Server: {wnd.tak_server}:{wnd.tak_port} + 
    + Total Distance: {wnd.total_distance_km}Km +  
    + Distance Between Direction Change: {wnd.distance_between_change}Km + 
    + Speed: {wnd.speed_kph}Kph + 
    _________________________________________________""")


# Print out to the terminal useful information about wanderer
print_info(wanderer, wanderer_tread)
print_info(wanderer1, wanderer1_thread)
