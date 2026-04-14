import tkinter as tk
from monitor_logic import obter_metricas

class GadgetMonitor:
    def __init__(self):
        """Inicializa a interface gráfica e as configurações do sistema."""
        self.root = tk.Tk()
        
        # --- CONFIGURAÇÃO DE PERFORMANCE & UX ---
        # Intervalo em milissegundos para o loop de atualização.
        # 1000ms (1 segundo) evita a percepção de 'bug' por atualizações frenéticas.
        self.update_interval = 1000 
        
        # Históricos: Listas que armazenam os últimos 20 pontos de dados para os gráficos.
        # Iniciamos com zeros para o gráfico começar do 'chão'.
        self.historico_cpu = [0] * 20 
        self.historico_ram = [0] * 20 
        self.historico_down = [0] * 20 
        
        # --- CONFIGURAÇÕES DE JANELA (GHOST UI) ---
        self.root.overrideredirect(True)      # Remove bordas, barra de título e botões padrão.
        self.root.attributes("-topmost", True) # Mantém o gadget sempre acima de outras janelas.
        self.root.attributes("-alpha", 0.9)    # Define uma leve transparência (90% opaco).
        self.root.configure(bg='#1e1e1e')      # Fundo cinza escuro (estilo VS Code).

        # Posicionamento: Canto superior direito da tela com margem de 20px.
        largura, altura = 200, 300
        pos_x = self.root.winfo_screenwidth() - largura - 20
        pos_y = 40
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # --- COMPONENTES DA INTERFACE (WIDGETS) ---
        
        # Botão Fechar: Posicionado manualmente no canto superior direito.
        self.btn_fechar = tk.Button(
            self.root, text="✕", command=self.root.destroy,
            bg="#1e1e1e", fg="#ff4444", bd=0, 
            activebackground="#ff4444", activeforeground="white",
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.btn_fechar.place(x=175, y=5)

        # Seção CPU: Rótulo e Área de Desenho (Canvas).
        self.label_cpu = tk.Label(self.root, text="CPU: --%", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_cpu.pack(pady=(20, 0))

        self.canvas_sys = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_sys.pack(pady=5)
        
        self.label_ram = tk.Label(self.root, text="RAM: --%", fg="#00ffff", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_ram.pack()

        # Seção Rede: Mostra a velocidade de Download no gráfico e Upload no texto.
        self.label_net = tk.Label(self.root, text="REDE (Download)", fg="white", bg="#1e1e1e", font=("Segoe UI", 8, "bold"))
        self.label_net.pack(pady=(10, 0))

        self.canvas_net = tk.Canvas(self.root, width=180, height=60, bg="#2d2d2d", highlightthickness=0)
        self.canvas_net.pack(pady=5)

        # Seção Extra: Rodapé com Bateria e Uso de Disco.
        self.label_extra = tk.Label(self.root, text="BAT: --% | DSK: --%", fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 8))
        self.label_extra.pack(pady=10)

        # --- INTERATIVIDADE ---
        # Permite arrastar a janela clicando em qualquer parte do fundo.
        self.root.bind("<Button-1>", self.iniciar_movimento)
        self.root.bind("<B1-Motion>", self.executar_movimento)

        # Inicia o ciclo de atualização.
        self.atualizar()

    def iniciar_movimento(self, event):
        """Registra as coordenadas iniciais quando o mouse é clicado."""
        self.x = event.x
        self.y = event.y

    def executar_movimento(self, event):
        """Calcula a nova posição da janela baseada no arrasto do mouse."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def desenhar_graficos(self):
        """Limpa e redesenha as linhas de tendência nos Canvas."""
        self.canvas_sys.delete("all")
        self.canvas_net.delete("all")
        
        largura_c, altura_c = 180, 60
        pontos = 20
        x_passo = largura_c / (pontos - 1) # Distância horizontal entre cada ponto.

        for i in range(pontos - 1):
            x1, x2 = i * x_passo, (i + 1) * x_passo
            
            # --- Gráfico de Sistema (CPU e RAM no mesmo espaço) ---
            # Cálculo do Y: Altura total menos o percentual (Invertido porque Y=0 é o topo).
            y1_cpu = altura_c - (self.historico_cpu[i] / 100 * altura_c)
            y2_cpu = altura_c - (self.historico_cpu[i+1] / 100 * altura_c)
            self.canvas_sys.create_line(x1, y1_cpu, x2, y2_cpu, fill="#4aff4a", width=2)

            y1_ram = altura_c - (self.historico_ram[i] / 100 * altura_c)
            y2_ram = altura_c - (self.historico_ram[i+1] / 100 * altura_c)
            self.canvas_sys.create_line(x1, y1_ram, x2, y2_ram, fill="#00ffff", width=2, dash=(2, 2))

            # --- Gráfico de Rede ---
            # Normalizamos o teto para 1000 KB/s para o gráfico ter uma escala visível.
            val1 = min(self.historico_down[i], 1000) / 1000 * altura_c
            val2 = min(self.historico_down[i+1], 1000) / 1000 * altura_c
            self.canvas_net.create_line(x1, altura_c - val1, x2, altura_c - val2, fill="#ffcc00", width=2)

    def obter_cor_alerta(self, percentual):
        """Retorna uma cor de alerta baseada na carga do hardware."""
        if percentual < 70: return "#4aff4a"  # Verde: Normal
        if percentual < 90: return "#ffcc00"  # Amarelo: Atenção
        return "#ff4444"                      # Vermelho: Crítico

    def atualizar(self):
        """Busca novos dados e atualiza todos os componentes da interface."""
        try:
            # Busca o dicionário de métricas vindo da monitor_logic.py
            d = obter_metricas()
            
            # Atualiza as listas de histórico (remove o mais antigo, adiciona o novo).
            self.historico_cpu.pop(0); self.historico_cpu.append(d['cpu_percent'])
            self.historico_ram.pop(0); self.historico_ram.append(d['ram_percent'])
            self.historico_down.pop(0); self.historico_down.append(d['net_down'])
            
            # Atualiza os textos e cores dinâmicas.
            self.label_cpu.config(text=f"CPU: {d['cpu_percent']}%", fg=self.obter_cor_alerta(d['cpu_percent']))
            self.label_ram.config(text=f"RAM: {d['ram_percent']}%")
            self.label_net.config(text=f"⬇ {d['net_down']} KB/s | ⬆ {d['net_up']} KB/s")
            self.label_extra.config(text=f"{d['bat_status']} {d['bat_percent']}% | 💽 {d['disco_percent']}%")
            
            # Redesenha os gráficos com os novos pontos.
            self.desenhar_graficos()
        except Exception as e:
            print(f"Erro na atualização da interface: {e}")

        # Agenda a próxima execução baseada no intervalo definido.
        self.root.after(self.update_interval, self.atualizar)

if __name__ == "__main__":
    try:
        app = GadgetMonitor()
        app.root.mainloop()
    except KeyboardInterrupt:
        print("\nGadget encerrado pelo usuário.")