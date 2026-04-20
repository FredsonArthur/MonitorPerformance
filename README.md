# 🖥️ Monitor de Performance de Sistema - v1.1.5

Este projeto é um agente de monitoramento desenvolvido em Python que fornece uma visão analítica e em tempo real sobre a saúde do hardware. Ele evoluiu de um monitor de terminal para um **Gadget Desktop flutuante** completo com gráficos dinâmicos e suporte multi-plataforma.

---

## 🔍 Visão Geral

O monitor extrai métricas vitais diretamente das APIs do sistema operacional, permitindo o acompanhamento de recursos de forma leve. A interface permanece visível sobre outros aplicativos (Always-on-Top), facilitando o monitoramento durante o uso intenso do computador.

## 🚀 Novidades da Versão 1.1.5

* **Monitoramento de FPS**: Captura em tempo real da taxa de quadros global do sistema via Performance Counters.
* **Telemetria Térmica**: Monitoramento de temperatura da CPU integrado (requer privilégios de administrador).
* **Gráficos Expandidos**: Novo gráfico laranja dedicado à estabilidade de FPS e carga de GPU.
* **Layout Otimizado**: Janela redimensionada para exibir simultaneamente Core, Temp, FPS, RAM e Rede.

## 🚀 Funcionalidades Atuais

* **Gadget Desktop**: Interface flutuante, sem bordas e com transparência ajustada.
* **Gráficos em Tempo Real**: Visualização tripla em linha para tendências de CPU/RAM, FPS/GPU e tráfego de Rede.
* **Métricas Expandidas**: Monitoramento de Download/Upload, nível de Bateria e uso de Disco.
* **Interatividade**: Suporte para arrastar a janela e botão de fechamento integrado.
* **Build Automático (CI/CD)**: Geração automática de executáveis para Windows via GitHub Actions.
* **Persistência de Dados**: Log automático em `.csv` incluindo agora FPS e Temperatura.

## 🛠️ Tecnologias e Ferramentas

* **Python**: Lógica central e automação.
* **psutil**: Captura de métricas de hardware e rede.
* **win32pdh & wmi**: Motores de captura para FPS, GPU e Temperatura.
* **Tkinter**: Interface gráfica (GUI).
* **PyInstaller**: Empacotamento para executáveis nativos.

## 📂 Estrutura do Projeto

* `src/monitor_logic.py`: Motor de captura de dados, FPS, temperatura e logs.
* `src/gadget_view.py`: Interface gráfica, renderização de gráficos e controles.
* `.github/workflows/build.yml`: Configuração do pipeline de automação de builds.

---
*Este projeto é parte de um estudo prático de desenvolvimento de ferramentas de sistema e automação.*