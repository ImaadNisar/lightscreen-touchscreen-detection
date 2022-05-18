from cv2 import warpPerspective
from LScalibratepoints import warpImage
import cv2
from ast import literal_eval
import numpy as np
import mouse
import LSsharedmodules
from threading import Thread

def start(root, pointsstr, maskparamsmalformed, w, h):
    points = literal_eval(pointsstr)
    maskparamsstr = ''.join([letter for letter in maskparamsmalformed if letter not in("array()")])
    maskparams = literal_eval(maskparamsstr)
    lower, upper = np.array(maskparams[0]), np.array(maskparams[1])
    
    

    cap = cv2.VideoCapture(0)
    cap.set(15, 2) #  may have to change the 2nd arg. Only supported for some cameras. Testing with droidcam therefore cannot use this myself
    mat = warpImage(cap, points)
    setbrightness = False


    while True:
        check, frame = cap.read()
        if not check:
            break

        
        
        frame = warpPerspective(frame, mat, (1000, 1000))
        hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskedimg = cv2.inRange(hsvimg, lower, upper)
        image = cv2.bitwise_and(frame, frame, mask=maskedimg)


        if not setbrightness:
            max = []
            for i in range(20):
                check, frame = cap.read()
                frame = warpPerspective(frame, mat, (1000, 1000))
                hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                maskedimg = cv2.inRange(hsvimg, lower, upper)
                image = cv2.bitwise_and(frame, frame, mask=maskedimg)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (5,5), 0)
                minv, maxv, minl, maxl = cv2.minMaxLoc(gray)
                max.append(maxv)
            avgmax = sum(max)//len(max)
            

            setbrightness = True

        """contours, rel = cv2.findContours(maskedimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # optional method of tracking (not as good when testing)

        if len(contours) != 0:
            contour = minContour(contours)
            if cv2.contourArea(contour) > 10:
                x, y, w, h = cv2.boundingRect(contour)
                x = (x+(x+w))//2
                y = (y+(y+h))//2
                cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
                print(x, y)
                print(x, y)"""


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        minv, maxv, minl, maxl = cv2.minMaxLoc(gray)

        if maxv > 50:  # change val
            controlCursor(maxl, w, h)

    
    cap.release()
    cv2.destroyAllWindows()
    root.deiconify()


def minContour(contours):
    return sorted(contours, key=cv2.contourArea, reverse=False)[0]

def controlCursor(pos, w, h):
    x = (pos[0]/1000)*w
    y = (pos[1]/1000)*h
    mouse.move(x, y, True)
