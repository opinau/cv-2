# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time

#some imports libraries etc.
from pyb import Pin #use hardware inputs / outputs
from pyb import LED #use bult-in LED

pin3 = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE) #output, to LED diffuser (MOSFET)

user_exposure_time=5000

sensor.reset() # Initialize the camera sensor
sensor.set_pixformat(sensor.GRAYSCALE) # set camera format to grayscale (color not important in this example)
sensor.set_framesize(sensor.QVGA) # set camera resolution to QVGA 320 x 240
sensor.set_auto_exposure(False, exposure_us=user_exposure_time) # set exposure time, user changable (user_exposure_time variable)
sensor.set_auto_gain(False,gain_db=22) #set camera gain, keep it as this value is optimised for given light source and exposure time

#these setting are manually set in order to prevent camera to change it during use (no automatic setting in machine vision!)
sensor.set_brightness(3) #set camera brightness #2
sensor.set_contrast(3) #set camera contrast #3
#sensor.set_saturation(-3) #set camera saturation
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    vrime=time.ticks_ms()
    img = sensor.snapshot()         # Take a picture and return the image.
    print("razlika je "+str(time.ticks_ms()-vrime))

    img.draw_rectangle(70, 100, 30, 60, color = (255, 255, 255), thickness = 2, fill = False)
    img.draw_line(85, 110, 85, 150, color = (255, 255, 255), thickness = 2)


    img.draw_line(100, 105, 250, 90, color = (255, 255, 255), thickness = 2)
    img.draw_line(250, 90,300,60, color = (255, 255, 255), thickness = 2)
    img.draw_line(300, 60,320,55, color = (255, 255, 255), thickness = 2)

    img.draw_line(100,155, 250, 170, color = (255, 255, 255), thickness = 2)
    img.draw_line(250, 170,300,200, color = (255, 255, 255), thickness = 2)
    img.draw_line(300, 200,320,205, color = (255, 255, 255), thickness = 2)


    #definiranje maske
    img.draw_line(102, 107, 250,92, color = (255, 255, 255), thickness = 1)
    img.draw_line(250, 92,250,166, color = (255, 255, 255), thickness = 1)

    img.draw_line(250,166, 102, 152, color = (255, 255, 255), thickness = 1)
    img.draw_line(102, 152,102,107, color = (255, 255, 255), thickness = 2)

    img.draw_circle(260,130,25,color = (255, 255, 255), thickness = 1, fill = False)



    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
    pin3.value(True)
