import cv2
import pyautogui
import numpy as np
import time

from hand_tracking import HandTracker
from utils import distance, smooth_coordinate

# Webcam settings
w_cam, h_cam = 640, 480

# Frame reduction (active region)
frame_r = 100

# Smoothening factor
smoothening = 7

# Scroll settings
scroll_threshold = 8
scroll_speed = 25
prev_scroll_y = 0

# Previous mouse location
p_x, p_y = 0, 0

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)

# Initialize hand tracker
tracker = HandTracker(max_hands=1)

# Screen size
screen_w, screen_h = pyautogui.size()

# Disable failsafe (prevents sudden stops)
pyautogui.FAILSAFE = False

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)

    # Detect hand
    img = tracker.find_hands(img, draw=True)
    lm_list = tracker.get_positions(img)

    if lm_list:
        x1, y1 = lm_list[8][1:]   # Index finger tip
        x2, y2 = lm_list[12][1:]  # Middle finger tip
        x3, y3 = lm_list[16][1:]  # Ring finger tip

        fingers = tracker.fingers_up(lm_list)

        # Draw control rectangle
        cv2.rectangle(
            img,
            (frame_r, frame_r),
            (w_cam - frame_r, h_cam - frame_r),
            (255, 0, 255),
            2,
        )

        # 🖱️ Move Mode (only index finger up)
        if len(fingers) >= 4 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:

            # Map coordinates
            x_m = np.interp(x1, (frame_r, w_cam - frame_r), (0, screen_w))
            y_m = np.interp(y1, (frame_r, h_cam - frame_r), (0, screen_h))

            # Smooth movement
            c_x = smooth_coordinate(p_x, x_m, smoothening)
            c_y = smooth_coordinate(p_y, y_m, smoothening)

            pyautogui.moveTo(c_x, c_y)

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

            p_x, p_y = c_x, c_y

        # 🖱️ Right Click Mode (index + middle + ring finger)
        elif len(fingers) >= 4 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:

            if distance(x1, y1, x3, y3) < 40:
                cv2.circle(
                    img,
                    ((x1 + x3) // 2, (y1 + y3) // 2),
                    10,
                    (0, 255, 255),
                    cv2.FILLED,
                )
                pyautogui.rightClick()
                time.sleep(0.25)

        # 🖱️ Scroll Mode (index + middle finger, fingers apart)
        elif len(fingers) >= 3 and fingers[1] == 1 and fingers[2] == 1 and distance(x1, y1, x2, y2) >= 50:

            current_scroll_y = (y1 + y2) // 2
            if prev_scroll_y != 0:
                delta_y = prev_scroll_y - current_scroll_y
                if abs(delta_y) > scroll_threshold:
                    pyautogui.scroll(int(delta_y * scroll_speed / 10))
            prev_scroll_y = current_scroll_y

        # 🖱️ Click Mode (index + middle finger)
        elif len(fingers) >= 3 and fingers[1] == 1 and fingers[2] == 1:

            if distance(x1, y1, x2, y2) < 40:
                cv2.circle(
                    img,
                    ((x1 + x2) // 2, (y1 + y2) // 2),
                    10,
                    (0, 255, 0),
                    cv2.FILLED,
                )
                pyautogui.click()
                time.sleep(0.25)
                prev_scroll_y = 0
        else:
            prev_scroll_y = 0

    cv2.imshow("AI Virtual Mouse", img)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()