# AGENT_TRANSITION_BOARD

## Objetivo

Acompanhar a transição do CindyAgent de um runtime centralizado para um time AIOps multiagente com Microsoft Agent Framework como plataforma de gestão.

> Status consolidado mais recente: ver `KB/aiops/HANDOFF_S3_2026-04-14.md`.

**Decisão central:** Nomes de agentes são baseados em papel — não em modelo. Microsoft Agent Framework é a plataforma de gestão approved — não mais referência futura.

---

## Papéis do time

| Papel | Responsabilidade | Status atual |
|---|---|---|
| Cindy (Coordenação) | Coordenação operacional, roteamento, visibilidade | Ativo |
| Builder | Execução técnica, código, automação | Materializado (Worker + OpenCode) |
| Reviewer | Validação, revisão, qualidade | Materializado (Worker + OpenCode) |
| Documenter | Documentação, kb, procedimentos | Materializado (Worker + OpenCode) |
| PlatformOps | Infraestrutura, runtime, observabilidade | Materializado (Worker + OpenCode) |

> Nenhum papel está atrelado a modelo ou provedor específico. Modelo é runtime strategy — não identidade.

---

## Decisões aprovadas

| # | Decisão | Data |
|---|---|---|
| D1 | Nomes de agente = papel (não modelo) | 2026-04-14 |
| D2 | Microsoft Agent Framework = plataforma de gestão approved | 2026-04-14 |
| D3 | ACP/Redis permanece como mesh interno durante transição | 2026-04-14 |
| D4 | OpenCode permanece como executor técnico dos especialistas | 2026-04-14 |
| D5 | Adoção incremental: produtos Microsoft pagos não são obrigatórios na fase 1 | 2026-04-14 |
| D6 | Gateway iniciado via WSL2 + systemd (`hermes-gateway.service`) — não mais via `.bat` | 2026-04-14 |
| D7 | Fix permanente de bytecode no unit file do systemd (`ExecStartPre` de limpeza de `.pyc`) — risco de drift pós-reboot eliminado | 2026-04-14 |

---

## Arquivos alterados

| Arquivo | Alteração | Status |
|---|---|---|
| `KB/aiops/AIOPS_TEAM_BASELINE.md` | Nomes papel + MAF approved + rationale | Feito |
| `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md` | Premissas, Fase 6, núcleo aprovado, logging mínimo na Fase 2 | Feito |
| `KB/hermes/MEMORY.md` | Fatos canônicos atualizados | Feito |
| `KB/aiops/AGENT_TRANSITION_BOARD.md` | Este board | Feito |
| `KB/aiops/S3_EXECUTION_PLAN.md` | **Documento oficial de execução da S3** | Feito |
| `KB/README.md` | Índice navegável e reorganização da KB | Feito |
| `.agents/scripts/` | Materialização do ACP Mesh e Workers especialistas | Feito |
| `/etc/systemd/system/hermes-gateway.service` | ExecStartPre de limpeza de `.pyc` adicionado | Feito |
| `tests/bugs_log.md` | BUG-S3-04 + TEST-S3-05 registrados | Feito |

---

## Sequência de execução (Fases do ACTION_PLAN)

1. **Fase 1** — Contrato operacional por papel ✅
2. **Fase 2** — ACP ampliado como mesh governado ✅
3. **Fase 3** — Materializar os especialistas (workers) ✅
4. **Fase 4** — Integrar OpenCode como executor ✅
5. **Fase 5** — Observabilidade e governança ← **próxima**
6. **Fase 6** — Adoção Microsoft Agent Framework

---

## Bloqueios abertos

| Bloqueio | Impacto | Ação necessária |
|---|---|---|
| ST-S2-05: porta 11434 do Ollama bloqueada para WSL2 | Builder não consegue usar Ollama local | Usuário libera firewall/Norton |
| ST-S2-04: credenciais SonarCloud pendentes | Análise de código bloqueada | PO fornece credenciais |
| Sprint S3 aberta, backlog não priorizado para execução | Materialização multiagente não iniciada | **PO confirma Fase 1 (agent_cards) para iniciar** |

> **Bloqueio encerrado (2026-04-14):** "Bootstrap Windows não endurecido para o serviço systemd" — resolvido pelo fix permanente de bytecode no unit file (D7, BUG-S3-04). Gateway agora limpa `.pyc` automaticamente em todo start, incluindo reboots.

---

## Pontos de validação

| Ponto | Critério | Responsável | Status |
|---|---|---|---|
| P1 | Todos os nomes de papel estão refletidos na KB canônica | Cindy | ✅ |
| P2 | MAF aparece como plataforma approved (não "futuro") nos docs | Cindy | ✅ |
| P3 | `KB/aiops/AGENT_TRANSITION_BOARD.md` criado e acessível | Cindy | ✅ |
| P4 | Backlog da S3 priorizado pelo PO antes de iniciar execução | PO | ⏳ pendente |
| P5 | Gateway estável após reboot sem intervenção manual | Cindy | ✅ (D7 / BUG-S3-04) |

---

## Referências

- Baseline: `KB/aiops/AIOPS_TEAM_BASELINE.md`
- Plano: `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md`
- Memória: `KB/hermes/MEMORY.md`
- Tracking: `Dev_Tracking.md`, `Dev_Tracking_S3.md`

---

*Board atualizado em 2026-04-14. Documento oficial de execução: `KB/aiops/S3_EXECUTION_PLAN.md`. Próxima ação: PO confirma Fase 1 (agent_cards) para iniciar execução da S3.*
