# InfraOps Auditor

> Ferramenta de auditoria de redes, descoberta de dispositivos e inventário de infraestrutura desenvolvida em Python.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

---

## Sobre o projeto

O **InfraOps Auditor** é uma ferramenta desenvolvida para automatizar tarefas de auditoria, descoberta de dispositivos e inventário de redes de computadores.

O projeto nasceu a partir de necessidades reais encontradas no gerenciamento de ambientes corporativos e está sendo desenvolvido de forma incremental, priorizando arquitetura, organização do código, persistência de informações e evolução contínua.

A proposta é ir além de um simples scanner de rede, evoluindo para uma plataforma capaz de manter inventários atualizados, detectar alterações na infraestrutura, correlacionar informações provenientes de diferentes fontes, gerar relatórios técnicos e futuramente integrar monitoramento e recursos voltados para operações de infraestrutura e segurança da informação.

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
- Identificar endereço IP.
- Identificar endereço MAC.
- Identificar hostname quando disponível.
- Identificar fabricante através do MAC Address.
- Persistir auditorias utilizando SQLite.
- Manter histórico de auditorias separado por rede.
- Comparar auditorias anteriores com a auditoria atual.
- Detectar novos dispositivos.
- Detectar dispositivos ausentes.
- Detectar dispositivos que retornaram à rede.
- Detectar alterações em dispositivos conhecidos.
- Identificar alterações de IP.
- Identificar alterações de hostname.
- Identificar alterações de status.
- Identificar alterações de fabricante.
- Integrar com equipamentos MikroTik através da API do RouterOS.
- Consultar leases DHCP do MikroTik.
- Representar leases DHCP através do modelo `DHCPLease`.

A integração com MikroTik está sendo desenvolvida e validada inicialmente em ambiente de laboratório.

---

## Motivação

Este projeto surgiu a partir de uma necessidade real do dia a dia na administração de ambientes de infraestrutura.

Entre as atividades que motivaram seu desenvolvimento estão:

- Descoberta automática de dispositivos.
- Inventário de ativos.
- Identificação de novos equipamentos.
- Detecção de alterações na rede.
- Análise histórica da infraestrutura.
- Integração com equipamentos de rede.
- Geração de relatórios técnicos.
- Apoio em auditorias de infraestrutura e segurança.

O objetivo é reduzir o tempo gasto em tarefas repetitivas e fornecer uma visão consolidada e histórica dos ambientes monitorados.

---

## Arquitetura atual

O projeto está sendo organizado com separação de responsabilidades entre modelos, serviços, persistência e aplicação.

Fluxo simplificado:

    InfraOps Auditor
            |
            v
       Application
            |
      +-----+-----+
      |           |
      v           v
    Scanner    MikroTik
    Service     Service
      |           |
      v           v
    Device     DHCPLease
      |           |
      +-----+-----+
            |
            v
    ComparisonService
            |
            v
          SQLite

A arquitetura está sendo construída de forma incremental para evitar que a lógica de negócio fique concentrada em uma única classe ou arquivo.

---

## Descoberta de dispositivos

O mecanismo de descoberta utiliza a rede selecionada para identificar dispositivos disponíveis.

As informações coletadas podem incluir:

- IP.
- MAC Address.
- Hostname.
- Fabricante.
- Status.

O endereço MAC é utilizado como identidade principal do dispositivo durante a comparação entre auditorias.

Isso permite detectar situações como:

    Auditoria anterior:

    MAC: AA:BB:CC:DD:EE:FF
    IP : 192.168.0.50

    Auditoria atual:

    MAC: AA:BB:CC:DD:EE:FF
    IP : 192.168.0.80

Nesse cenário, o InfraOps identifica que o dispositivo continua sendo o mesmo, mas seu endereço IP foi alterado.

---

## Identificação de fabricantes

O InfraOps utiliza o MAC Address para identificar o fabricante do dispositivo quando essa informação está disponível.

Durante os testes já foram identificados fabricantes como:

- Routerboard.com
- Raspberry Pi Foundation
- Seiko Epson
- Ubiquiti
- Dell
- Intel Corporate
- TP-Link Systems
- Control iD
- Khomp

Quando não é possível identificar o fabricante, o sistema utiliza:

    Desconhecido

---

## Persistência e histórico

As auditorias são armazenadas utilizando SQLite.

Cada auditoria registra a rede analisada e os dispositivos encontrados naquele momento.

O histórico é isolado por rede.

Isso é importante porque uma mesma aplicação pode realizar auditorias em redes diferentes sem misturar os dispositivos entre elas.

Exemplo:

    192.168.0.0/24
    192.168.3.0/24
    172.31.128.0/20

Cada rede possui seu próprio histórico de auditorias.

---

## Comparação entre auditorias

O InfraOps possui um mecanismo de comparação entre auditorias.

Atualmente são identificadas quatro categorias principais:

### Novos dispositivos

Dispositivos que não estavam presentes nas auditorias anteriores.

### Dispositivos ausentes

Dispositivos presentes na auditoria anterior que não foram encontrados na auditoria atual.

