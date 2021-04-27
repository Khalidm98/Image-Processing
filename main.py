import cv2
import time
import hand_tracking_module as htm


def draw_keypad(image, left_top=(0, 0), space=10):
    side = 60
    (left, top) = left_top
    keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '<', '0', '>']

    for row in range(4):
        y = int(top + row * (side + space))
        for col in range(3):
            x = int(left + col * (side + space))
            cv2.rectangle(image, (x, y), (x + side, y + side), (255, 0, 0), 3)
            cv2.putText(image, keys[3 * row + col], (x + 10, y + 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)


def check_pressed(image, left_top=(0, 0), space=10):
    side = 60
    (left, top) = left_top
    keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '<', '0', '>']

    for row in range(4):
        y_key = top + (side + space) * row
        if (y > y_key) and (y < y_key + side):
            for col in range(3):
                x_key = left + (side + space) * col
                if (x > x_key) and (x < x_key + side):
                    key = keys[3 * row + col]
                    cv2.rectangle(image, (x_key, y_key), (x_key + side, y_key + side), (255, 255, 255), cv2.FILLED)
                    cv2.putText(image, key, (x_key + 10, y_key + 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
                    return key
    cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)


video = cv2.VideoCapture(0)
left = int(video.get(3) - 240)
top = 40
# video.set(3, 800)   # width
# video.set(4, 600)   # height

detector = htm.HandDetector(max_hands=1, detect_con=0.75)
t1, t2 = 0, 0
value = ''

while True:
    success, img = video.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img, draw=False)
    x, y = detector.get_point_position(img, 8)  # index finger tip
    draw_keypad(img, (left, top))

    if x:
        key = check_pressed(img, (left, top))
        if key:
            if t1 == 0:
                t1 = time.time()
            else:
                t2 = time.time()
                if t2 - t1 > 1.5:
                    t1 = t2 = 0
                    if key == '>':
                        pass
                    elif key == '<':
                        value = value[:-1]
                    else:
                        value = value + key
        else:
            t1 = t2 = 0

    cv2.putText(img, value, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
    cv2.imshow('Camera', img)
    cv2.waitKey(1)
