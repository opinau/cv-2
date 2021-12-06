# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, os

#some imports libraries etc.
from pyb import Pin #use hardware inputs / outputs
from pyb import LED #use bult-in LED

pin3 = Pin('P4', Pin.OUT_PP, Pin.PULL_NONE) #output, to LED diffuser (MOSFET)

min_degree = 80
max_degree = 100

user_exposure_time=10000

sensor.reset() # Initialize the camera sensor
sensor.set_pixformat(sensor.GRAYSCALE) # set camera format to grayscale (color not important in this example)
sensor.set_framesize(sensor.QVGA) # set camera resolution to QVGA 320 x 240
sensor.set_auto_exposure(False, exposure_us=user_exposure_time) # set exposure time, user changable (user_exposure_time variable)
sensor.set_auto_gain(False,gain_db=22) #set camera gain, keep it as this value is optimised for given light source and exposure time

#these setting are manually set in order to prevent camera to change it during use (no automatic setting in machine vision!)
sensor.set_brightness(3) #set camera brightness #2
sensor.set_contrast(3) #set camera contrast #3
#sensor.set_saturation(-3) #set camera saturation

extra_fb = sensor.alloc_extra_fb(320,240, sensor.GRAYSCALE)
#extra_fb2 = sensor.alloc_extra_fb(320,240, sensor.GRAYSCALE)
#extra_fb2 = sensor.alloc_extra_fb(640,480, sensor.GRAYSCALE)

kernel_size = 1 # 3x3==1, 5x5==2, 7x7==3, etc.
kernel = [2, 2,  2, \
          0, 0,  0, \
           -1,  -1,  -1]

sensor.set_framebuffers(1)

sensor.skip_frames(time = 2000)


#clock = time.clock()                # Create a clock object to track the FPS.

counter_img=0

if not "images" in os.listdir(): os.mkdir("images") # Make a temp directory

while(True):
    #clock.tick()                    # Update the FPS clock.
    pin3.value(1)
    time.sleep_ms(10)
    img = sensor.snapshot()         # Take a picture and return the image.
    #sensor.skip_frames(1)
    time.sleep_ms(2)
    #img.lens_corr(1.8)
    extra_fb.replace(img)

   #sensor.flush()
    pin3.value(0)
    time.sleep_ms(10)
    img = sensor.snapshot()
    time.sleep_ms(2)
    #img.lens_corr(1.8)
    counter_img+=1

    newName1='slika_'+str(counter_img)+"_on.bmp"
    newName2='slika_'+str(counter_img)+"_off.bmp"

    extra_fb.save('images/' + newName1)
    img.save('images/' + newName2)



    time.sleep_ms(2)
    #img.laplacian(1)
    #img.find_edges(image.EDGE_CANNY, threshold=(100, 255))
    #for l in img.find_lines(threshold = 5, theta_margin = 25, rho_margin = 25):
        #if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            #img.draw_line(l.line(), color = (255, 0, 0))
            #print(l)
    print(img.compress_for_ide(), end="")
    time.sleep_ms(50)
    #time.sleep_ms(500)
   # print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
