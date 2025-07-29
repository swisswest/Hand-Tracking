#!/usr/bin/env python3
"""
Erweiterte Hand Tracking mit Gesten-Erkennung
Dieses Programm erkennt nicht nur Handbewegungen, sondern auch einfache Gesten.

Features:
- Hand-Tracking mit Bewegungsspur
- Geschwindigkeitsmessung
- Einfache Gesten-Erkennung (Kreis, Linie)
- Verschiedene Visualisierungsmodi

Steuerung:
- 'q' zum Beenden
- 's' zum Kalibrieren der Hautfarbe
- 'r' zum Zurücksetzen
- 'c' zum Löschen der Spur
- 'm' zum Wechseln des Modus
"""

import cv2
import numpy as np
import time
import math

class AdvancedHandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Hautfarben-Bereich in HSV
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Tracking-Variablen
        self.hand_positions = []
        self.timestamps = []
        self.max_trail_length = 50
        self.calibrated = False
        self.calibrating = False
        
        # Geschwindigkeits-Tracking
        self.velocities = []
        self.max_velocity = 0
        
        # Gesten-Erkennung
        self.gesture_buffer = []
        self.current_gesture = "Keine"
        self.gesture_threshold = 30  # Mindestanzahl Punkte für Geste
        
        # Display-Modi
        self.display_modes = ["Normal", "Spur", "Geschwindigkeit", "Gesten"]
        self.current_mode = 0
        
    def mouse_callback(self, event, x, y, flags, param):
        """Callback für Hautkalibrierung"""
        if event == cv2.EVENT_LBUTTONDOWN and self.calibrating:
            hsv = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)
            pixel_hsv = hsv[y, x]
            
            h, s, v = pixel_hsv
            self.lower_skin = np.array([max(0, h-15), 50, 50], dtype=np.uint8)
            self.upper_skin = np.array([min(179, h+15), 255, 255], dtype=np.uint8)
            
            print(f"Neue Hautfarbe kalibriert: HSV({h}, {s}, {v})")
            self.calibrated = True
            self.calibrating = False
    
    def detect_hand(self, frame):
        """Erweiterte Hand-Erkennung"""
        # Konvertiere zu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Erstelle Hautmaske
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Erweiterte morphologische Operationen
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Median Blur für bessere Glättung
        mask = cv2.medianBlur(mask, 15)
        
        return mask
    
    def find_hand_features(self, mask):
        """Findet Hand-Features inklusive Fingerspitzen"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None, None
        
        # Größte Kontur finden
        largest_contour = max(contours, key=cv2.contourArea)
        
        if cv2.contourArea(largest_contour) < 2000:
            return None, None, None
        
        # Schwerpunkt berechnen
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return None, None, None
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        center = (cx, cy)
        
        # Konvexe Hülle und Defekte finden (für Fingererkennung)
        hull = cv2.convexHull(largest_contour, returnPoints=False)
        if len(hull) > 3:
            defects = cv2.convexityDefects(largest_contour, hull)
            fingertips = []
            
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(largest_contour[s][0])
                    end = tuple(largest_contour[e][0])
                    far = tuple(largest_contour[f][0])
                    
                    # Berechne Winkel
                    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    
                    if b != 0 and c != 0:
                        angle = math.acos((b**2 + c**2 - a**2) / (2*b*c)) * 180 / math.pi
                        
                        # Wenn Winkel klein genug, ist es wahrscheinlich ein Finger
                        if angle <= 90 and d > 10000:
                            fingertips.append(start)
        else:
            fingertips = []
        
        return center, largest_contour, fingertips
    
    def calculate_velocity(self, current_pos):
        """Berechnet die Geschwindigkeit der Hand"""
        current_time = time.time()
        
        if len(self.hand_positions) > 1 and len(self.timestamps) > 1:
            prev_pos = self.hand_positions[-1]
            prev_time = self.timestamps[-1]
            
            # Berechne Distanz und Zeit
            dx = current_pos[0] - prev_pos[0]
            dy = current_pos[1] - prev_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            time_diff = current_time - prev_time
            
            if time_diff > 0:
                velocity = distance / time_diff
                self.velocities.append(velocity)
                
                # Begrenze Geschwindigkeitspuffer
                if len(self.velocities) > 10:
                    self.velocities.pop(0)
                
                # Update max Geschwindigkeit
                if velocity > self.max_velocity:
                    self.max_velocity = velocity
                
                return velocity
        
        return 0
    
    def detect_gesture(self):
        """Einfache Gesten-Erkennung"""
        if len(self.gesture_buffer) < self.gesture_threshold:
            return "Sammle Daten..."
        
        points = np.array(self.gesture_buffer[-self.gesture_threshold:])
        
        # Berechne Bounding Box
        x_coords = points[:, 0]
        y_coords = points[:, 1]
        width = np.max(x_coords) - np.min(x_coords)
        height = np.max(y_coords) - np.min(y_coords)
        
        # Klassifiziere Geste basierend auf Form
        if width < 50 and height < 50:
            return "Punkt/Stopp"
        elif width > height * 2:
            return "Horizontale Linie"
        elif height > width * 2:
            return "Vertikale Linie"
        elif abs(width - height) < 30:
            # Prüfe auf Kreis
            center_x = np.mean(x_coords)
            center_y = np.mean(y_coords)
            radius = min(width, height) / 2
            
            # Berechne Abweichung vom Kreis
            deviations = []
            for point in points:
                expected_radius = math.sqrt((point[0] - center_x)**2 + (point[1] - center_y)**2)
                deviations.append(abs(expected_radius - radius))
            
            avg_deviation = np.mean(deviations)
            if avg_deviation < radius * 0.3:
                return "Kreis"
            else:
                return "Unregelmäßig"
        
        return "Unbekannt"
    
    def draw_advanced_info(self, frame):
        """Zeichnet erweiterte Informationen"""
        mode = self.display_modes[self.current_mode]
        
        # Header
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)
        cv2.putText(frame, f"Modus: {mode}", (10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Status
        status = "Kalibriert" if self.calibrated else "Nicht kalibriert"
        color = (0, 255, 0) if self.calibrated else (0, 0, 255)
        cv2.putText(frame, f"Status: {status}", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Geschwindigkeit
        if self.velocities:
            current_velocity = self.velocities[-1] if self.velocities else 0
            cv2.putText(frame, f"Geschw: {current_velocity:.1f} px/s", (300, 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(frame, f"Max: {self.max_velocity:.1f} px/s", (300, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Geste
        cv2.putText(frame, f"Geste: {self.current_gesture}", (10, 75), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        # Footer mit Anweisungen
        footer_y = frame.shape[0] - 120
        cv2.rectangle(frame, (0, footer_y), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
        
        instructions = [
            "Steuerung: 's'-Kalibrierung | 'r'-Reset | 'c'-Spur löschen | 'm'-Modus | 'q'-Beenden",
            f"Verfolgte Punkte: {len(self.hand_positions)}",
            f"Gesten-Puffer: {len(self.gesture_buffer)}"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, footer_y + 25 + i*20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_trail_advanced(self, frame):
        """Erweiterte Trail-Visualisierung"""
        if len(self.hand_positions) < 2:
            return
        
        mode = self.display_modes[self.current_mode]
        
        if mode == "Spur" or mode == "Normal":
            # Farbverlauf basierend auf Geschwindigkeit
            for i in range(1, len(self.hand_positions)):
                alpha = i / len(self.hand_positions)
                
                if mode == "Geschwindigkeit" and i < len(self.velocities):
                    # Farbe basierend auf Geschwindigkeit
                    velocity = self.velocities[i-1] if i-1 < len(self.velocities) else 0
                    normalized_vel = min(velocity / max(self.max_velocity, 1), 1)
                    color = (int(255 * (1-normalized_vel)), 0, int(255 * normalized_vel))
                else:
                    # Standard Farbverlauf
                    color = (int(255 * (1-alpha)), int(255 * alpha), 0)
                
                thickness = max(1, int(8 * alpha))
                cv2.line(frame, self.hand_positions[i-1], self.hand_positions[i], color, thickness)
        
        elif mode == "Gesten":
            # Zeichne Gesten-Puffer
            if len(self.gesture_buffer) > 1:
                for i in range(1, len(self.gesture_buffer)):
                    cv2.line(frame, self.gesture_buffer[i-1], self.gesture_buffer[i], (0, 255, 255), 3)
    
    def run(self):
        """Hauptschleife des erweiterten Hand-Trackers"""
        print("Erweitertes Hand Tracking gestartet!")
        print("Drücke 's' und klicke auf deine Hand zur Kalibrierung")
        print("Drücke 'm' zum Wechseln der Anzeigemodi")
        
        cv2.namedWindow('Advanced Hand Tracking')
        cv2.setMouseCallback('Advanced Hand Tracking', self.mouse_callback)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Fehler beim Lesen der Webcam!")
                break
            
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            self.current_frame = frame.copy()
            
            # Hand-Erkennung
            mask = self.detect_hand(frame)
            hand_center, hand_contour, fingertips = self.find_hand_features(mask)
            
            if hand_center:
                current_time = time.time()
                
                # Geschwindigkeit berechnen
                velocity = self.calculate_velocity(hand_center)
                
                # Position hinzufügen
                self.hand_positions.append(hand_center)
                self.timestamps.append(current_time)
                self.gesture_buffer.append(hand_center)
                
                # Buffer begrenzen
                if len(self.hand_positions) > self.max_trail_length:
                    self.hand_positions.pop(0)
                    self.timestamps.pop(0)
                
                if len(self.gesture_buffer) > self.gesture_threshold * 2:
                    self.gesture_buffer.pop(0)
                
                # Geste erkennen
                self.current_gesture = self.detect_gesture()
                
                # Visualisierung
                if hand_contour is not None:
                    cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
                
                # Handzentrum
                cv2.circle(frame, hand_center, 12, (255, 0, 0), -1)
                cv2.circle(frame, hand_center, 18, (255, 255, 255), 3)
                
                # Fingerspitzen
                for fingertip in fingertips:
                    cv2.circle(frame, fingertip, 8, (0, 0, 255), -1)
                
                # Geschwindigkeitsanzeige am Cursor
                if velocity > 0:
                    cv2.putText(frame, f"{velocity:.0f}", 
                               (hand_center[0] + 20, hand_center[1] - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Erweiterte Trail-Visualisierung
            self.draw_trail_advanced(frame)
            
            # Erweiterte Informationen
            self.draw_advanced_info(frame)
            
            # Kalibrierungs-Hinweis
            if self.calibrating:
                cv2.putText(frame, "Klicke auf deine Hand!", 
                           (frame.shape[1]//2 - 150, frame.shape[0]//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            
            # Anzeige
            cv2.imshow('Advanced Hand Tracking', frame)
            
            # Tastatur-Input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                print("Kalibrierungsmodus aktiviert.")
                self.calibrating = True
            elif key == ord('r'):
                print("Alles zurückgesetzt.")
                self.calibrated = False
                self.hand_positions = []
                self.timestamps = []
                self.velocities = []
                self.gesture_buffer = []
                self.max_velocity = 0
                self.current_gesture = "Keine"
            elif key == ord('c'):
                print("Spur gelöscht.")
                self.hand_positions = []
                self.gesture_buffer = []
            elif key == ord('m'):
                self.current_mode = (self.current_mode + 1) % len(self.display_modes)
                print(f"Modus gewechselt zu: {self.display_modes[self.current_mode]}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        print("Erweitertes Hand Tracking beendet.")

def main():
    """Hauptfunktion"""
    try:
        tracker = AdvancedHandTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\nProgramm durch Benutzer beendet.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
