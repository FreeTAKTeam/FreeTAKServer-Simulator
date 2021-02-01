from ftssim import gpx
from threading import Thread

player = gpx.GpxPlayer('192.168.3.2', 'test_file.gpx', "A1_Walk", speed_kph=5, max_time_step_secs=4)
player2 = gpx.GpxPlayer('192.168.3.2', 'test.gpx', "A2_Walk", speed_kph=5, max_time_step_secs=4, repeated_objects=5)

# Setup A thread for each player
player_thread = Thread(target=player.play_gpx)
player2_thread = Thread(target=player2.play_gpx)

# Start each thread
player_thread.start()
player2_thread.start()

# Kick off player 2 with its repeated objects
player2.play_gpx_multiple()


def print_info(wnd, thread):
    print(f"""
    _________________________________________________
    + {wnd.callsign} is Running +
    + File: {wnd.filename} + 
    + Process ID: {thread.native_id} + 
    + UID: {wnd.uid} + 
    + Server: {wnd.tak_server}:{wnd.tak_port} + 
    + Speed: {wnd.speed_kph}Kph + 
    _________________________________________________""")

# Print out to the terminal useful information about wanderer
print_info(player, player_thread)
print_info(player2, player2_thread)