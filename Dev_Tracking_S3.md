# Dev_Tracking_S3.md — Sprint 3 (Ativa)

## Identificação

| Campo | Valor |
|---|---|
| Sprint | S3 |
| Status | **Ativa** |
| Início | 2026-04-14 |
| Versão | 1.0 |
| PO | A definir |
| Substitui | S2 — substituída por este novo objetivo |

---

## Contexto

### Documentos de referência

Este planejamento tem como fonte de verdade os seguintes documentos:

- `KB/aiops/AIOPS_TEAM_BASELINE.md` — baseline arquitetural e estado atual do time
- `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md` — plano de ação em 6 fases para materialização do time AIOps

### Situação atual

A sprint S2 tinha como foco consolidar ferramentas internas (TTS, MCP, Playwright, SonarCloud, Whisper STT). Porém, o objetivo do projeto evoluiu. O novo objetivo é materializar um time AIOps multiagente completo e autônomo, usando Microsoft Agent Framework como plataforma de gestão e orquestração.

Conforme registrado no `KB/aiops/AIOPS_TEAM_BASELINE.md`:

- O runtime atual opera como `PO -> Cindy -> Hermes + ferramentas + delegação + Redis`
- Cindy é o agente operacional real, mas a equipe de 5 agentes ainda está parcialmente materializada
- O objetivo é transformar esse estado em um time AIOps/de desenvolvimento real com mesh governado

### Objetivo da Sprint S3

**Materializar o time AIOps completo usando Microsoft Agent Framework como plataforma de gestão approved**, com:

- Agentes por papel: Cindy (coordenação), Builder (execução), Reviewer (validação), Documenter (docs), PlatformOps (infra)
- ACP/Redis como mesh/bus interno durante a transição
- OpenCode como executor técnico dos especialistas
- Playwright + SonarCloud como ferramentas de validação automatizada
- PO como human-in-the-loop por gates

### Decisões já aprovadas (de sessões anteriores)

| ID | Descrição |
|---|---|
| D1 | Nomes baseados em papel (Cindy, Builder, Reviewer, Documenter, PlatformOps) — não atrelados a modelo |
| D2 | Microsoft Agent Framework = plataforma de gestão approved — não mais referência futura |
| D3 | ACP/Redis permanece como mesh interno durante a transição |
| D4 | OpenCode permanece como executor técnico dos especialistas |
| D5 | Adoção incremental — produtos Microsoft pagos não são obrigatórios na fase 1 |

---

## Escopo

### Fase 1 — Agent Cards dos 5 papéis

Definir o contrato operacional de cada agente:

- `agent_card` com missão, domínio, ferramentas, skills, workflows, limites e critérios de escala
- Regras de autonomia e política de escalação ao PO
- Estratégia de modelo/provedor por papel

### Fase 2 — Microsoft Agent Framework

Avaliação e setup inicial:

- Definir trilha de adoção do Microsoft Agent Framework como plataforma de gestão
- Avaliar Agent Governance Toolkit como referência de guardrails
- Configurar ambiente de desenvolvimento para avaliação

### Fase 3 — ACP/Redis Mesh Governado

Evoluir o ACP para protocolo operacional completo:

- Capability registry por agente
- Ciclo de vida formal de tarefas: `queued`, `claimed`, `running`, `blocked`, `review`, `done`, `failed`, `escalated`
- Handoffs formais e rastreáveis
- Heartbeat e presença
- Tracing base por tarefa

### Fase 4 — OpenCode como Executor

Integrar OpenCode ao mesh:

- Perfis OpenCode especializados: planner, coder, reviewer, tester, docs-writer, sre-debugger, context-scout
- Regras, permissões e MCPs por perfil
- Chamada controlada pelos workers dos agentes
- Output devolvido ao ACP com artefatos

### Fase 5 — Validação Automatizada

Playwright + SonarCloud:

- Playwright: testes de validação básica de automação (já instalado — ST-S2-03 Concluída)
- SonarCloud: configuração e varredura de código (ST-S2-04 pendente — credenciais não disponíveis)
- Pipeline de validação automatizada

