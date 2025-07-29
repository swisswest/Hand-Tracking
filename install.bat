@echo off
echo 🚀 Gesten-Sound-Bot Installation
echo ================================
echo.

REM Prüfe Python-Installation
echo 🐍 Prüfe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert oder nicht im PATH!
    echo Bitte installiere Python 3.8+ von https://python.org
    pause
    exit /b 1
)
echo ✅ Python gefunden!
echo.

REM Upgrade pip
echo 📦 Aktualisiere pip...
python -m pip install --upgrade pip
echo.

REM Installiere Pakete
echo 📚 Installiere erforderliche Pakete...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Fehler bei der Paket-Installation!
    pause
    exit /b 1
)
echo ✅ Alle Pakete installiert!
echo.

REM Erstelle Sounds-Ordner
echo 📁 Erstelle Sounds-Ordner...
if not exist "sounds" mkdir sounds
echo ✅ Sounds-Ordner erstellt!
echo.

REM Teste System
echo 🔍 Teste System...
python test_system.py
echo.

echo 🎉 Installation abgeschlossen!
echo.
echo 📋 Nächste Schritte:
echo 1. Installiere VB-Audio Cable von https://vb-audio.com/Cable/
echo 2. Füge Sound-Dateien zum sounds/ Ordner hinzu
echo 3. Starte mit: python gesture_sound_bot.py
echo.
pause
