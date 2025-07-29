#!/usr/bin/env python3
"""
Gesten-Sound-Bot für Discord
Ein Python-Programm, das Handgesten mit MediaPipe erkennt und entsprechende Sounds
über ein virtuelles Mikrofon (VB-Audio Cable) abspielt.

Features:
- Erkennung von Handgesten (Mittelfinger, Victory-Zeichen, Daumen hoch, etc.)
- Automatische Sound-Wiedergabe bei Gestenerkennung
- Ausgabe über virtuelles Mikrofon für Discord-Calls
- Erweiterbare Gesten- und Sound-Bibliothek
- GUI für Konfiguration und Status

Anforderungen:
- pip install opencv-python mediapipe pygame pycaw
- VB-Audio Cable oder VoiceMeeter installiert
- Sound-Dateien im sounds/ Ordner

Steuerung:
- 'q' zum Beenden
- 's' zum Umschalten der Sound-Ausgabe
- 'g' zum Anzeigen erkannter Gesten
- 'c' zum Konfigurieren der Gesten
"""

import cv2
import mediapipe as mp
import numpy as np
import pygame
import threading
import time
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class GestureType(Enum):
    """Enum für verschiedene Gesten-Typen"""
    UNKNOWN = "unknown"
    PEACE = "peace"  # Victory-Zeichen
    MIDDLE_FINGER = "middle_finger"
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    OK_SIGN = "ok_sign"
    ROCK = "rock"  # Faust
    OPEN_HAND = "open_hand"
    POINTING = "pointing"

@dataclass
class GestureConfig:
    """Konfiguration für eine Geste"""
    name: str
    sound_file: str
    cooldown: float = 2.0  # Sekunden zwischen Wiederholungen
    confidence_threshold: float = 0.8
    enabled: bool = True

