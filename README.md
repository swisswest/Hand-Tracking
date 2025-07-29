# Hand Tracking Programme

Dieses Verzeichnis enthält zwei Python-Programme für Hand-Tracking mit der Webcam.

## Programme

### 1. `hand_tracking.py` - Einfaches Hand-Tracking

Ein grundlegendes Hand-Tracking-Programm mit folgenden Features:

- Erkennung von hautfarbenen Bereichen
- Bewegungsspur der Hand
- Einfache Kalibrierung

### 2. `advanced_hand_tracking.py` - Erweiterte Version

Eine verbesserte Version mit zusätzlichen Features:

- Geschwindigkeitsmessung
- Einfache Gesten-Erkennung (Kreis, Linien, etc.)
- Verschiedene Visualisierungsmodi
- Fingerspitzen-Erkennung

## Installation

1. Stelle sicher, dass Python 3.13 installiert ist
2. Installiere die benötigten Pakete:
   ```
   pip install opencv-python numpy
   ```

## Verwendung

### Einfache Version starten:

```bash
python hand_tracking.py
```

### Erweiterte Version starten:

```bash
python advanced_hand_tracking.py
```

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
