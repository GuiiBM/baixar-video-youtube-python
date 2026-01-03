#!/usr/bin/env python3
import subprocess
import sys
import os

def atualizar_yt_dlp():
    """Atualiza o yt-dlp para a versão mais recente"""
    print("🔄 Atualizando yt-dlp...")
    
    try:
        # Atualizar yt-dlp
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                              capture_output=True, text=True, check=True)
        print("✅ yt-dlp atualizado com sucesso!")
        print(f"Saída: {result.stdout}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao atualizar yt-dlp: {e}")
        print(f"Erro: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ATUALIZADOR YT-DLP")
    print("=" * 50)
    
    if atualizar_yt_dlp():
        print("\n✅ Atualização concluída!")
        print("💡 Execute INICIAR.py para usar o downloader")
    else:
        print("\n❌ Falha na atualização")
    
    input("\nPressione Enter para sair...")