import cv2
import numpy as np

"""
Implementação completa dos 10 filtros obrigatórios.
Cada filtro retorna uma nova imagem processada com OpenCV.
"""


#Aplica gaussian blur
def apply_gaussian(image, ksize=5):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


#box blur
def apply_box(image, ksize=3):
    return cv2.blur(image, (ksize, ksize))


#median blur
def apply_median(image, ksize=5):
    return cv2.medianBlur(image, ksize)


#sharpen
def apply_sharpen(image):
    #kernel de nitidez
    kernel = np.array([
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ])
    return cv2.filter2D(image, -1, kernel)


#laplacian
def apply_laplacian(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))
    return cv2.cvtColor(lap, cv2.COLOR_GRAY2BGR)


#sobel edge
def apply_sobel(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    sobel = np.sqrt(sobelx**2 + sobely**2)
    sobel = np.uint8((sobel / sobel.max()) * 255)

    return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)


#gray
def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#escolher canais específicos
def select_channel(image, channel='r'):
    b, g, r = cv2.split(image)

    channel = channel.lower()

    if channel == 'r':
        return cv2.merge([np.zeros_like(b), np.zeros_like(g), r])
    elif channel == 'g':
        return cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])
    elif channel == 'b':
        return cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])
    else:
        print("Canal inválido. Use r, g ou b.")
        return image


#threshold
def apply_threshold(image, thresh=127):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


#canny edge
def apply_canny(image, t1=100, t2=200):
    edges = cv2.Canny(image, t1, t2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def get_filter_description(name):
    desc = {
        "gaussian": "Suavização utilizando um kernel Gaussiano (reduz ruído).",
        "box": "Suavização simples baseada na média dos pixels.",
        "median": "Remoção de ruído preservando bordas com filtro de mediana.",
        "sharpen": "Realce de detalhes através de um kernel de nitidez.",
        "laplacian": "Detecção de bordas pela segunda derivada (Laplaciano).",
        "sobel": "Detecção de bordas baseada em gradiente horizontal e vertical.",
        "gray": "Converte a imagem para escala de cinza.",
        "channel": "Mostra apenas um canal específico (R, G ou B).",
        "threshold": "Transforma a imagem em preto e branco usando limiarização.",
        "canny": "Detecção de bordas avançada usando o algoritmo de Canny."
    }
    return desc.get(name, "Nenhuma descrição disponível.")