### Dispositivos retornados

Dispositivos que já haviam sido conhecidos pelo sistema, ficaram ausentes em uma auditoria e posteriormente retornaram.

### Dispositivos alterados

Dispositivos conhecidos cujo estado ou informações foram modificados.

As alterações atualmente analisadas podem envolver:

- IP Address.
- Hostname.
- Status.
- Fabricante.

O MAC Address é utilizado como identidade principal durante essa comparação.

---

## Integração com MikroTik

O InfraOps possui uma integração inicial com equipamentos MikroTik utilizando a API do RouterOS.

A comunicação é realizada através da biblioteca:

    librouteros

Atualmente a aplicação consegue:

- Estabelecer conexão com o RouterOS.
- Autenticar utilizando um usuário configurado no equipamento.
- Consultar a identidade do MikroTik.
- Consultar os leases DHCP.
- Transformar os registros retornados pela API em objetos `DHCPLease`.

Fluxo da integração:

    InfraOps
       |
       v
    MikroTikService
       |
       v
    librouteros
       |
       v
    TCP / 8728
       |
       v
    RouterOS API
       |
       v
    /ip/dhcp-server/lease
       |
       v
    DHCPLease

A integração está sendo desenvolvida inicialmente em laboratório para evitar alterações em equipamentos de produção.

---

## DHCP Detector

A integração com MikroTik é o primeiro passo para a criação de um detector de informações DHCP.

Atualmente o InfraOps consegue consultar registros como:

    IP       : 192.168.3.254
    MAC      : 00:E0:6F:FF:D3:69
    Hostname : DESKTOP-41TK77D
    Status   : bound

A próxima evolução será correlacionar as informações obtidas pelo DHCP com os dispositivos encontrados pelo scanner.

Exemplo:

    Scanner
       |
       +-- IP
       +-- MAC
       +-- Hostname
       +-- Fabricante
       |
       v
    InfraOps
       ^
       |
    DHCP do MikroTik
       |
       +-- IP
       +-- MAC
       +-- Hostname
       +-- Status

Essa correlação permitirá aumentar a qualidade das informações utilizadas durante as auditorias.

---

## Funcionalidades planejadas

### Descoberta de dispositivos

- ✅ Descoberta automática de hosts
- ✅ Seleção da interface de rede
- ✅ Cálculo automático da rede IPv4
- ✅ Identificação de fabricantes (MAC Vendor)
- ✅ Descoberta de hostname
- ⏳ Detecção de sistema operacional
- ⏳ Identificação de portas abertas
- ⏳ Identificação de serviços

### Inventário

- ✅ Inventário persistente em SQLite
- ✅ Histórico de equipamentos
- ⏳ Classificação dos dispositivos
- ⏳ Organização por cliente

### Comparação entre auditorias

- ✅ Novos dispositivos
- ✅ Equipamentos ausentes
- ✅ Dispositivos retornados
- ✅ Alteração de IP
- ✅ Alteração de hostname
- ✅ Alteração de status
- ✅ Alteração de fabricante
- ⏳ Alteração de serviços
- ⏳ Detecção de mudanças mais avançadas

### Integração MikroTik

- ✅ Comunicação com RouterOS API
- ✅ Autenticação
- ✅ Consulta da identidade do equipamento
- ✅ Consulta de leases DHCP
- ✅ Modelo `DHCPLease`
- ⏳ Correlação DHCP × Scanner
- ⏳ Detecção de inconsistências entre DHCP e scanner
- ⏳ Suporte a múltiplos MikroTik
- ⏳ Configuração externa dos equipamentos

### Relatórios

- ⏳ Excel
- ⏳ PDF
- ⏳ CSV
- ⏳ Relatórios técnicos de auditoria
- ⏳ Histórico visual de alterações

### Auditoria de Segurança

- ⏳ Portas administrativas abertas
- ⏳ Protocolos legados
- ⏳ Verificações básicas de exposição
- ⏳ Identificação de serviços potencialmente inseguros
- ⏳ Classificação básica de riscos

### Integrações futuras

- ⏳ SNMP
- ⏳ Wazuh
- ⏳ Zabbix
- ⏳ Telegram
- ⏳ E-mail

---

## Estrutura do projeto

    InfraOps-Auditor
    |
    +-- docs/
    +-- exports/
    +-- logs/
    +-- src/
    |   +-- app/
    |   +-- config/
    |   +-- database/
    |   +-- inventory/
    |   +-- models/
    |   |   +-- device.py
    |   |   +-- dhcp_lease.py
    |   |   +-- ...
    |   +-- reports/
    |   +-- scanner/
    |   +-- services/
    |   |   +-- comparison_service.py
    |   |   +-- interface_service.py
    |   |   +-- mikrotik_service.py
    |   |   +-- network_service.py
    |   |   +-- scanner_service.py
    |   +-- utils/
    |   +-- main.py
    |
    +-- tests/
    +-- test_mikrotik.py
    +-- README.md
    +-- requirements.txt

---

## Tecnologias

