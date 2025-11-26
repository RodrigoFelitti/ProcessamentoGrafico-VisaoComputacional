import cv2
import numpy as np

"""
Operações aritméticas entre duas imagens.
Todas retornam uma nova imagem.
"""

# ----------------------------------------------------
# Soma simples entre imagens (clamp automático)
# ----------------------------------------------------
def add_images(img1, img2):
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.add(img1, img2)


# ----------------------------------------------------
# Subtração entre imagens (clamp automático)
# ----------------------------------------------------
def subtract_images(img1, img2):
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.subtract(img1, img2)


# ----------------------------------------------------
# Blending (mistura) usando alpha
# ----------------------------------------------------
def blend(img1, img2, alpha=0.5):
    if alpha < 0: alpha = 0
    if alpha > 1: alpha = 1

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    beta = 1 - alpha
    return cv2.addWeighted(img1, alpha, img2, beta, 0)


# ----------------------------------------------------
# Multiplicação pixel a pixel
# ----------------------------------------------------
def multiply_images(img1, img2):
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.multiply(img1, img2)