import tkinter as tk
from monitor_logic import obter_metricas

class GadgetMonitor:
    def __init__(self):
        self.root = tk.Tk()
        
        # Históricos: Listas para guardar os últimos 20 estados de cada métrica
        self.historico_cpu = [0] * 20 
        self.historico_ram = [0] * 20 
        self.historico_down = [0] * 20 
        
        # Configurações de Janela (sem bordas, transparente e sempre no topo)
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        self.root.attributes("-alpha", 0.9) 
        self.root.configure(bg='#1e1e1e')

        # Ajuste de tamanho para comportar gráficos, botão de fechar e infos extras
        largura, altura = 200, 300
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # --- BOTÃO FECHAR (X) ---
        self.btn_fechar = tk.Button(
            self.root, text="✕", command=self.root.destroy,
            bg="#1e1e1e", fg="#ff4444", bd=0, 
            activebackground="#ff4444", activeforeground="white",
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.btn_fechar.place(x=175, y=5)

        # --- SEÇÃO CPU & RAM ---
        self.label_cpu = tk.Label(self.root, text="CPU: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_cpu.pack(pady=(20, 0)) # Padding maior para não sobrepor o botão X

        self.canvas_sys = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_sys.pack(pady=5)
        
        self.label_ram = tk.Label(self.root, text="RAM: --%", fg="#00ffff", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_ram.pack()

        # --- SEÇÃO REDE (Download) ---
        self.label_net = tk.Label(self.root, text="REDE (Download)", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_net.pack(pady=(10, 0))

        self.canvas_net = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_net.pack(pady=5)

        # --- SEÇÃO INFO EXTRA (Bateria e Disco) ---
        self.label_extra = tk.Label(self.root, text="BAT: --% | DSK: --%", fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 8))
        self.label_extra.pack(pady=10)

        # Eventos para arrastar a janela com o mouse
        self.root.bind("<Button-1>", self.iniciar_movimento)
        self.root.bind("<B1-Motion>", self.parar_movimento)

        self.atualizar()

    def iniciar_movimento(self, event):
        """Captura a posição inicial do clique."""
        self.x = event.x
        self.y = event.y

    def parar_movimento(self, event):
        """Calcula o deslocamento e move a janela."""
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def desenhar_graficos(self):
        """Renderiza as linhas de tendência nos respectivos Canvas."""
        self.canvas_sys.delete("all")
        self.canvas_net.delete("all")
        
        largura_c, altura_c = 180, 60
        pontos = 20
        x_passo = largura_c / (pontos - 1)

        for i in range(pontos - 1):
            x1, x2 = i * x_passo, (i + 1) * x_passo
            
            # --- Gráfico de Sistema ---
            # CPU (Verde)
            y1_cpu = altura_c - (self.historico_cpu[i] / 100 * altura_c)
            y2_cpu = altura_c - (self.historico_cpu[i+1] / 100 * altura_c)
            self.canvas_sys.create_line(x1, y1_cpu, x2, y2_cpu, fill="#4aff4a", width=2)

            # RAM (Ciano pontilhado)
            y1_ram = altura_c - (self.historico_ram[i] / 100 * altura_c)
            y2_ram = altura_c - (self.historico_ram[i+1] / 100 * altura_c)
            self.canvas_sys.create_line(x1, y1_ram, x2, y2_ram, fill="#00ffff", width=2, dash=(2, 2))

            # --- Gráfico de Rede (Download) ---
            val1 = min(self.historico_down[i], 1000) / 1000 * altura_c
            val2 = min(self.historico_down[i+1], 1000) / 1000 * altura_c
            self.canvas_net.create_line(x1, altura_c - val1, x2, altura_c - val2, fill="#ffcc00", width=2)

    def obter_cor(self, percentual):
        """Define a cor baseada no nível de uso."""
        if percentual < 70: return "#4aff4a"
        if percentual < 90: return "#ffcc00"
        return "#ff4444"

    def atualizar(self):
        """Ciclo principal de atualização de dados e interface."""
        try:
            d = obter_metricas()
            
            # Atualiza os históricos
            self.historico_cpu.pop(0); self.historico_cpu.append(d['cpu_percent'])
            self.historico_ram.pop(0); self.historico_ram.append(d['ram_percent'])
            self.historico_down.pop(0); self.historico_down.append(d['net_down'])
            
            # Atualiza textos e cores
            self.label_cpu.config(text=f"CPU: {d['cpu_percent']}%", fg=self.obter_cor(d['cpu_percent']))
            self.label_ram.config(text=f"RAM: {d['ram_percent']}%")
            self.label_net.config(text=f"⬇ {d['net_down']} KB/s | ⬆ {d['net_up']} KB/s")
            self.label_extra.config(text=f"{d['bat_status']} {d['bat_percent']}% | 💽 {d['disco_percent']}%")
            
            self.desenhar_graficos()
        except Exception as e:
            print(f"Erro na atualização: {e}")

        self.root.after(1000, self.atualizar)

if __name__ == "__main__":
    try:
        app = GadgetMonitor()
        app.root.mainloop()
    except KeyboardInterrupt:
        print("\nGadget encerrado.")