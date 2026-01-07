import threading
from tkinter import simpledialog, messagebox

# Try importing libraries, set flag if failed
try:
    import cv2
    from pyzbar.pyzbar import decode
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

class BarcodeScanner:
    def __init__(self):
        self.camera_index = 0
        self.running = False
        
    def scan_single(self):
        """
        Attempts to open camera and scan a single barcode.
        Returns the barcode string or None if failed/cancelled.
        """
        if not HAS_LIBS:
            return self.manual_input("Librerías de escáner (opencv-python, pyzbar) no encontradas.")

        try:
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                raise Exception("Camera not found")

            # Simple UI simulation using OpenCV window
            detected_code = None
            
            while True:
                ret, frame = cap.read()
                if not ret: break
                
                # Decode
                decoded_objects = decode(frame)
                for obj in decoded_objects:
                    detected_code = obj.data.decode('utf-8')
                    # Draw rect
                    (x, y, w, h) = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, detected_code, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                cv2.imshow("Escáner de Código de Barras (Presione 'q' para salir)", frame)
                
                if detected_code:
                    cv2.waitKey(500) # Show success briefly
                    break
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            return detected_code

        except Exception as e:
            return self.manual_input(f"Error de Cámara: {str(e)}")

    def manual_input(self, reason):
        # Fallback to manual entry
        return simpledialog.askstring("Escáner Manual", f"{reason}\n\nIngrese Código/ID manualmente:")


# Mock for systems without Camera
class MockScanner:
    def scan_single(self):
        return simpledialog.askstring("Simulador de Escáner", "[MODO SIMULACIÓN]\nIngrese código de producto:")
