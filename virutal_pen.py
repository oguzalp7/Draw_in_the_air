import numpy as np
import cv2
import imutils
import time
import keyboard


def nothing(x):
    pass


once = 0
paint = np.zeros((480, 640, 3)) + 255
paint_copy = paint.copy()
greenLower = (14, 88, 121)
greenUpper = (32, 171, 255)
pts = []
cap = cv2.VideoCapture(0)
time.sleep(2.0)
pen_down = 0
cv2.namedWindow('Frame')
cv2.createTrackbar('mavi', 'Frame', 0, 255, nothing)
cv2.createTrackbar('yesil', 'Frame', 0, 255, nothing)
cv2.createTrackbar('kirmizi', 'Frame', 0, 255, nothing)
cv2.createTrackbar('kalinlik', 'Frame', 2, 10, nothing)
while True:

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    b = cv2.getTrackbarPos('mavi', 'Frame')
    g = cv2.getTrackbarPos('yesil', 'Frame')
    r = cv2.getTrackbarPos('kirmizi', 'Frame')
    thickness = cv2.getTrackbarPos('kalinlik', 'Frame')
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (b, g, r), -1)
            # cv2.circle(paint, center, 5, (255, 0, 255), -1)

        if keyboard.is_pressed('space'):
            pen_down = 1
        if keyboard.is_pressed('b'):
            pen_down = 0
            once = 1
        if pen_down == 1:
            pts.append(center)
        if pen_down == 0 and once == 1:
            pts.pop()
            once = 0
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            if pen_down == 0:
                pts[i - 1], pts[i] = None, None
            # thickness = 2
            cv2.line(frame, pts[i - 1], pts[i], (b, g, r), thickness)
            cv2.line(paint, pts[i - 1], pts[i], (b, g, r), thickness)
        if keyboard.is_pressed('c'):
            pts.clear()
            paint = cv2.bitwise_or(paint, paint_copy)
    cv2.imshow("Frame", frame)
    cv2.imshow('Paint', paint)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()