### Utilizadas atualmente

- Python 3.13+
- Nmap
- python-nmap
- psutil
- SQLite
- Git
- RouterOS API
- librouteros

### Previstas para as próximas versões

- Netmiko
- Pandas
- OpenPyXL
- Rich
- Flask

As tecnologias serão incorporadas conforme cada necessidade do projeto, evitando adicionar dependências antes que exista uma funcionalidade que realmente as utilize.

---

## Roadmap

### Versão 0.1 — Descoberta

- [x] Estrutura inicial do projeto
- [x] Menu principal
- [x] Descoberta das interfaces de rede
- [x] Seleção da interface
- [x] Cálculo da rede IPv4
- [x] Descoberta inicial de dispositivos
- [x] Identificação de hostname
- [x] Identificação de fabricante

### Versão 0.2 — Persistência

- [x] Banco SQLite
- [x] Inventário persistente
- [x] Histórico de auditorias
- [x] Isolamento do histórico por rede

### Versão 0.3 — Comparação

- [x] Comparação entre auditorias
- [x] Detecção de novos dispositivos
- [x] Detecção de dispositivos ausentes
- [x] Detecção de dispositivos retornados
- [x] Detecção de alterações
- [x] Detecção de alteração de IP
- [x] Detecção de alteração de hostname
- [x] Detecção de alteração de status
- [x] Detecção de alteração de fabricante

### Versão 0.4 — Integração de infraestrutura

- [x] Integração inicial com MikroTik
- [x] Comunicação com RouterOS API
- [x] Consulta de identidade
- [x] Consulta de leases DHCP
- [x] Modelo `DHCPLease`
- [ ] Correlação DHCP × Scanner
- [ ] Detecção de inconsistências DHCP
- [ ] Suporte a múltiplos equipamentos
- [ ] Configuração externa dos equipamentos

### Versão 0.5 — Scanner avançado

- [ ] Descoberta de portas
- [ ] Identificação de serviços
- [ ] Identificação de sistema operacional
- [ ] Detecção de serviços inesperados
- [ ] Scanner automático

### Versão 0.6 — Relatórios

- [ ] Relatórios de auditoria
- [ ] Exportação CSV
- [ ] Exportação Excel
- [ ] Exportação PDF
- [ ] Histórico visual de alterações

### Versão 0.7 — Integrações

- [ ] SNMP
- [ ] Zabbix
- [ ] Wazuh
- [ ] Telegram
- [ ] E-mail

### Versão 0.8 — Auditoria de Segurança

- [ ] Verificação de portas administrativas
- [ ] Identificação de protocolos legados
- [ ] Verificação de serviços expostos
- [ ] Regras básicas de segurança
- [ ] Classificação de riscos

### Versão 1.0 — Plataforma de auditoria

- [ ] Inventário completo
- [ ] Auditorias automatizadas
- [ ] Histórico completo
- [ ] Relatórios
- [ ] Integrações
- [ ] Alertas
- [ ] Interface consolidada
- [ ] Base estável para utilização em ambientes reais

---

## Filosofia do projeto

O InfraOps Auditor está sendo desenvolvido de forma incremental.

Cada funcionalidade é implementada, validada e integrada antes da próxima etapa ser iniciada.

O processo utilizado é:

    Planejamento
         ↓
    Implementação
         ↓
       Teste
         ↓
     Validação
         ↓
       Estudo
         ↓
     Integração

O objetivo não é apenas criar uma ferramenta funcional.

O desenvolvimento também serve como laboratório prático para aprofundar conhecimentos em:

- Python.
- Engenharia de software.
- Arquitetura de aplicações.
- Lógica de programação.
- Redes de computadores.
- Protocolos de rede.
- Administração de infraestrutura.
- Segurança da informação.
- Automação.
- Monitoramento.
- Integração entre sistemas.

Cada nova funcionalidade deve aumentar não apenas a capacidade da ferramenta, mas também a compreensão técnica de como a infraestrutura funciona.

---

## Ambiente de desenvolvimento

O projeto é desenvolvido e validado em ambientes reais e de laboratório.

O laboratório permite testar integrações com equipamentos de infraestrutura sem realizar alterações inicialmente em equipamentos de produção.

Essa abordagem permite validar funcionalidades como:

- Descoberta de rede.
- DHCP.
- Integração com MikroTik.
- APIs de infraestrutura.
- Auditoria.
- Correlação de informações.

antes de sua utilização em ambientes produtivos.

---

## Segurança

O InfraOps está sendo desenvolvido com preocupação crescente em relação à segurança.

As integrações com equipamentos de infraestrutura serão projetadas considerando:

- Princípio do menor privilégio.
- Separação de credenciais.
- Evitar credenciais diretamente no código.
- Controle de acesso.
- Validação das entradas.
- Registro de operações relevantes.
- Separação entre leitura e operações de alteração.

As integrações com equipamentos de produção devem ser inicialmente realizadas em modo somente leitura sempre que possível.

---

## Licença

Este projeto está licenciado sob a licença MIT.
