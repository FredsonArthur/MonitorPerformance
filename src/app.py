import os
import time
from monitor_logic import obter_metricas, salvar_log

# Definição de cores ANSI para o terminal
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
RESET = "\033[0m"

def obter_cor(percentual):
    """Define a cor com base no nível de uso dos recursos."""
    if percentual < 70:
        return VERDE
    elif percentual < 90:
        return AMARELO
    else:
        return VERMELHO

def formatar_tela(dados):
    """Limpa o console e exibe as métricas com cores e detalhes de disco."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Define as cores conforme o uso
    cor_cpu = obter_cor(dados['cpu_percent'])
    cor_ram = obter_cor(dados['ram_percent'])
    cor_disco = obter_cor(dados['disco_percent'])

    print("="*50)
    print(f"{'DASHBOARD DE PERFORMANCE':^50}")
    print("="*50)
    
    # Exibição de CPU e RAM
    print(f" CPU   : {cor_cpu}{dados['cpu_percent']:>6}%{RESET}")
    print(f" RAM   : {cor_ram}{dados['ram_percent']:>6}%{RESET} ({dados['ram_usada_gb']} GB)")
    
    print("-" * 50)
    
    # Exibição Detalhada de Disco
    print(f" DISCO : {cor_disco}{dados['disco_percent']:>6}%{RESET}")
    print(f"         Livre: {dados['disco_livre_gb']} GB / Total: {dados['disco_total_gb']} GB")
    
    print("="*50)
    print(f"{'Pressione Ctrl+C para encerrar':^50}")

if __name__ == "__main__":
    try:
        # Habilita suporte a cores ANSI no terminal do Windows se necessário
        if os.name == 'nt':
            os.system('')

        while True:
            # 1. Coleta as métricas (incluindo novos dados de disco)
            metricas = obter_metricas()
            
            # 2. Atualiza a interface com cores e formatação
            formatar_tela(metricas)
            
            # 3. Registra os dados no CSV
            salvar_log(metricas)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{AMARELO}Monitoramento finalizado e logs preservados.{RESET}")