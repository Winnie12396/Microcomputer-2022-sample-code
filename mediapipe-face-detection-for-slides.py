import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
count = 0
cap = cv2.VideoCapture(0)

# min_detection_confidence為最低信心指數，範圍為0~1，超過設定的值則偵測到人臉
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    count = count + 1

    # 相機未成功開啟
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # 將image設為not writable來增加效能
    image.flags.writeable = False

    # 將色彩轉換為RGB，因為opencv是BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 呼叫process()辨識人臉
    results = face_detection.process(image)

    # 辨識完後將色彩及writable恢復
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 如果偵測到人臉則繪製出來
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection)
      # 30幀印一次鼻尖的座標；把最後的NOSE_TIP換掉則可印其他臉部關鍵點
      if count % 30 == 0:
        print('Nose tip:')
        print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))

    # 翻轉影像以得到正確視角
    cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))

    # 按esc可退出
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
cv2.destroyAllWindows()