### Fase 6 — PO Gates e Observabilidade

Governança e HITL:

- Gates formais do PO (criação/ajuste de sprint, aprovação de plano, decisões grandes, aceite final)
- Tracing multiagente
- Métricas de throughput, falhas e retrabalho
- Log de handoffs e auditoria de intervenção humana

---

## Backlog

### user Stories — Sprint S3

| ID | Estória | SP | Dependência | Status |
|---|---|---|---|---|
| ST-S3-01 | Definir agent_card da Cindy: missão de orquestração, domínio de coordenação, habilidades de triage e escala, ferramentas permitidas (Hermes, ACP, Redis), limites de autonomia, critérios de escalação ao PO | 3 | — | Done |
| ST-S3-02 | Definir agent_card do Builder: missão de execução técnica, domínio de código e automações, habilidades de refatoração e pipeline, ferramentas permitidas (OpenCode, git, terminal), limites de autonomia | 3 | — | Done |
| ST-S3-03 | Definir agent_card do Reviewer: missão de validação, domínio de QA e compliance, habilidades de revisão semântica e auditoria, ferramentas permitidas (Playwright, SonarCloud, grep), limites de autonomia | 3 | — | Done |
| ST-S3-04 | Definir agent_card do Documenter: missão de documentação técnica, domínio de contratos e material operacional, habilidades de escrita técnica, ferramentas permitidas (markdown, docs), limites de autonomia | 3 | — | Done |
| ST-S3-05 | Definir agent_card do PlatformOps: missão de infraestrutura, domínio de IoT/telemetria/runtime, habilidades de ops e integrações (n8n, ThingsBoard), ferramentas permitidas (docker, redis-cli, terminal), limites de autonomia | 3 | — | Done |
| ST-S3-06 | Microsoft Agent Framework: instalar ambiente de avaliação, configurar projeto-teste, documentar API de agent management, avaliar Agent Governance Toolkit como referência de guardrails | 8 | — | Pending |
| ST-S3-07 | ACP Capability Registry: implementar registro de capacidades por agente (nome, domínio, ferramentas, skills, workflows, limites), permitir roteamento por capacidade no mesh | 5 | ST-S3-01 a ST-S3-05 | Done |
| ST-S3-08 | ACP Task Lifecycle: formalizar estados de tarefa (`queued`, `claimed`, `running`, `blocked`, `review`, `done`, `failed`, `escalated`), implementar transições e políticas de lock/lease | 5 | ST-S3-07 | Done |
| ST-S3-09 | ACP Handoffs: implementar protocolo formal de passagem de tarefa entre agentes, com trace_id, artifact_ref, deadline e semântica de resposta esperada | 5 | ST-S3-08 | Done |
| ST-S3-10 | OpenCode Integration: criar perfis especializados (planner, coder, reviewer, tester, docs-writer, sre-debugger, context-scout), definir permissões e MCPs por perfil, integrar chamada ao ACP mesh | 8 | ST-S3-01 a ST-S3-05 | Done |
| ST-S3-11 | OpenCode Executor Flow: implementar fluxo Cindy -> worker do agente -> OpenCode -> resultado com artefatos -> ACP, isolar tarefas complexas em worktree/sandbox | 5 | ST-S3-10 | Done |
| ST-S3-12 | Playwright Validation Suite: criar testes automatizados para validação básica de comportamento multiagente (smoke tests de handoff, smoke tests de task lifecycle) | 5 | Playwright instalado (ST-S2-03) | Pending |
| ST-S3-13 | SonarCloud Configuration: configurar SonarScanner apontando para `scaixeta/CindyAgent`, integrar ao pipeline de validação (depende de credenciais — ST-S2-04 bloqueado) | 3 | Credenciais SonarCloud (ST-S2-04) | Pending |
| ST-S3-14 | PO Gate Definition: documentar gates formais do PO (criação/ajuste sprint, aprovação plano, decisões de escopo/arquitetura/custo/risco, aceite final), definir política de quando PO entra e quando não entra | 3 | — | Pending |
| ST-S3-15 | Observabilidade Multiagente: implementar tracing por tarefa, log de handoffs, métricas de throughput/falhas/retrabalho, dashboard de saúde da sprint | 8 | ST-S3-08, ST-S3-09 | Pending |

