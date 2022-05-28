import cv2
import numpy as np
import LSsharedmodules
import math

def selectPoints():  # function for user to define corners of screen for warping

    global points  # initialise points var - stores co-ords of points for use during warping
    points = []
  
    cap = cv2.VideoCapture(0)  # init webcam capture
    LSsharedmodules.popUp("Select points","To calibrate, please select the corners of your screen \n\nPress 'ENTER' to save config or 'R' to reset points", 1)

    check, frame = cap.read()
    cv2.imshow("Calibration", frame)
    set_top = True
    while True:  # cv2 loop
        check, frame = cap.read()
        if not check:  # checks frames are being recieved
            break
        
        cv2.imshow("Calibration", frame)  # displays current frame

        if set_top:  # opens the window in front of all windows
            cv2.setWindowProperty("Calibration",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty("Calibration",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
            set_top = False

        cv2.setMouseCallback("Calibration", click)  # mouse event callback func

        displayPoints(frame)  # displays selected points on the screen
        
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # exits calibration if esc pressed
            break
        elif key == ord('r') and len(points) != 0:  # clears all points and resets frame
            points.clear()
            displayPoints(frame)
            cv2.imshow("Calibration", frame)
        elif key == 13 and len(points) == 4:  # moves onto warping if 4 points chosen and ENTER is pressed
            cv2.destroyWindow('Calibration')
            matrix = warpImage(cap, points)  # calls functions and returns matrix and mask parameters
            maskparams = maskImage(cap, matrix)
            if maskparams == False:
                return (False, False)
            confirm = LSsharedmodules.popUp("Save Profile", "Do you want to save this profile?", 2)
            cv2.destroyAllWindows()
            return (points, maskparams) if confirm else (False, False)

    cap.release()
    cv2.destroyWindow('Calibration')
    return (False, False)


def click(event, x, y, flags, params,):  # event function to detect user calibration clicks
        global point
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:  # appends point to points var. only allows 4 points
            point = [x,y]
            print(point)
            points.append(point)  # adds point to list of points


def displayPoints(frame):
    for i in range(len(points)):  # draws all points on frame
        cv2.circle(frame, points[i], 5, (0, 0, 255), -1)

    if len(points) == 4:
        for point in points:
            distances = [math.sqrt((point[0]-other_p[0])**2+(point[1]-other_p[1])**2) for other_p in points]  # formula for distance between 2 points
            sorted_d = sorted(distances, reverse=True)
            sorted_d.pop()
            for i in range(2):  # connects each point to the nearest two points
                connected_d = sorted_d.pop()
                connected_p = points[distances.index(connected_d)]
                cv2.line(frame, point, connected_p, (0, 255, 0), 1)

    cv2.imshow("Calibration", frame)


def warpImage(cap, points):
    left, right = sorted(points)[:2], sorted(points)[2:]  # calculates which points are for which corner of the screen
    tl, bl = sorted(left, key=lambda x: x[1])             # + allows point selection in any order
    tr, br = sorted(right, key=lambda x: x[1])

    pts1 = np.float32([tl, tr, bl, br])  # creates source matrix of points on orignial frame
    pts2 = np.float32([[0, 0], [1000, 0], [0, 1000], [1000, 1000]])  # creates destination matrix of points on warped frame
    matrix = cv2.getPerspectiveTransform(pts1, pts2)  # creates perspective transform matrix for warping below
    return matrix
    

def maskImage(cap, mat):
    saved = False
    selected = False
    while True:
        check, frame = cap.read()
        if not check:
            break

        frame = cv2.warpPerspective(frame, mat, (1000, 1000))
        hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # converts img to hsv for masking

        if not selected:
            auto = LSsharedmodules.popUp("Select a masking method", "Would you like to automatically generate a mask?\nPress 'No' to manually create a mask.\n\nIf unsure, automatic mask generation is recommended", 2)  # branches to auto or manual masking
            if not auto:
                n = "Create Mask"  # Creates trackbar menu
                cv2.namedWindow(n)
                cv2.createTrackbar("Lower H", n, 0, 255, noFunc)
                cv2.createTrackbar("Lower S", n, 0, 255, noFunc)
                cv2.createTrackbar("Lower V", n, 0, 255, noFunc)

                cv2.createTrackbar("Upper H", n, 255, 255, noFunc)
                cv2.createTrackbar("Upper S", n, 255, 255, noFunc)
                cv2.createTrackbar("Upper V", n, 255, 255, noFunc)
                link = "https://imaadnisar.github.io/Lightscreen-Touchscreen-Detection/"
                LSsharedmodules.popUp("Info", f"Press 'ENTER' to save the mask.\nFor more info on how to create a manual mask, click 'How to Use'.", 1)  # add hyperlink 
            selected = True

        if not saved:  # exits once maskparams created and saved
            if auto:
                maskparams = automaticMaskParams(frame, hsvimg)
                saved = True
            else:
                maskparams = manualMaskParams(frame, hsvimg)
                if len(maskparams) == 3:  # checks returned values to see if values saved
                    maskparams = maskparams[:-1]
                    saved = True
                showMaskCreation(maskparams, frame, hsvimg, saved)  # displays image and trackbar menu

        if saved:
            return maskparams

        if cv2.waitKey(1) == 27:
            break
        if cv2.waitKey(1) == 13:
            cv2.destroyWindow(n)
            saved = True
        

    cap.release()
    cv2.destroyAllWindows()
    return False


def noFunc(x):  # dummy function
    pass


def manualMaskParams(img, hsv):
    pos = []
    n = "Create Mask"
    tbn = {  # trackbar names
        1: "Lower H",
        2: "Lower S",
        3: "Lower V",
        4: "Upper H",
        5: "Upper S",
        6: "Upper V",
    }
    
    for i in range(1, 7):
        pos.append(cv2.getTrackbarPos(tbn[i], n))  # adds trackbar names to interface

    # creates lower and upper bound masking arrays from current positions of trackbar
    lower = np.array([pos[0], pos[1], pos[2]])
    upper = np.array([pos[3], pos[4], pos[5]])

    if cv2.waitKey(1) == 13:
        cv2.destroyWindow(n)
        return [lower, upper, "saved"]  # returns the params and check str once saved

    return [lower, upper]


def automaticMaskParams(img, hsv):  # automatic masking settings for blue light
    lower = np.array([100, 50, 20])
    upper = np.array([130, 255, 255])
    
    return [lower, upper]


def showMaskCreation(maskparams, frame, hsv, saved):
    mask = cv2.inRange(hsv, maskparams[0], maskparams[1])  # creates mask using hsv image, upper and lower bound
    img = cv2.bitwise_and(frame, frame, mask=mask)  # creates original image with mask using bitwise and
    cv2.imshow("Windows", img)
    if saved:
        cv2.destroyAllWindows()
