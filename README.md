# InfraOps Auditor

> Ferramenta de auditoria de redes e inventário de infraestrutura desenvolvida em Python.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

---

## Sobre o projeto

O **InfraOps Auditor** é uma ferramenta desenvolvida para automatizar tarefas de auditoria e inventário de redes de computadores.

O projeto tem como objetivo identificar dispositivos conectados à rede, organizar essas informações em um inventário, detectar alterações na infraestrutura ao longo do tempo e gerar relatórios técnicos que auxiliem administradores de redes e infraestrutura.

Diferente de um simples scanner de rede, a proposta é evoluir para uma plataforma capaz de acompanhar mudanças nos ambientes monitorados, facilitando auditorias e reduzindo tarefas repetitivas.

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

- Descoberta automática de hosts.
- Identificação de fabricantes (MAC Vendor).
- Detecção de sistema operacional.
- Identificação de portas abertas.
- Identificação de serviços.

### Inventário

- Cadastro automático de ativos.
- Histórico de equipamentos.
- Classificação dos dispositivos.
- Organização por cliente.

### Comparação entre auditorias

- Novos dispositivos.
- Equipamentos removidos.
- Alteração de IP.
- Alteração de hostname.
- Alteração de serviços.

### Relatórios

- Excel
- PDF
- CSV

### Auditoria de Segurança

- Portas administrativas abertas.
- Protocolos legados.
- Verificações básicas de exposição.

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
│   ├── config/
│   ├── database/
│   ├── inventory/
│   ├── reports/
│   ├── scanner/
│   ├── utils/
│   └── main.py
│
├── tests/
├── README.md
└── requirements.txt
```

---

## Tecnologias

- Python
- Git
- Nmap
- SQLite

Tecnologias previstas para as próximas versões:

- Netmiko
- Pandas
- OpenPyXL
- Rich
- Flask

---

## Roadmap

### Versão 0.1

- [x] Estrutura inicial do projeto
- [ ] Menu principal
- [ ] Módulo de configuração

### Versão 0.2

- [ ] Scanner de rede

### Versão 0.3

- [ ] Banco SQLite
- [ ] Inventário de ativos

### Versão 0.4

- [ ] Comparação entre auditorias

### Versão 0.5

- [ ] Relatórios

### Versão 1.0

- [ ] Primeira versão estável

---

## Filosofia do projeto

O desenvolvimento segue alguns princípios fundamentais:

- Código limpo.
- Separação de responsabilidades.
- Arquitetura modular.
- Facilidade de manutenção.
- Evolução contínua.

O objetivo é construir uma ferramenta realmente útil para profissionais de infraestrutura, e não apenas um projeto de demonstração.

---

## Licença

Este projeto está licenciado sob a licença MIT.
