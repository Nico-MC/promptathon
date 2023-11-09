@echo off
REM Überprüfen, ob das .venv-Verzeichnis existiert, wenn nicht, wird es erstellt
if not exist ".venv" (
    echo Erstelle eine virtuelle Umgebung...
    python -m venv .venv
)

REM Aktivieren der virtuellen Umgebung
call .venv\Scripts\activate

REM Installieren der Abhängigkeiten
pip install -r requirements.txt

echo Die virtuelle Umgebung ist bereit und die Abhängigkeiten sind installiert.
pause