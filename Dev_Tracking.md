# Dev_Tracking.md — Índice de Sprints

## Sprint Ativa

| ID | Status | Inicio | Escopo |
|---|---|---|---|
| S3 | Ativa | 2026-04-14 | Time AIOps multiagente com Microsoft Agent Framework — agent cards, ACP mesh governado, OpenCode executor, Playwright + SonarCloud, PO gates — Modelo de pensamento: Codex |

## Sprints Encerradas

| ID | Status | Periodo | Entrega |
|---|---|---|---|
| S1 | Encerrada | 2026-04-09 a 2026-04-13 | Cindy Agent v1.0 — Hermes + Telegram + DOC2.5 + OpenCode + equipe de 5 agentes com ACP via Redis |
| S2 | Encerrada (substituída) | 2026-04-13 a 2026-04-14 | Ferramentas internas da Cindy — substituída por S3 com novo objetivo time AIOps |

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
- `2026-04-14` — S3 aberta: time AIOps multiagente com Microsoft Agent Framework — S2 substituída
- `2026-04-14` — D-S3-11: Codex é o modelo de pensamento e validação do time
- `2026-04-14` — Runtime Linux do Hermes corrigido após reboot: `MiniMax-M2.7` mantido como primário e `gpt-5.3-codex` como fallback
- `2026-04-14` — `hermes-gateway.service` reiniciado com sucesso; healthcheck `/health` e `hermes chat -Q` validados no Linux
- `2026-04-14` — Remote oficial reconciliado como `https://github.com/scaixeta/CindyAgent`
- `2026-04-14` — Passagem de bastão registrada em `KB/aiops/HANDOFF_S3_2026-04-14.md`
- `2026-04-14` — Hermes atualizado de `v0.8.0` para `v0.9.0`; alteração local em `cron/scheduler.py` preservada com stash e patch de backup antes do update


## Estrutura de Tracking

- `Dev_Tracking.md` — indice das sprints
- `Dev_Tracking_S3.md` — sprint ativa
- `Sprint/` — historico de sprints encerradas

## Referencia

Consulte `Dev_Tracking_S3.md` para backlog, decisões e pendências da sprint ativa.
