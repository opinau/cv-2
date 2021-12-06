#*****************************************
# Fluid fill level sensor, based on machine vision
# This verion uses RPi4B + CAM + 20W LED
# Created by FESB CV team || 11. 2021.
# istancic@fesb.hr jmusic@fesb.hr
# Project Opinau-Filler-CV-2
#*****************************************

#basic definitons, iports, etc.

#some imports libraries etc.
import arducam_mipicamera as arducam
import v4l2 #sudo pip install v4l2, camera driver
import time
import cv2 #sudo apt-get install python-opencv
import numpy as np;
from gpiozero import LED

#output pin to LED
red = LED(17)

# identity kernel  for filtering, for vertical camera installation
kernel1 = np.array([[1, 0, -1],
                    [1, 0, -1],
                    [1, 0, -1]])
#kernel for dilatation
kernel = np.ones((3,3),np.uint8)

#definition of top fill level in pixels - please change!
fill_top_level=100

#mv system starts in measurement mode. 
#changes via keypress
#s - start measurement and report
#t - terminate measurement and reporting
measurement_mode=True

#mask definitions, only part of image under mask is considered
#mask is prepared as bmp image 
maska=cv2.imread('maska_rpi.bmp', cv2.IMREAD_GRAYSCALE)
_, maska = cv2.threshold(maska, 64, 255, cv2.THRESH_BINARY)

#commands for basic camera operations
def align_down(size, align):
    return (size & ~((align)-1))

def align_up(size, align):
    return align_down(size + align - 1, align)

def set_controls(camera):
    try:
        print("Reset the focus...")
        camera.reset_control(V4L2_AUTO_FOCUS_RANGE_MACRO)
        camera.set_control(V4L2_CID_EXPOSURE_ABSOLUTE, 100)
    except Exception as e:
        print(e)
        print("The camera may not support this control.")

    try:
        print("Enable Auto Exposure...")
        #camera.software_auto_exposure(enable = True)
        print("Enable Auto White Balance...")
        camera.software_auto_white_balance(enable = False)
    except Exception as e:
        print(e)
#end of commands for basic camera operations

