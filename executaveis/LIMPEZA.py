#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import glob
import platform

def print_colored(text, color="white"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    if platform.system() == "Windows":
        try:
            import colorama
            colorama.init()
            print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")
        except ImportError:
            print(text)
    else:
        print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def is_orphan_file(filename):
    """Identifica arquivos órfãos por padrões específicos"""
    import re
    
    # Padrões de arquivos órfãos
    orphan_patterns = [
        r'^=\d+\.\d+\.\d+$',  # =2.3.3
        r'^\d+\.\d+\.\d+$',   # 2024.1.0
        r'^\d+\.\d+$',        # 0.4.6
        r'^\d+$',             # 2
        r'^[a-zA-Z]+=.*',     # Flask=2.3.3
        r'^.*\.whl$',         # arquivos wheel órfãos
        r'^.*\.egg-info$',    # egg-info órfãos
        r'^pip-.*\.txt$',     # pip logs
        r'^.*\.dist-info$'    # dist-info órfãos
    ]
    
    for pattern in orphan_patterns:
        if re.match(pattern, filename):
            return True
    return False

def clean_files():
    # Ir para pasta raiz do projeto
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print_colored("🧹 Iniciando limpeza de arquivos desnecessários...", "yellow")
    
    cleaned_count = 0
    
    # 1. Remover cache Python
    print_colored("Removendo cache Python...", "white")
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            cleaned_count += 1
            print_colored(f"  ✓ {pycache_path}", "green")
    
    # Remover arquivos .pyc
    for pyc_file in glob.glob("**/*.pyc", recursive=True):
        os.remove(pyc_file)
        cleaned_count += 1
    
    # 2. Remover arquivos órfãos (identificação inteligente)
    print_colored("Removendo arquivos órfãos...", "white")
    for item in os.listdir("."):
        if os.path.isfile(item) and is_orphan_file(item):
            try:
                os.remove(item)
                cleaned_count += 1
                print_colored(f"  ✓ {item}", "green")
            except:
                pass  # Ignorar erros de permissão
    
    # 3. Remover arquivos temporários
    print_colored("Removendo arquivos temporários...", "white")
    temp_patterns = ["*.zip", "*.tar.gz", "*.tmp", "*.log", "pip-*.txt"]
    for pattern in temp_patterns:
        for temp_file in glob.glob(pattern):
            os.remove(temp_file)
            cleaned_count += 1
            print_colored(f"  ✓ {temp_file}", "green")
    
    # 4. Remover FFmpeg baixado (será reinstalado se necessário)
    ffmpeg_files = ["ffmpeg.exe", "ffplay.exe", "ffprobe.exe"]
    for ffmpeg_file in ffmpeg_files:
        if os.path.exists(ffmpeg_file):
            os.remove(ffmpeg_file)
            cleaned_count += 1
            print_colored(f"  ✓ {ffmpeg_file}", "green")
    
    # Remover pasta FFmpeg extraída
    for item in os.listdir("."):
        if item.startswith("ffmpeg-") and os.path.isdir(item):
            shutil.rmtree(item)
            cleaned_count += 1
            print_colored(f"  ✓ {item}/", "green")
    
    print_colored(f"\n✅ Limpeza concluída! {cleaned_count} itens removidos.", "green")

if __name__ == "__main__":
    try:
        clean_files()
    except Exception as e:
        print_colored(f"❌ Erro durante limpeza: {e}", "red")
    
    input("Pressione Enter para sair...")