import cv2

#link do app ipcamera resolução 640 x 320
url = 'http://192.168.1.187:8000/video'

video_capture = cv2.VideoCapture(url)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Erro ao acessar a stream de vídeo.")
        break

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()