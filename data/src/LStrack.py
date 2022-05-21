from cv2 import warpPerspective
from LScalibrate import warpImage
import cv2
from ast import literal_eval
import numpy as np
import mouse

def start(root, pointsstr, maskparamsmalformed, width, height):
    points = literal_eval(pointsstr)
    maskparamsstr = ''.join([letter for letter in maskparamsmalformed if letter not in("array()")])
    maskparams = literal_eval(maskparamsstr)
    lower, upper = np.array(maskparams[0]), np.array(maskparams[1])
    
    root.withdraw()

    cap = cv2.VideoCapture(0)
    cap.set(15, 3) #  may have to change the 2nd arg. Only supported for some cameras. Testing with droidcam therefore cannot use this myself
    mat = warpImage(cap, points)
    while True:
        check, frame = cap.read()
        if not check:
            break
        
        
        frame = warpPerspective(frame, mat, (1000, 1000))

        hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskedimg = cv2.inRange(hsvimg, lower, upper)
        image = cv2.bitwise_and(frame, frame, mask=maskedimg)

        contours, rel = cv2.findContours(maskedimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        pts = None
        

        contourpts = []
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 10:
                    x, y, w, h = cv2.boundingRect(contour)
                    x = (x+(x+w))//2
                    y = (y+(y+h))//2
                    
                    pts = (x, y)
                    contourpts.append(pts)

        
        check = set(contourpts)
        if len(check) > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5,5), 0)
            minv, maxv, minl, maxl = cv2.minMaxLoc(gray)
            pts = maxl
        



        if pts is not None:
            controlCursor(pts, width, height)
            cv2.circle(frame, pts, 3, (0, 0, 255), -1)
        else:
            mouse.release("left")

        cv2.imshow("win", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    
    cap.release()
    cv2.destroyAllWindows()
    root.deiconify()


def minContour(contours):
    return sorted(contours, key=cv2.contourArea, reverse=False)[0]

def controlCursor(pos, w, h):
    print(pos)
    print(w, h)
    x = (pos[0]/1000)*w
    y = (pos[1]/1000)*h
    print(x, y)
    mouse.move(x, y, True)
    mouse.press("left")