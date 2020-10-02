import cv2
import numpy as np

capture = cv2.VideoCapture(0)

# Initializes screen
frame_width = 1280
frame_height = 720

# Width, id number 3
capture.set(3, frame_width)

# Height, id number 4
capture.set(4, frame_height)

# Adjust brightness, id 10
capture.set(10, 100)

my_colours = [[99, 148, 135, 141, 255, 255],
              [140, 113, 105, 172, 255, 255],
              [59, 41, 119, 87, 255, 255]]

# BGR
my_colour_values = [[255, 0, 0],
                    [180, 105, 255],
                    [47, 255, 173]]
my_points = []  # x, y, colour


def find_colour(img, my_colours, my_colour_values):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for colour in my_colours:
        lower = np.array(colour[0:3])
        upper = np.array(colour[3:6])
        mask = cv2.inRange(img_HSV, lower, upper)

        x, y = get_contours(mask)

        cv2.circle(img_result, (x, y), 10, my_colour_values[count], cv2.FILLED)

        if x != 0 and y != 0:
            new_points.append([x, y, count])
        count += 1
        # cv2.imshow(str(colour[0]), mask)
    return new_points

def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:

            # Draws contours around object // check
            # cv2.drawContours(img_result, contour, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x + w // 2, y

def draw_on_canvas(my_points, my_colour_values):
    for point in my_points:
        cv2.circle(img_result, (point[0], point[1]), 10, my_colour_values[point[2]], cv2.FILLED)

while True:
    success, img = capture.read()

    # Flips camera
    img = cv2.flip(img, 1)
    img_result = img.copy()
    new_points = find_colour(img, my_colours, my_colour_values)

    if len(new_points) != 0:
        for new_point in new_points:
            my_points.append(new_point)

    draw_on_canvas(my_points, my_colour_values)

    # Displays result
    cv2.imshow("Result", img_result)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
    if cv2.waitKey(1) & 0xff == ord('c'):
        my_points.clear()
