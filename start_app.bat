@echo off
echo ==========================================
echo   GenoPredict AD — Demarrage du serveur
echo ==========================================
echo.
echo [1/1] Lancement du serveur FastAPI...
echo Ouvrez votre navigateur sur http://127.0.0.1:8000
echo.
cd /d "%~dp0"
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
pause
