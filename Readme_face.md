# Detecção de Faces, Olhos e Sorrisos em Stream de Câmera IP

Este projeto utiliza OpenCV para capturar uma stream de vídeo de uma câmera IP e aplicar detecção de faces, olhos e sorrisos em tempo real. Ele faz uso de classificadores Haar Cascade pré-treinados para detectar esses elementos e desenha retângulos ao redor das regiões detectadas no vídeo.

## Funcionalidades

- Captura de vídeo em tempo real a partir de uma câmera IP.
- Detecção de:
  - **Faces** usando o classificador `haarcascade_frontalface_default.xml`.
  - **Olhos** usando o classificador `haarcascade_eye.xml`.
  - **Sorrisos** usando o classificador `haarcascade_smile.xml`.
- Exibição em tempo real do vídeo com as regiões detectadas destacadas por retângulos coloridos.
- Encerramento do programa ao pressionar a tecla `q`.

## Requisitos

- Python 3.x
- OpenCV (`opencv-python`)
  
Para instalar as dependências necessárias, você pode usar o seguinte comando:

```bash
pip install opencv-python PyOpenGL mediapipe

```

## Como executar

1. **Instale as dependências** utilizando o comando `pip install opencv-python PyOpenGL mediapipe`.
2. **Configure o URL da câmera IP**:
    - Altere a variável `url` no código para corresponder ao endereço IP da sua câmera, seguido pela porta e caminho do vídeo.
    - Exemplo: `url = 'http://192.168.1.187:8000/video'`
3. **Execute o script**:

```bash
python face_cap.py
```

## Estrutura do Código

1. **Captura de vídeo**:
    - O vídeo é capturado a partir da câmera IP utilizando a URL fornecida e a função `cv2.VideoCapture`.
  
2. **Classificadores Haar Cascade**:
    - Três classificadores Haar Cascade são carregados para detectar faces, olhos e sorrisos:
      - `haarcascade_frontalface_default.xml`
      - `haarcascade_eye.xml`
      - `haarcascade_smile.xml`
  
3. **Detecção em tempo real**:
    - Para cada quadro capturado, o script converte a imagem para escala de cinza e aplica os classificadores para detectar faces, olhos e sorrisos.
    - Um retângulo verde é desenhado ao redor das faces detectadas, um retângulo azul ao redor dos olhos e um retângulo vermelho ao redor dos sorrisos.
  
4. **Exibição do vídeo**:
    - O vídeo processado é exibido em uma janela OpenCV, com as detecções destacadas.
    - Pressione a tecla `q` para encerrar a execução.

## Personalização

Você pode ajustar os seguintes parâmetros para melhorar a detecção:

- **URL da câmera IP**: Modifique o valor da variável `url` para corresponder à sua câmera IP.
- **Parâmetros dos classificadores**: 
    - O parâmetro `scaleFactor` ajusta o quão minuciosa é a detecção, e `minNeighbors` controla quantos vizinhos são necessários para cada detecção ser validada.
    - Esses valores podem ser ajustados para cada tipo de detecção para melhorar a precisão conforme necessário.

## Exemplo de Código

```python
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
        gray, scaleFactor=1.2, minNeighbors=15, minSize=(30, 30)
    )

    # Detectar sorrisos dentro das faces
    smiles = smile_cascade.detectMultiScale(
        gray, scaleFactor=1.5, minNeighbors=20, minSize=(30, 30)
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
```

## Observações

- Verifique se o seu dispositivo está na mesma rede da câmera IP e se o URL fornecido está correto.
- Se a detecção não estiver funcionando como esperado, ajuste os parâmetros `scaleFactor` e `minNeighbors` ou verifique se a câmera está transmitindo corretamente.

