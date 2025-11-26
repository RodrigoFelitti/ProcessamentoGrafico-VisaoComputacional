import cv2
import numpy as np

#imagem do sticker
def load_sticker(path):
    sticker = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if sticker is None:
        raise ValueError(f"Erro ao carregar sticker: {path}")

    if sticker.shape[2] == 3:
        #cria canal alfa cheio se não houver
        alpha = np.ones((sticker.shape[0], sticker.shape[1]), dtype=np.uint8) * 255
        sticker = np.dstack([sticker, alpha])

    return sticker

def overlay_sticker(base_image, sticker, position):
    """
    base_image: imagem original (BGR) - MODIFICADA IN-PLACE
    sticker: imagem BGRA
    position: (x, y) topo-esquerda do sticker
    """
    x, y = position
    h, w = sticker.shape[:2]

    #evitar sair do limite
    if x >= base_image.shape[1] or y >= base_image.shape[0]:
        return base_image  # fora da imagem → ignora

    #cálculos de corte para bordas
    #se x < 0 (sticker saindo pela esquerda), cortar o início do sticker
    sticker_x_start = 0
    sticker_y_start = 0
    
    if x < 0:
        sticker_x_start = -x
        x = 0
    if y < 0:
        sticker_y_start = -y
        y = 0

    x_end = min(x + w - sticker_x_start, base_image.shape[1])
    y_end = min(y + h - sticker_y_start, base_image.shape[0])

    #se o corte resultou em tamanho 0 ou negativo, aborta
    if x_end <= x or y_end <= y:
        return base_image

    #recortar sticker
    sticker_crop = sticker[sticker_y_start : sticker_y_start + (y_end - y), 
                           sticker_x_start : sticker_x_start + (x_end - x)]

    #separar canais
    sticker_rgb = sticker_crop[:, :, :3]
    alpha = sticker_crop[:, :, 3] / 255.0  # normalize 0–1
    alpha = alpha[:, :, np.newaxis]

    roi = base_image[y:y_end, x:x_end]

    #mistura BGR + sticker RGB usando alpha
    blended = (alpha * sticker_rgb + (1 - alpha) * roi).astype(np.uint8)

    base_image[y:y_end, x:x_end] = blended

    return base_image


#clique do mouse
def apply_stickers_interactive(image, sticker_path):
    try:
        sticker = load_sticker(sticker_path)
    except Exception as e:
        print(e)
        return image

    #cópias e informação de estado
    original_state = image.copy()
    canvas = image.copy()
    
    window_name = "Clique para adicionar Sticker (Enter: Salvar | R: Reset | ESC: Cancelar)"
    cv2.namedWindow(window_name)

    #controle
    st_h, st_w = sticker.shape[:2]

    #callback do mouse
    def mouse_callback(event, x, y, flags, param):
        nonlocal canvas
        if event == cv2.EVENT_LBUTTONDOWN:
            #centraliza sticker na posição do mouse
            pos_x = x - (st_w // 2)
            pos_y = y - (st_h // 2)
            
            #aplica sticker
            overlay_sticker(canvas, sticker, (pos_x, pos_y))
            cv2.imshow(window_name, canvas)

    cv2.setMouseCallback(window_name, mouse_callback)

    print("\n--- MODO STICKER INTERATIVO ---")
    print(" [Mouse Click] Colar sticker")
    print(" [R] Resetar imagem (limpar stickers)")
    print(" [ENTER] Confirmar e salvar")
    print(" [ESC] Cancelar alterações")
    
    cv2.imshow(window_name, canvas)

    #loop para mais de um sticker
    while True:
        key = cv2.waitKey(1) & 0xFF

        #enter
        if key == 13:
            cv2.destroyWindow(window_name)
            return canvas
        
        #esc
        elif key == 27:
            cv2.destroyWindow(window_name)
            print("Operação cancelada.")
            return original_state

        #r
        elif key == ord('r') or key == ord('R'):
            canvas = original_state.copy()
            cv2.imshow(window_name, canvas)
            print("Stickers limpos.")
    
    return canvas