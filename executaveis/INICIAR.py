#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess
import atexit
import signal

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

def cleanup_on_exit():
    """Executa limpeza ao encerrar o servidor"""
    try:
        print_colored("\n🧹 Executando limpeza automática...", "yellow")
        cleanup_script = os.path.join("executaveis", "LIMPEZA.py")
        if os.path.exists(cleanup_script):
            subprocess.run(["python", cleanup_script])
            print_colored("✅ Limpeza concluída!", "green")
    except Exception as e:
        print_colored(f"❌ Erro na limpeza: {e}", "red")

def signal_handler(signum, frame):
    """Captura Ctrl+C para executar limpeza"""
    cleanup_on_exit()
    sys.exit(0)

def main():
    # Registrar limpeza automática
    atexit.register(cleanup_on_exit)
    signal.signal(signal.SIGINT, signal_handler)
    
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print_colored("========================================", "green")
    print_colored("    YouTube MP4 Downloader v1.0", "green")
    print_colored("========================================", "green")
    
    system = platform.system()
    print_colored(f"\nSistema: {system}", "white")
    print_colored(f"Pasta atual: {os.getcwd()}", "white")
    
    # Verificar se app.py existe
    if not os.path.exists("app.py"):
        print_colored("\n[ERRO] app.py não encontrado nesta pasta!", "red")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Definir comandos baseado no sistema
    if system == "Windows":
        python_cmd = "venv\\Scripts\\python"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        python_cmd = "venv/bin/python"
        pip_cmd = "venv/bin/pip"
    
    # Verificar e atualizar dependências
    print_colored("\nVerificando dependências...", "white")
    
    # Atualizar yt-dlp automaticamente
    print_colored("Atualizando yt-dlp...", "white")
    success, _, _ = run_command(f"{pip_cmd} install --upgrade yt-dlp --quiet")
    if success:
        print_colored("yt-dlp atualizado!", "green")
    else:
        print_colored("Falha ao atualizar yt-dlp (continuando...)", "yellow")
    
    # Verificar FFmpeg
    print_colored("Verificando FFmpeg...", "white")
    if system == "Windows":
        ffmpeg_exists = os.path.exists("ffmpeg.exe")
    else:
        ffmpeg_exists = bool(run_command("which ffmpeg")[0])
    
    if not ffmpeg_exists:
        print_colored("[AVISO] FFmpeg não encontrado - alguns vídeos podem falhar", "yellow")
    else:
        print_colored("FFmpeg encontrado!", "green")
    
    print_colored("\nTudo OK! Iniciando servidor...", "green")
    print_colored("\n========================================", "yellow")
    print_colored("    ACESSE: http://localhost:5000", "yellow")
    print_colored("========================================", "yellow")
    print_colored("\nPressione Ctrl+C para parar\n", "white")
    
    # Iniciar aplicação
    try:
        subprocess.run([python_cmd, "app.py"])
    except KeyboardInterrupt:
        print_colored("\n\nServidor parado pelo usuário.", "white")
    except Exception as e:
        print_colored(f"\n[ERRO] {e}", "red")
    
    # Limpeza será executada automaticamente via atexit
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()