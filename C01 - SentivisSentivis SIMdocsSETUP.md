# SETUP - Sentivis IAOps

## Proposito

Preparar o ambiente local para operar o projeto Sentivis IAOps. Define o que existe validado, o que permanece pendente e os limites operacionais da fase atual.

## 1. Contexto do repositorio

| Item | Valor |
|---|---|
| Projeto | Sentivis IAOps |
| Fase atual | S3 Encerrada (2026-03-22 - 2026-04-11) |
| Sprint activa | Nenhuma (S3 arquivada em `Sprint/Dev_Tracking_S3.md`) |
| Escopo aprovado | Mock telemetry validation + baseline hardware real via Cirrus Lab |
| Repository type | Repo materializado |

## 2. Requisitos minimos

| Ferramenta | Versao | Proposito |
|---|---|---|
| Git | 2.x+ | Controle de versao |
| VS Code | 1.75+ | Editor e terminal |
| curl | latest | Teste de APIs HTTP |
| Python | 3.10+ | Scripts utilitarios |

## 3. Estrutura minima esperada

```
Sentivis SIM/
├── README.md
├── Dev_Tracking.md
├── docs/
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   └── OPERATIONS.md
├── rules/
│   └── WORKSPACE_RULES.md
├── tests/
│   └── bugs_log.md
└── Sprint/
    ├── Dev_Tracking_S0.md
    ├── Dev_Tracking_S1.md
    ├── Dev_Tracking_S2.md
    └── Dev_Tracking_S3.md
```

## 4. Fontes de evidencia actuais

### 4.1 Evidencias ja disponiveis

- `tests/bugs_log.md` — log de testes e bugs, incluindo TEST-S3-T1/T2/T3 (Cirrus Lab)
- `Sprint/Dev_Tracking_S3.md` — backlog executado e encerrado
- `Dev_Tracking.md` — indice de sprints com S3 como Encerrada
- `docs/HARDWARE_BASELINE.md` — inventario de hardware Cirrus Lab

### 4.2 Classificacao das evidencias

- Confirmado: host ThingsBoard (`204.168.202.5:8080`), JWT Cirrus Lab valido, n8n operacional
- Inferido: proxima fase de integracao hardware local
- Pendente de validacao: fluxo Cirrus -> ThingsBoard local

### 4.3 Preservacao

Arquivos adicionais criados na S3 devem ser mantidos:

- `docs/TELEMETRY_CONTRACT.md`
- `docs/DEVICE_PROFILE_MODELING.md`
- `docs/DASHBOARD_BASELINE.md`
- `docs/RULE_ENGINE_EVALUATION.md`
- `docs/TRILHA_EVIDENCIA.md`
- `docs/HARDWARE_BASELINE.md`

## 5. Ambientes validados

### 5.1 ThingsBoard CE (local)

| Item | Valor |
|---|---|
| Host | `http://204.168.202.5:8080` |
| Tipo | Tenant Administrator |
| Porta HTTP | 8080 |
| Porta MQTT | 1883 |
| Porta SSH | 22 |
| Porta DB | 5432 (fechada externamente) |

**Endpoints validados:**

| Endpoint | Metodo | Estado |
|---|---|---|
| `/api/auth/login` | POST | 200 (JWT valido) |
| `/api/device` | GET | 200 |
| `/api/v1/{TOKEN}/telemetry` | POST | 200 |
| `/api/user` (update) | POST | 200 |
| `/api/user/{id}` | PUT | 405 (metodo nao suportado) |

**Device existente:**

| Item | Valor |
|---|---|
| Nome | `Sentivis | 0001` |
| Profile | default |
| Estado | Inactive |

### 5.2 n8n (Railway)

| Item | Valor |
|---|---|
| URL base | `https://stvsiaopsdevice-api-production.up.railway.app` |
| Workflow | `STVSIAOps_Device API` (ID: `Dq5322GMwAllfgyN`) |
| Webhook URL | `https://stvsiaopsdevice-api-production.up.railway.app/webhook/device-telemetry` |
| Autenticacao | `X-N8N-API-KEY` |
| Estado | Operacional |

### 5.3 Cirrus Lab (ThingsBoard Cloud)

| Item | Valor |
|---|---|
| Portal | `https://portal.cirrus-lab.com/` |
| Utilizador | `contateste@cirruslab.com` |
| Authority | CUSTOMER_USER |
| JWT exp | 2026-04-10 21:35:05 |
| Tenant ID | `2a75a5c0-ba4f-11ee-a124-0d00bef77fcc` |
| Customer ID | `f23b9a70-1d8e-11f1-88f8-7daa5068de06` |

**Devices activos:**

| Device | ID | Telemetria |
|---|---|---|
| NIMBUS-AERO 1-09821699 | 27ad32e0 | temperature, humidity, lat/long |
| ATMOS-WIND 1-09821699 | 9c5178a0 | lat/long |
| ATMOS-LINK 1-09821699 | bdda85a0 | lat/long |
| NIMBUS-ECHO-R1 0860228052083660 | cbec4881 | lat/long |

**Localizacao:** SP, Brasil (-22.59467, -48.80054)

**Acesso:** `GET /api/plugins/telemetry/DEVICE/{id}/values/timeseries` via Bearer JWT

## 6. Credenciais

Ficheiro: `.scr/.env` (nao versionado)

```
TB_HOST=204.168.202.5
TB_PORT=8080
TB_URL=http://204.168.202.5:8080
TB_USERNAME=sentivis@sentivis.com.br
TB_TENANT_ROLE=TENANT_ADMIN
THINGSBOARD_CIRRUS_JWT_Token=Bearer <JWT valido>
THINGSBOARD_CIRRUS_URL=https://portal.cirrus-lab.com/
N8N_BASE_URL=https://stvsiaopsdevice-api-production.up.railway.app
```

**Regra:** Nunca versionar `.scr/.env`. Manter sempre no `.gitignore`.

## 7. Preparacao inicial

### 7.1 Clonar o repositorio

```bash
git clone <repo_url>
cd "Sentivis SIM"
```

### 7.2 Verificar estrutura

```bash
ls
ls docs
ls Sprint
ls tests
```

### 7.3 Ler antes de operar

1. `README.md`
2. `Dev_Tracking.md`
3. `Sprint/Dev_Tracking_S3.md`
4. `docs/SETUP.md` (este)
5. `docs/ARCHITECTURE.md`
6. `docs/DEVELOPMENT.md`
7. `docs/OPERATIONS.md`

## 8. O que ainda nao esta configurado

- Integracao Cirrus Lab -> ThingsBoard local
- Rule Engine com alarmes reais
- Dashboards com hardware Cirrus
- Device Profiles para tipos NIMBUS/ATMOS

## 9. Proximos passos

- Iniciar Sprint S4 com integracao Cirrus -> ThingsBoard local
- Consultar `docs/HARDWARE_BASELINE.md` para inventario de devices
- Consultar `docs/DEVICE_PROFILE_MODELING.md` para modelo de entities
