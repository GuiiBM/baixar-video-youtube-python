@echo off
title YouTube MP4 Downloader
color 0A

REM Ir para a pasta pai (onde esta o app.py)
cd /d "%~dp0.."

echo.
echo ========================================
echo    YouTube MP4 Downloader v1.0
echo ========================================
echo.
echo Pasta atual: %CD%
echo.

REM Verificar se app.py existe
if not exist "app.py" (
    echo [ERRO] app.py nao encontrado nesta pasta!
    echo.
    pause
    exit /b 1
)

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python em: https://python.org
    pause
    exit /b 1
)

REM Verificar Flask
echo Verificando Flask...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Flask nao encontrado!
    echo Execute: executaveis\INSTALAR_DEPENDENCIAS.bat
    pause
    exit /b 1
)

REM Verificar yt-dlp
echo Verificando yt-dlp...
pip show yt-dlp >nul 2>&1
if errorlevel 1 (
    echo [ERRO] yt-dlp nao encontrado!
    echo Execute: executaveis\INSTALAR_DEPENDENCIAS.bat
    pause
    exit /b 1
)

echo.
echo Tudo OK! Iniciando servidor...
echo.
echo ========================================
echo    ACESSE: http://localhost:5000
echo ========================================
echo.
echo Pressione Ctrl+C para parar
echo.

python app.py

echo.
echo Servidor parado.
pause