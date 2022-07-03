import numpy as np
import cv2
import mediapipe as mp
import time
import keyboard
from matplotlib import pyplot as plt


class hand_detector:
    handlist = [1, 12]
    str = 'test'
    mode = False
    maxHands = 1
    detectionCon = 0.5
    modelComplex = 1
    trackCon = 0.5
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)
    mpDraw = mp.solutions.drawing_utils
    handList = [1, 2]

    def __init__(self, mode: object = False, maxHands: object = 1, detectionCon: object = 0.5, trackCon: object = 0.5,
                 modelComplexity: object = 1) -> object:
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.handList = [1, 2]

    def findHands(self, img, draw=True):
        img = np.uint8(img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findHandsAB(self, img, img2, draw=True):
        img = np.uint8(img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img2, handLms, self.mpHands.HAND_CONNECTIONS)
        return img2

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
        handlist = lmlist
        return lmlist

    def getLmlist(self):
        return self.lmList
    def hand_detector_run(detector, img):
        hdt = hand_detector()
        pTime = 0
        cTime = 0
        x = 300
        y = 200
        color = (255, 0, 0)
        thickness = 2
        first_time = True
        t1 = 0
        t2 = 0
        dt = 0
        seconds_until_click = 2
        counter = 0
        startPoint = (1000, 100)
        endPoint = (1400, 300)
        # TO-DO: detector Klasse übergeben!
        # CV2 Operation ausführen
        img = detector.findHands(hdt, img)

        img = cv2.rectangle(img, startPoint, endPoint, color, thickness)

        # TO-DO Loading animation Circle
        lmlist = detector.findPosition(hdt, img)
        # Setze Globale Liste!
        handlist = lmlist
        hand_detector.handlist = lmlist
        if len(lmlist) != 0:
            center = (int(lmlist[0].__getitem__(1)), int(lmlist[0].__getitem__(2)))
            img = cv2.circle(img, center, 20, (255, 255, 0), 2)
            # TO-DO: Implement Timer
            if detector.intersection(hdt, lmlist, x, y, startPoint, endPoint) == True:
                counter += 1
                color = (255, 255, 40)

                t1 = time.time()

                if dt >= seconds_until_click:
                    color = (0, 0, 255)
                    cv2.circle(img, (400, 400), 30, (0, 0, 0), cv2.FILLED)
                    # send a message

                if first_time:
                    first_time = False
                else:
                    dt += t1 - t2

                t2 = t1
            else:
                first_time = True
                dt = 0
                color = (255, 0, 0)
                counter = 0
                t1 = 0
                t2 = 0
                dt = 0
                first_time = True

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        print('FPS: ',fps)


        return img
    def find_hands_on_image(self, img):
        # TO -DO Intersection außerhalb der While Methode
        x = 300
        y = 200
        color = (255, 0, 0)
        thickness = 2
        counter = 0
        startPoint = (1000, 100)
        endPoint = (1400, 300)
        img = self.findHands(self, img)
        lmlist = self.findPosition(self, img)
        handlist = lmlist
        hand_detector.handlist = lmlist
        if len(lmlist) != 0:
            center = (int(lmlist[0].__getitem__(1)), int(lmlist[0].__getitem__(2)))
            img = cv2.circle(img, center, 20, (255, 255, 0), 2)

        return img

def main(self):
    print("TRUE INI!!!!!!")
    detector = hand_detector()


if __name__ == "__main__":
   main()
