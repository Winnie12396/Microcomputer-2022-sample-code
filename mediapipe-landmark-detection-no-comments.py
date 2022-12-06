import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
      for face in results.multi_face_landmarks:
        ls_single_face=face.landmark

        # right eye
        x1 = int(640*float(ls_single_face[225].x))
        y1 = int(480*float(ls_single_face[225].y))
        x2 = int(640*float(ls_single_face[233].x))
        y2 = int(480*float(ls_single_face[233].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255),2)

        # left eye
        x1 = int(640*float(ls_single_face[445].x))
        y1 = int(480*float(ls_single_face[445].y))
        x2 = int(640*float(ls_single_face[453].x))
        y2 = int(480*float(ls_single_face[453].y))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255),2)

        # mouth
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

    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()