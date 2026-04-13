import psutil
import csv
import os
from datetime import datetime

# Variáveis globais para rastrear o tráfego de rede entre as chamadas
ult_net_rec = psutil.net_io_counters().bytes_recv
ult_net_env = psutil.net_io_counters().bytes_sent

def obter_metricas():
    """Captura métricas detalhadas incluindo Rede e Bateria."""
    global ult_net_rec, ult_net_env
    
    # Cálculo de Velocidade de Rede (KB/s)
    net = psutil.net_io_counters()
    vel_download = (net.bytes_recv - ult_net_rec) / 1024
    vel_upload = (net.bytes_sent - ult_net_env) / 1024
    
    # Atualiza globais para a próxima leitura
    ult_net_rec, ult_net_env = net.bytes_recv, net.bytes_sent

    # Dados da Bateria (Lida com desktops que não possuem bateria)
    bateria = psutil.sensors_battery()
    bat_percent = bateria.percent if bateria else 0
    carregando = bateria.power_plugged if bateria else False

    uso_disco = psutil.disk_usage('/')
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_usada_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disco_percent": uso_disco.percent,
        "disco_livre_gb": round(uso_disco.free / (1024**3), 2),
        "disco_total_gb": round(uso_disco.total / (1024**3), 2),
        "net_down": round(vel_download, 1),
        "net_up": round(vel_upload, 1),
        "bat_percent": bat_percent,
        "bat_status": "⚡" if carregando else "🔋"
    }

def salvar_log(dados):
    """Salva o histórico expandido de performance em CSV."""
    diretorio_atual = os.path.dirname(__file__)
    caminho_logs = os.path.abspath(os.path.join(diretorio_atual, '..', 'logs'))
    caminho_arquivo = os.path.join(caminho_logs, 'performance.csv')

    if not os.path.exists(caminho_logs):
        os.makedirs(caminho_logs)

    arquivo_novo = not os.path.exists(caminho_arquivo)

    with open(caminho_arquivo, mode='a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        
        # Cabeçalho atualizado com novas colunas
        if arquivo_novo:
            escritor.writerow(['Data/Hora', 'CPU (%)', 'RAM (%)', 'Disco (%)', 'Down (KB/s)', 'Up (KB/s)', 'Bat (%)'])
        
        escritor.writerow([
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            dados['cpu_percent'],
            dados['ram_percent'],
            dados['disco_percent'],
            dados['net_down'],
            dados['net_up'],
            dados['bat_percent']
        ])