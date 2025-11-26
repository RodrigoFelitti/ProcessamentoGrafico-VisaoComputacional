import cv2
from src.core import filters, operations, stickers
from src.app.ui import show_menu
from src.app.image_loader import load_image, save_image, load_second_image
from src.app.video import run_webcam_filters
import os

current_image = None
original_image = None


# --------------------------
# Aplicar filtros
# --------------------------
def apply_filter(image, filter_name):
    if filter_name == "gaussian":
        return filters.apply_gaussian(image)
    elif filter_name == "box":
        return filters.apply_box(image)
    elif filter_name == "median":
        return filters.apply_median(image)
    elif filter_name == "sharpen":
        return filters.apply_sharpen(image)
    elif filter_name == "laplacian":
        return filters.apply_laplacian(image)
    elif filter_name == "sobel":
        return filters.apply_sobel(image)
    elif filter_name == "gray":
        return filters.to_grayscale(image)
    elif filter_name == "channel":
        canal = input("Canal (r/g/b): ").strip().lower()
        return filters.select_channel(image, canal)
    elif filter_name == "threshold":
        return filters.apply_threshold(image)
    elif filter_name == "canny":
        return filters.apply_canny(image)
    else:
        print("Filtro inválido.")
        return image


# ==========================
# Helper pós-operação
# ==========================
def pause_and_cleanup():
    """Fecha janelas, limpa buffer OpenCV e espera ENTER."""
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    input("\nPressione ENTER para voltar ao menu...")



# --------------------------
# Menu principal
# --------------------------
def main():
    global current_image, original_image

    while True:
        choice = show_menu()

        # -------------------
        # Carregar imagem
        # -------------------
        if choice == "1":
            path = input("Caminho da imagem: ").strip()
            current_image = load_image(path)

            if current_image is None:
                print("Erro ao carregar a imagem.")
            else:
                original_image = current_image.copy()
                print("Imagem carregada.")

            pause_and_cleanup()

        # -------------------
        # Webcam
        # -------------------
        elif choice == "2":
            # A função agora gerencia todo o ciclo de vida da janela e filtros
            run_webcam_filters()
            
            pause_and_cleanup()

        # -------------------
        # Aplicar filtro
        # -------------------
        elif choice == "3":
            if current_image is None:
                print("Carregue uma imagem primeiro.")
                pause_and_cleanup()
                continue

            print("\nFiltros disponíveis:")
            print("gaussian, box, median, sharpen, laplacian, sobel, gray, channel, threshold, canny\n")

            name = input("Nome do filtro: ").strip().lower()
            print(filters.get_filter_description(name))

            current_image = apply_filter(current_image, name)

            cv2.imshow("Resultado", current_image)
            cv2.waitKey(0)

            pause_and_cleanup()

        # -------------------
        # Operações aritméticas
        # -------------------
        elif choice == "4":
            if current_image is None:
                print("Carregue uma imagem antes de usar operações.")
                pause_and_cleanup()
                continue

            print("\nOperações disponíveis:")
            print("add, subtract, blend, multiply\n")

            op = input("Operação: ").strip().lower()

            path2 = input("Imagem secundária (img2): ")
            img2 = load_second_image(path2, current_image)

            if img2 is None:
                print("Erro ao carregar a segunda imagem.")
                pause_and_cleanup()
                continue

            if op == "add":
                current_image = operations.add_images(current_image, img2)
            elif op == "subtract":
                current_image = operations.subtract_images(current_image, img2)
            elif op == "blend":
                alpha = float(input("Valor de alpha (0 a 1): "))
                current_image = operations.blend(current_image, img2, alpha)
            elif op == "multiply":
                current_image = operations.multiply_images(current_image, img2)
            else:
                print("Operação inválida.")

            cv2.imshow("Resultado", current_image)
            cv2.waitKey(0)

            pause_and_cleanup()

        # -------------------
        # Stickers (Interativo)
        # -------------------
        elif choice == "5":
            if current_image is None:
                print("Carregue uma imagem primeiro.")
                pause_and_cleanup()
                continue

            st_path = input("Caminho do sticker (PNG com alpha): ")
            
            # Chama a nova função interativa
            # Ela retorna a imagem editada ou a original (se cancelar)
            current_image = stickers.apply_stickers_interactive(current_image, st_path)
            
            # Mostra o resultado final (opcional, pois já vemos na interação)
            # Mas útil para confirmar que foi salvo na variável current_image
            cv2.imshow("Resultado Final", current_image)
            cv2.waitKey(0)

            pause_and_cleanup()

            pause_and_cleanup()

        # -------------------
        # Salvar imagem
        # -------------------
        elif choice == "6":
            if current_image is None:
                print("Nenhuma imagem carregada.")
                pause_and_cleanup()
                continue

            out = input("Salvar como (ex: resultado.png): ")
            
            # A função save_image agora cuida de tudo e retorna True/False
            save_image(out, current_image)

            pause_and_cleanup()

        # -------------------
        # Resetar imagem
        # -------------------
        elif choice == "7":
            if original_image is not None:
                current_image = original_image.copy()
                print("Imagem restaurada ao original.")
            else:
                print("Nenhuma imagem carregada.")

            pause_and_cleanup()

        # -------------------
        # Sair
        # -------------------
        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
            pause_and_cleanup()


if __name__ == "__main__":
    main()
