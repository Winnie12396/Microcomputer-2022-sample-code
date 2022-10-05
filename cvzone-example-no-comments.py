from cvzone.HandTrackingModule import HandDetector
import cv2

def mapFromTo(x, a, b, c, d):
    y = int((x - a) / (b - a) * (d - c) + c)
    return y

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.7, maxHands=2)

control = False
 
while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)
    control = False

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]

        # print(hand1)
        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # print(handType1)

        # fingers1 = detector.fingersUp(hand1) 
        # print(fingers1)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2["center"]
            handType2 = hand2["type"]

            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)

            beta = mapFromTo(length, 100, 600, 0, 100)

            adjusted = cv2.convertScaleAbs(img, alpha=1, beta=beta)
            control = True

            cv2.putText(img, f'Dist:{int(length)}',(40, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
  
    if control:
        cv2.imshow("Image", cv2.flip(adjusted, 1))
    else:
        cv2.imshow("Image", cv2.flip(img, 1))

    if cv2.waitKey(5) & 0xFF == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