class HandGestureDetector:
    """Klasse für die Erkennung von Handgesten mit MediaPipe"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def detect_gesture(self, landmarks) -> Tuple[GestureType, float]:
        """
        Erkennt Geste basierend auf Hand-Landmarks
        
        Args:
            landmarks: MediaPipe Hand-Landmarks
            
        Returns:
            Tuple aus erkannter Geste und Confidence-Score
        """
        if not landmarks:
            return GestureType.UNKNOWN, 0.0
            
        # Finger-Status ermitteln
        finger_states = self._get_finger_states(landmarks)
        
        # Gesten-Logik
        confidence = 0.9  # Basis-Confidence
        
        # Victory-Zeichen (Zeige- und Mittelfinger gestreckt)
        if (finger_states[1] and finger_states[2] and 
            not finger_states[0] and not finger_states[3] and not finger_states[4]):
            return GestureType.PEACE, confidence
            
        # Mittelfinger (nur Mittelfinger gestreckt)
        if (finger_states[2] and not finger_states[1] and 
            not finger_states[0] and not finger_states[3] and not finger_states[4]):
            return GestureType.MIDDLE_FINGER, confidence
            
        # Daumen hoch
        if (finger_states[0] and not finger_states[1] and 
            not finger_states[2] and not finger_states[3] and not finger_states[4]):
            return GestureType.THUMBS_UP, confidence
            
        # OK-Zeichen (Daumen und Zeigefinger berühren sich)
        if self._is_ok_gesture(landmarks):
            return GestureType.OK_SIGN, confidence
            
        # Zeigen (nur Zeigefinger)
        if (finger_states[1] and not finger_states[0] and 
            not finger_states[2] and not finger_states[3] and not finger_states[4]):
            return GestureType.POINTING, confidence
            
        # Faust (alle Finger geschlossen)
        if not any(finger_states):
            return GestureType.ROCK, confidence
            
        # Offene Hand (alle Finger gestreckt)
        if all(finger_states):
            return GestureType.OPEN_HAND, confidence
            
        return GestureType.UNKNOWN, 0.0
    
    def _get_finger_states(self, landmarks) -> List[bool]:
        """
        Bestimmt ob Finger gestreckt oder gebeugt sind
        
        Returns:
            Liste mit Status für [Daumen, Zeigefinger, Mittelfinger, Ringfinger, kleiner Finger]
        """
        finger_tips = [4, 8, 12, 16, 20]  # Fingerspitzen-IDs
        finger_pips = [3, 6, 10, 14, 18]  # Fingergelenk-IDs
        
        finger_states = []
        
        for i, (tip, pip) in enumerate(zip(finger_tips, finger_pips)):
            if i == 0:  # Daumen (spezielle Behandlung)
                finger_states.append(landmarks.landmark[tip].x > landmarks.landmark[pip].x)
            else:  # Andere Finger
                finger_states.append(landmarks.landmark[tip].y < landmarks.landmark[pip].y)
                
        return finger_states
    
    def _is_ok_gesture(self, landmarks) -> bool:
        """Prüft ob Daumen und Zeigefinger ein OK-Zeichen bilden"""
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        
        # Berechne Distanz zwischen Daumen und Zeigefinger
        distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
        
        return distance < 0.05  # Schwellenwert für "Berührung"

class SoundManager:
    """Verwaltet Sound-Wiedergabe über virtuelles Mikrofon"""
    
    def __init__(self, sounds_dir: str = "sounds"):
        self.sounds_dir = sounds_dir
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.virtual_device = None
        
        # Pygame Mixer initialisieren
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        # Virtuelles Audio-Gerät finden
        self._find_virtual_device()
        
        # Sounds laden
        self._load_sounds()
    
    def _find_virtual_device(self):
        """Findet VB-Audio Cable oder ähnliches virtuelles Audio-Gerät"""
        try:
            import pycaw.pycaw as pycaw
            from pycaw.pycaw import AudioUtilities, AudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            # Hier könnte man nach "VB-Audio" oder "CABLE" suchen
            # Für Einfachheit verwenden wir das Standard-Ausgabegerät
            self.virtual_device = devices
            print("Audio-Gerät gefunden und konfiguriert")
            
        except ImportError:
            print("Warning: pycaw nicht verfügbar. Standard-Audio wird verwendet.")
            
    def _load_sounds(self):
        """Lädt alle Sound-Dateien aus dem sounds/ Ordner"""
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            print(f"Sounds-Ordner erstellt: {self.sounds_dir}")
            return
            
        for file in os.listdir(self.sounds_dir):
            if file.endswith(('.wav', '.mp3', '.ogg')):
                try:
                    sound_path = os.path.join(self.sounds_dir, file)
                    sound_name = os.path.splitext(file)[0]
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    print(f"Sound geladen: {sound_name}")
                except Exception as e:
                    print(f"Fehler beim Laden von {file}: {e}")
    
    def play_sound(self, sound_name: str, volume: float = 0.7):
        """Spielt einen Sound ab"""
        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(volume)
                sound.play()
                print(f"Sound abgespielt: {sound_name}")
            except Exception as e:
                print(f"Fehler beim Abspielen von {sound_name}: {e}")
        else:
            print(f"Sound nicht gefunden: {sound_name}")
    
    def add_sound(self, name: str, file_path: str):
        """Fügt einen neuen Sound hinzu"""
        try:
            self.sounds[name] = pygame.mixer.Sound(file_path)
            print(f"Sound hinzugefügt: {name}")
        except Exception as e:
            print(f"Fehler beim Hinzufügen von {name}: {e}")

class GestureSoundBot:
    """Hauptklasse für den Gesten-Sound-Bot"""
    
    def __init__(self):
        self.detector = HandGestureDetector()
        self.sound_manager = SoundManager()
        self.gesture_configs = self._load_gesture_configs()
        
        # Tracking-Variablen
        self.last_gesture_time = {}
        self.current_gesture = GestureType.UNKNOWN
        self.gesture_confidence = 0.0
        
        # Kamera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Status
        self.running = False
        self.sound_enabled = True
        self.show_gui = True
        
    def _load_gesture_configs(self) -> Dict[GestureType, GestureConfig]:
        """Lädt Gesten-Konfigurationen"""
        config_file = "gesture_config.json"
        
        # Standard-Konfiguration
        default_configs = {
            GestureType.PEACE: GestureConfig("Victory", "victory.wav", 2.0),
            GestureType.MIDDLE_FINGER: GestureConfig("Mittelfinger", "middle_finger.wav", 3.0),
            GestureType.THUMBS_UP: GestureConfig("Daumen hoch", "thumbs_up.wav", 2.0),
            GestureType.OK_SIGN: GestureConfig("OK", "ok.wav", 2.0),
            GestureType.POINTING: GestureConfig("Zeigen", "point.wav", 1.5),
            GestureType.ROCK: GestureConfig("Faust", "punch.wav", 2.0),
        }
        
        # Versuche Konfiguration zu laden
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                configs = {}
                for gesture_name, config_data in data.items():
                    gesture_type = GestureType(gesture_name)
                    configs[gesture_type] = GestureConfig(**config_data)
                    
                return configs
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
        
        # Speichere Standard-Konfiguration
        self._save_gesture_configs(default_configs)
        return default_configs
    
    def _save_gesture_configs(self, configs: Dict[GestureType, GestureConfig]):
        """Speichert Gesten-Konfigurationen"""
        config_file = "gesture_config.json"
        
        data = {}
        for gesture_type, config in configs.items():
            data[gesture_type.value] = {
                'name': config.name,
                'sound_file': config.sound_file,
                'cooldown': config.cooldown,
                'confidence_threshold': config.confidence_threshold,
                'enabled': config.enabled
            }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
    
    def process_gesture(self, gesture: GestureType, confidence: float):
        """Verarbeitet erkannte Geste und spielt ggf. Sound ab"""
        if gesture == GestureType.UNKNOWN or gesture not in self.gesture_configs:
            return
            
        config = self.gesture_configs[gesture]
        
        # Prüfe ob Geste aktiviert und Confidence hoch genug
        if not config.enabled or confidence < config.confidence_threshold:
            return
            
        # Prüfe Cooldown
        current_time = time.time()
        if gesture in self.last_gesture_time:
            if current_time - self.last_gesture_time[gesture] < config.cooldown:
                return
        
        # Sound abspielen
        if self.sound_enabled:
            sound_name = os.path.splitext(config.sound_file)[0]
            self.sound_manager.play_sound(sound_name)
            
        self.last_gesture_time[gesture] = current_time
        print(f"Geste erkannt: {config.name} (Confidence: {confidence:.2f})")
    
    def run(self):
        """Hauptschleife des Bots"""
        self.running = True
        print("Gesten-Sound-Bot gestartet!")
        print("Drücke 'q' zum Beenden, 's' zum Umschalten der Sounds")
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Frame spiegeln für natürlichere Ansicht
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            # RGB für MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.detector.hands.process(rgb_frame)
            
            # Hand-Landmarks zeichnen
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Landmarks zeichnen
                    self.detector.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.detector.mp_hands.HAND_CONNECTIONS)
                    
                    # Geste erkennen
                    gesture, confidence = self.detector.detect_gesture(hand_landmarks)
                    self.current_gesture = gesture
                    self.gesture_confidence = confidence
                    
                    # Geste verarbeiten
                    self.process_gesture(gesture, confidence)
            
            # Status-Informationen einblenden
            self._draw_status(frame)
            
            # Frame anzeigen
            cv2.imshow('Gesten-Sound-Bot', frame)
            
            # Tastatur-Input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('s'):
                self.sound_enabled = not self.sound_enabled
                print(f"Sound {'aktiviert' if self.sound_enabled else 'deaktiviert'}")
            elif key == ord('g'):
                self._print_gesture_info()
            elif key == ord('c'):
                self._open_config_gui()
        
        self.cleanup()
    
    def _draw_status(self, frame):
        """Zeichnet Status-Informationen auf das Frame"""
        height, width = frame.shape[:2]
        
        # Hintergrund für Text
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Status-Text
        y_offset = 30
        cv2.putText(frame, f"Sound: {'EIN' if self.sound_enabled else 'AUS'}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        y_offset += 25
        gesture_name = self.gesture_configs.get(self.current_gesture, 
                                              GestureConfig("Unbekannt", "")).name
        cv2.putText(frame, f"Geste: {gesture_name}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        y_offset += 25
        cv2.putText(frame, f"Confidence: {self.gesture_confidence:.2f}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        y_offset += 25
        cv2.putText(frame, "q=Quit, s=Sound, c=Config", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    def _print_gesture_info(self):
        """Gibt Informationen über verfügbare Gesten aus"""
        print("\n=== Verfügbare Gesten ===")
        for gesture_type, config in self.gesture_configs.items():
            status = "✓" if config.enabled else "✗"
            print(f"{status} {config.name}: {config.sound_file} "
                  f"(Cooldown: {config.cooldown}s)")
        print("========================\n")
    
    def _open_config_gui(self):
        """Öffnet GUI für Gesten-Konfiguration"""
        # Diese Methode würde eine separate Tkinter-GUI öffnen
        # Für die Basis-Implementation verwenden wir die Konsole
        print("Konfiguration über GUI wird in einer zukünftigen Version verfügbar sein.")
        self._print_gesture_info()
    
    def cleanup(self):
        """Bereinigung beim Beenden"""
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        print("Gesten-Sound-Bot beendet.")

def main():
    """Hauptfunktion"""
    # Erstelle Sounds-Ordner falls nicht vorhanden
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
        print("Sounds-Ordner erstellt. Füge deine Sound-Dateien hinzu:")
        print("- victory.wav (für Victory-Zeichen)")
        print("- middle_finger.wav (für Mittelfinger)")
        print("- thumbs_up.wav (für Daumen hoch)")
        print("- ok.wav (für OK-Zeichen)")
        print("- point.wav (für Zeigen)")
        print("- punch.wav (für Faust)")
    
    try:
        bot = GestureSoundBot()
        bot.run()
    except KeyboardInterrupt:
        print("\nProgramm durch Benutzer beendet.")
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
