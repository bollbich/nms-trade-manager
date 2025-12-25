@echo off
title Build NMS Trade Manager EXE
setlocal ENABLEDELAYEDEXPANSION

echo =====================================
echo   Generando EXE - NMS Trade Manager
echo =====================================
echo.

:: 1. Ir a la raiz del proyecto
cd /d "%~dp0"

:: 2. Activar entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] No se encontro el entorno virtual (.venv)
    echo Ejecuta primero: NMS Trade Manager.bat
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

:: 3. Instalar PyInstaller si no esta
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PyInstaller...
    pip install pyinstaller
)

:: 4. Limpiar builds anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: 5. Generar EXE
echo.
echo [INFO] Generando ejecutable...
echo.

pyinstaller ^
  --name "NMS_Trade_Manager" ^
  --onefile ^
  --console ^
  run_app.py

:: 6. Resultado
echo.
echo =====================================
echo   EXE generado en:
echo   dist\NMS_Trade_Manager.exe
echo =====================================
pause
