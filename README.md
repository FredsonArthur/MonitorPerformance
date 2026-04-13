# 🖥️ Monitor de Performance de Sistema

Este projeto consiste em um agente de monitoramento desenvolvido em Python, focado em fornecer uma visão analítica e em tempo real sobre a saúde e o consumo de recursos do hardware. 

O objetivo é transformar o terminal em um dashboard informativo e leve, evitando a necessidade de interfaces pesadas para checagens rápidas de performance.

---

## 🔍 Visão Geral do Projeto

O monitor opera através de um ciclo de interrogação do sistema, onde extrai métricas vitais diretamente das APIs do sistema operacional. Ele foi projetado para ser modular, permitindo que novas camadas de análise (como logs e notificações) sejam acopladas à estrutura base.

## 🛠️ Tecnologias e Ferramentas

Para a construção deste ecossistema, estamos utilizando:

* **Linguagem Python**: Base para toda a lógica de processamento e automação.
* **Biblioteca psutil**: O principal componente para recuperação de informações do sistema (CPU, memória, discos, rede e processos).
* **Git & GitHub**: Para versionamento semântico e gerenciamento do ciclo de vida do software.
* **Visual Studio Code**: Ambiente de desenvolvimento principal, integrado com ferramentas de depuração e terminal.

## 🚀 Próximos Passos (Roadmap de Evolução)

O projeto está sendo construído seguindo uma trilha de evolução incremental:

### 1. Camada de Monitoramento Base
* [x] Captura de percentual de uso da CPU.
* [x] Medição de memória RAM disponível e utilizada.
* [x] Ciclo de atualização em tempo real no terminal.

### 2. Inteligência e Persistência (Em Planejamento)
* **Logging Analítico**: Implementação de registros em arquivos `.csv` ou `.log` para análise histórica de comportamento do hardware.
* **Alertas de Pico**: Sistema de monitoramento que identifica quando os recursos atingem níveis críticos (ex: acima de 90%) e gera avisos.

### 3. Interface e Experiência
* **Refinamento Visual**: Implementação de bibliotecas para exibição de gráficos de barras e tabelas coloridas no console.
* **Detalhamento de Hardware**: Inclusão de métricas de temperatura, leitura/escrita de disco e tráfego de rede (Upload/Download).

---
*Este projeto é parte de um estudo prático de desenvolvimento de ferramentas de sistema e automação.*