import cv2
import os

#Função de carregar a imagem se existir
def load_image(path):
    if not os.path.exists(path):
        print(f"Erro: Arquivo '{path}' não encontrado.")
        return None
    
    image = cv2.imread(path)
    if image is None:
        print(f"Erro: Não foi possível decodificar a imagem '{path}'.")
    return image

#Carrega uma segunda imagem e a redimensiona para o tamanho da base.
def load_second_image(path, base_image):
    img2 = load_image(path)
    if img2 is None:
        return None
    
    #Redimensiona img2 para ter o mesmo tamanho da imagem base (para usar em operations)
    return cv2.resize(img2, (base_image.shape[1], base_image.shape[0]))

#Salva a imagem
def save_image(path, image):
    if image is None:
        print("Erro: Nenhuma imagem em memória para salvar.")
        return False

    path = path.strip()
    
    #salva como .jpg
    filename, ext = os.path.splitext(path)
    if not ext:
        print("Aviso: Extensão não fornecida. Adicionando '.jpg' automaticamente.")
        path = path + ".jpg"
    
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Diretório '{directory}' criado.")
        except OSError as e:
            print(f"Erro ao criar diretório: {e}")
            return False

    success = cv2.imwrite(path, image)

    if success:
        # Usa abspath para mostrar onde o arquivo foi parar exatamente
        full_path = os.path.abspath(path)
        print(f"Sucesso! Imagem salva em: {full_path}")
        return True
    else:
        print("Erro: O OpenCV falhou ao salvar o arquivo. Verifique permissões ou o caminho.")
        return False