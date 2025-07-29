#!/usr/bin/env python3
"""
Test-Script für Gesten-Sound-Bot
Überprüft ob alle erforderlichen Pakete installiert sind und das System funktioniert.
"""

import sys
import importlib

def test_imports():
    """Testet ob alle erforderlichen Pakete importiert werden können"""
    required_packages = [
        ('cv2', 'opencv-python'),
        ('mediapipe', 'mediapipe'),
        ('pygame', 'pygame'),
        ('numpy', 'numpy'),
    ]
    
    print("🔍 Teste Python-Pakete...")
    
    missing_packages = []
    
    for package, pip_name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - FEHLT")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n❌ Fehlende Pakete: {', '.join(missing_packages)}")
        print(f"Installation: pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n✅ Alle Pakete verfügbar!")
        return True

def test_camera():
    """Testet Kamera-Zugriff"""
    print("\n📹 Teste Kamera-Zugriff...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Kamera kann nicht geöffnet werden")
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print("✅ Kamera funktioniert!")
            print(f"   Auflösung: {frame.shape[1]}x{frame.shape[0]}")
            return True
        else:
            print("❌ Kein Kamera-Frame erhalten")
            return False
            
    except Exception as e:
        print(f"❌ Kamera-Fehler: {e}")
        return False

def test_mediapipe():
    """Testet MediaPipe Hand-Tracking"""
    print("\n👋 Teste MediaPipe Hand-Tracking...")
    
    try:
        import mediapipe as mp
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        
        print("✅ MediaPipe Hand-Tracking initialisiert!")
        hands.close()
        return True
        
    except Exception as e:
        print(f"❌ MediaPipe-Fehler: {e}")
        return False

def test_audio():
    """Testet Audio-System"""
    print("\n🔊 Teste Audio-System...")
    
    try:
        import pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        print("✅ Pygame Audio-System initialisiert!")
        
        # Teste ob pycaw verfügbar ist (optional)
        try:
            import pycaw
            print("✅ Pycaw für Audio-Kontrolle verfügbar")
        except ImportError:
            print("⚠️  Pycaw nicht verfügbar (optional für Audio-Kontrolle)")
        
        pygame.mixer.quit()
        return True
        
    except Exception as e:
        print(f"❌ Audio-Fehler: {e}")
        return False

def test_gesture_detection():
    """Testet Gesten-Erkennung mit Dummy-Daten"""
    print("\n🤖 Teste Gesten-Erkennung...")
    
    try:
        # Importiere die Hauptklasse
        import sys
        import os
        
        # Füge aktuelles Verzeichnis zum Python-Pfad hinzu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Teste Import der Hauptklasse
        from gesture_sound_bot import HandGestureDetector, GestureType
        
        detector = HandGestureDetector()
        print("✅ Gesten-Detektor erstellt!")
        
        # Teste Enum
        gestures = list(GestureType)
        print(f"✅ {len(gestures)} Gesten-Typen verfügbar:")
        for gesture in gestures:
            print(f"   - {gesture.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gesten-Erkennungs-Fehler: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests"""
    print("🚀 Gesten-Sound-Bot System-Test")
    print("=" * 40)
    
    tests = [
        ("Paket-Import", test_imports),
        ("Kamera", test_camera),
        ("MediaPipe", test_mediapipe),
        ("Audio", test_audio),
        ("Gesten-Erkennung", test_gesture_detection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Unerwarteter Fehler in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test-Ergebnisse:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ BESTANDEN" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(tests)} Tests bestanden")
    
    if passed == len(tests):
        print("\n🎉 System bereit! Du kannst gesture_sound_bot.py starten.")
    else:
        print("\n⚠️  System nicht vollständig bereit. Behebe die Fehler oben.")
        print("\nHäufige Lösungen:")
        print("- pip install -r requirements.txt")
        print("- Webcam anschließen und Berechtigungen prüfen")
        print("- VB-Audio Cable installieren")
        print("- Python neu starten")

if __name__ == "__main__":
    main()
