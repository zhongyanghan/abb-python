import numpy
import mediapipe as mp
import cv2
import time
import math
import socket

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('127.0.0.1',1234))					#绑定监听的对象
server.listen(5)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

fpstime = time.time()
cap = cv2.VideoCapture(0)

while True:
    conn,addr = server.accept()
    with mp_hands.Hands(min_detection_confidence=0.7,
                        min_tracking_confidence=0.5,
                        max_num_hands=2) as hands:
        t=0
        while cap.isOpened():
            success,image = cap.read()
            image = cv2.resize(image,(640,480))
            image.flags.writeable = False
            image = cv2.flip(image,1)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            if results.multi_hand_landmarks :

                for hand_landmark in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image,
                                              hand_landmark,
                                              mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())
                    landmark_list = []
                    for landmark_id,finger_axis in enumerate(
                        hand_landmark.landmark):
                        landmark_list.append([
                            landmark_id,finger_axis.x,finger_axis.y,
                            finger_axis.z
                        ])
                    if t!=0:
                        temp1=index_finger_tip_x
                        temp2=index_finger_tip_y
                    if landmark_list:
                        index_finger_tip = landmark_list[4]
                        index_finger_tip_x = math.ceil(index_finger_tip[1]*640)
                        index_finger_tip_y = math.ceil(index_finger_tip[2]*480)
                    if t!=0:
                        print(index_finger_tip_x - temp1)
                        print(index_finger_tip_y - temp2)
                        if conn.recv(512) == b'ok':
                            X = str((index_finger_tip_x - temp1))
                            conn.send(X.encode(('utf-8')))
                        if conn.recv(512) == b'ok1':
                            X = str((temp2-index_finger_tip_y))
                            conn.send(X.encode(('utf-8')))
                    t=t+1
                    index_finger_point =(index_finger_tip_x,index_finger_tip_y)
                    image = cv2.circle(image,index_finger_point,10,(255,0,255),-1)

                    ctime = time.time()
                    fps_text = 1/(ctime-fpstime+0.01)
                    fpstime=ctime
                    cv2.putText(image,"FPS:"+str(int(fps_text)),(10,70),
                                cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
                    cv2.imshow('MediaPipe Hands',image)
                    if cv2.waitKey(5) & 0xFF == 27 or cv2.getWindowProperty('MediaPipe Hands', cv2.WND_PROP_VISIBLE) < 1:
                        break
        cap.release()
        cv2.destroyAllWindows()
             #开始监听
