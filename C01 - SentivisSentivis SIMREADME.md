# Sentivis IAOps

## Visao Geral do Projeto

| Item | Valor |
|---|---|
| Nome do Projeto | Sentivis IAOps |
| Plataforma IoT | ThingsBoard CE + ThingsBoard Cloud (Cirrus Lab) |
| Fase Atual | Sprint S3 Encerrada |
| Versao | 1.0.0-S3 |

## Escopo do Projeto

### O que este projeto valida

- Backbone de dados em ThingsBoard CE
- Fluxo de telemetria via mock e hardware real (Cirrus Lab)
- Integracao e persistencia de dados time-series
- Dashboards para visualizacao operacional
- API REST para automacao e configuracao

### O que este projeto NAO valida

- Gateway LoRa standalone
- Hardware ESP32 de campo (Cirrus Lab substitui)
- Validacao agronomica
- Implantacao em producao

## Fase 1: Mock Telemetry + Cirrus Lab Hardware Real

### Contexto

Sprint S3 estabeleceu o baseline operacional com mock telemetry validado e hardware real Cirrus Lab conectado.

**Baseline operacional:**

- ThingsBoard CE (`204.168.202.5:8080`) — storage de telemetria
- n8n Railway — orquestrador de fluxos via webhook
- Cirrus Lab — hardware real IoT (4 devices activos)
- Fluxo mock `n8n -> ThingsBoard Device API` — validado

**Hardware real Cirrus Lab:**

- NIMBUS-AERO 1-09821699 — temperature, humidity, lat/long
- ATMOS-WIND 1-09821699 — lat/long
- ATMOS-LINK 1-09821699 — lat/long
- NIMBUS-ECHO-R1 — lat/long
- Localizacao: SP, Brasil (-22.59467, -48.80054)

## Estrutura do Projeto

```
Sentivis SIM/
├── README.md                    # Este arquivo
├── Dev_Tracking.md              # Indice de sprints
├── docs/
│   ├── SETUP.md                # Pre-requisitos e configuracao
│   ├── ARCHITECTURE.md         # Arquitetura tecnica
│   ├── DEVELOPMENT.md          # Fluxo de desenvolvimento
│   └── OPERATIONS.md           # Operacao e validacao
├── KB/                         # Conhecimento e referencias
│   ├── SwaggerTB.md
│   ├── ThingsBoard_CE_Modelagem_Sentivis_MLE.md
│   └── ...
├── rules/
│   └── WORKSPACE_RULES.md      # Regras locais
├── tests/
│   └── bugs_log.md             # Log de bugs e testes
└── Sprint/
    ├── Dev_Tracking_S0.md
    ├── Dev_Tracking_S1.md
    ├── Dev_Tracking_S2.md
    └── Dev_Tracking_S3.md
```

## Controle de Sprints

| Sprint | Objetivo | Estado | Link |
|---|---|---|---|
| S0 | Validar data backbone ThingsBoard CE | Encerrada | `Sprint/Dev_Tracking_S0.md` |
| S1 | Estruturar integracao Jira Cloud | Encerrada | `Sprint/Dev_Tracking_S1.md` |
| S2 | Consolidar visibilidade executiva | Encerrada (local) | `Sprint/Dev_Tracking_S2.md` |
| S3 | Baseline mock + hardware real Cirrus Lab | Encerrada (local) | `Sprint/Dev_Tracking_S3.md` |

## Ambientes Validados

### ThingsBoard CE

- URL: `http://204.168.202.5:8080`
- Swagger: `http://204.168.202.5:8080/swagger-ui/index.html`
- Device: `Sentivis | 0001`
- Device API: `POST /api/v1/{TOKEN}/telemetry`

### n8n (Railway)

- URL: `https://stvsiaopsdevice-api-production.up.railway.app`
- Workflow: `STVSIAOps_Device API` (ID: `Dq5322GMwAllfgyN`)
- Webhook: `POST /webhook/device-telemetry`

### Cirrus Lab (ThingsBoard Cloud)

- Portal: `https://portal.cirrus-lab.com/`
- 4 devices activos — telemetria real via API REST
- Acesso: `GET /api/plugins/telemetry/DEVICE/{id}/values/timeseries`

## Documentacao de Referencia

1. [SETUP.md](docs/SETUP.md) — Pre-requisitos e configuracao
2. [ARCHITECTURE.md](docs/ARCHITECTURE.md) — Arquitetura tecnica
3. [DEVELOPMENT.md](docs/DEVELOPMENT.md) — Fluxo de desenvolvimento
4. [OPERATIONS.md](docs/OPERATIONS.md) — Operacao e validacao
5. [KB/SwaggerTB.md](KB/SwaggerTB.md) — Endpoints ThingsBoard
6. [KB/ThingsBoard_CE_Modelagem_Sentivis_MLE.md](KB/ThingsBoard_CE_Modelagem_Sentivis_MLE.md) — Modelagem de dominio

## Notas Importantes

- Toda a documentacao esta em **Portugues (pt-BR)**, exceto comandos e APIs
- Nome oficial: **Sentivis IAOps**
- `Sentivis SIM` e o nome do diretorio local de trabalho
- Proxima fase: integracao Cirrus Lab -> ThingsBoard CE local

---

Este repositorio e orquestrado pela Cindy sob a doutrina DOC2.5.

## Cindy — Orquestradora (Context Router)

A Cindy e o agente principal do projeto. Em cada run, ela identifica o orchestrator ativo (Cline/Codex/Antigravity), a superficie de execucao (VSCode/CLI) e o workspace root; em seguida, descobre e seleciona as skills/workflows disponiveis no contexto atual, respeitando os gates DOC2.5 (plano aprovado antes de execucao; commit/push apenas sob ordem explicita do PO).

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy — Orquestradora" width="220" />
</p>
