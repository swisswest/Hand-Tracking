#!/usr/bin/env python3
"""
Hand Tracking Programm mit OpenCV
Dieses Programm nutzt die Webcam, um Handbewegungen zu verfolgen.
Es erkennt hautfarbene Bereiche und zeigt die Bewegung in Echtzeit an.

Steuerung:
- 'q' zum Beenden
- 's' zum Kalibrieren der Hautfarbe (klicke auf deine Hand)
- 'r' zum Zurücksetzen der Kalibrierung
"""

import cv2
import numpy as np
import time

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Hautfarben-Bereich in HSV (Standardwerte für helle Haut)
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Tracking-Variablen
        self.hand_positions = []
        self.max_trail_length = 20
        self.calibrated = False
        
        # Mouse Callback für Hautkalibrierung
        self.calibrating = False
        
    def mouse_callback(self, event, x, y, flags, param):
        """Callback-Funktion für Mausklicks zur Hautkalibrierung"""
        if event == cv2.EVENT_LBUTTONDOWN and self.calibrating:
            hsv = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)
            pixel_hsv = hsv[y, x]
            
            # Erweitere den Bereich um den geklickten Pixel
            h, s, v = pixel_hsv
            self.lower_skin = np.array([max(0, h-10), 50, 50], dtype=np.uint8)
            self.upper_skin = np.array([min(179, h+10), 255, 255], dtype=np.uint8)
            
            print(f"Neue Hautfarbe kalibriert: HSV({h}, {s}, {v})")
            print(f"Bereich: {self.lower_skin} bis {self.upper_skin}")
            self.calibrated = True
            self.calibrating = False
    
    def detect_hand(self, frame):
        """Erkennt die Hand basierend auf Hautfarbe"""
        # Konvertiere zu HSV für bessere Farbsegmentierung
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Erstelle Maske für Hautfarbe
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Anwenden von morphologischen Operationen zum Entfernen von Rauschen
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Gaussian Blur zum Glätten
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        return mask
    
    def find_hand_center(self, mask):
        """Findet den Mittelpunkt der größten hautfarbenen Region"""
        # Finde Konturen
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Finde die größte Kontur (wahrscheinlich die Hand)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Berechne den Schwerpunkt nur wenn die Kontur groß genug ist
            if cv2.contourArea(largest_contour) > 1000:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy), largest_contour
        
        return None, None
    
    def draw_trail(self, frame):
        """Zeichnet die Bewegungsspur der Hand"""
        for i in range(1, len(self.hand_positions)):
            # Farbverlauf von rot zu grün basierend auf der Zeitlinie
            alpha = i / len(self.hand_positions)
            color = (int(255 * (1-alpha)), int(255 * alpha), 0)
            thickness = max(1, int(5 * alpha))
            
            cv2.line(frame, self.hand_positions[i-1], self.hand_positions[i], color, thickness)
    
    def draw_info(self, frame):
        """Zeichnet Informationen auf das Bild"""
        # Status-Informationen
        status = "Kalibriert" if self.calibrated else "Nicht kalibriert"
        cv2.putText(frame, f"Status: {status}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if self.calibrated else (0, 0, 255), 2)
        
        # Anweisungen
        instructions = [
            "Steuerung:",
            "'s' - Hautfarbe kalibrieren",
            "'r' - Zuruecksetzen", 
            "'q' - Beenden"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, frame.shape[0] - 80 + i*20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Anzahl der getrackteten Positionen
        if self.hand_positions:
            cv2.putText(frame, f"Positionen: {len(self.hand_positions)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    def run(self):
        """Hauptschleife des Hand-Trackers"""
        print("Hand Tracking gestartet!")
        print("Drücke 's' und klicke auf deine Hand um die Hautfarbe zu kalibrieren")
        print("Drücke 'q' zum Beenden")
        
        # Erstelle Fenster und setze Mouse Callback
        cv2.namedWindow('Hand Tracking')
        cv2.setMouseCallback('Hand Tracking', self.mouse_callback)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Fehler beim Lesen der Webcam!")
                break
            
            # Drehe das Bild um 180° für natürlichere Bewegung
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            self.current_frame = frame.copy()
            
            # Hand-Erkennung
            mask = self.detect_hand(frame)
            hand_center, hand_contour = self.find_hand_center(mask)
            
            if hand_center:
                # Füge Position zur Spur hinzu
                self.hand_positions.append(hand_center)
                
                # Begrenze die Länge der Spur
                if len(self.hand_positions) > self.max_trail_length:
                    self.hand_positions.pop(0)
                
                # Zeichne Hand-Kontur
                if hand_contour is not None:
                    cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
                
                # Zeichne Handzentrum
                cv2.circle(frame, hand_center, 10, (255, 0, 0), -1)
                cv2.circle(frame, hand_center, 15, (255, 255, 255), 2)
            
            # Zeichne Bewegungsspur
            self.draw_trail(frame)
            
            # Zeichne Informationen
            self.draw_info(frame)
            
            # Zeige Kalibrierungs-Status
            if self.calibrating:
                cv2.putText(frame, "Klicke auf deine Hand!", (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Zeige das Ergebnis
            cv2.imshow('Hand Tracking', frame)
            
            # Zeige auch die Maske (optional)
            cv2.imshow('Hautmaske', mask)
            
            # Tastatur-Input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                print("Kalibrierungsmodus aktiviert. Klicke auf deine Hand.")
                self.calibrating = True
            elif key == ord('r'):
                print("Kalibrierung zurückgesetzt.")
                self.calibrated = False
                self.hand_positions = []
                # Setze Standardwerte zurück
                self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
                self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Aufräumen
        self.cap.release()
        cv2.destroyAllWindows()
        print("Hand Tracking beendet.")

def main():
    """Hauptfunktion"""
    try:
        tracker = HandTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\nProgramm durch Benutzer beendet.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
