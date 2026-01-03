#!/bin/bash

# Ir para a pasta pai
cd "$(dirname "$0")/.." || { echo "Erro: Não foi possível acessar o diretório pai"; exit 1; }

# Executar inicializador Python universal
if command -v python3 &> /dev/null; then
    python3 executaveis/INICIAR.py
elif command -v python &> /dev/null; then
    python executaveis/INICIAR.py
else
    echo "[ERRO] Python não encontrado!"
    echo "Instale Python usando o gerenciador de pacotes da sua distribuição"
    echo "Ubuntu/Debian: sudo apt install python3"
    echo "CentOS/RHEL: sudo yum install python3"
    echo "Arch: sudo pacman -S python"
    read -p "Pressione Enter para sair..."
fi