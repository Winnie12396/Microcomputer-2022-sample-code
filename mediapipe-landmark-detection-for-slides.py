import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

# max_num_faces是最大可偵測的人臉數
with mp_face_mesh.FaceMesh(
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # 如果載入一支影片，這裡要用break而不是continue
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 如果有抓到臉
    if results.multi_face_landmarks:
          
      # 對每張臉做以下操作
      for face in results.multi_face_landmarks:
            
        # ls_single_face 存有某張臉的所有坐標點
        ls_single_face=face.landmark

        # 右眼
        # 坐標計算方式：ls_single_face中所儲存的位置資訊經過標準化，值介於0~1
        # 0對應該軸向的最小值，1則是最大值
        # 需要把介於0~1的值對應回畫面上的坐標
        # 預設視窗大小為640*480，如果有調整視窗大小記得修改此處數值
        # 255跟233為可以框選出右眼的坐標點
        x1 = int(640*float(ls_single_face[225].x))
        y1 = int(480*float(ls_single_face[225].y))
        x2 = int(640*float(ls_single_face[233].x))
        y2 = int(480*float(ls_single_face[233].y))

        # 繪製出(x1, y1)到(x2, y2)的矩形，(x1, y1)-(x2, y2)為矩形對角線
        # (255, 255, 255)為顏色，最後的2為線條粗細
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255),2)

        # 左眼
        x1 = int(640*float(ls_single_face[445].x))
        y1 = int(480*float(ls_single_face[445].y))
        x2 = int(640*float(ls_single_face[453].x))
        y2 = int(480*float(ls_single_face[453].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255),2)

        # 嘴巴
        x1 = int(640*float(ls_single_face[165].x))
        y1 = int(480*float(ls_single_face[165].y))
        x2 = int(640*float(ls_single_face[406].x))
        y2 = int(480*float(ls_single_face[406].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255),2)

        '''# 右邊瞳孔；三個單引號為多行註解的一種方式，刪掉後即可標示出瞳孔
        x1 = int(640*float(ls_single_face[471].x))
        y1 = int(480*float(ls_single_face[470].y))
        x2 = int(640*float(ls_single_face[469].x))
        y2 = int(480*float(ls_single_face[472].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (100,0,100),2)
        # 左邊瞳孔
        x1 = int(640*float(ls_single_face[476].x))
        y1 = int(480*float(ls_single_face[475].y))
        x2 = int(640*float(ls_single_face[474].x))
        y2 = int(480*float(ls_single_face[477].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (158, 239, 255),2)'''

    # 為了符合自拍的方向，翻轉畫面
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()