#main loop
if __name__ == "__main__":
    try:
        camera = arducam.mipi_camera()
        print("Open camera...")
        camera.init_camera() #starting the camera
        print("Setting the resolution...")
        fmt = camera.set_resolution(640,480) #low resolution for faster operation
        print("Current resolution is {}".format(fmt))
        set_controls(camera)
		
        while True: #loop until q key is presses
            
            
            start=time.time() #record current time, for FPS calculation
            
            keypress=cv2.waitKey(1)    #wait for input key
            if keypress & 0xFF == ord('s'): #start measurement mode
                    measurement_mode=True
            elif keypress & 0xFF == ord('t'): #terminate measurement mode
                    measurement_mode=False
            elif keypress & 0xFF == ord('q'): #quit main loop
                    break
                    
            if measurement_mode==True: #execute if set to measurement mode    
                
                red.on() #turn on LED
                time.sleep(0.005) #wait for 50ms 
                frame1 = camera.capture(encoding = 'i420') #capture  firstimage
                time.sleep(0.002) #wait for 2ms 
                red.off() #turn off LED
                time.sleep(0.012) #wait for 12ms 
                frame2 = camera.capture(encoding = 'i420') #capture second image
                
                image1 = frame1.as_array.reshape(600, 640) #decode fist image
                image1 = cv2.cvtColor(image1, cv2.COLOR_YUV2GRAY_I420) #convert to grayscale
                
                image2 = frame2.as_array.reshape(600, 640) #decode second image
                image2 = cv2.cvtColor(image2, cv2.COLOR_YUV2GRAY_I420) #convert to grayscale
                
                image=cv2.absdiff(image1,image2) #absoule diff of both images
                
                image= cv2.filter2D(src=image, ddepth=-1, kernel=kernel1) #kernel filtering, keep only verical lines (camera is roatated)
                _, image = cv2.threshold(image, 64, 255, cv2.THRESH_BINARY) #create binary image
                
                image=cv2.bitwise_and(image, maska) #mask operation, keep only are under mask

                image = cv2.dilate(image,kernel,iterations = 2) #dilatation, to connect if blob is separated on several close blobs
                image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel) #close some holes in blob

                contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find contours in binaryimage
                
                x_max,h_max,w_max,cont_area=320,0,0,0  #to keep location and info for largest blob/ contour
                
                x_top,w_top=320,0 #to keep location and info for topmost blob
                contours_counter=0  #contours counter
                for c in contours: #for loop, check all contours

                    message="" #message placeholder, 

                    if cv2.contourArea(c)>80: #check only contours larger than 80 pix
                        contours_counter+=1 #increment contours by one
                        x,y,w,h = cv2.boundingRect(c) #extract contour size info
                        if cv2.contourArea(c)>cont_area: #if area of courrently largest
                            x_max=x  #record cuurently largest contour info
                            w_max=w
                            h_max=h
							
                        if x<x_top: #if current contour is topomost (closest to bottle throat)
                            x_top=x #record cuurently topmost contour info
                            w_top=w
                        
						#drav rectange on image around contours
                        image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0,),2)
                
                #preparing message  -> to ROS or other
				#currently message is printed to serial console
				
                if contours_counter==1: #if number of conturs is one!
                    if h_max/w_max>1.5: #single elongated blob, class 1, no foam. steady fluid
                        fill_level_px=x_max+int(w_max/2)-fill_top_level
                        message="<{},{},{},{}>".format(1,fill_level_px,x_max,w_max)
                        image = cv2.line(image,(x_max+int(w_max/2),1),(x_max+int(w_max/2),320),(255,255,0,),2)
                    else: #one large blob, class 2, excesive  foam 
                        fill_level_px=(x_max+3)-fill_top_level
                        message="<{},{},{},{}>".format(2,fill_level_px,x_max,w_max)
                        image = cv2.line(image,(x_max+3,1),(x_max+3,320),(255,255,0,),2)
                elif contours_counter>1: #several blobs, fill line is the topmost blob - 3px due to dilatation
                    fill_level_px=(x_top-3)-fill_top_level
                    message="<{},{},{},{}>".format(3,fill_level_px,x_top,w_top)
                    image = cv2.line(image,(x_top+3,1),(x_top+3,320),(255,255,0,),2)
                else: #no blobs detected, all zeros printed / sent to USART
                    message="<{},{},{},{}>".format(0,0,0,0)

                print(message) #printig current message
                
				#adding line for bottle alignment , fist image
				#user may change line location according to bottle type
				#in that scenario, mask should also be changed
                image1 = cv2.line(image1,(180,160),(435,125),(255,255,0,),2)
                image1 = cv2.line(image1,(435,125),(500,84),(255,255,0,),2)
                image1 = cv2.line(image1,(180,240),(435,255),(255,255,0,),2)
                image1 = cv2.line(image1,(435,255),(500,300),(255,255,0,),2)

                #rotate image 90 deg (camera is installed vertically)
                image1=cv2.transpose(image1)
                image1=cv2.flip(image1,flipCode=1)
                #rotate image 90 deg (camera is installed vertically)
                image2=cv2.transpose(image2)
                image2=cv2.flip(image2,flipCode=1)
                #rotate image 90 deg (camera is installed vertically)
                image=cv2.transpose(image)
                image=cv2.flip(image,flipCode=1)
                #concatenate all three images in one
                image=np.concatenate((image1, image2,image), axis=1)
                
                #calculate current FPS
                fps=1/(time.time()-start)
                fps_str="FPS:{0:.1f}".format(fps) #prepare string message
                image = cv2.putText(image, fps_str, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 2, cv2.LINE_AA) #print current FPS on image
                
                image = cv2.putText(image, message, (820,600), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 2, cv2.LINE_AA) #print current message to last image
                #image=cv2.resize(image, (800,480), interpolation = cv2.INTER_AREA) #resize for small LCD screen

                cv2.imshow("Filler", image) #show image

            else: #if not in measurement mode
                frame1 = camera.capture(encoding = 'i420') #capture  firstimage
                image1 = frame1.as_array.reshape(600, 640) #decode fist image
                image1 = cv2.cvtColor(image1, cv2.COLOR_YUV2GRAY_I420) #convert to grayscale
				#rotate image 90 deg (camera is installed vertically)
                image1=cv2.transpose(image1)
                image1=cv2.flip(image1,flipCode=1)
				#concatenate two same images into one, no reason :)
                image1=np.concatenate((image1, image1), axis=1)
				#resize for small LCD screen
                #image1=cv2.resize(image1, (800,480), interpolation = cv2.INTER_AREA)
                cv2.imshow("Filler", image1) #show image
            


        # Release memory
        del frame1
        del frame2
        print("Close camera...")
        cv2.imwrite("last_frame.jpg",image) #record last image into jpg file
        camera.close_camera() #close camera
        cv2.destroyAllWindows() #close all windows
		
    except Exception as e: #print if some exceptation occurs
        print(e)

