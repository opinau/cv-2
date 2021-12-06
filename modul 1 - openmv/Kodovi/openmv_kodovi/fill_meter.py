#*****************************************
# Fluid fill level sensor, based on machine vision
# Project uses OpenCV H7plus camera + 20W LED
# Created by FESB CV team || 11. 2021.
# istancic@fesb.hr jmusic@fesb.hr
# Project Opinau-Filler-CV-2
#*****************************************

#basic definitons, iports, etc.

#some imports libraries etc.
import sensor, image, time, lcd #basic libraries
from pyb import Pin #use hardware inputs / outputs
from pyb import LED #use bult-in LED
from pyb import UART  #enables use of hardware serial (UART)


#Built in LED definitions, used for fill status indication
red_led   = LED(1) # red led- fluid >500ml
green_led = LED(2) # green led - fluid detected, <500 ml
blue_led  = LED(3) # blue led - no fluid detected


#output pin, no pullup
#pin_LED = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE) #output, to LED  (MOSFET)

uart = UART(3, 115200)  #UART pin 4, 9600 baudrate
#uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)


#iput pin,pullup (button or jumper can be connected between pin and GND line)
#setup jumper, connect if allignmet of camera is required (enters setup mode)
pin_setup = Pin('P9', Pin.IN, Pin.PULL_UP) #input - setup jumper


# camera expostion time in ms. keep it between 4000 and 10000 interval
user_exposure_time=4000 #change if bottle type and/or color is changed


#use debug mode for forcing output to IDE, additional delay 500ms per measerement
#debug_mode=True
debug_mode=False

#mv system starts in measurement mode. changes via USART commands
measurement_mode=True


#fill level definitions, user chan change this
fill_top_level=100 #define line which represenst top of the bottle (throat begining)

#please adjust this option to different bottle type
fill_level_px_limit=90 # defines diff in pixels between fill_top_level and current fill level line

#minimal size og blod - detected line, 20 is the default option
min_blob_size=20

#camera sensor setup
sensor.reset() # Initialize the camera sensor
sensor.set_pixformat(sensor.GRAYSCALE) # set camera format to grayscale (color not important in this example)
sensor.set_framesize(sensor.QVGA) # set camera resolution to QVGA 320 x 240
sensor.set_auto_exposure(False, exposure_us=user_exposure_time) # set exposure time, user changable (user_exposure_time variable)
sensor.set_auto_gain(False,gain_db=22) #set camera gain, keep it as this value is optimised for given light source and exposure time
sensor.set_brightness(3) #set camera brightness , range -3 to +3
sensor.set_contrast(3) #set camera contrast , range -3 to +3

#important command! forces camere not to store frames!!
sensor.set_framebuffers(1) #only single frame in buffer!
sensor.skip_frames(time = 2000) #alow some time for camera to initialise
#camera setup is finished


#additional frame buffers
extra_fb = sensor.alloc_extra_fb(320,240, sensor.GRAYSCALE) #for frame diferencing
extra_fb2 = sensor.alloc_extra_fb(120,160, sensor.RGB565) #not used ...
mask = sensor.alloc_extra_fb(320,240, sensor.GRAYSCALE) #mask definition

lcd.init(type=lcd.LCD_SHIELD) # Initialize the lcd screen.


#kernel definitions, object filtering by orientation
kernel_size = 1 # 3x3==1, 5x5==2, 7x7==3, etc. our kernel is size 3x3

#kernel for horizontal camera instalaltion
#kernel = [2, 2,  2, \
          #0, 0,  0, \
           #-1,  -1,  -1]

#kernel for vertical camera installation
kernel = [2, 0,  -1, \
          2, 0,  -1, \
           2,  0,  -1]
#kernel definiton is finished

#threshold defininitions for binarisation. please change lower number if required (20 default)
low_threshold=(20, 255)

#mask definitions, only part of image under mask is considered
#mask is defined by series of simple objects(lines), than area defined by lines is filled
mask.clear() #clear mask, add some lines

mask.draw_line(102, 107, 250,92, color = (255, 255, 255), thickness = 1)
mask.draw_line(250, 92,250,166, color = (255, 255, 255), thickness = 1)

mask.draw_line(250,166, 102, 152, color = (255, 255, 255), thickness = 1)
mask.draw_line(102, 152,102,107, color = (255, 255, 255), thickness = 2)

#mask.draw_circle(260,130,25,color = (255, 255, 255), thickness = 1, fill = False)

mask.flood_fill(190, 120, seed_threshold=0.05, floating_thresholds=0.05,color=(255, 255, 255), invert=False, clear_background=False)
mask.draw_circle(260,130,25,color = (255, 255, 255), thickness = 1, fill = False)
#maska.draw_circle(290,110,25,color = (0, 0, 0), thickness = 1, fill = True)

mask.binary([(20, 255)]) #bynarise mask,
mask.erode(3) #erode mask, small movement or vibrations of bottle can detect false fill level on bottle edges
#eroding the mask can help prevent this
#mask definition is compleete


