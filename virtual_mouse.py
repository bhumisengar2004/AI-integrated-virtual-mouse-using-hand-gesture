import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

# Webcam settings
wCam, hCam = 640, 480

# Frame reduction (for smooth control)
frameR = 100
smoothening = 7

# Previous mouse location
pX, pY = 0, 0
cX, cY = 0, 0

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Screen size
screen_w, screen_h = pyautogui.size()

def find_finger_positions(img, hand_landmarks):
    lmList = []
    h, w, c = img.shape

    for id, lm in enumerate(hand_landmarks.landmark):
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmList.append((id, cx, cy))

    return lmList

def fingers_up(lmList):
    fingers = []

    # Index finger
    if lmList[8][2] < lmList[6][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle finger
    if lmList[12][2] < lmList[10][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            lmList = find_finger_positions(img, handLms)

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]   # Index tip
                x2, y2 = lmList[12][1:]  # Middle tip

                fingers = fingers_up(lmList)

                # Draw rectangle
                cv2.rectangle(img, (frameR, frameR), 
                              (wCam - frameR, hCam - frameR), 
                              (255, 0, 255), 2)

                # 👉 Moving Mode (Only index finger)
                if fingers[0] == 1 and fingers[1] == 0:
                    # Convert coordinates
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, screen_w))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, screen_h))

                    # Smoothening
                    cX = pX + (x3 - pX) / smoothening
                    cY = pY + (y3 - pY) / smoothening

                    pyautogui.moveTo(cX, cY)
                    cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

                    pX, pY = cX, cY

                # 👉 Clicking Mode (Index + Middle finger)
                if fingers[0] == 1 and fingers[1] == 1:
                    length = math.hypot(x2 - x1, y2 - y1)

                    if length < 40:
                        cv2.circle(img, ((x1 + x2)//2, (y1 + y2)//2),
                                   10, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
    """_summary_
    """                        time.sleep(0.2)

    cv2.imshow("AI Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()