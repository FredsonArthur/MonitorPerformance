import tkinter as tk
import time
from monitor_logic import collect_telemetry_payload

class PerformanceGadget:
    def __init__(self):
        """Inicializa a interface v1.1.5 com suporte simultâneo a FPS e Temperatura."""
        self.root = tk.Tk()
        
        # --- CONFIGURAÇÃO DE PERFORMANCE & UX ---
        self.update_interval = 1000 
        
        # Históricos para os gráficos de tendência
        self.history_core = [0] * 20  
        self.history_mem = [0] * 20   
        self.history_fps = [0] * 20    
        self.history_stream = [0] * 20 
        
        # --- CONFIGURAÇÕES DE JANELA (GHOST UI) ---
        self.root.overrideredirect(True)      
        self.root.attributes("-topmost", True) 
        self.root.attributes("-alpha", 0.9)    
        self.root.configure(bg='#1e1e1e')      

        # Ajuste de altura (420) para acomodar Temperatura + FPS + GPU
        largura, altura = 200, 420 
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # --- COMPONENTES DA INTERFACE (WIDGETS) ---
        
        # Botão de fechar
        self.btn_close = tk.Button(
            self.root, text="✕", command=self.root.destroy,
            bg="#1e1e1e", fg="#ff4444", bd=0, 
            activebackground="#ff4444", activeforeground="white",
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.btn_close.place(x=175, y=5)

        # Monitor de CPU (Carga e Temperatura)
        self.label_core = tk.Label(self.root, text="CORE: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_core.pack(pady=(20, 0))
        
        self.label_temp = tk.Label(self.root, text="TEMP: --°C", fg="#ff4444", bg="#1e1e1e", font=("Segoe UI", 7))
        self.label_temp.pack()

        self.canvas_telemetry = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_telemetry.pack(pady=5)
        
        self.label_mem = tk.Label(self.root, text="MEM: --%", fg="#00ffff", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_mem.pack()

        # Monitor de Performance (FPS e GPU)
        self.label_fps = tk.Label(self.root, text="FPS: --", fg="#ff8800", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_fps.pack(pady=(10, 0))

        self.canvas_fps = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_fps.pack(pady=5)
        
        self.label_gpu = tk.Label(self.root, text="GPU Usage: --%", fg="#ff8800", bg="#1e1e1e", font=("Segoe UI", 7))
        self.label_gpu.pack()

        # Monitor de Rede
        self.label_stream = tk.Label(self.root, text="DATA STREAM", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_stream.pack(pady=(10, 0))

        self.canvas_stream = tk.Canvas(self.root, width=180, height=40, bg="#2d2d2d", highlightthickness=0)
        self.canvas_stream.pack(pady=5)

        # Informações de Energia e Volume
        self.label_sub = tk.Label(self.root, text="PWR: --% | VOL: --%", fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 8))
        self.label_sub.pack(pady=10)

        # --- INTERATIVIDADE ---
        self.root.bind("<Button-1>", self.init_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        self.refresh()

    def init_drag(self, event):
        self.drag_x, self.drag_y = event.x, event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")

    def render_charts(self):
        """Redesenha os gráficos para Core, RAM, FPS e Rede."""
        self.canvas_telemetry.delete("all")
        self.canvas_fps.delete("all")
        self.canvas_stream.delete("all")
        
        w, h = 180, 60
        points = 20
        step = w / (points - 1)

        for i in range(points - 1):
            x1, x2 = i * step, (i + 1) * step
            
            # Gráfico CPU (Verde) e RAM (Ciano)
            y1_core = h - (self.history_core[i] / 100 * h)
            y2_core = h - (self.history_core[i+1] / 100 * h)
            self.canvas_telemetry.create_line(x1, y1_core, x2, y2_core, fill="#4aff4a", width=2)

            y1_mem = h - (self.history_mem[i] / 100 * h)
            y2_mem = h - (self.history_mem[i+1] / 100 * h)
            self.canvas_telemetry.create_line(x1, y1_mem, x2, y2_mem, fill="#00ffff", width=2, dash=(2, 2))

            # Gráfico FPS (Laranja) - Normalizado para 120 FPS
            y1_fps = h - (min(self.history_fps[i], 120) / 120 * h)
            y2_fps = h - (min(self.history_fps[i+1], 120) / 120 * h)
            self.canvas_fps.create_line(x1, y1_fps, x2, y2_fps, fill="#ff8800", width=2)

            # Gráfico Rede (Amarelo)
            h_s = 40
            val1 = min(self.history_stream[i], 1000) / 1000 * h_s
            val2 = min(self.history_stream[i+1], 1000) / 1000 * h_s
            self.canvas_stream.create_line(x1, h_s - val1, x2, h_s - val2, fill="#ffcc00", width=2)

    def refresh(self):
        """Sincroniza a interface com as métricas capturadas em monitor_logic."""
        try:
            payload = collect_telemetry_payload()
            
            # Atualização de históricos
            self.history_core.pop(0); self.history_core.append(payload['core_load'])
            self.history_mem.pop(0); self.history_mem.append(payload['memory_usage'])
            self.history_fps.pop(0); self.history_fps.append(payload['fps_rate'])
            self.history_stream.pop(0); self.history_stream.append(payload['stream_in'])
            
            # Atualização dos textos (Labels)
            self.label_core.config(text=f"CORE: {payload['core_load']}%")
            self.label_temp.config(text=f"TEMP: {payload.get('cpu_temp', 0.0)}°C")
            self.label_mem.config(text=f"MEM: {payload['memory_usage']}%")
            self.label_fps.config(text=f"FPS: {payload['fps_rate']}")
            self.label_gpu.config(text=f"GPU Usage: {payload['gpu_load']}%")
            self.label_stream.config(text=f"⬇ {payload['stream_in']} KB/s | ⬆ {payload['stream_out']} KB/s")
            self.label_sub.config(text=f"{payload['energy_icon']} {payload['energy_percent']}% | 💽 {payload['volume_load']}%")
            
            self.render_charts()
        except Exception:
            pass

        self.root.after(self.update_interval, self.refresh)

if __name__ == "__main__":
    time.sleep(0.5)
    app = PerformanceGadget()
    app.root.mainloop()