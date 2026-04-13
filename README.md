# 🖥️ Monitor de Performance de Sistema

Este projeto é um agente de monitoramento desenvolvido em Python que fornece uma visão analítica e em tempo real sobre a saúde do hardware. Ele evoluiu de um monitor de terminal para um **Gadget Desktop flutuante** completo com gráficos dinâmicos e suporte multi-plataforma.

---

## 🔍 Visão Geral

O monitor extrai métricas vitais diretamente das APIs do sistema operacional, permitindo o acompanhamento de recursos de forma leve. A interface permanece visível sobre outros aplicativos (Always-on-Top), facilitando o monitoramento durante o uso intenso do computador.

## 🚀 Funcionalidades Atuais

* **Gadget Desktop**: Interface flutuante, sem bordas e com transparência ajustada.
* **Gráficos em Tempo Real**: Visualização dupla em linha para tendências de CPU/RAM e tráfego de Rede.
* **Métricas Expandidas**: Monitoramento de Download/Upload, nível de Bateria e uso de Disco.
* **Interatividade**: Suporte para arrastar a janela e botão de fechamento integrado.
* **Build Automático (CI/CD)**: Geração automática de executáveis para Windows e Linux via GitHub Actions.
* **Persistência de Dados**: Log automático de métricas em arquivos `.csv` para análise posterior.

## 🛠️ Tecnologias e Ferramentas

* **Python**: Lógica central e automação.
* **psutil**: Captura de métricas de hardware e rede.
* **Tkinter**: Interface gráfica (GUI).
* **PyInstaller**: Empacotamento para executáveis nativos.
* **GitHub Actions**: Automação de builds (CI) para múltiplas plataformas.

## 📂 Estrutura do Projeto

* `src/monitor_logic.py`: Motor de captura de dados, cálculo de rede e logs.
* `src/gadget_view.py`: Interface gráfica, renderização de gráficos e controles.
* `.github/workflows/build.yml`: Configuração do pipeline de automação de builds.
* `logs/`: Histórico de performance armazenado em CSV.

## 🚀 Roadmap de Evolução

### 1. Núcleo e Interface (Concluído)
* [x] Captura de métricas base (CPU, RAM, Disco).
* [x] Interface flutuante "Always-on-top" com suporte a drag-and-drop.
* [x] Botão de fechamento e melhorias de UI.

### 2. Expansão e Automação (Concluído)
* [x] **Monitoramento de Rede**: Gráfico dinâmico de Download/Upload.
* [x] **Status de Bateria**: Ícones dinâmicos para carga e descarga.
* [x] **Distribuição**: Builds automáticos para Windows (.exe) e Linux.

### 3. Personalização (Próximos Passos)
* [ ] Sistema de notificações nativas para picos de uso (>90%).
* [ ] Interface de configuração para ajuste de cores e opacidade.

---
*Este projeto é parte de um estudo prático de desenvolvimento de ferramentas de sistema e automação.*