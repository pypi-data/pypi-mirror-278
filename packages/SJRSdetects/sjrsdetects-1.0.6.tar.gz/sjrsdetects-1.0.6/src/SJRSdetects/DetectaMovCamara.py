import cv2
import numpy as np

class DetectaMovCamara:
    def __init__(self):
        self.prevFrame = None
        self.prevCenter = None
        self.resultados = None

    def detectarMovimiento(self):
        capture = cv2.VideoCapture(0)
        self.prevFrame = None
        self.prevCenter = None
    
        while True:
            ret, frame = capture.read()
            if not ret:
                break
    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
            if self.prevFrame is None:
                self.prevFrame = gray
                continue
    
            frameDelta = cv2.absdiff(self.prevFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
            direction = None

            frame_count = 0  
            frame_limit = 100  
            
            for contour in contours:
                if frame_count >= frame_limit:  # Verificar si se ha alcanzado el límite
                    break  # Detener el bucle si se alcanza el límite
            
                if cv2.contourArea(contour) < 1500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                center = (x + w / 2, y + h / 2)
            
                if self.prevCenter is None:
                    self.prevCenter = center
                    continue
            
                dx = center[0] - self.prevCenter[0]
                dy = center[1] - self.prevCenter[1]
            
                if abs(dx) > 250 and abs(dy) > 250:
                    direction = "movimiento en diagonal hacia " + ("abajo, derecha" if dx > 0 and dy > 0 else "arriba, derecha" if dx > 0 
                                                                   else "abajo, izquierda" if dy > 0 else "arriba, izquierda")
                elif abs(dx) > 2:
                    direction = "movimiento hacia la " + ("derecha" if dx > 0 else "izquierda")
                elif abs(dy) > 2:
                    direction = "movimiento hacia " + ("abajo" if dy > 0 else "arriba")
                self.prevCenter = center
            
                if direction is not None:
                    yield direction
            
                frame_count += 1  # Incrementar el contador en cada iteración
            
            self.prevFrame = gray
            cv2.waitKey(1500)  # Esperar 1 segundo antes de procesar el siguiente fotograma
        capture.release()
    
    
    def mostrarCamara(self):
        print ("Se esta mostrado la camara")