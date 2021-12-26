import cv2
import numpy as np
import time
import Gesture_volume_control.HandTracking_module as htm


wCam, hCam = 640, 480
pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector()

while True:
    success, frame = cap.read()
    detector.findHands(frame)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (5, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break
