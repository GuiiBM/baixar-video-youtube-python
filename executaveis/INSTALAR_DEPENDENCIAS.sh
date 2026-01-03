#!/bin/bash

# Ir para a pasta pai
cd "$(dirname "$0")/.." || { echo "Erro: Não foi possível acessar o diretório pai"; exit 1; }

# Executar instalador Python universal
if command -v python3 &> /dev/null; then
    python3 executaveis/INSTALAR.py || { echo "[ERRO] Falha na instalação!"; exit 1; }
elif command -v python &> /dev/null; then
    python executaveis/INSTALAR.py || { echo "[ERRO] Falha na instalação!"; exit 1; }
else
    echo "[ERRO] Python não encontrado!"
    echo "Instale Python usando o gerenciador de pacotes da sua distribuição"
    echo "Ubuntu/Debian: sudo apt install python3"
    echo "CentOS/RHEL: sudo yum install python3"
    echo "Arch: sudo pacman -S python"
    read -p "Pressione Enter para sair..."
fi