**Total de SP planejado:** 70

---

## Decisões Registradas

| ID | Descrição | Data |
|---|---|---|
| D-S3-01 | Sprint S2 substituída — novo objetivo é materializar time AIOps multiagente com Microsoft Agent Framework | 2026-04-14 |
| D-S3-02 | Microsoft Agent Framework é a plataforma de gestão approved — não mais apenas referência futura de arquitetura | 2026-04-14 |
| D-S3-03 | ACP/Redis permanece como mesh/bus interno durante a transição para Microsoft Agent Framework | 2026-04-14 |
| D-S3-04 | OpenCode permanece como executor técnico dos especialistas — não assume papel de barramento do mesh | 2026-04-14 |
| D-S3-05 | Adoção incremental de produtos Microsoft — pagos apenas quando houver ganho operacional claro | 2026-04-14 |
| D-S3-06 | Nomes de agentes são baseados em papel — Cindy, Builder, Reviewer, Documenter, PlatformOps — não atrelados a modelo ou provedor | 2026-04-14 |
| D-S3-07 | Playwright já instalado (ST-S2-03 Concluída) — foco de S3 é criar suite de testes de validação | 2026-04-14 |
| D-S3-08 | SonarCloud pendente — credenciais não disponíveis (ST-S2-04) — gate de depends para ST-S3-13 | 2026-04-14 |
| D-S3-09 | Task lifecycle segue estados: `queued`, `claimed`, `running`, `blocked`, `review`, `done`, `failed`, `escalated` | 2026-04-14 |
| D-S3-10 | PO é HITL por gates, não por microgestão — entra em definição de sprint, aprovação de plano, decisões de escopo/arquitetura/custo/risco, aceite final | 2026-04-14 |
| D-S3-11 | Codex é o modelo de pensamento e validação do time — usado para raciocínio profundo, planejamento e verificação de fatos contra o SoT | 2026-04-14 |
| D-S3-12 | Drift de reboot identificado no Hermes: o runtime subiu com configuração antiga de Codex como primário e causou HTTP 400; estado tratado como transitório e superado pela D-S3-13 | 2026-04-14 |
| D-S3-13 | Hermes Linux alinhado ao canônico: `MiniMax-M2.7` como primário via `minimax`, `gpt-5.3-codex` como fallback via `openai-codex`, `hermes-gateway.service` reiniciado com healthcheck e `hermes chat -Q` validados | 2026-04-14 |
| D-S3-14 | Passagem de bastão analítica registrada em `KB/aiops/HANDOFF_S3_2026-04-14.md` para consolidar o que foi feito, o estado atual e o horizonte plausível da S3 | 2026-04-14 |
| D-S3-15 | Hermes atualizado de `v0.8.0` para `v0.9.0 (2026.4.13)` com proteção prévia da alteração local em `cron/scheduler.py` por stash e patch de backup; serviço e chamadas locais permaneceram válidos após o update | 2026-04-14 |
| D-S3-16 | Bytecode envenenado (`.pyc` do Hermes v0.8.0) bloqueava sessões Telegram mesmo após correção do `config.yaml`; a limpeza de `__pycache__` e `.pyc` foi necessária para resolver `ImportError: cannot import name '_write_codex_cli_tokens'` no contexto de sessão | 2026-04-14 |
| D-S3-17 | Materialização do AIOps Mesh e OpenCode Profiles estabelecida e refletida na base de código (.agents/scripts/). A infraestrutura core de agentes não requer produtos MS na fase atual. | 2026-04-14 |
| D-S3-18 | A base de conhecimentos da CindyAgent foi reorganizada para não conter lixo operacional e separar referências de aplicações da documentação de governança. | 2026-04-14 |

---

## Gates (pré-abertura)

