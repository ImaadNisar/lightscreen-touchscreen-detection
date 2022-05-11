import cv2  # imports the cv2 library

img = cv2.imread('filepath')  # reads image

cv2.imshow('window', img)  # displays the image

cv2.waitKey(0)  # waits. 0 = infinite duration. waits for keypress to exit

capture = cv2.VideoCapture(1)  # gets video at webcam id 1

img.set(3, 640)  # sets the width res of image
img.set(4, 480)  # sets the height res of image

check, frane = capture.read()  # returns a boolean and a frame from a video capture

img = cv2.resize(img, (1920, 1080))  # resizes the image. args: (image, (width, height))

cropped = img[200:300, 225:275]  # crops the image [yregion, xregion]

cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0, 0, 255), 5)  # creates a line (img, start, end, color, thickness)

cv2.rectangle(img, (50, 50), (250, 250), (255, 0, 0), cv2.FILLED)  # creates a rectange (img, start, end, color, thickness/fill(-ve))

cv2.circle(img, (0, 0), 100, (0, 255, 0), -10)  # creates a circle (img, centre, radius, color, thickness)

cv2.putText(img, "CV2?", (250, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)  # puts text (img, text, origin, font, scale, color, thickness)

def click(event, x, y, flags, param):  # events params
    if event == cv2.EVENT_LBUTTONDOWN:  # event name
        return