#setup mode, run if setup jumper is set!
#this allows user to correcty alling bottle
while(pin_setup.value()==False):  #execute while jumper is set
    img = sensor.snapshot() #take single image

    #draw alignmenet lines
    img.draw_rectangle(70, 100, 30, 60, color = (255, 255, 255), thickness = 2, fill = False)
    img.draw_line(85, 110, 85, 150, color = (255, 255, 255), thickness = 2)


    img.draw_line(100, 105, 250, 90, color = (255, 255, 255), thickness = 2)
    img.draw_line(250, 90,300,60, color = (255, 255, 255), thickness = 2)
    img.draw_line(300, 60,320,55, color = (255, 255, 255), thickness = 2)

    img.draw_line(100,155, 250, 170, color = (255, 255, 255), thickness = 2)
    img.draw_line(250, 170,300,200, color = (255, 255, 255), thickness = 2)
    img.draw_line(300, 200,320,205, color = (255, 255, 255), thickness = 2)

    #show image to LCD
    lcd.display(img,x_size=128,y_size=160) # Take a picture and display the image.
    print(img.compress_for_ide(), end="") #force image to IDE
    time.sleep_ms(100) #small delay, fps is reducet to 5
#setup mode is finished
lcd.set_backlight(0)
lcd.clear()
lcd.deinit()
#output pin, no pullup
pin_LED = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE) #output, to LED  (MOSFET)

clock = time.clock()   # Create a clock object to track the FPS.

counter=0 #simple counter

#here goes the main code!



