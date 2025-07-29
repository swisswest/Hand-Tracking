# Gesten-Sound-Bot Setup Anleitung

## 🎯 Überblick

Dieses Programm erkennt Handgesten mit der Webcam und spielt entsprechende Sounds ab, die in Discord-Calls hörbar sind.

## 📋 Anforderungen

### Software

1. **Python 3.8+** installiert
2. **VB-Audio Cable** oder **VoiceMeeter** für virtuelles Mikrofon
3. **Webcam** (eingebaut oder extern)

### Hardware

- Webcam mit mindestens 720p Auflösung (empfohlen)
- Ausreichend Beleuchtung für Handerkennung

## 🚀 Installation

### 1. Python-Pakete installieren

```bash
pip install -r requirements.txt
```

### 2. VB-Audio Cable installieren

1. Download von: https://vb-audio.com/Cable/
2. Installiere "VB-Audio Virtual Cable"
3. Neustart des Computers

### 3. Discord Konfiguration

1. Öffne Discord Einstellungen
2. Gehe zu "Sprache & Video"
3. Wähle "CABLE Input (VB-Audio Virtual Cable)" als Mikrofon
4. Teste die Verbindung

## 📁 Projekt-Struktur

```
Hand-Tracking/
├── gesture_sound_bot.py      # Hauptprogramm
├── requirements.txt          # Python-Abhängigkeiten
├── gesture_config.json       # Gesten-Konfiguration
├── setup_guide.md           # Diese Anleitung
├── sounds/                  # Sound-Dateien Ordner
│   ├── victory.wav
│   ├── middle_finger.wav
│   ├── thumbs_up.wav
│   ├── ok.wav
│   ├── point.wav
│   └── punch.wav
└── README.md
```

## 🎵 Sound-Dateien hinzufügen

### 1. Sounds-Ordner erstellen

Das Programm erstellt automatisch einen `sounds/` Ordner beim ersten Start.

### 2. Sound-Dateien hinzufügen

Unterstützte Formate: `.wav`, `.mp3`, `.ogg`

**Standard-Sounds:**

- `victory.wav` - Victory/Peace-Zeichen ✌️
- `middle_finger.wav` - Mittelfinger 🖕
- `thumbs_up.wav` - Daumen hoch 👍
- `ok.wav` - OK-Zeichen 👌
- `point.wav` - Zeigen 👉
- `punch.wav` - Faust 👊

### 3. Sound-Quellen

- **Freesound.org** (kostenlos, Registrierung erforderlich)
- **Zapsplat.com** (kostenlos, Registrierung erforderlich)
- **Eigene Aufnahmen** mit Audacity o.ä.

## 🎮 Verwendung

### Programm starten

```bash
python gesture_sound_bot.py
```

### Steuerung

- **q** - Programm beenden
- **s** - Sound ein/ausschalten
- **g** - Verfügbare Gesten anzeigen
- **c** - Konfiguration öffnen (zukünftige Funktion)

### Erkannte Gesten

1. **Victory-Zeichen** ✌️ - Zeige- und Mittelfinger gestreckt
2. **Mittelfinger** 🖕 - Nur Mittelfinger gestreckt
3. **Daumen hoch** 👍 - Nur Daumen gestreckt
4. **OK-Zeichen** 👌 - Daumen und Zeigefinger berühren sich
5. **Zeigen** 👉 - Nur Zeigefinger gestreckt
6. **Faust** 👊 - Alle Finger geschlossen

## ⚙️ Konfiguration

### Gesten-Einstellungen anpassen

Bearbeite `gesture_config.json`:

```json
{
  "peace": {
    "name": "Victory-Zeichen",
    "sound_file": "victory.wav",
    "cooldown": 2.0,                 # Sekunden zwischen Wiederholungen
    "confidence_threshold": 0.8,      # Erkennungs-Schwellenwert
    "enabled": true                   # Geste aktiviert/deaktiviert
  }
}
```

### Parameter-Erklärung

- **cooldown**: Wartezeit zwischen Sound-Wiederholungen (verhindert Spam)
- **confidence_threshold**: Mindest-Erkennungsqualität (0.0-1.0)
- **enabled**: Geste aktivieren/deaktivieren

## 🎯 Discord Integration

### VoiceMeeter Setup (Alternative zu VB-Cable)

1. Download VoiceMeeter von: https://vb-audio.com/Voicemeeter/
2. Installiere VoiceMeeter Banana
3. Konfiguriere Audio-Routing
4. Verwende VoiceMeeter Input als Discord-Mikrofon

### Audio-Test

1. Starte das Programm
2. Führe eine Geste aus
3. Überprüfe ob Sound abgespielt wird
4. Teste in Discord mit Freunden

## 🔧 Troubleshooting

### Gesten werden nicht erkannt

- **Beleuchtung verbessern** - Verwende gleichmäßiges Licht
- **Kamera-Position** - Hand sollte deutlich sichtbar sein
- **Hintergrund** - Verwende einfarbigen Hintergrund
- **Confidence-Threshold senken** in der Konfiguration

### Kein Sound in Discord

- **VB-Cable richtig installiert?** - Neustart nach Installation
- **Discord-Mikrofon korrekt eingestellt?** - CABLE Input wählen
- **Audio-Treiber aktualisieren**
- **Windows Audio-Einstellungen prüfen**

### Performance-Probleme

- **Kamera-Auflösung reduzieren** - Ändere `CAP_PROP_FRAME_WIDTH/HEIGHT`
- **MediaPipe-Einstellungen anpassen** - Reduziere `min_detection_confidence`
- **Webcam-FPS begrenzen**

### Python-Fehler

```bash
# Bei Problemen mit MediaPipe
pip uninstall mediapipe
pip install mediapipe --no-cache-dir

# Bei Audio-Problemen
pip install pygame --upgrade
```

## 🔄 Erweiterungen

### Neue Gesten hinzufügen

1. **Gesten-Logik erweitern** in `detect_gesture()` Methode
2. **Neue GestureType hinzufügen** in Enum
3. **Konfiguration aktualisieren** in `gesture_config.json`
4. **Sound-Datei hinzufügen** im `sounds/` Ordner

### Beispiel für neue Geste:

```python
# In GestureType Enum
CALL_ME = "call_me"

# In detect_gesture() Methode
if (finger_states[0] and finger_states[4] and
    not finger_states[1] and not finger_states[2] and not finger_states[3]):
    return GestureType.CALL_ME, confidence
```

## 📞 Support

Bei Problemen oder Fragen:

1. Überprüfe diese Anleitung
2. Prüfe die Konsolen-Ausgabe für Fehlermeldungen
3. Teste mit verschiedenen Gesten und Beleuchtung

## 🎉 Viel Spaß!

Das Programm ist bereit für den Einsatz in Discord-Calls. Experimentiere mit verschiedenen Gesten und Sounds!
