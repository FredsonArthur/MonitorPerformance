import tkinter as tk
from monitor_logic import obter_metricas

class GadgetMonitor:
    def __init__(self):
        self.root = tk.Tk()
        
        # Configurações de Janela
        self.root.overrideredirect(True)  # Remove bordas
        self.root.attributes("-topmost", True)  # Sempre no topo
        self.root.attributes("-alpha", 0.85)  # Transparência
        self.root.configure(bg='#1e1e1e') # Fundo escuro grafite

        # Tamanho e posição inicial
        largura, altura = 180, 80
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Labels formatadas
        self.label_cpu = tk.Label(self.root, text="CPU: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 11, "bold"))
        self.label_cpu.pack(pady=(10, 0))
        
        self.label_ram = tk.Label(self.root, text="RAM: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 11, "bold"))
        self.label_ram.pack(pady=5)

        # Eventos para arrastar a janela
        self.root.bind("<Button-1>", self.iniciar_movimento)
        self.root.bind("<B1-Motion>", self.parar_movimento)

        self.atualizar()

    def iniciar_movimento(self, event):
        self.x = event.x
        self.y = event.y

    def parar_movimento(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def obter_cor(self, percentual):
        if percentual < 70: return "#4aff4a" # Verde neon
        if percentual < 90: return "#ffcc00" # Amarelo
        return "#ff4444" # Vermelho

    def atualizar(self):
        try:
            # Importante: obter_metricas agora deve rodar sem interval=1 dentro da logic
            dados = obter_metricas()
            
            self.label_cpu.config(text=f"CPU: {dados['cpu_percent']}%", fg=self.obter_cor(dados['cpu_percent']))
            self.label_ram.config(text=f"RAM: {dados['ram_percent']}%", fg=self.obter_cor(dados['ram_percent']))
        except:
            pass

        # Atualiza a cada 1 segundo (1000ms)
        self.root.after(1000, self.atualizar)

if __name__ == "__main__":
    try:
        app = GadgetMonitor()
        app.root.mainloop()
    except KeyboardInterrupt:
        print("Gadget Monitor encerrado com sucesso.")