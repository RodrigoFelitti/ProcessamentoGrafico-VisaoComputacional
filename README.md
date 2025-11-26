# Processador de Imagens e Vídeo com OpenCV

Este projeto é uma ferramenta desenvolvida em Python para manipulação de imagens estáticas e processamento de vídeo em tempo real. O sistema é modular e permite aplicar filtros, realizar operações aritméticas e adicionar stickers interativos.

## 👥 Autores

* **Rodrigo Felitti**
* **Eduardo Arsand**
* **Augusto Hoff**

---

## 🚀 Funcionalidades

1.  **Filtros de Imagem:** Gaussian, Box, Median, Sharpen, Laplacian, Sobel, Canny, Threshold, Grayscale e Separação de Canais (RGB).
2.  **Operações Aritméticas:** Adição, Subtração, Multiplicação e Blending (mistura) entre duas imagens.
3.  **Stickers Interativos:** Aplicação de imagens com transparência (PNG) usando o mouse.
4.  **Webcam em Tempo Real:** Aplicação de todos os filtros na transmissão da câmera ao vivo.
5.  **I/O Robusto:** Carregamento e salvamento de imagens com verificação de erros e criação automática de diretórios.

## 📦 Pré-requisitos

Certifique-se de ter o Python instalado. As dependências do projeto são:

```bash
pip install opencv-python numpy