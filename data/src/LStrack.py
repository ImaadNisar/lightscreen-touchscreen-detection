import math  # used to calculate max distance between points
from cv2 import warpPerspective  # used in warping image
from LScalibrate import warpImage  # used to warp image
import cv2
from ast import literal_eval  # gets settings from file and gets literal type from str type
import numpy as np
import mouse  # used to control mouse (dragging and drawing)
from playsound import playsound  # used for ping sound when changing modes
from threading import Thread  # used to thread playsound

def start(root, pointsstr, maskparamsmalformed, width, height):
    # gets literal vals from str
    points = literal_eval(pointsstr)
    maskparamsstr = ''.join([letter for letter in maskparamsmalformed if letter not in("array()")])
    maskparams = literal_eval(maskparamsstr)

    lower, upper = np.array(maskparams[0]), np.array(maskparams[1])
    
    root.withdraw()

    cap = cv2.VideoCapture(0)
    cap.set(15, -5) #  may have to change the 2nd arg. Only supported for some cameras. Testing with droidcam therefore cannot use this myself
    mat = warpImage(cap, points)  # creates warped image 
    hold = []  # list of points to detect when held
    count = 0
    drawmode = False 
    previous = None 

    while True:
        check, frame = cap.read()
        if not check:
            break
        # generates image from mask

        frame = warpPerspective(frame, mat, (1000, 1000)) 
        hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskedimg = cv2.inRange(hsvimg, lower, upper)
        image = cv2.bitwise_and(frame, frame, mask=maskedimg)


        # gets points >
        contours, rel = cv2.findContours(maskedimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # gets simple contours
        pts = None
        contourpts = []
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 10:  # gets contour area for large objects on screen
                    x, y, w, h = cv2.boundingRect(contour)
                    x = (x+(x+w))//2
                    y = (y+(y+h))//2
                    
                    pts = (x, y)
                    contourpts.append(pts)

        check = set(contourpts)
        if len(check) > 1:  # confirms points using brightest point detection if multiple contours
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5,5), 0)  # converts to grayscale and gaussian blur to reduce influence of individual pixels
            minv, maxv, minl, maxl = cv2.minMaxLoc(gray)
            pts = maxl  # obtains final points var
        # < gets points  
        
        if not setHold(count, hold, pts):  # adds point tuple to hold list
            count += 1

        if pts is not None:
            if getHold(hold):  # function to see if led being held
                count = 0
                drawmode = changeMode(drawmode)  # function to change input mode

            if drawmode:
                temp = draw(pts, width, height, previous)  # drawmode function
                previous = temp  # sets previous point
            else:
               drag(pts, width, height)  # drag function
        else:  # releases mouse when LED off
            if drawmode: 
                mouse.release("left")
                previous = None
            else:
                mouse.release("left")

        blank = np.ones((300, 300))
        cv2.putText(blank, "Press ESC to quit", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("Lightscreen", blank)
        
        # exits once ESC pressed or close button pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if cv2.getWindowProperty("Lightscreen", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    root.deiconify()


def setHold(count, hold, pts):
    if count < 20:
        hold.append(pts)
        return False
    else:
        hold.append(pts)  # appends latest point and remove oldest point (keeps track of points on latest 20 frames)
        hold.pop(0)
        return True


def getHold(hold):
    if None not in hold and len(hold) == 20:  # detects if LED being held
        res = 0
        for p in hold:
            holdcopy = hold.copy()
            holdcopy.remove(p)
            cur = max([(math.sqrt((p[0]-c[0])**2+(p[1]-c[1])**2)) for c in holdcopy])  # obtains the maximum distance between all points
            if cur > res:
                res = cur
        if res < 5:  # if the maximum distance between points is small, triggers held state. Allows the pen to be slightly moved
            hold.clear()
            return True
    return False


def changeMode(drawmode):
    Thread(target=lambda:sound(drawmode)).start()  # threaded function to allow the points to be updated whilst sound plays
    if drawmode:  # changes the drawmode var
        return False
    else:
        return True
    

def sound(drawmode):
    if drawmode:  # sound played depending on current mode
        playsound("data/sound/dragging.mp3")
    else:
        playsound("data/sound/drawing.mp3")


def drag(pos, w, h):
    # obtains co-ordinates using screen res and current point
    x = (pos[0]/1000)*w 
    y = (pos[1]/1000)*h
    mouse.move(x, y, True)  # moves mouse to new people
    mouse.press("left")  # for drag mode, LMB pressed until LED turns off and is then released 


def draw(pos, w, h, previous):
    x = (pos[0]/1000)*w
    y = (pos[1]/1000)*h
    mouse.move(x, y, True)  # moves mouse to new people

    if previous is not None:
        mouse.drag(previous[0], previous[1], x, y)  # drags the mouse between previous position from last frame and current position
    return (x,y)