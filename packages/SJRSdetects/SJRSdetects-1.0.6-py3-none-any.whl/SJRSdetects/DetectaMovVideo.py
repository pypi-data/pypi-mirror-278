import cv2
import numpy as np

class DetectaMovVideo:
    def __init__(self):
        self.prevFrame = None
        self.prevCenter = None

    def detectarMovimiento(self, videoPath):
        resultados = []

        # Abrir el video
        capture = cv2.VideoCapture(videoPath)
        if not capture.isOpened():
            resultados.append("No se pudo abrir el video")
            return resultados

        while True:
            ret, frame = capture.read()
            if not ret:
                break

            # Convertir a escala de grises y difuminar
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Si es el primer cuadro, guardar y continuar
            if self.prevFrame is None:
                self.prevFrame = gray
                continue

            # Calcular la diferencia absoluta entre el cuadro actual y el anterior
            frameDelta = cv2.absdiff(self.prevFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # Encontrar contornos en el umbral
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue

                # Calcular el centroide del contorno
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center = (cX, cY)

                # Si es el primer centro, guardar y continuar
                if self.prevCenter is None:
                    self.prevCenter = center
                    continue

                # Calcular la dirección del movimiento
                dx = center[0] - self.prevCenter[0]
                dy = center[1] - self.prevCenter[1]

                if abs(dx) > 2 and abs(dy) > 2:
                    if dx > 0 and dy > 0:
                        resultados.append("\n movimiento en diagonal hacia abajo y a la derecha")
                    elif dx > 0 and dy < 0:
                        resultados.append("\n movimiento en diagonal hacia arriba y a la derecha")
                    elif dx < 0 and dy > 0:
                        resultados.append("\n movimiento en diagonal hacia abajo y a la izquierda")
                    elif dx < 0 and dy < 0:
                        resultados.append("\n movimiento en diagonal hacia arriba y a la izquierda")

                elif abs(dx) > 2:
                    resultados.append("\n movimiento " + ("hacia la derecha" if dx > 0 else "hacia la izquierda"))
                elif abs(dy) > 2:
                    resultados.append("\n movimiento " + ("hacia abajo" if dy > 0 else "hacia arriba"))

                self.prevCenter = center

            self.prevFrame = gray

        capture.release()
        return resultados