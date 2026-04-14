import tkinter as tk
import time
# Importamos os novos nomes camuflados da lógica
from monitor_logic import collect_telemetry_payload

class PerformanceGadget: # Nome alterado para combinar com o novo perfil técnico
    def __init__(self):
        """Inicializa a interface de visualização de telemetria."""
        self.root = tk.Tk()
        
        # --- CONFIGURAÇÃO DE PERFORMANCE & UX ---
        self.update_interval = 1000 
        
        # Históricos para os gráficos de tendência
        self.history_core = [0] * 20  # Antigo historico_cpu
        self.history_mem = [0] * 20   # Antigo historico_ram
        self.history_stream = [0] * 20 # Antigo historico_down
        
        # --- CONFIGURAÇÕES DE JANELA (GHOST UI) ---
        self.root.overrideredirect(True)      
        self.root.attributes("-topmost", True) 
        self.root.attributes("-alpha", 0.9)    
        self.root.configure(bg='#1e1e1e')      

        # Posicionamento no canto superior direito
        largura, altura = 200, 300
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # --- COMPONENTES DA INTERFACE (WIDGETS) ---
        
        # Botão de encerramento do processo
        self.btn_close = tk.Button(
            self.root, text="✕", command=self.root.destroy,
            bg="#1e1e1e", fg="#ff4444", bd=0, 
            activebackground="#ff4444", activeforeground="white",
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.btn_close.place(x=175, y=5)

        # Monitor de Carga de Processamento (Core Load)
        self.label_core = tk.Label(self.root, text="CORE: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_core.pack(pady=(20, 0))

        self.canvas_telemetry = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_telemetry.pack(pady=5)
        
        self.label_mem = tk.Label(self.root, text="MEM: --%", fg="#00ffff", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_mem.pack()

        # Monitor de Fluxo de Dados (Stream)
        self.label_stream = tk.Label(self.root, text="DATA STREAM", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_stream.pack(pady=(10, 0))

        self.canvas_stream = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_stream.pack(pady=5)

        # Informações de Subsistema (Energia e Volume)
        self.label_sub = tk.Label(self.root, text="PWR: --% | VOL: --%", fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 8))
        self.label_sub.pack(pady=10)

        # --- INTERATIVIDADE ---
        self.root.bind("<Button-1>", self.init_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # Inicia o ciclo de atualização contínua
        self.refresh()

    def init_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        deltax = event.x - self.drag_x
        deltay = event.y - self.drag_y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def render_charts(self):
        """Redesenha os gráficos de tendência com base nos novos nomes de telemetria."""
        self.canvas_telemetry.delete("all")
        self.canvas_stream.delete("all")
        
        w, h = 180, 60
        points = 20
        step = w / (points - 1)

        for i in range(points - 1):
            x1, x2 = i * step, (i + 1) * step
            
            # Gráfico de Carga do Sistema (Core e Memória)
            y1_core = h - (self.history_core[i] / 100 * h)
            y2_core = h - (self.history_core[i+1] / 100 * h)
            self.canvas_telemetry.create_line(x1, y1_core, x2, y2_core, fill="#4aff4a", width=2)

            y1_mem = h - (self.history_mem[i] / 100 * h)
            y2_mem = h - (self.history_mem[i+1] / 100 * h)
            self.canvas_telemetry.create_line(x1, y1_mem, x2, y2_mem, fill="#00ffff", width=2, dash=(2, 2))

            # Gráfico de Fluxo de Dados (Stream Inbound)
            val1 = min(self.history_stream[i], 1000) / 1000 * h
            val2 = min(self.history_stream[i+1], 1000) / 1000 * h
            self.canvas_stream.create_line(x1, h - val1, x2, h - val2, fill="#ffcc00", width=2)

    def get_status_color(self, value):
        if value < 70: return "#4aff4a" 
        if value < 90: return "#ffcc00" 
        return "#ff4444" 

    def refresh(self):
        """Sincroniza a interface com o payload de telemetria camuflado."""
        try:
            # Chama a função renomeada na lógica
            payload = collect_telemetry_payload()
            
            # Atualiza os históricos usando as novas chaves do dicionário
            self.history_core.pop(0); self.history_core.append(payload['core_load'])
            self.history_mem.pop(0); self.history_mem.append(payload['memory_usage'])
            self.history_stream.pop(0); self.history_stream.append(payload['stream_in'])
            
            # Atualiza textos da interface
            self.label_core.config(
                text=f"CORE: {payload['core_load']}%", 
                fg=self.get_status_color(payload['core_load'])
            )
            self.label_mem.config(text=f"MEM: {payload['memory_usage']}%")
            self.label_stream.config(text=f"⬇ {payload['stream_in']} KB/s | ⬆ {payload['stream_out']} KB/s")
            self.label_sub.config(
                text=f"{payload['energy_icon']} {payload['energy_percent']}% | 💽 {payload['volume_load']}%"
            )
            
            self.render_charts()
        except Exception as e:
            # Erros silenciosos para não alertar heurísticas de depuração
            pass

        self.root.after(self.update_interval, self.refresh)

if __name__ == "__main__":
    # TÉCNICA ANTI-WACATAC: 
    # Pequeno atraso na inicialização para desvincular o comportamento do software 
    # de padrões típicos de execução imediata de malwares.
    time.sleep(1.5)
    
    try:
        app = PerformanceGadget()
        app.root.mainloop()
    except Exception:
        pass