import pathlib
import pkg_resources
import cv2
import mediapipe as mp
import time
import keyboard
import os

class hand_detector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5, modelComplexity=1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)
        # print(self.results.multi_hand_world_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def intersection(self, lmList, x, y, start_Point, end_Point):
        # X Range
        x_wert = False
        y_wert = False

        for x in range(start_Point[0], end_Point[0]):
            if lmList[0].__getitem__(1) == x:
                x_wert = True
                break
            else:
                x_wert = False
        # Y Range
        for y in range(start_Point[1], end_Point[1]):
            if lmList[0].__getitem__(2) == y:
                y_wert = True
                break
            else:
                y_wert = False

        if (x_wert & y_wert):
            print("Intersection Y: True")
            print("Intersection X: True")
            return True

    def findPosition(self, img, handNo=0, draw=True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist



def main():
    first_time = True
    t1 = 0
    t2 = 0
    dt = 0
    seconds_until_click = 2
    counter = 0
    startPoint = (1000, 100)
    endPoint = (1400, 300)
    enabale_webcam = False
    video = ""
    print("Bitte wählen Sie '0' für Webcam und '1' für ein Testvideo!")
    input1 = input('Wahl: ')
    if input1 == '1':
        enabale_webcam = False
        video = "hands.mp4"
        startPoint = (1000, 100)
        endPoint = (1400, 300)
    elif input1 == '0':
        enable_wbacam = True
        video = 0
        startPoint = (100, 100)
        endPoint = (300, 300)
    print(input1)

    # video = str(video)
    pTime = 0
    cTime = 0
    x = 300
    y = 200
    cap = cv2.VideoCapture(video)
    detector = hand_detector()

    color = (255, 0, 0)
    thickness = 2

    while cap.isOpened():
        success, img = cap.read()
        img = detector.findHands(img)
        img = cv2.rectangle(img, startPoint, endPoint, color, thickness)

        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            center = (int(lmlist[0].__getitem__(1)), int(lmlist[0].__getitem__(2)))
            img = cv2.circle(img, center, 20,(255, 255, 0), 2)
            # TO-DO: Implement Timer
            if detector.intersection(lmlist, x, y, startPoint, endPoint)== True:
                counter += 1
                color = (255, 255, 40)

                t1 = time.time()

                print(dt)
                if dt >= seconds_until_click:
                    color = (0, 0,  255)
                    cv2.circle(img, (400, 400), 30, (0, 0, 0), cv2.FILLED)
                    #send a message

                if first_time:
                    first_time = False
                else:
                    dt += t1 - t2

                t2 = t1
            else:
                color = (255, 0, 0)
                counter = 0
                t1 = 0
                t2 = 0
                dt = 0
                first_time = True

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, "Press ' q ' to exit!", (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        # cv2.putText(img, "Testfield", (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if keyboard.is_pressed('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
