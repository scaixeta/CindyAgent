# Dev_Tracking - Sprint S5 (Sentivis IAOps)

## 1. Identificação da Sprint

- Sprint: S5
- Projeto: Sentivis IAOps
- Período: 2026-04-10 - 2026-04-11
- Contexto inicial:
  - S4 encerrada com Cirrus integrado e 12 registros reais de telemetria validados
  - Objetivo S5: relatório operacional de microclima sobre dados reais de S4
  - Restrição: sem acesso remoto ao ThingsBoard (JWT expirado)
  - Entrega via Telegram

---

## 2. Objetivos da Sprint

### Objetivo de Negócio da Sprint

`Gerar um relatório operacional de microclima com base nos 12 registros reais da janela S4, extraindo tendências de umidade e temperatura, aplicando marcadores operativos seguros (sem claims agronómicos não validados), e entregando o resultado via Telegram.`

- [OBJ-S5-01] Parser de collection_log.txt da S4 — Concluído (S5-01)
- [OBJ-S5-02] Motor de tendência (umidade e temperatura) — Concluído (S5-02)
- [OBJ-S5-03] Marcadores operativos e output Markdown — Concluído (S5-03)
- [OBJ-S5-04] Output JSON + entrega Telegram — Concluído (S5-04)
- [OBJ-S5-05] Camada Redis operacional mínima — Concluído (S5-05)
- [OBJ-S5-06] Validação de recuperação de estado e janela curta — Concluído (S5-06)
- [OBJ-S5-07] Registo de evidência DOC2.5 do teste Redis — Pendente (S5-07)

---

## 3. Backlog da Sprint

| Estado | SP | Estória |
|---|---:|---|
| Concluído | 3 | ST-S5-01 - Parser de collection_log.txt (12 registros reais) |
| Concluído | 5 | ST-S5-02 - Motor de tendência (umidade e temperatura) |
| Concluído | 3 | ST-S5-03 - Marcadores operativos e output Markdown |
| Concluído | 5 | ST-S5-04 - Output JSON + entrega Telegram |
| Concluído | 3 | ST-S5-05 - Camada Redis operacional mínima |
| Concluído | 3 | ST-S5-06 - Validação de recuperação de estado e janela curta |

**Total: 25 SP | Concluído: 22 SP | A Fazer: 3 SP (OBJ-S5-07)**

---

## 4. Decisões

[S5-D01] — 2026-04-10 — Arquitetura MVP
  - Core analítico em Python local (scripts/s5_microclimate.py)
  - Output: artifacts/s5-relatorio.md + artifacts/s5-relatorio.json
  - Entrega via Telegram (via Hermes gateway)
  - Redis fora do CP0 (sem necessidade demonstrada para dados finitos)
  - n8n fora do CP0 (não evidenciado no workspace)

[S5-D02] — 2026-04-10 — Regras operacionais seguras
  - Intervalo 18-24°C: "referência operativa" (não verdade agronómica validada)
  - Umidade > 85%: "proxy de molhamento foliar" (não "janela de chuva")
  - Tendência: "subida/estável/descendo" (não "previsão")
  - VPD: fora do MVP (Buck equation inexistente no canon)
  - "Risco de ferrugem": bloqueado como framing canónico; usar "proxy de risco fungico"

[S5-D03] — 2026-04-10 — Limites de telemetria
  - Dados reais: janela S4 de 12 pontos (2026-04-10 17:59-18:57 UTC)
  - Temperatura: constante 25.0°C (sem variação na janela)
  - Umidade: salto de 64.45% para 88.28% na iteração 3
  - Acesso TB remoto: bloqueado (JWT expirado)
  - Historico 24h: não disponível nesta fase

[S5-D04] — 2026-04-10 — Decisão Redis para Sprint 5
  - Redis instalado e funcional no ambiente local (localhost:6379)
  - Chave `microclimate:{device}:latest` — latest state snapshot com TTL 1h
  - Chave `microclimate:{device}:window` — rolling window de 20 registos com TTL 1h
  - Chave `microclimate:{device}:memory_state:last_run` — estado operacional com TTL 2h
  - Resultado: Redis melhora state persistence entre execuções; recall de estado confirmado
  - Degradaçãograceful: script continua se Redis estiver indisponível

---

## 5. Resumo Técnico

### Dados de Entrada (S4)

| Campo | Valor |
|---|---|
| Fonte | artifacts/s4-cirrus/2026-04-10/collection_log.txt |
| Registros | 12 pontos reais |
| Janela | 2026-04-10 17:59:15 - 18:57:15 UTC |
| Temperatura | 25.0°C (constante) |
| Umidade | 64.45% → 88.28% (shift na iteração 3) |

### Artefatos de Saída

| Artefato | Descrição |
|---|---|
| scripts/s5_microclimate.py | Parser + motor analítico |
| artifacts/s5-relatorio.md | Relatório operacional em Markdown |
| artifacts/s5-relatorio.json | Relatório operacional em JSON |

---

## 6. Referências

- `Sprint/Dev_Tracking_S4.md` — sprint anterior encerrada
- `artifacts/s4-cirrus/2026-04-10/collection_log.txt` — dados reais de entrada
- `docs/TELEMETRY_CONTRACT.md` — contrato de telemetria
- `tests/bugs_log.md` — log de testes e bugs

---

## 7. Timestamp UTC

Event | Start | Finish | Estado
---|---|---|---
ST-S5-01 | 2026-04-10T22:30:00-ST | 2026-04-10T22:35:00-FN | Concluído
ST-S5-02 | 2026-04-10T22:35:00-ST | 2026-04-10T22:40:00-FN | Concluído
ST-S5-03 | 2026-04-10T22:40:00-ST | 2026-04-10T22:41:00-FN | Concluído
ST-S5-04 | 2026-04-10T22:41:00-ST | 2026-04-10T22:42:00-FN | Concluído
ST-S5-05 | 2026-04-10T22:50:00-ST | 2026-04-10T22:53:00-FN | Concluído
ST-S5-06 | 2026-04-10T22:53:00-ST | 2026-04-10T22:53:50-FN | Concluído
TEST-S5-01 | 2026-04-10T22:53:50-ST | 2026-04-10T22:53:55-FN | A Fazer
TEST-S5-02 | 2026-04-10T22:53:55-ST | 2026-04-10T22:54:00-FN | A Fazer
TEST-S5-03 | 2026-04-10T22:54:00-ST | 2026-04-10T22:54:05-FN | A Fazer
TEST-S5-04 | 2026-04-10T22:54:05-ST | 2026-04-10T22:54:10-FN | A Fazer

---

## 8. Regra de Commits

- Commit e push apenas sob ordem expressa do PO
- Sprint encerrada: mover para `Sprint/Dev_Tracking_S5.md`
- Rastreabilidade: bugs_log.md com TEST-S5-XX
