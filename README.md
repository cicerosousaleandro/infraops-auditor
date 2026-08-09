# InfraOps Auditor

> Ferramenta de auditoria de redes e inventário de infraestrutura desenvolvida em Python.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

---

## Sobre o projeto

O **InfraOps Auditor** é uma ferramenta desenvolvida para automatizar tarefas de auditoria, descoberta de dispositivos e inventário de redes de computadores.

O projeto nasceu a partir de necessidades reais encontradas no gerenciamento de ambientes corporativos e está sendo desenvolvido de forma incremental, priorizando arquitetura, organização do código e evolução contínua.

A proposta é ir além de um simples scanner de rede, evoluindo para uma plataforma capaz de manter inventários atualizados, detectar alterações na infraestrutura, gerar relatórios técnicos e futuramente integrar monitoramento e recursos voltados para operações de infraestrutura e segurança.

---

## Estado atual do projeto

Atualmente o InfraOps Auditor já é capaz de:

- Descobrir as interfaces de rede da máquina.
- Permitir a seleção da interface que será utilizada.
- Calcular automaticamente as informações da rede IPv4.
- Identificar:
  - Endereço da rede
  - Broadcast
  - Prefixo CIDR
  - Primeiro host
  - Último host
  - Quantidade de hosts utilizáveis
- Realizar descoberta de dispositivos utilizando Nmap.
- Exibir os dispositivos encontrados na rede.

Todo o desenvolvimento está sendo realizado passo a passo, com foco em arquitetura e boas práticas, permitindo que a aplicação cresça sem perder organização.

---

## Motivação

Este projeto surgiu a partir de uma necessidade real do dia a dia na administração de ambientes de infraestrutura.

Entre as atividades que motivaram seu desenvolvimento estão:

- Descoberta automática de dispositivos.
- Inventário de ativos.
- Identificação de novos equipamentos.
- Detecção de alterações na rede.
- Geração de relatórios técnicos.
- Apoio em auditorias de infraestrutura.

O objetivo é reduzir o tempo gasto em tarefas repetitivas e fornecer uma visão consolidada dos ambientes monitorados.

---

## Funcionalidades planejadas

### Descoberta de dispositivos

- ✅ Descoberta automática de hosts
- ✅ Seleção da interface de rede
- ✅ Cálculo automático da rede IPv4
- ⏳ Identificação de fabricantes (MAC Vendor)
- ⏳ Descoberta de hostname
- ⏳ Detecção de sistema operacional
- ⏳ Identificação de portas abertas
- ⏳ Identificação de serviços

### Inventário

- Cadastro automático de ativos
- Histórico de equipamentos
- Classificação dos dispositivos
- Organização por cliente

### Comparação entre auditorias

- Novos dispositivos
- Equipamentos removidos
- Alteração de IP
- Alteração de hostname
- Alteração de serviços

### Relatórios

- Excel
- PDF
- CSV

### Auditoria de Segurança

- Portas administrativas abertas
- Protocolos legados
- Verificações básicas de exposição

### Integrações futuras

- MikroTik
- SNMP
- Wazuh
- Zabbix
- Telegram
- E-mail

---

## Estrutura do projeto

```text
InfraOps-Auditor
│
├── docs/
├── exports/
├── logs/
├── src/
│   ├── app/
│   ├── config/
│   ├── database/
│   ├── inventory/
│   ├── models/
│   ├── reports/
│   ├── scanner/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
├── README.md
└── requirements.txt
```

---

## Tecnologias

### Utilizadas atualmente

- Python 3.13
- Nmap
- python-nmap
- psutil
- SQLite
- Git

### Previstas para as próximas versões

- Netmiko
- Pandas
- OpenPyXL
- Rich
- Flask

---

## Roadmap

### Versão 0.1

- [x] Estrutura inicial do projeto
- [x] Menu principal
- [x] Descoberta das interfaces de rede
- [x] Seleção da interface
- [x] Cálculo da rede IPv4
- [x] Descoberta inicial de dispositivos
- [ ] Organização do inventário

### Versão 0.2

- [ ] Identificação de hostname
- [ ] Identificação de fabricante (MAC Vendor)
- [ ] Descoberta de portas
- [ ] Descoberta de serviços

### Versão 0.3

- [ ] Banco SQLite
- [ ] Inventário persistente
- [ ] Histórico de auditorias

### Versão 0.4

- [ ] Comparação entre auditorias
- [ ] Detecção de alterações

### Versão 0.5

- [ ] Relatórios
- [ ] Exportação para Excel, CSV e PDF

### Versão 1.0

- [ ] Plataforma estável para inventário e auditoria de infraestrutura

---

## Filosofia do projeto

O InfraOps Auditor está sendo desenvolvido de forma incremental.

Cada funcionalidade é implementada, validada e integrada antes da próxima etapa ser iniciada.

Esse processo permite compreender cada decisão arquitetural, manter o código organizado e preparar uma base sólida para futuras funcionalidades, como inventário distribuído, monitoramento, integração com ferramentas de infraestrutura e recursos voltados para segurança da informação.

---

## Licença

Este projeto está licenciado sob a licença MIT.
