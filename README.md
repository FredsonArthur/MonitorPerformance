# 🖥️ Monitor de Performance de Sistema

Este projeto é um agente de monitoramento desenvolvido em Python que fornece uma visão analítica e em tempo real sobre a saúde do hardware. Ele evoluiu de um simples monitor de terminal para um **Gadget Desktop flutuante** com gráficos dinâmicos.

---

## 🔍 Visão Geral

O monitor extrai métricas vitais diretamente das APIs do sistema operacional, permitindo o acompanhamento de recursos sem a necessidade de softwares pesados. Ele agora conta com uma interface gráfica leve que permanece visível sobre outros aplicativos.

## 🚀 Funcionalidades Atuais

* **Gadget Desktop**: Interface flutuante, sem bordas e transparente (Always-on-Top).
* **Gráficos em Tempo Real**: Visualização em linha para tendências de uso de CPU e RAM.
* **Interatividade**: O gadget pode ser arrastado para qualquer posição da tela.
* **Sistema de Alertas**: Mudança dinâmica de cores (Verde/Amarelo/Vermelho) conforme o nível de estresse do hardware.
* **Persistência de Dados**: Log automático de métricas em arquivos `.csv` para análise posterior.

## 🛠️ Tecnologias e Ferramentas

* **Python**: Lógica central e automação.
* **psutil**: Captura de métricas de CPU, RAM, Disco e Rede.
* **Tkinter**: Interface gráfica (GUI) para o gadget flutuante.
* **Git & GitHub**: Gerenciamento de versão e workflow de desenvolvimento.

## 📂 Estrutura do Projeto

* `src/monitor_logic.py`: Motor de captura de dados e salvamento de logs.
* `src/gadget_view.py`: Interface gráfica e renderização dos gráficos.
* `src/app.py`: Versão clássica para monitoramento via terminal.
* `logs/`: Armazenamento dos históricos de performance.

## 🚀 Próximos Passos (Roadmap)

### 1. Camada Base & Interface (Concluído)
* [x] Captura de CPU, RAM e Disco.
* [x] Criação do Gadget flutuante com suporte a arrastar.
* [x] Gráficos de linha dinâmicos para CPU e RAM.

### 2. Expansão de Métricas (Em Andamento)
* [ ] **Monitoramento de Rede**: Gráfico exclusivo para Download e Upload.
* [ ] **Status de Bateria**: Monitoramento de carga e conexão para notebooks (IdeaPad).

### 3. Personalização e Alertas
* [ ] Configuração de opacidade e cores via interface.
* [ ] Notificações de sistema para picos de uso acima de 95%.

---
*Este projeto é parte de um estudo prático de desenvolvimento de ferramentas de sistema e automação.*