while(True): #execute this loop


   #check for new commands on USART
   # S - start  measurement_mode
   # T - terminate  measurement_mode
   # camera starts with measurement mode
    if uart.any()>0:
        print(uart.any())
        usart_input=uart.readline()
        if usart_input[0]==83:
            measurement_mode=True
        if usart_input[0]==84:
            measurement_mode=False


    if measurement_mode==True:

        #simple snippet to measure time required for block of code, part 1
        timer_ms=time.ticks_ms()

        clock.tick() # Update the FPS clock.

        counter+=1 #increment counter


        pin_LED.value(True) #turn on main LED
        time.sleep_ms(5) #sleep for 5ms (allow LED to reach full brightness)

        #img = sensor.snapshot() #take first image (led is on)
        time.sleep_ms(2)        # wait for a few ms
        extra_fb.replace(sensor.snapshot())   #put first image in to additional frame buffer

        pin_LED.value(False)       #turn off main LED
        time.sleep_ms(5)

        img = sensor.snapshot() #take second image (led is off)
        time.sleep_ms(2)        # wait for a few ms



        #img.lens_corr(1.8) #if required use lens distortion removal. not used

        img.difference(extra_fb) #simple frame differencing, first and second image
        #please note that .difference metod can accpet mask, .b_and method showed to be more efficient!

        img.b_and(mask) # extract ony part defined by the mask (bottle throat)

        #filtering
        #img.gaussian(1) #simple gaussian filter, smoothing

        #kernel filtering ephases vertical objects! (please note that camera is rotated)
        img.morph(kernel_size, kernel) #kernel filter, user defined kernel and kernel size

        img.binary([low_threshold]) #binarise image, user defined low_threshold

        img.close(2) #fill some small holes in binary image


        #defines blob / fill level type
        # 0 no blobs - no fill level detected
        # 1 elongated blob, fluid is steady
        # 2 one large blob, fluid is moving
        # 3 several blobs (foam, large fluid movement)
        level_type=0 #defines fill level blob type, 0-4

        #some definition for detected blobs,used for classification of blobs
        x_top,w_top,h_top=320,0,0  #topmost blob
        x_largest,w_largest,pix_count,h_largest=320,0,0,0 #largest blob
        blob_count=0 #number of blobs (please note that some blobs can be rejected)
        fill_level_px=320 #fill level placeholder, set to max (320px)
        message="" #placeholder for str message send by USART

        #part which detects blob,user can adjust pixels_threshold and area_threshold
        for blob in img.find_blobs([low_threshold], pixels_threshold=min_blob_size, area_threshold=min_blob_size, merge=True, margin=5):

                #used for debuging, print blob info
                #print(blob.rect()) #bllop pos and size
                #print(blob.pixels()) #blob size in pix

                x,y,w,h=blob.rect() #extract blob size features
                img.draw_rectangle(blob.rect()) #draw rectangle around blob

                if h/w>0.8: #accept only vertical blobs (please note camera rotations)
                    blob_count+=1 #blob counter, increment

                    if x<x_top: #replace topmost blob in image if new blob is near top
                        x_top=x
                        w_top=w
                        h_top=h

                    if blob.pixels()>pix_count: #replace largest blob in image, if found
                        pix_count>blob.pixels()
                        x_largest=x
                        w_largest=w
                        h_largest=h


        #fill level classification
        if blob_count==1: #single elongated blob, class 1, no foam. steady fluid
            if h_top/w_top >1.5:
                level_type=1
                fill_level_px=int(x_top+w_top/2)-fill_top_level #fill line is object center
                img.draw_line(fill_level_px+fill_top_level, 10, fill_level_px+fill_top_level, 220, color = (255, 255, 255), thickness = 2)
                message="<{},{},{},{}>".format(level_type,fill_level_px,x_top,w_top)
            else: #one large blob, class 2, excesive  foam
                level_type=2
                fill_level_px=int(x_top+3)-fill_top_level #fill line is top level -3px, due to dilatation
                img.draw_line(fill_level_px+fill_top_level, 10, fill_level_px+fill_top_level, 220, color = (255, 255, 255), thickness = 2)
                message="<{},{},{},{}>".format(level_type,fill_level_px,x_top,w_top)
        elif blob_count>1:
            level_type=3 #several blobs, fill line is the topmost blob - 3px due to dilatation
            fill_level_px=int(x_top+3)-fill_top_level #fill line is top level -3px, due to dilatation
            img.draw_line(fill_level_px+fill_top_level, 10, fill_level_px+fill_top_level, 220, color = (255, 255, 255), thickness = 2)
            message="<{},{},{},{}>".format(level_type,fill_level_px,x_top,w_top)
        else: #no blobs detected, all zeros printed / sent to USART
            level_type=0
            message="<{},{},{},{}>".format(level_type,0,0,0)
        #fill level clasiification is compleete

        #check if fill level reached 500 ml - defined by pixel size
        #if >500 ml turn on RED LED
        if fill_level_px<fill_level_px_limit and blob_count>0:
            red_led.on()
            green_led.off()
            blue_led.off()
        elif fill_level_px>=fill_level_px_limit and blob_count>0:
            red_led.off()
            green_led.on()
            blue_led.off()
        else:
            red_led.off()
            green_led.off()
            blue_led.on() #else turn on blue led (idle status

        #preparing message to UART
        print(message) #print prepared message

        #write message to uart
        uart.write(message+"\n")

        #send message to USART

        #if debug mode is enabled, current image is forced to IDEm additional 500ms delay
        #please note that fps drops (due to additional delay)
        if debug_mode==True:
            print(img.compress_for_ide(), end="") #force image to IDE
            time.sleep_ms(500) #delay, allow enaugh time to display image on IDE


        print("current fps: "+str(clock.fps())) #print current fps


        #simple snippet to measure time required for block of code, part 2
        print("time difference "+str(time.ticks_ms()-timer_ms))

        #due to occupation P1 to MISO line, LCD and LED cannot be used at the same time.
        #LCD shield does not use P1 pin (issue that has to br resolved with fimware update)
        #constant init and deinit of LCD may drastically lower FPS
        #when this issue is resolved, you can uncomment those lines
        ##draw new image on LCD every 10th frame

        #if counter%10==0:
            ##crtanje boce
            #extra_fb2.clear()
            #extra_fb2.draw_line(120, 100, 120, 140, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(120, 100, 60, 100, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(120, 140, 60, 140, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(60, 140,40,130, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(40,130,10,127, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(60, 100,40,110, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_line(40,110,10,112, color = (0, 255, 0), thickness = 2)
            #extra_fb2.draw_rectangle(2,110,8,20, color = (0, 255, 0), thickness = 2)

            ##filling line display
            #if fill_level_px<40:
                #extra_fb2.draw_line(20,128,20,112, color = (0, 255, 0), thickness = 1)
                #extra_fb2.flood_fill(110, 110, seed_threshold=0.05, floating_thresholds=0.05,color=(0, 20, 255), invert=False, clear_background=False)

            #elif fill_level_px<125:
                #extra_fb2.draw_line(30,128,30,112, color = (0, 255, 0), thickness = 1)
                #extra_fb2.flood_fill(110, 110, seed_threshold=0.05, floating_thresholds=0.05,color=(0, 20, 255), invert=False, clear_background=False)

            #elif fill_level_px<140:
                #extra_fb2.draw_line(40,130,40,110, color = (0, 255, 0), thickness = 1)
                #extra_fb2.flood_fill(110, 110, seed_threshold=0.05, floating_thresholds=0.05,color=(0, 20, 255), invert=False, clear_background=False)

            #elif counter%20==0:
                #extra_fb2.draw_line(60, 100,60, 140, color = (0, 255, 0), thickness = 1)
                #extra_fb2.flood_fill(110, 110, seed_threshold=0.05, floating_thresholds=0.05,color=(0, 20, 255), invert=False, clear_background=False)



            #extra_fb2.draw_string(10, 90, "fill_px="+str(fill_level_px), color = (10, 255, 0), scale = 2, mono_space = False,
                                #char_rotation = 0, char_hmirror = False, char_vflip = False,
                                #string_rotation = 270, string_hmirror = False, string_vflip = False)

            #lcd.display(extra_fb2)#),x_size=128,y_size=160) # Take a picture and display the image.
    else:
        img = sensor.snapshot()

    #code is now finisehd!

