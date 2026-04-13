import os
import time
from monitor_logic import obter_metricas

def formatar_tela(dados):
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
            metricas = obter_metricas()
            formatar_tela(metricas)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMonitoramento finalizado.")