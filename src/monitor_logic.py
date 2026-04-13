import psutil

def obter_metricas():
    """Retorna um dicionário com as métricas atuais do sistema."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_usada_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disco_percent": psutil.disk_usage('/').percent
    }