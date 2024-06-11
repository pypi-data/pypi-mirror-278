import cv2

class DetectaFormas:
    def detectarFormas(self, rutaImagen):
        # Cargar la imagen
        src = cv2.imread(rutaImagen)

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        # Aplicar desenfoque para suavizar la imagen
        gray = cv2.blur(gray, (3, 3))

        # Detectar los bordes usando Canny
        edges = cv2.Canny(gray, 50, 150)

        # Encontrar contornos
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        formas = []

        # Iterar sobre los contornos detectados
        for contour in contours:
            # Calcular el perímetro del contorno
            perimeter = cv2.arcLength(contour, True)

            # Aproximar el contorno a una forma más simple
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            # Clasificar la forma del contorno
            if len(approx) == 2:
                formas.append("linea")
            if len(approx) == 3:
                formas.append("triangulo")
            elif len(approx) == 4:
                formas.append("cuadrado")
            elif len(approx) == 5:
                formas.append("pentagono")
            elif len(approx) == 6:
                formas.append("hexagono")
            elif len(approx) == 7:
                formas.append("heptagono")
            elif len(approx) >= 8:
                formas.append("circulo")
            else:
                formas.append("forma desconocida")

        return formas