- [ ] PO aprova backlog S3
- [ ] Escopo S3 confirmado com PO
- [ ] Agent cards validados como contratos operacionais
- [ ] Microsoft Agent Framework avaliado e ambiente de desenvolvimento configurado
- [ ] Dependências externas (credenciais SonarCloud) identificadas como bloqueantes
- [ ] Policy de escalação ao PO documentada

---

## Timestamp UTC (planejado)

| Event | Start | Finish | Status |
|---|---|---|---|
| Kickoff S3 | 2026-04-14T20:00:00-ST | — | Done |
| ST-S3-01 (Agent Card Cindy) | 2026-04-14T23:20:00-ST | 2026-04-14T23:26:00-FN | Done |
| ST-S3-02 (Agent Card Builder) | 2026-04-14T23:20:00-ST | 2026-04-14T23:26:30-FN | Done |
| ST-S3-03 (Agent Card Reviewer) | 2026-04-14T23:20:00-ST | 2026-04-14T23:27:00-FN | Done |
| ST-S3-04 (Agent Card Documenter) | 2026-04-14T23:20:00-ST | 2026-04-14T23:27:40-FN | Done |
| ST-S3-05 (Agent Card PlatformOps) | 2026-04-14T23:20:00-ST | 2026-04-14T23:28:20-FN | Done |
| ST-S3-06 (MS Agent Framework) | — | — | Pending |
| ST-S3-07 (Capability Registry) | 2026-04-14T23:20:00-ST | 2026-04-14T23:24:10-FN | Done |
| ST-S3-08 (Task Lifecycle) | 2026-04-14T23:20:00-ST | 2026-04-14T23:23:20-FN | Done |
| ST-S3-09 (ACP Handoffs) | 2026-04-14T23:24:00-ST | 2026-04-14T23:25:00-FN | Done |
| ST-S3-10 (OpenCode Integration) | 2026-04-14T23:28:00-ST | 2026-04-14T23:29:20-FN | Done |
| ST-S3-11 (OpenCode Executor Flow) | 2026-04-14T23:28:00-ST | 2026-04-14T23:29:00-FN | Done |
| ST-S3-12 (Playwright Suite) | — | — | Pending |
| ST-S3-13 (SonarCloud Config) | — | — | Pending |
| ST-S3-14 (PO Gate Definition) | — | — | Pending |
| ST-S3-15 (Observabilidade) | — | — | Pending |
| Hermes update v0.9.0 | 2026-04-14T21:18:22-ST | 2026-04-14T21:21:51-FN | Done |
| Sprint close | — | — | Pending |

---

## Notas Técnicas

- **Workspace Windows:** `C:\CindyAgent`
- **Workspace WSL:** `/mnt/c/CindyAgent`
- **Runtime Hermes:** `/root/.hermes`
- **Hermes Agent:** `v0.9.0 (2026.4.13)`
- **Git remote:** `https://github.com/scaixeta/CindyAgent.git`
- **Branch atual:** `v1.1`
- **Canal operacional:** Telegram
- **Redis:** `localhost:6379` — namespaces `hermes:*` e `acp:*`
- **Playwright:** instalado — v1.58.0 (pip) / v1.54.1 (npm) — browsers Chromium, Firefox, WebKit
- **SonarCloud:** pendente de credenciais — ST-S2-04 bloqueado
- **Node.js:** v22.22.2
- **Python:** 3.12.3
- **RAM disponível:** 9.7 GiB
- **Disco disponível:** 950 GB

### Fontes de verdade

- Baseline: `KB/aiops/AIOPS_TEAM_BASELINE.md`
- Plano de ação: `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md`
- Sprint anterior: `Dev_Tracking_S2.md` (substituída)
- Sprint atual: `Dev_Tracking_S3.md` (esta)

### Stack aprovado

| Camada | Componente |
|---|---|
| Coordenação | Cindy + Microsoft Agent Framework (plataforma de gestão approved) |
| Mesh | ACP via Redis (interno durante transição) |
| Executor | OpenCode |
| Validação | Playwright + SonarCloud |
| Runtime | Hermes |
| Memória | KB canônica + Dev_Tracking + memória privada/compartilhada |
| Modelo de pensamento | Codex (raciocínio profundo, validação, verificação contra SoT) |
