# ARCHITECTURE - Sentivis IAOps

## Proposito

Descrever a arquitectura conceitual do projeto, camadas, componentes, fluxos e decisoes arquitecturais relevantes.

## 1. Visao geral da arquitectura

| Camada | Descricao |
|---|---|
| Coleta | Sensores (Cirrus Lab) + mock local |
| Transmissao | HTTP via n8n |
| Plataforma | ThingsBoard CE (local) + ThingsBoard Cloud (Cirrus Lab) |
| Orquestracao | n8n (Railway) |
| Visualizacao | Dashboards ThingsBoard |

## 2. Camadas principais

### 2.1 Nucleo funcional

- ThingsBoard CE (`204.168.202.5:8080`) — storage de telemetria
- n8n Railway — orquestrador de fluxos via webhook
- Cirrus Lab — hardware real (4 devices activos)

### 2.2 Memoria e evidencia

- `Dev_Tracking.md` — indice de sprints
- `Sprint/Dev_Tracking_S3.md` — sprint encerrada
- `tests/bugs_log.md` — log de testes e bugs
- `docs/` — documentacao operacional e tecnica

### 2.3 Operacao e validacao

- Gate de telemetria (TEST-GATE-S3-F0)
- Testes Cirrus Lab (TEST-S3-T1, T2, T3)
- Validadores REST (curl)

## 3. Componentes principais

| Componente | Descricao | Estado |
|---|---|---|
| ThingsBoard CE | Storage telemetria + dashboards | Operacional |
| n8n Railway | Orquestrador de fluxos | Operacional |
| Cirrus Lab | Hardware real IoT | Operacional |
| Mock Telemetry | Simulacao via script/n8n | Validado |

## 4. Fluxos principais

### 4.1 Fluxo mock (validado)

```
[Mock Script] --> [HTTP POST /webhook/device-telemetry]
                        |
                        v
                   [n8n: STVSIAOps_Device API]
                        |
                        v
                   [HTTP POST /api/v1/{TOKEN}/telemetry]
                        |
                        v
                   [ThingsBoard CE: 204.168.202.5:8080]
```

**Estado:** Validado (TEST-GATE-S3-F0)

### 4.2 Fluxo Cirrus Lab (hardware real)

```
[Devices Cirrus Lab] --> [ThingsBoard Cloud: portal.cirrus-lab.com]
                                |
                                v
                         [GET /api/plugins/telemetry/DEVICE/{id}/values/timeseries]
                                |
                                v
                         [JWT Bearer: THINGSBOARD_CIRRUS_JWT_Token]
```

**Devices:**

- NIMBUS-AERO — temperature, humidity, lat/long
- ATMOS-WIND — wind, lat/long
- ATMOS-LINK — link, lat/long
- NIMBUS-ECHO-R1 — echo, lat/long

**Estado:** Operacional (TEST-S3-T2)

## 5. Limites arquitecturais

### Faz parte

- ThingsBoard CE (storage + API)
- n8n (orquestracao)
- Cirrus Lab (hardware real)
- Mock telemetry (validacao)

### Nao faz parte

- Gateway LoRa standalone
- Hardware ESP32 de campo
- ThingsBoard PE/EE
- Base de dados adicional

## 6. Decisoes arquitecturais

- D-S3-01: ThingsBoard CE como storage primario
- D-S3-02: n8n como orquestrador externo
- D-S3-03: Cirrus Lab como fonte de hardware real
- D-S3-10: Gateway ThingsBoard `204.168.202.5` validado

## 7. Relacao com outros artefatos

- `docs/SETUP.md` — configuracao de ambientes
- `docs/DEVELOPMENT.md` — fluxo de desenvolvimento
- `docs/OPERATIONS.md` — operacao e validacao
- `docs/HARDWARE_BASELINE.md` — inventario Cirrus Lab
- `docs/DEVICE_PROFILE_MODELING.md` — modelo de entities
