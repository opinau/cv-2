# imports
import cv2
import numpy as np;


# Apply identity kernel
kernel1 = np.array([[1, 0, -1],
                    [1, 0, -1],
                    [1, 0, -1]])

kernel = np.ones((3,3),np.uint8)

fill_top_level=100

# Read image
image = cv2.imread('diff_16.bmp', cv2.IMREAD_GRAYSCALE)
maska=cv2.imread('maska.bmp', cv2.IMREAD_GRAYSCALE)
_, maska = cv2.threshold(maska, 64, 255, cv2.THRESH_BINARY)

cv2.imshow('base',image)

image= cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)
_, image = cv2.threshold(image, 64, 255, cv2.THRESH_BINARY)

image=cv2.bitwise_and(image, maska)

image = cv2.dilate(image,kernel,iterations = 2)
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Find the index of the largest contour
#areas = [cv2.contourArea(c) for c in contours]

x_max,h_max,w_max,cont_area=320,0,0,0
x_top,w_top=320,0
contours_counter=0
for c in contours:

    #max_index = np.argmax(areas)
    #cnt=contours[max_index]
    #print(cv2.contourArea(c))
    message=""

    if cv2.contourArea(c)>80:
        contours_counter+=1 #increment contours by one
        x,y,w,h = cv2.boundingRect(c)
        if cv2.contourArea(c)>cont_area:
            x_max=x
            w_max=w
            h_max=h
        if x<x_top:
            x_top=x
            w_top=w
        #print(x,y,w,h, cv2.contourArea(c))


    #print(contours)
    #image = cv2.drawContours(image, contours, -1, (255, 255, 0), 2)
        image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0,),2)

#image = cv2.line(image,(x_max+h_max-5,1),(x_max+h_max-5,320),(255,255,0,),2)
if contours_counter==1:
    if h_max/w_max>1.5: #class 1
        fill_level_px=x_max+int(w_max/2)-fill_top_level
        message="<{},{},{},{}>".format(1,fill_level_px,x_max,w_max)
        image = cv2.line(image,(x_max+int(w_max/2),1),(x_max+int(w_max/2),320),(255,255,0,),2)
    else:
        fill_level_px=(x_max+3)-fill_top_level
        message="<{},{},{},{}>".format(2,fill_level_px,x_max,w_max)
        image = cv2.line(image,(x_max+3,1),(x_max+3,320),(255,255,0,),2)
elif contours_counter>1:
    fill_level_px=(x_top-3)-fill_top_level
    message="<{},{},{},{}>".format(3,fill_level_px,x_top,w_top)
    image = cv2.line(image,(x_top+3,1),(x_top+3,320),(255,255,0,),2)
else:
    message="<{},{},{},{}>".format(0,0,0,0)

print(message)

cv2.imshow('Slika',image)
cv2.waitKey(0)