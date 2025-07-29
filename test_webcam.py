#!/usr/bin/env python3
"""
Webcam-Test Programm
Dieses einfache Programm testet, ob die Webcam verfügbar ist.
"""

import cv2
import sys

def test_webcam():
    print("Teste Webcam-Verfügbarkeit...")
    
    # Versuche Webcam zu öffnen
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Fehler: Webcam konnte nicht geöffnet werden!")
        print("Mögliche Lösungen:")
        print("- Überprüfe, ob die Webcam angeschlossen ist")
        print("- Stelle sicher, dass keine andere App die Webcam verwendet")
        print("- Versuche einen anderen Index (1, 2, etc.)")
        return False
    
    print("✅ Webcam erfolgreich geöffnet!")
    
    # Teste Frame-Aufnahme
    ret, frame = cap.read()
    
    if ret:
        height, width = frame.shape[:2]
        print(f"✅ Webcam funktioniert! Auflösung: {width}x{height}")
        print("Drücke 'q' um den Test zu beenden...")
        
        # Zeige Live-Video für 10 Sekunden oder bis 'q' gedrückt wird
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Fehler beim Lesen des Frames")
                break
            
            # Drehe das Bild um 180°
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            
            # Füge Text hinzu
            cv2.putText(frame, "Webcam Test - Druecke 'q' zum Beenden", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Aufloesung: {width}x{height}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Webcam Test', frame)
            
            # Beenden mit 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Webcam-Test erfolgreich abgeschlossen!")
        return True
    else:
        print("❌ Fehler: Konnte keinen Frame von der Webcam lesen")
        cap.release()
        return False

if __name__ == "__main__":
    if test_webcam():
        print("\n🎉 Deine Webcam ist bereit für das Hand-Tracking!")
        print("Du kannst jetzt das Hand-Tracking-Programm starten:")
        print("  python hand_tracking.py")
        print("  python advanced_hand_tracking.py")
    else:
        print("\n❌ Webcam-Problem erkannt. Bitte behebe das Problem, bevor du das Hand-Tracking startest.")
        sys.exit(1)
