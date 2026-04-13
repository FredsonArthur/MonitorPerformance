import psutil
import csv
import os
from datetime import datetime

def obter_metricas():
    """Captura métricas detalhadas de CPU, RAM e Disco."""
    uso_disco = psutil.disk_usage('/')
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_usada_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disco_percent": uso_disco.percent,
        "disco_livre_gb": round(uso_disco.free / (1024**3), 2),
        "disco_total_gb": round(uso_disco.total / (1024**3), 2)
    }

def salvar_log(dados):
    """Salva o histórico de performance em um arquivo CSV na pasta /logs."""
    # Localiza o caminho absoluto da pasta 'logs' subindo um nível a partir de 'src'
    diretorio_atual = os.path.dirname(__file__)
    caminho_logs = os.path.abspath(os.path.join(diretorio_atual, '..', 'logs'))
    caminho_arquivo = os.path.join(caminho_logs, 'performance.csv')

    # Garante que a pasta logs existe antes de tentar salvar
    if not os.path.exists(caminho_logs):
        os.makedirs(caminho_logs)

    # Verifica se o arquivo já existe para decidir se escreve o cabeçalho
    arquivo_novo = not os.path.exists(caminho_arquivo)

    # Abre o arquivo em modo 'append' (acrescentar)
    with open(caminho_arquivo, mode='a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        
        # Se for um arquivo novo, cria o cabeçalho das colunas
        if arquivo_novo:
            escritor.writerow(['Data/Hora', 'CPU (%)', 'RAM (%)', 'Disco (%)'])
        
        # Escreve a linha com os dados atuais
        escritor.writerow([
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            dados['cpu_percent'],
            dados['ram_percent'],
            dados['disco_percent']
        ])