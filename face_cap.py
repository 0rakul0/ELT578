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

    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Detectar olhos dentro das faces
    eyes = eye_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=18, minSize=(30, 30)
    )

    # Detectar sorrisos dentro das faces
    smiles = smile_cascade.detectMultiScale(
        gray, scaleFactor=1.7, minNeighbors=20
    )

    # Desenhar retângulos em volta das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Desenhar retângulos em volta dos olhos detectados
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Desenhar retângulos em volta dos sorrisos detectados
    for (x, y, w, h) in smiles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Exibir o vídeo com as detecções
    cv2.imshow('video', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o capturador de vídeo e fecha todas as janelas
video_capture.release()
cv2.destroyAllWindows()
