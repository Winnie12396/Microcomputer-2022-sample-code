from cvzone.HandTrackingModule import HandDetector
import cv2

# 稍後計算亮度用的map函式
def mapFromTo(x, a, b, c, d):
    y = int((x - a) / (b - a) * (d - c) + c)
    return y

cap = cv2.VideoCapture(0)

# detectionCon: 偵測的信心值，一般而言0.5就已經相當精準
# 此範例最多偵測兩隻手，但也可以更多
detector = HandDetector(detectionCon=0.7, maxHands=2)

# 此變數記錄是否透過手來控制亮度
control = False
 
while True:
    success, img = cap.read()

    # 尋找標記出找到的左右手
    # hands, img = detector.findHands(img)
    
    # 但此範例有翻轉畫面因此不繪製出標記，同學可自己把第23行換成20行、
    # 把81跟83行的 cv2.imshow("Image", cv2.flip(..., 1)) 改成 cv2.imshow("Image", ...) 看看效果

    # 尋找手但不標記出來
    hands = detector.findHands(img, draw=False)

    # 每個frame都把control變數重設為False，如果有偵測到雙手再開啟
    control = False

    # 如果有找到至少一隻手
    if hands:
        # 取第一隻手的資料，存放於一個dictionary中
        hand1 = hands[0]
        # 21個手部關鍵點座標，存放於一個list中
        lmList1 = hand1["lmList"]
        # 手部長方形範圍的四點座標(x, y, w, h)
        bbox1 = hand1["bbox"]
        # 手的中心點座標
        centerPoint1 = hand1["center"]
        # 左手或右手
        handType1 = hand1["type"]

        # 以上的資料都可以印出或利用
        # print(hand1)
        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # print(handType1)

        # 也可以偵測哪隻手指有伸出來，以1跟0組成的list印出，分別代表拇指、食指、中指、無名指、小指
        # fingers1 = detector.fingersUp(hand1) 
        # print(fingers1)

        #如果找到兩隻手
        if len(hands) == 2:
            # 取第二隻手的資料，說明同上
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2["center"]
            handType2 = hand2["type"]
 
            # fingers2 = detector.fingersUp(hand2)
            # print(fingers1, fingers2)

            # 用兩隻手的中心點資料去偵測雙手距離
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)

            # 計算雙手距離對應出來的亮度值
            beta = mapFromTo(length, 100, 600, 0, 100)

            # 調整畫面亮度，並把control設為True
            adjusted = cv2.convertScaleAbs(img, alpha=1, beta=beta)
            control = True

            # 在畫面上標示出偵測到的雙手距離
            cv2.putText(img, f'Dist:{int(length)}',(40, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 如果control為True，則呈現調整過亮度的畫面，否則呈現相機原本拍到的畫面      
    if control:
        cv2.imshow("Image", cv2.flip(adjusted, 1))
    else:
        cv2.imshow("Image", cv2.flip(img, 1))

    # 按esc退出
    if cv2.waitKey(5) & 0xFF == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
