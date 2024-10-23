import cv2

# Link do app ipcamera (resolução 640 x 320)
url = 'http://192.168.1.187:8000/video'

video_capture = cv2.VideoCapture(url)

# Carregar os classificadores Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Erro ao acessar a stream de vídeo.")
        break

    # Verifica se o quadro foi capturado corretamente
    if frame is None:
        print("Quadro vazio, falha ao capturar vídeo.")
        continue

    brightness_factor = 1.4
    frame = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)

    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Desenhar retângulos em volta das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Focar a detecção de sorriso na parte inferior do rosto
        face_roi_gray = gray[y:y + h, x:x + w]
        face_roi_color = frame[y:y + h, x:x + w]

        # Definir a região onde o sorriso é mais provável (metade inferior do rosto)
        lower_face_gray = face_roi_gray[h // 2:, :]
        lower_face_color = face_roi_color[h // 2:, :]

        # Detectar sorrisos apenas na região inferior da face
        smiles = smile_cascade.detectMultiScale(
            lower_face_gray, scaleFactor=1.7, minNeighbors=20, minSize=(25, 25)
        )

        for (sx, sy, sw, sh) in smiles:
            sy = sy + h // 2
            cv2.rectangle(face_roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o capturador de vídeo e fecha todas as janelas
video_capture.release()
cv2.destroyAllWindows()
