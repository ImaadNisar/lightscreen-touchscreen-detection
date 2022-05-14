import cv2


image= cv2.imread('Containers.png')
original_image= image

gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)


contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print ('Number of contours found = ', len(contours))


def get_contour_areas(contours):

    all_areas= []

    for cnt in contours:
        area= cv2.contourArea(cnt)
        all_areas.append(area)

    return all_areas


sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)


smallest_item= sorted_contours[0]

cv2.drawContours(original_image, smallest_item, -1, (255,0,0),10)
cv2.waitKey(0)
cv2.imshow('Smallest Object', original_image)


cv2.waitKey(0)
cv2.destroyAllWindows()

