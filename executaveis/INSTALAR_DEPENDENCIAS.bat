@echo off
title Instalacao de Dependencias
color 0B
echo.
echo ========================================
echo    YouTube MP4 Downloader - Instalacao
echo ========================================
echo.
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao foi encontrado!
    echo.
    echo Solucoes:
    echo 1. Instale Python em: https://python.org
    echo 2. Marque "Add to PATH" durante instalacao
    echo 3. Reinicie o computador apos instalar
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% encontrado!
echo.
echo [2/4] Atualizando pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo Erro ao atualizar pip. Continuando...
)
echo.
echo [3/4] Instalando Flask...
pip install "Flask>=2.3.3" --quiet
if errorlevel 1 (
    echo [ERRO] Falha ao instalar Flask
    pause
    exit /b 1
)
echo Flask instalado com sucesso!
echo.
echo [4/5] Instalando yt-dlp...
pip install "yt-dlp>=2024.1.0" --quiet
if errorlevel 1 (
    echo [ERRO] Falha ao instalar yt-dlp
    pause
    exit /b 1
)
echo yt-dlp instalado com sucesso!
echo.
echo [5/5] Instalando FFmpeg (OBRIGATORIO para alta qualidade)...
echo Baixando FFmpeg...
curl -L "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -o ffmpeg.zip
echo Extraindo...
tar -xf ffmpeg.zip
echo Copiando executavel...
copy "ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" .
echo Limpando arquivos temporarios...
rmdir /s /q ffmpeg-master-latest-win64-gpl
del ffmpeg.zip
if exist "ffmpeg.exe" (
    echo FFmpeg instalado com sucesso!
    echo IMPORTANTE: Agora voce pode baixar em alta qualidade!
) else (
    echo [ERRO] FFmpeg nao foi instalado - apenas qualidade baixa disponivel
)
echo.
echo ========================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo Todas as dependencias instaladas!
echo Agora voce pode baixar videos em alta qualidade.
echo.
echo Proximo passo: Execute INICIAR.bat
echo.
pause