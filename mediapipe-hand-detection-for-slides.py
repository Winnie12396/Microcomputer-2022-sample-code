import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
count = 0

# min_detection_confidence為最低信心指數，範圍為0~1，超過設定的值則判斷為偵測到手勢
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    count += 1

    # 如果相機未成功開啟
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # 將image設為not writable、將色彩轉換為RGB
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 呼叫process()辨識手勢
    results = hands.process(image)

    # 如果偵測到手勢則繪製出關鍵點和連接
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # 30個frame約為一秒，
        if count % 30 == 0:
              
          # 印出所有關鍵點的座標
          print('hand_landmarks:', hand_landmarks)

          # 印出指定關鍵點的x, y座標，此例為食指指尖
          print(
            'Index finger tip coordinates: (',
            hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
            hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y, ')')
          
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # 翻轉影像以得到正確視角
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    # 按esc可退出
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
cv2.destroyAllWindows()

