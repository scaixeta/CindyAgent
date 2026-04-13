# Dev_Tracking.md — Índice de Sprints

## Sprint Ativa

| ID | Status | Inicio | Escopo |
|---|---|---|---|
| S2 | Planejada | 2026-04-13 | Operacionalização da equipe de 5 agentes no Sentivis SIM — ThingsBoard CE, n8n Railway, dashboards, alarms, validações e integrações |

## Sprints Encerradas

| ID | Status | Periodo | Entrega |
|---|---|---|---|
| S1 | Encerrada | 2026-04-09 a 2026-04-13 | Cindy Agent v1.0 — Hermes + Telegram + DOC2.5 + OpenCode + equipe de 5 agentes com ACP via Redis |

---

## Registros recentes

- `2026-04-09` — WSL Ubuntu reinstalado e Hermes operacionalizado
- `2026-04-09` — Telegram pareado e gateway funcional no runtime Hermes
- `2026-04-09` — KB canônica `KB/hermes/` sincronizada com o runtime vivo em `/root/.hermes`
- `2026-04-09` — branch principal consolidada em `main` com proteção de `.scr/.env`
- `2026-04-09` — `Replicar.md` reconhecido como mapa dos projetos principais da Cindy
- `2026-04-10` — OpenCode CLI integrado com MiniMax M2.7 via wrapper `run_opencode.bat`; TEST-S1-05 (API FastAPI) passou
- `2026-04-10` — Análise aprofundada dos 8 repositórios; 5 repositórios pessoais removidos de `Replicar.md`; `KB/REPOSITORIES_STATUS.md` criado
- `2026-04-12` — ST-S1-18: Codex CLI integrado como engine secundária de raciocínio
- `2026-04-13` — ST-S1-19: Arquitetura dual-modelo (MiniMax + GLM-5.1) implementada com RACI e gate de iteração
- `2026-04-13` — ST-S1-20: Comunicação ACP entre agentes via Redis (Pub/Sub + Streams) implementada e testada
- `2026-04-13` — ST-S1-21: Equipe de 5 agentes (Cindy, Sentivis, MiniMax, Scribe, GLM-5.1) documentada e operacional
- `2026-04-13` — D-S1-13: Equipe de 5 agentes com ACP via Redis — modelo aprovado
- `2026-04-13` — D-S1-14: Agentes se comunicam via ACP/JSON — nunca em linguagem humana entre si
- `2026-04-13` — D-S1-15: PO approves planos; agentes escalam decisões grandes via Cindy
- `2026-04-13` — ST-S2-03: Playwright instalado e funcional (Chromium, Firefox, WebKit) — venv Hermes como ambiente Python preferencial


## Estrutura de Tracking

- `Dev_Tracking.md` — indice das sprints
- `Dev_Tracking_S1.md` — sprint ativa
- `Sprint/` — historico de sprints encerradas

## Referencia

Consulte `Dev_Tracking_S1.md` para backlog, decisões e pendências da sprint ativa.
