import cv2
from src.core import filters

#Mudança de filtros pelo teclado
def run_webcam_filters():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao iniciar webcam. Verifique a conexão.")
        return

    #variavel de estado
    current_filter = None
    
    current_channel = 'r' 

    print("\n--- CONTROLES DA WEBCAM ---")
    print(" [0] Normal (Limpar)")
    print(" [1] Gaussian   [2] Box       [3] Median")
    print(" [4] Sharpen    [5] Laplacian [6] Sobel")
    print(" [7] Grayscale  [8] Threshold [9] Canny")
    print(" [R/G/B] Canais de cor específicos")
    print(" [Q] Sair")
    print("---------------------------")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha na captura do frame.")
            break

        #aplicação dos filtros
        if current_filter == "gaussian":
            frame = filters.apply_gaussian(frame)
        
        elif current_filter == "box":
            frame = filters.apply_box(frame)
        
        elif current_filter == "median":
            frame = filters.apply_median(frame)
        
        elif current_filter == "sharpen":
            frame = filters.apply_sharpen(frame)
        
        elif current_filter == "laplacian":
            frame = filters.apply_laplacian(frame)
        
        elif current_filter == "sobel":
            frame = filters.apply_sobel(frame)
        
        elif current_filter == "gray":
            frame = filters.to_grayscale(frame)
        
        elif current_filter == "channel":
            frame = filters.select_channel(frame, current_channel)
        
        elif current_filter == "threshold":
            frame = filters.apply_threshold(frame)
        
        elif current_filter == "canny":
            frame = filters.apply_canny(frame)

        #texto para identificar o filtro usando função do opencv
        label = f"Filtro: {current_filter if current_filter else 'Normal'}"
        if current_filter == "channel":
            label += f" ({current_channel.upper()})"
            
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Webcam - Pressione Q para sair", frame)

        #leitura do teclado
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        
        elif key == ord('0'): current_filter = None
        elif key == ord('1'): current_filter = "gaussian"
        elif key == ord('2'): current_filter = "box"
        elif key == ord('3'): current_filter = "median"
        elif key == ord('4'): current_filter = "sharpen"
        elif key == ord('5'): current_filter = "laplacian"
        elif key == ord('6'): current_filter = "sobel"
        elif key == ord('7'): current_filter = "gray"
        elif key == ord('8'): current_filter = "threshold"
        elif key == ord('9'): current_filter = "canny"
        
        elif key == ord('r'): 
            current_filter = "channel"
            current_channel = 'r'
        elif key == ord('g'): 
            current_filter = "channel"
            current_channel = 'g'
        elif key == ord('b'): 
            current_filter = "channel"
            current_channel = 'b'

    cap.release()
    cv2.destroyAllWindows()