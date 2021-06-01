import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detect_con=0.5, track_con=0.5):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, max_hands, detect_con, track_con)
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if draw:
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for idx, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([idx, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lm_list

    def get_point_position(self, img, point):
        if self.results.multi_hand_landmarks:
            land_mark = self.results.multi_hand_landmarks[0].landmark[point]
            h, w, c = img.shape
            x, y = int(land_mark.x * w), int(land_mark.y * h)
            return x, y
        return None, None


def main():
    prev_time = 0
    video = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = video.read()
        img = cv2.flip(img, 1)

        img = detector.find_hands(img)
        # lm_list = detector.find_position(img)
        # if len(lm_list) != 0:
        #     print(lm_list[4])

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow('Camera', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
