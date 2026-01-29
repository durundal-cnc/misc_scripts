# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:47:10 2022

@author: AndrewMiller
"""

#%% serial writer 

import serial
import time

serialPort = serial.Serial(
    port="COM15", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
serialString = ""  # Used to hold data coming over UART
serialPort.write(b"IP\r\n")
serialPort.write(b"PSN\r\n")


while 1:
    # Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        try:
            print(serialString.decode("Ascii"))
        except:
            pass
        
#%%
        
        
# Import the OpenDMX or uDMX controller from PyDMXControl,
#  this will be how the data is outputted.
#from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.controllers import SerialController

# from PyDMXControl.controllers import uDMXController

# Import the fixture profile we will use,
#  the simple Dimmer in this example.
from PyDMXControl.profiles.Generic import Dimmer

# Create an instance of the uDMX controller, 
#  this holds all the fixture information and outputs it.
# This will start outputting data immediately.
#dmx = OpenDMXController()
dmx = SerialController(port='COM5')
# dmx = uDMXController()

# Add a new Dimmer fixture to our controller
#  and save it to a variable so we can access it.
# We give it a name so it's easier to identify in the debug control options.
fixture = dmx.add_fixture(Dimmer, name="My_First_Dimmer")

# Next, dim the intensity of the fixture from it's initial value of zero
#  to full, which is represented as 255 in DMX.
# This is done over 5000 milliseconds, or 5 seconds.
fixture.dim(255, 5000)
fixture.dim(0, 5000)
fixture.dim(128, 50000)

import time
i = 0
delay = 3000
while i < 10:
    if i%2 > 0:
        fixture.dim(0, delay)
    else:
        fixture.dim(128, delay)
    i = i + 1
    print(i)
    time.sleep(delay/1000)
    
#fixture.dim(128, delay)
fixture.dim(0, delay)
fixture.dim(48, 0)

    
# We can now start the web control panel built into PyDMXControl.
# This will output the web address in console, but should be http://0.0.0.0:8080
# This runs in the background and so we can continue to do other things still.
# dmx.web_control()

# # The console debug mode can also be started if required,
# #  this provides basic control options in the console of the program.
# # This is blocking however and so the script will not continue past here until
# #  the debug control is exited. This won't stop DMX output.
# dmx.debug_control()

# # Once the console debug mode is exited the script will continue, to stop it
# #  exiting and stopping DMX output when can use a built-in sleep function.
# # This sleep function will wait until enter is pressed in the console before continuing.
# dmx.sleep_till_enter()

# With everything done, you can terminate the DMX output and the program by calling
#  the close method of the controller.
# This will cleanly close any threads in use and stop DMX output.
dmx.close() #this restarts the kernel?


#%% https://github.com/MattIPv4/PyDMXControl/blob/master/tests/home.py
        

from datetime import datetime
from subprocess import run, CalledProcessError
from time import sleep
from typing import List, Dict, Callable

from PyDMXControl import Colors
#from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.controllers import SerialController as Controller
#from PyDMXControl.controllers import OpenDMXController

from PyDMXControl.effects.Color import Color_Chase
from timed_events_data import get_timed_events

# This is my home setup, which also acts as a great demo of some of what this library is capable of doing.
# See the tests directory for other recent/new features that I've possibly been working on.

# Create our controller
dmx = Controller(dynamic_frame=True)

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

# Define some custom colors, a global fade time and the divoom device
custom_blue = [0, 16, 255, 0]
custom_blue_2 = [0, 160, 255, 0]
custom_snow = [32, 48, 255, 0]
custom_cyan = [0, 128, 255, 0]
custom_cyan_2 = [0, 255, 64, 0]
custom_white = [255, 255, int(255 * 0.8), 255]
flood_warm = [255, int(255 * 0.9), int(255 * 0.5), 255]
flood_white = [int(255 * 0.9), 255, 255, 255]
key_white = [int(255 * 0.75), int(255 * 0.9 * 0.75), int(255 * 0.8 * 0.75), 255]
fade_time = 5000
divoom_address = '11:75:58:2D:A8:65'


# Create all the custom state methods

# XMAS state, used throughout the day in December
# Warm shelves + flood, with snowy art/books/board, standard white desk + key
def xmas():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_warm, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Shelf'):
        f.color(Colors.Warm, fade_time)
        f.dim(64, fade_time)

    blue_white_group = dmx.get_fixtures_by_name_include('Art') \
                       + dmx.get_fixtures_by_name_include('Board') \
                       + dmx.get_fixtures_by_name_include('Books') \
                       + dmx.get_fixtures_by_name_include('Shelving')
    Color_Chase.group_apply(blue_white_group, 60 * 1000,
                            colors=[custom_blue, custom_snow, custom_blue, custom_blue])
    for f in blue_white_group:
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)


# Nighttime state, everything off
def night():
    dmx.clear_all_effects()

    for f in dmx.get_all_fixtures():
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    divoom_off()


# Daytime state, used during the day outside December
# White flood + desk + key, no art/shelves/board, blue books
def day():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_white, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    off_group = dmx.get_fixtures_by_name_include('Art') \
                + dmx.get_fixtures_by_name_include('Board') \
                + dmx.get_fixtures_by_name_include('Shelf') \
                + dmx.get_fixtures_by_name_include('Shelving')
    for f in off_group:
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    books = dmx.get_fixtures_by_name_include('Books')
    for f in books:
        f.dim(255, fade_time)

    Color_Chase.group_apply(books, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)

    divoom_on()


# Evening state, used later in the day outside December
# Warm flood, standard white desk + key, blue art/books/board/shelves
def full():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_warm, fade_time)
        f.dim(255, fade_time)

    main_blue_group = dmx.get_fixtures_by_name_include('Art') \
                      + dmx.get_fixtures_by_name_include('Board') \
                      + dmx.get_fixtures_by_name_include('Books') \
                      + dmx.get_fixtures_by_name_include('Shelving')
    for f in main_blue_group:
        f.dim(255, fade_time)

    Color_Chase.group_apply(main_blue_group, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Shelf'):
        f.dim(255, fade_time)

    Color_Chase.group_apply(dmx.get_fixtures_by_name_include('Shelf'), 60 * 1000,
                            colors=[custom_blue_2, custom_blue_2, custom_cyan_2, custom_blue_2])

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)


# Late at night state
# No flood + key, warm desk + art/board/shelves, blue books
def late():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    dim_group = dmx.get_fixtures_by_name_include('Art') \
                + dmx.get_fixtures_by_name_include('Board') \
                + dmx.get_fixtures_by_name_include('Shelf') \
                + dmx.get_fixtures_by_name_include('Shelving')
    for f in dim_group:
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.75), fade_time)

    books = dmx.get_fixtures_by_name_include('Books')
    for f in books:
        f.dim(255, fade_time)

    Color_Chase.group_apply(books, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)


def divoom_off():
    try:
        run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '0'], shell=True)
        sleep(2)
        run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '0'], shell=True)
    except CalledProcessError as e:
        print('Divoom control error:\nExit code: ', e.returncode, '\nOutput: ', e.stderr.decode('utf-8'))


def divoom_on():
    try:
        run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '100'], shell=True)
        sleep(2)
        run(['divoom-control', 'display-custom', '-a', divoom_address], shell=True)
        sleep(2)
        run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '100'], shell=True)
        sleep(2)
        run(['divoom-control', 'display-custom', '-a', divoom_address], shell=True)
    except CalledProcessError as e:
        print('Divoom control error:\nExit code: ', e.returncode, '\nOutput: ', e.stderr.decode('utf-8'))


# Create a time map of states for each day
def get_times() -> List[Dict[int, Callable]]:
    times = [
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Monday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Tuesday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Wednesday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Thursday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Friday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Saturday
        {0: night, 1200: day, 1300: full, 2200: late, 2300: night},  # Sunday
    ]
    # Xmas/jingle jam adjustment
    if datetime.today().month == 12:
        for i in range(len(times)):
            del times[i][1300]
            times[i][1200] = xmas
    return times


last_state = None


# Create the callback to turn lights on/off and change colors at certain times
def callback():
    global last_state

    # Get map for today and current time
    times = get_times()
    time_map = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    # Find most recent passed time in the map
    keys = sorted(time_map.keys())
    index = -1
    while index + 1 < len(keys) and keys[index + 1] <= time:
        index += 1
    state = keys[index]

    # Run the mapped state if not previously run
    run_callback = time_map[state]
    if last_state != run_callback:
        run_callback()
        last_state = run_callback


# Enable the callback
dmx.ticker.add_callback(callback, 500)

# Debug
callbacks = {
    "night": night,
    "day": day,
    "full": full,
    "late": late,
    "xmas": xmas,
    "divoom-off": divoom_off,
    "divoom-on": divoom_on,
}
dmx.web_control(callbacks=callbacks, timed_events={
    "you-will-be-found": get_timed_events(dmx)
})
# dmx.debug_control(callbacks)

# Close the controller once we're done
dmx.sleep_till_interrupt()
dmx.close()