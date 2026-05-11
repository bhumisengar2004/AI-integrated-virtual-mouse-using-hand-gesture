import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def get_positions(self, img, hand_no=0):
        lm_list = []
        if not self.results or not self.results.multi_hand_landmarks:
            return lm_list

        h, w, _ = img.shape
        hand = self.results.multi_hand_landmarks[hand_no]

        for idx, lm in enumerate(hand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((idx, cx, cy))

        return lm_list

    def fingers_up(self, lm_list):
        if not lm_list:
            return []

        fingers = []

        # Thumb
        fingers.append(1 if lm_list[4][1] > lm_list[3][1] else 0)

        # Other fingers
        fingers.append(1 if lm_list[8][2] < lm_list[6][2] else 0)   # Index
        fingers.append(1 if lm_list[12][2] < lm_list[10][2] else 0) # Middle
        fingers.append(1 if lm_list[16][2] < lm_list[14][2] else 0) # Ring
        fingers.append(1 if lm_list[20][2] < lm_list[18][2] else 0) # Pinky

        return fingers