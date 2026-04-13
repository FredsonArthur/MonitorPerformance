import os
import time
from monitor_logic import obter_metricas, salvar_log

def formatar_tela(dados):
    """Limpa o console e exibe as métricas formatadas."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*35)
    print(f"{'MONITOR DE SISTEMA':^35}")
    print("="*35)
    print(f" CPU:    {dados['cpu_percent']}%")
    print(f" RAM:    {dados['ram_percent']}% ({dados['ram_usada_gb']} GB)")
    print(f" DISCO:  {dados['disco_percent']}%")
    print("="*35)
    print(" Pressione Ctrl+C para encerrar")

if __name__ == "__main__":
    try:
        while True:
            # 1. Coleta as métricas atuais do hardware
            metricas = obter_metricas()
            
            # 2. Atualiza a interface no terminal
            formatar_tela(metricas)
            
            # 3. Registra os dados no arquivo CSV em /logs
            salvar_log(metricas)
            
            # Intervalo de 1 segundo para um log equilibrado
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nMonitoramento finalizado e dados salvos com sucesso.")