#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import shutil

def print_colored(text, color="white"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    # Habilitar cores ANSI no Windows 10+
    if platform.system() == "Windows":
        try:
            import colorama
            colorama.init()
            print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")
        except ImportError:
            # Fallback sem cores
            print(text)
    else:
        print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def run_command(cmd, shell=None):
    try:
        # Usar shell=True apenas no Windows para compatibilidade
        if shell is None:
            shell = platform.system() == "Windows"
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print_colored("========================================", "blue")
    print_colored("    YouTube MP4 Downloader - Instalação", "blue")
    print_colored("========================================", "blue")
    
    system = platform.system()
    print_colored(f"Sistema detectado: {system}", "green")
    
    # [1/5] Verificar Python
    print_colored("\n[1/5] Verificando Python...", "yellow")
    python_cmd = "python" if system == "Windows" else "python3"
    
    success, output, _ = run_command(f"{python_cmd} --version")
    if not success:
        print_colored("[ERRO] Python não encontrado!", "red")
        if system == "Windows":
            print_colored("Instale Python em: https://python.org", "white")
        else:
            print_colored("Instale: sudo apt install python3 python3-pip", "white")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    version = output.strip().split()[1]
    print_colored(f"Python {version} encontrado!", "green")
    
    # [2/5] Criar ambiente virtual
    print_colored("\n[2/5] Criando ambiente virtual...", "yellow")
    if os.path.exists("venv"):
        shutil.rmtree("venv")
    
    success, _, error = run_command(f"{python_cmd} -m venv venv")
    if not success:
        print_colored("[ERRO] Falha ao criar ambiente virtual", "red")
        if system != "Windows":
            print_colored("Instale: sudo apt install python3-venv", "white")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Ativar ambiente virtual
    if system == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
        python_venv = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_venv = "venv/bin/python"
    
    # [3/5] Atualizar pip
    print_colored("\n[3/5] Atualizando pip...", "yellow")
    run_command(f"{python_venv} -m pip install --upgrade pip --quiet")
    
    # [4/6] Instalar todas as dependências Python
    print_colored("\n[4/5] Instalando dependências Python...", "yellow")
    dependencies = [
        "Flask>=2.3.3",
        "yt-dlp>=2024.1.0",
        "requests>=2.31.0",
        "urllib3>=2.0.0"
    ]
    
    if system == "Windows":
        dependencies.append("colorama>=0.4.6")
    
    for dep in dependencies:
        print_colored(f"Instalando {dep.split('>=')[0]}...", "white")
        success, _, _ = run_command(f"{pip_cmd} install {dep} --quiet")
        if not success:
            print_colored(f"[ERRO] Falha ao instalar {dep.split('>=')[0]}", "red")
            input("Pressione Enter para sair...")
            sys.exit(1)
    
    print_colored("Todas as dependências Python instaladas!", "green")
    # [5/6] Instalar FFmpeg
    print_colored("\n[5/5] Instalando FFmpeg...", "yellow")
    
    if system == "Windows":
        # Windows - baixar FFmpeg
        try:
            print_colored("Baixando FFmpeg para Windows...", "white")
            url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            urllib.request.urlretrieve(url, "ffmpeg.zip")
            
            with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Encontrar e copiar ffmpeg.exe
            for root, dirs, files in os.walk("."):
                if "ffmpeg.exe" in files:
                    src_path = os.path.join(root, "ffmpeg.exe")
                    if not os.path.exists("ffmpeg.exe"):
                        shutil.copy(src_path, "ffmpeg.exe")
                    break
            
            # Limpar arquivos temporários
            os.remove("ffmpeg.zip")
            for item in os.listdir("."):
                if item.startswith("ffmpeg-master-latest"):
                    shutil.rmtree(item)
            
            if os.path.exists("ffmpeg.exe"):
                print_colored("FFmpeg instalado com sucesso!", "green")
            else:
                print_colored("[AVISO] FFmpeg não foi instalado", "yellow")
        except Exception as e:
            print_colored(f"[AVISO] Erro ao instalar FFmpeg: {e}", "yellow")
    
    else:
        # Linux - usar gerenciador de pacotes
        if shutil.which("ffmpeg"):
            print_colored("FFmpeg já está instalado!", "green")
        else:
            print_colored("Instalando FFmpeg...", "white")
            if shutil.which("apt"):
                success, _, _ = run_command("sudo apt update && sudo apt install -y ffmpeg")
            elif shutil.which("yum"):
                success, _, _ = run_command("sudo yum install -y ffmpeg")
            elif shutil.which("dnf"):
                success, _, _ = run_command("sudo dnf install -y ffmpeg")
            elif shutil.which("pacman"):
                success, _, _ = run_command("sudo pacman -S --noconfirm ffmpeg")
            else:
                print_colored("[AVISO] Instale FFmpeg manualmente", "yellow")
                success = False
            
            if success and shutil.which("ffmpeg"):
                print_colored("FFmpeg instalado com sucesso!", "green")
            else:
                print_colored("[AVISO] FFmpeg não foi instalado", "yellow")
    
    print_colored("\n========================================", "green")
    print_colored("    INSTALAÇÃO CONCLUÍDA COM SUCESSO!", "green")
    print_colored("========================================", "green")
    print_colored("\nTodas as dependências instaladas!", "white")
    print_colored("Agora você pode baixar vídeos em alta qualidade.", "white")
    
    # Criar arquivo requirements.txt
    print_colored("\nCriando requirements.txt...", "white")
    requirements_content = """Flask>=2.3.3
yt-dlp>=2024.1.0
requests>=2.31.0
urllib3>=2.0.0
colorama>=0.4.6
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print_colored("requirements.txt criado!", "green")
    
    if system == "Windows":
        print_colored("\nPróximo passo: Execute INICIAR.bat", "white")
    else:
        print_colored("\nPróximo passo: Execute ./INICIAR.sh", "white")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()