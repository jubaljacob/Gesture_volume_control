import cv2
import numpy as np
import time
import HandTracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 640, 480
pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionconf=0.8)

#################################################################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

######################################################################

vol = 0
volBar = 20
while True:
    success, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(frame, (x1, y1), 8, (225, 0, 225), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 8, (225, 0, 225), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (225, 0, 225), 2)
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(frame, (cx, cy), 5, (225, 225, 225), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # hand range = 35 to 150
        # vol range -65 to 0

        vol = np.interp(length, [25, 150], [minVol, maxVol])
        volper = np.interp(length, [25, 150], [0, 100])

        print(int(length), vol)
        cv2.putText(frame, f'{int(volper)}% ', (25, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

        volume.SetMasterVolumeLevel(vol, None)
        if length < 35:
            cv2.circle(frame, (cx, cy), 5, (0, 0, 225), cv2.FILLED)

    # cv2.rectangle(frame, (50, 150), (85, 400), (0, 225, 0), 3)
    # cv2.rectangle(frame, (50, int(vol)), (85, 400), (0, 225, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (5, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 225), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break
