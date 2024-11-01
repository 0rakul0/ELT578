#%% importes
import threading
import cv2
from deepface import DeepFace

#%% start camera
url = 'http://192.168.1.119:8000/video'
video_capture = cv2.VideoCapture(url)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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

    brightness_factor = 1.8
    frame = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)

    if face_detector:
        cv2.putText(frame, "MATCH", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
    else:
        cv2.putText(frame, "NO MATCH", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
