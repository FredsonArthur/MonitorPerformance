import psutil
import csv
import os
import win32pdh
import wmi
from datetime import datetime

# Sincronização de estado para cálculo de tráfego de rede
last_inbound_stream = psutil.net_io_counters().bytes_recv
last_outbound_stream = psutil.net_io_counters().bytes_sent

def get_cpu_temp():
    """
    Tenta capturar a temperatura através de múltiplos métodos.
    REQUER EXECUÇÃO COMO ADMINISTRADOR.
    """
    # Método 1: MSAcpi (Padrão Windows via WMI)
    try:
        w = wmi.WMI(namespace="root\\wmi")
        temp_data = w.MSAcpi_ThermalZoneTemperature()
        if temp_data:
            return round((temp_data[0].CurrentTemperature / 10.0) - 273.15, 1)
    except:
        pass

    # Método 2: Fallback via Performance Counters
    try:
        query = win32pdh.OpenQuery()
        handle = win32pdh.AddCounter(query, r"\Thermal Zone Information(*)\Temperature")
        win32pdh.CollectQueryData(query)
        _, val = win32pdh.GetFormattedCounterValue(handle, win32pdh.PDH_FMT_DOUBLE)
        win32pdh.CloseQuery(query)
        # Converte Kelvin para Celsius se o valor parecer ser K
        return round(val - 273.15, 1) if val > 200 else round(val, 1)
    except:
        return 0.0

def get_performance_metrics():
    """
    Captura FPS e carga de GPU de forma combinada para otimizar o uso da PDH Query.
    """
    res = {"fps": 0.0, "gpu": 0.0}
    try:
        query = win32pdh.OpenQuery()
        h_fps = win32pdh.AddCounter(query, r"\Display Output(*)\FramesPerSec")
        h_gpu = win32pdh.AddCounter(query, win32pdh.MakeCounterPath((None, "GPU Engine", "pid_*", None, -1, "Utilization")))
        
        # O Windows precisa de dois samples para calcular taxas (deltas)
        win32pdh.CollectQueryData(query)
        win32pdh.CollectQueryData(query)
        
        _, v_fps = win32pdh.GetFormattedCounterValue(h_fps, win32pdh.PDH_FMT_DOUBLE)
        _, v_gpu = win32pdh.GetFormattedCounterValue(h_gpu, win32pdh.PDH_FMT_DOUBLE)
        
        res["fps"] = round(v_fps, 1) if v_fps > 0 else 0.0
        res["gpu"] = round(min(v_gpu, 100.0), 1)
        win32pdh.CloseQuery(query)
    except:
        pass
    return res

def collect_telemetry_payload():
    """Consolida todas as métricas para a v1.1.5 (Inclui FPS e Temperatura)."""
    global last_inbound_stream, last_outbound_stream
    
    # Captura métricas de performance (FPS/GPU) e Térmica
    perf = get_performance_metrics()
    cpu_temp = get_cpu_temp()
    
    # 1. Rede
    raw_io = psutil.net_io_counters()
    inbound_delta = (raw_io.bytes_recv - last_inbound_stream) / 1024
    outbound_delta = (raw_io.bytes_sent - last_outbound_stream) / 1024
    last_inbound_stream, last_outbound_stream = raw_io.bytes_recv, raw_io.bytes_sent

    # 2. Energia e Disco
    power_cell = psutil.sensors_battery()
    energy_level = power_cell.percent if power_cell else 0
    is_charging = power_cell.power_plugged if power_cell else False
    volume_stats = psutil.disk_usage('/')

    return {
        "core_load": psutil.cpu_percent(interval=None),
        "cpu_temp": cpu_temp,
        "fps_rate": perf["fps"],
        "memory_usage": psutil.virtual_memory().percent,
        "volume_load": volume_stats.percent,
        "stream_in": round(inbound_delta, 1),
        "stream_out": round(outbound_delta, 1),
        "energy_percent": energy_level,
        "energy_icon": "⚡" if is_charging else "🔋",
        "gpu_load": perf["gpu"],
        "gpu_mem": 0.0 
    }

def commit_telemetry_log(data_payload):
    """Persiste o payload completo no CSV para auditoria de performance."""
    working_dir = os.path.dirname(__file__)
    data_vault = os.path.abspath(os.path.join(working_dir, '..', 'logs'))
    target_registry = os.path.join(data_vault, 'performance.csv')

    if not os.path.exists(data_vault):
        os.makedirs(data_vault)

    is_initial_entry = not os.path.exists(target_registry)

    with open(target_registry, mode='a', newline='', encoding='utf-8') as registry:
        writer = csv.writer(registry)
        if is_initial_entry:
            # Cabeçalho completo v1.1.5
            writer.writerow(['Timestamp', 'CoreLoad', 'Temp', 'FPS', 'MemUsage', 'Inbound(KB/s)', 'GPULoad'])
        
        writer.writerow([
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            data_payload['core_load'],
            data_payload['cpu_temp'],
            data_payload['fps_rate'],
            data_payload['memory_usage'],
            data_payload['stream_in'],
            data_payload['gpu_load']
        ])