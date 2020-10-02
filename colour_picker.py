import cv2
import numpy as np

capture = cv2.VideoCapture(0)

# Initializes screen
frame_width = 640
frame_height = 480

# Width, id number 3
capture.set(3, frame_width)

# Height, id number 4
capture.set(4, frame_height)

# Adjust brightness, id 10
capture.set(10, 1)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)

# HSV: Min
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)

# HSV: Max
cv2.createTrackbar("HUE Max", "HSV", 0, 179, empty)
cv2.createTrackbar("SAT Max", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 0, 255, empty)

while True:

    _ , img = capture.read()
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")

    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(img_HSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask = mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    h_stack = np.hstack([img, mask, result])

    cv2.imshow("Horizontal Stacking", h_stack)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()