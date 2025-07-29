@echo off
title Gesten-Sound-Bot für Discord
echo.
echo 🎮 Gesten-Sound-Bot für Discord
echo ==============================
echo.

REM Prüfe ob Sounds-Ordner existiert
if not exist "sounds" (
    echo ⚠️  Sounds-Ordner nicht gefunden!
    echo Erstelle sounds/ Ordner und füge Sound-Dateien hinzu.
    mkdir sounds
    echo Beispiel-Sounds benötigt:
    echo - victory.wav
    echo - middle_finger.wav  
    echo - thumbs_up.wav
    echo - ok.wav
    echo - point.wav
    echo - punch.wav
    echo.
    echo Drücke eine Taste um trotzdem zu starten...
    pause >nul
)

REM Zeige verfügbare Sounds
if exist "sounds" (
    echo 🎵 Verfügbare Sounds:
    dir /b sounds\*.wav sounds\*.mp3 sounds\*.ogg 2>nul
    if errorlevel 1 (
        echo ⚠️  Keine Sound-Dateien gefunden!
    )
    echo.
)

echo 🚀 Starte Gesten-Sound-Bot...
echo.
echo Steuerung:
echo - Q = Beenden
echo - S = Sound ein/aus
echo - G = Gesten anzeigen
echo - C = Konfiguration
echo.
echo Für Discord: Mikrofon auf "CABLE Input" stellen!
echo.

REM Starte Programm
python gesture_sound_bot.py

REM Bei Fehler pausieren
if errorlevel 1 (
    echo.
    echo ❌ Fehler beim Starten! 
    echo Führe zuerst install.bat aus oder prüfe die Installation.
    pause
)
