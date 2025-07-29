# Hand Tracking Programme

Dieses Verzeichnis enthält Python-Programme für Hand-Tracking und Gesten-Erkennung mit der Webcam.

## 🎯 Programme

### 1. `gesture_sound_bot.py` - 🆕 Gesten-Sound-Bot für Discord

**Das Hauptprogramm!** Ein fortschrittlicher Bot, der Handgesten erkennt und entsprechende Sounds in Discord-Calls abspielt.

**Features:**

- ✌️ Erkennt 6+ verschiedene Handgesten (Victory, Mittelfinger, Daumen hoch, etc.)
- 🔊 Spielt Sounds über virtuelles Mikrofon in Discord ab
- 🎮 Einfache Steuerung und Konfiguration
- 🔧 Erweiterbar für neue Gesten und Sounds
- 📱 Live-Vorschau mit Status-Anzeige

**Erkannte Gesten:**

- Victory-Zeichen ✌️
- Mittelfinger 🖕
- Daumen hoch 👍
- OK-Zeichen 👌
- Zeigen 👉
- Faust 👊

### 2. `hand_tracking.py` - Einfaches Hand-Tracking

Ein grundlegendes Hand-Tracking-Programm mit folgenden Features:

- Erkennung von hautfarbenen Bereichen
- Bewegungsspur der Hand
- Einfache Kalibrierung

### 3. `advanced_hand_tracking.py` - Erweiterte Version

Eine verbesserte Version mit zusätzlichen Features:

- Geschwindigkeitsmessung
- Einfache Gesten-Erkennung (Kreis, Linien, etc.)
- Verschiedene Visualisierungsmodi
- Fingerspitzen-Erkennung

## 🚀 Schnellstart (Gesten-Sound-Bot)

### Automatische Installation:

```bash
# 1. Installation ausführen
install.bat

# 2. Bot starten
start_bot.bat
```

### Manuelle Installation:

```bash
# 1. Pakete installieren
pip install -r requirements.txt

# 2. System testen
python test_system.py

# 3. Bot starten
python gesture_sound_bot.py
```

## 📋 Anforderungen für Gesten-Sound-Bot

### Software:

- Python 3.8+
- VB-Audio Cable (für Discord-Integration)
- Webcam

### Hardware:

- Webcam (720p+ empfohlen)
- Mikrofon-fähiges System
- Gute Beleuchtung

## 🎵 Discord-Setup

1. **VB-Audio Cable installieren:**

   - Download: https://vb-audio.com/Cable/
   - Nach Installation: Computer neu starten

2. **Discord konfigurieren:**

   - Einstellungen → Sprache & Video
   - Mikrofon: "CABLE Input (VB-Audio Virtual Cable)" wählen

3. **Sounds hinzufügen:**
   - Sound-Dateien in `sounds/` Ordner legen
   - Unterstützte Formate: `.wav`, `.mp3`, `.ogg`

## 🎮 Verwendung

### Gesten-Sound-Bot:

```bash
python gesture_sound_bot.py
```

**Steuerung:**

- `Q` - Beenden
- `S` - Sound ein/ausschalten
- `G` - Verfügbare Gesten anzeigen
- `C` - Konfiguration (zukünftig)

### Klassische Hand-Tracking Programme:

## Steuerung

### Beide Programme:

- **'s'** - Hautkalibrierung starten (dann auf deine Hand klicken)
- **'r'** - Kalibrierung zurücksetzen
- **'q'** - Programm beenden

### Erweiterte Version zusätzlich:

- **'c'** - Bewegungsspur löschen
- **'m'** - Zwischen Anzeigemodi wechseln

## Anzeigemodi (Erweiterte Version)

1. **Normal** - Standard-Anzeige mit Bewegungsspur
2. **Spur** - Fokus auf die Bewegungsspur
3. **Geschwindigkeit** - Farbkodierte Geschwindigkeitsanzeige
4. **Gesten** - Gesten-Erkennungsmodus

## Kalibrierung

Für beste Ergebnisse:

1. Starte das Programm
2. Drücke 's' für Kalibrierung
3. Klicke auf einen gut beleuchteten Bereich deiner Hand
4. Das Programm passt automatisch die Hautfarben-Erkennung an

## Tipps für bessere Erkennung

- **Beleuchtung**: Sorge für gleichmäßige Beleuchtung
- **Hintergrund**: Verwende einen kontrastierenden Hintergrund
- **Hautfarbe**: Kalibriere für deine spezifische Hautfarbe
- **Bewegung**: Langsame, deutliche Bewegungen funktionieren besser

## Erkannte Gesten (Erweiterte Version)

- **Punkt/Stopp** - Kleine kreisförmige Bewegung
- **Horizontale Linie** - Bewegung von links nach rechts
- **Vertikale Linie** - Bewegung von oben nach unten
- **Kreis** - Kreisförmige Bewegung
- **Unregelmäßig** - Komplexere Bewegungsmuster

## Fehlerbehebung

### Webcam wird nicht erkannt:

- Überprüfe, ob die Webcam richtig angeschlossen ist
- Stelle sicher, dass keine andere Anwendung die Webcam verwendet

### Schlechte Hand-Erkennung:

- Führe eine neue Kalibrierung durch
- Verbessere die Beleuchtung
- Verwende einen einfarbigen Hintergrund

### Programm startet nicht:

- Überprüfe die Python-Installation
- Stelle sicher, dass alle Pakete installiert sind:
  ```bash
  pip list | findstr opencv
  pip list | findstr numpy
  ```

## Technische Details

### Verwendete Bibliotheken:

- **OpenCV** - Computer Vision und Bildverarbeitung
- **NumPy** - Numerische Berechnungen
- **Time/Math** - Zeitstempel und mathematische Operationen

### Algorithmus:

1. Webcam-Frame erfassen
2. HSV-Farbkonvertierung
3. Hautfarben-Segmentierung
4. Morphologische Operationen zur Rauschunterdrückung
5. Kontur-Erkennung
6. Schwerpunkt-Berechnung
7. Bewegungsverfolgung und Visualisierung

## Erweiterungsmöglichkeiten

- Integration von MediaPipe für bessere Hand-Erkennung
- Mehr Gesten-Erkennungsalgorithmen
- 3D-Hand-Tracking
- Aufzeichnung und Wiedergabe von Bewegungen
- Maus-Steuerung durch Handbewegungen
- Spracherkennung kombiniert mit Gesten

## Lizenz

Diese Programme sind für Bildungszwecke erstellt und können frei verwendet und modifiziert werden.
