import tkinter as tk
from monitor_logic import obter_metricas

class GadgetMonitor:
    def __init__(self):
        self.root = tk.Tk()
        
        # Históricos: Listas para guardar os últimos 20 estados de CPU e RAM
        self.historico_cpu = [0] * 20 
        self.historico_ram = [0] * 20 
        
        # Configurações de Janela (sem bordas, transparente e sempre no topo)
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        self.root.attributes("-alpha", 0.9) 
        self.root.configure(bg='#1e1e1e')

        # Ajuste de tamanho para comportar o gráfico duplo
        largura, altura = 200, 180
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Label da CPU
        self.label_cpu = tk.Label(self.root, text="CPU: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 9, "bold"))
        self.label_cpu.pack(pady=(5, 0))

        # ÁREA DO GRÁFICO (Canvas)
        self.canvas = tk.Canvas(self.root, width=180, height=80, bg="#2d2d2d", highlightthickness=0)
        self.canvas.pack(pady=5)
        
        # Label da RAM
        self.label_ram = tk.Label(self.root, text="RAM: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 9, "bold"))
        self.label_ram.pack(pady=5)

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
        """Desenha as linhas de tendência de CPU e RAM no Canvas."""
        self.canvas.delete("all") # Limpa o desenho anterior
        largura_c = 180
        altura_c = 80
        pontos = 20
        x_passo = largura_c / (pontos - 1)

        for i in range(pontos - 1):
            x1 = i * x_passo
            x2 = (i + 1) * x_passo
            
            # Cálculo e desenho da linha da CPU (Verde)
            y1_cpu = altura_c - (self.historico_cpu[i] / 100 * altura_c)
            y2_cpu = altura_c - (self.historico_cpu[i+1] / 100 * altura_c)
            self.canvas.create_line(x1, y1_cpu, x2, y2_cpu, fill="#4aff4a", width=2)

            # Cálculo e desenho da linha da RAM (Ciano pontilhado)
            y1_ram = altura_c - (self.historico_ram[i] / 100 * altura_c)
            y2_ram = altura_c - (self.historico_ram[i+1] / 100 * altura_c)
            self.canvas.create_line(x1, y1_ram, x2, y2_ram, fill="#00ffff", width=2, dash=(2, 2))

    def obter_cor(self, percentual):
        """Define a cor baseada no nível de uso (para o texto da CPU)."""
        if percentual < 70: return "#4aff4a" # Verde neon
        if percentual < 90: return "#ffcc00" # Amarelo
        return "#ff4444" # Vermelho

    def atualizar(self):
        """Ciclo principal de atualização de dados e interface."""
        try:
            dados = obter_metricas()
            cpu = dados['cpu_percent']
            ram = dados['ram_percent']
            
            # Atualiza os históricos deslocando os valores
            self.historico_cpu.pop(0)
            self.historico_cpu.append(cpu)
            
            self.historico_ram.pop(0)
            self.historico_ram.append(ram)
            
            # Atualiza textos e cores dinâmicas
            cor_cpu = self.obter_cor(cpu)
            self.label_cpu.config(text=f"CPU: {cpu}%", fg=cor_cpu)
            self.label_ram.config(text=f"RAM: {ram}%", fg="#00ffff")
            
            self.desenhar_graficos()
        except Exception as e:
            print(f"Erro na atualização: {e}")

        # Agenda a próxima execução para 1 segundo
        self.root.after(1000, self.atualizar)

if __name__ == "__main__":
    try:
        app = GadgetMonitor()
        app.root.mainloop()
    except KeyboardInterrupt:
        print("\nGadget encerrado com sucesso.")