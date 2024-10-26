# %% Importação de bibliotecas
import cv2
import numpy as np

# %% Definição das coordenadas das vagas
# Cada vaga é representada por um retângulo com os valores [x, y, largura, altura]
vag1 = [1, 89, 108, 213]
vag2 = [115, 88, 150, 213]
vag3 = [289, 89, 130, 213]
vag4 = [439, 89, 130, 213]
vag5 = [591, 89, 130, 213]
vag6 = [738, 89, 130, 213]
vag7 = [881, 89, 130, 213]
vag8 = [1027, 89, 130, 213]

# %% Armazenando todas as vagas em uma lista
# A lista `vags` contém todas as coordenadas das vagas
vags = [vag1, vag2, vag3, vag4, vag5, vag6, vag7, vag8]

# %% Carregando o vídeo
# Carrega o vídeo especificado para processamento
video = cv2.VideoCapture('./CTI/video.mp4')

while True:
    # Leitura de cada frame do vídeo
    ret, frame = video.read()

    # Convertendo o frame para escala de cinza para facilitar o processamento
    frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicação de threshold adaptativo para detecção de vagas livres
    frameThreshed = cv2.adaptiveThreshold(
        frameCinza,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        16
    )

    # Aplicação de filtro para suavizar a imagem
    frameBlur = cv2.medianBlur(frameThreshed, 5)

    # Dilatação para preencher pequenos buracos e melhorar a contagem de pixels
    kernel = np.ones((3, 3), np.uint8)
    frameDil = cv2.dilate(frameBlur, kernel)

    # Contador de vagas disponíveis
    qteVagas = 0

    # Loop para verificar cada vaga
    for x, y, w, h in vags:
        # Corta a área correspondente à vaga no frame dilatado
        recorte = frameDil[y:y + h, x:x + w]
        qteBranco = cv2.countNonZero(recorte)  # Conta os pixels brancos

        # Exibe a contagem de pixels brancos na vaga
        cv2.putText(frame, str(qteBranco), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Se a contagem de pixels brancos for >= 3000, a vaga está ocupada (retângulo vermelho)
        if qteBranco >= 3000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            # Caso contrário, a vaga está livre (retângulo verde)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            qteVagas += 1

    # Exibe o contador de vagas livres no canto superior esquerdo do frame
    cv2.rectangle(frame, (90, 0), (415, 60), (255, 0, 0), -1)
    cv2.putText(frame, f'LIVRE, {qteVagas}/8', (95, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)

    # Exibe o frame principal e os frames de etapas intermediárias para análise
    cv2.imshow('Video', frame)
    cv2.imshow('frameCinza', frameThreshed)
    cv2.imshow('frameBlur', frameBlur)
    cv2.imshow('frameDil', frameDil)

    # Encerra o loop ao pressionar 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Libera os recursos e fecha as janelas abertas
cv2.destroyAllWindows()
