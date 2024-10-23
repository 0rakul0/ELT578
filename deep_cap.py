#%% importes
import threading
import cv2
from deepface import DeepFace

#%% start camera
url = 'http://192.168.1.187:8000/video'
video_capture = cv2.VideoCapture(url)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

#%% parametros
counter = 0
face_detector = False
referecence = cv2.imread("./face/treino/1_1.jpg")

def check_face(frame):
    global face_detector
    try:
        if DeepFace.verify(frame, referecence.copy())['verified']:
            face_detector = True
        else:
            face_detector = False

    except ValueError:
        face_detector = False

#%% captura de video
while True:
    ret, frame = video_capture.read()
    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1
    if face_detector:
        cv2.putText(frame, "MATCH", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
    else:
        cv2.putText(frame, "NO MATCH", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

    cv2.imshow("video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
