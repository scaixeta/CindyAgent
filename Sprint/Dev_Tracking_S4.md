# Dev_Tracking - Sprint S4 (Sentivis IAOps)

## 1. Identificacao da Sprint

- Sprint: S4
- Projeto: Sentivis IAOps
- Periodo: 2026-04-10 - 2026-04-11
- Contexto inicial:
  - S3 encerrada com baseline operacional completo (contrato telemetria, modelagem, dashboard, Cirrus conectado)
  - Cirrus Lab JWT valido, 4 devices acessiveis
  - Objetivo S4: integrar Cirrus como estacao monitorada externa no ecossistema Sentivis

---

## 2. Objetivos da Sprint

### Objetivo de Negocio da Sprint

`Integrar Cirrus-Lab como estacao monitorada externa, usando JWT existente, normalizando payload para o contrato interno, persistindo via fluxo aprovado, e validando janela de 1 hora com 12 coletas de 5 em 5 minutos.`

- [OBJ-S4-01] Registrar Cirrus-Lab como estacao logica no TB local — Done
- [OBJ-S4-02] Construir adapter de leitura Cirrus via JWT existente — Done
- [OBJ-S4-03] Normalizar payload Cirrus para contrato interno — Done
- [OBJ-S4-04] Persistir dados normalizados via fluxo aprovado (POST /api/v1/{token}/telemetry) — Done
- [OBJ-S4-05] Executar janela de validacao: 1 hora, 12 coletas, 5 min interval — Done
- [OBJ-S4-06] Gerar evidencias auditaveis — Done

---

## 3. Backlog da Sprint

| Status | SP | Estoria |
|---|---:|---|
| Done | 3 | ST-S4-01 - Criar estrutura de sprint e artefatos S4 |
| Done | 5 | ST-S4-02 - Registrar Cirrus-Lab como device no TB local |
| Done | 8 | ST-S4-03 - Construir cirrus_collector.py (leitura + normalizacao + persistencia) |
| Done | 3 | ST-S4-04 - Executar janela de 1 hora (12 coletas, 5 min) |
| Done | 5 | ST-S4-05 - Gerar evidencias em artifacts/s4-cirrus/ |
| Done | 5 | ST-S4-06 - Documentar design e gap analysis |

**Total: 29 SP | Done: 29 SP**

---

## 4. Decisoes

[D-S4-01] — 2026-04-10 — Cirrus como estacao externa e device no TB local
  - Cirrus nao sera mapeado como asset; sera device no TB com profile dedicado
  - Credential: usa o JWT existente em .scr/.env (THINGSBOARD_CIRRUS_JWT_Token)
  - Persistence: via POST /api/v1/{device_token}/telemetry para o device local

[D-S4-02] — 2026-04-10 — Normalizacao de payload
  - Cirrus key "temperature" -> "air_temperature" (contrato interno)
  - Cirrus key "humidity" -> "air_humidity" (contrato interno)
  - latitude/longitude mantidos como lat/long
  - source_station = "CIRRUS-NIMBUS-AERO"

[D-S4-03] — 2026-04-10 — Historico 10 dias
  - Backfill via batch POST /api/v1/{token}/telemetry com array JSON
  - 712 points de humidity (2026-03-31 a 2026-04-10) persistidos no TB local
  - Limite: humidity apenas (temperature so 1 point disponivel no Cirrus)

---

## 5. Resumo Tecnico

### Device Cirrus Registrado no TB Local

| Campo | Valor |
|---|---|
| Nome | Sentivis \| CIRRUS-NIMBUS-AERO |
| Device ID | cdb2a970-3506-11f1-86b7-01315d8eb3e7 |
| Device Token | EMlf0gDIPJp9nn4CFvkF |
| Tipo | WeatherStation |
| Profile ID | cdaba490-3506-11f1-86b7-01315d8eb3e7 |

### Cirrus Collector (scripts/cirrus_collector.py)

Modulo standalone para coleta, normalizacao e persistencia de telemetria Cirrus.
Argumentos: --device, --iterations, --interval, --dry-run, --device-token

### Resultado Janela de Validacao (TEST-S4-01)

Janela: 2026-04-10 17:59:15 - 18:57:15 UTC (58 min)
Resultado: 12/12 SUCCESS, 0 failed

| Iteracao | Timestamp | Temp (C) | Humidity (%) | Persisted |
|---:|---|---:|---:|---:|
|  1 | 17:59:15 | 25.0 | 64.45 | True |
|  2 | 18:04:30 | 25.0 | 64.45 | True |
|  3 | 18:09:47 | 25.0 | 88.28 | True |
|  4 | 18:15:02 | 25.0 | 88.28 | True |
|  5 | 18:20:18 | 25.0 | 88.28 | True |
|  6 | 18:25:36 | 25.0 | 88.67 | True |
|  7 | 18:30:52 | 25.0 | 88.67 | True |
|  8 | 18:36:08 | 25.0 | 88.67 | True |
|  9 | 18:41:25 | 25.0 | 88.67 | True |
| 10 | 18:46:41 | 25.0 | 88.67 | True |
| 11 | 18:51:57 | 25.0 | 87.11 | True |
| 12 | 18:57:15 | 25.0 | 87.11 | True |

### Gap Analysis

1. Humidity shift: variacao de 64.45 para 88.28 as 18:09 (salto ~24%) — dados reais, nao erro
2. Temperature sensor: apenas 1 point historico no Cirrus para NIMBUS-AERO — possivel problema de hardware
3. JWT Cirrus: funcional as 2026-04-10 17:58 (contradiz estimativas de expiracao anteriores)
4. Lacuna historica: 2025-12-17 a 2026-02-20 (~65 dias sem dados humidity)

---

## 6. Referencias

- `docs/TELEMETRY_CONTRACT.md` — contrato interno de telemetria
- `docs/HARDWARE_BASELINE.md` — baseline Cirrus (devices, JWT, telemetria)
- `docs/CIRRUS_INTEGRATION.md` — design da integracao Cirrus
- `tests/bugs_log.md` — log de testes e bugs
- `artifacts/s4-cirrus/2026-04-10/collection_log.txt` — log de coleta

---

## 7. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S4-01 | 2026-04-10T14:38:00-ST | 2026-04-10T14:45:00-FN | Done
ST-S4-02 | 2026-04-10T14:45:00-ST | 2026-04-10T15:10:00-FN | Done
ST-S4-03 | 2026-04-10T15:10:00-ST | 2026-04-10T17:30:00-FN | Done
ST-S4-04 | 2026-04-10T17:59:00-ST | 2026-04-10T18:57:00-FN | Done
ST-S4-05 | 2026-04-10T18:57:00-ST | 2026-04-10T19:00:00-FN | Done
ST-S4-06 | 2026-04-10T19:00:00-ST | 2026-04-10T19:10:00-FN | Done
TEST-S4-01 | 2026-04-10T17:59:00-ST | 2026-04-10T18:57:00-FN | Done

---

## 8. Regra de Commits

- Commit e push apenas sob ordem expressa do PO
- sprints encerradas: mover para `Sprint/`
- rastreabilidade: bugs_log.md com TEST-S4-XX
