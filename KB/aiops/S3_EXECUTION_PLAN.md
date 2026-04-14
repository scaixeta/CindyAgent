# S3_EXECUTION_PLAN.md

## Identificação

| Campo | Valor |
|---|---|
| Documento | Plano de Execução Oficial S3 |
| Sprint | S3 — Ativa |
| Objetivo | Materializar o time AIOps multiagente com Microsoft Agent Framework |
| Fonte | Derivado de `KB/aiops/AIOPS_TEAM_BASELINE.md` e `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md` |
| Data | 2026-04-14 |
| Status | **Aprovado pelo PO — pronto para execução** |

---

## Premissas ativas

- Runtime Hermes `v0.9.0` estável em WSL2 — canal Telegram operacional
- Gateway iniciado via `hermes-gateway.service` (systemd) — fix permanente de bytecode aplicado
- Redis ativo em `localhost:6379` com namespaces `hermes:*` e `acp:*`
- OpenCode disponível via `run_opencode.bat` com modelo `MiniMax-M2.7`
- Playwright instalado (v1.58.0 pip / v1.54.1 npm) — pronto para uso na Fase 5
- SonarCloud bloqueado por credenciais (ST-S2-04) — depende de PO
- Nomes de agente são baseados em papel — nunca em modelo ou provedor
- PO é HITL por gates — não por microgestão de execução

---

## Visão do time alvo

```
PO (gates)
  └── Cindy (coordenação)
        ├── Builder     → código, automações, pipelines
        ├── Reviewer    → QA, validação, compliance
        ├── Documenter  → documentação, contratos, KB
        └── PlatformOps → infra, IoT, runtime, n8n, ThingsBoard
```

Comunicação via **ACP/Redis mesh**. Execução técnica via **OpenCode**. Gestão via **Microsoft Agent Framework**.

---

## Sequência de execução

```
Fase 1 → Agent Cards (contratos operacionais dos 5 papéis)
Fase 2 → ACP/Redis Mesh + logging mínimo de tarefa  ← rastreabilidade obrigatória antes de Fase 3
Fase 3 → Workers dos especialistas
Fase 4 → Integração OpenCode
Fase 5 → Observabilidade completa + Validação automatizada (Playwright / SonarCloud)
Fase 6 → Adoção Microsoft Agent Framework
```

> **Regra de portão:** nenhuma fase começa antes da fase anterior atingir o critério de pronto. Gates do PO são obrigatórios nos pontos marcados.

---

## Fase 1 — Agent Cards (contratos operacionais)

**Stories:** ST-S3-01 a ST-S3-05 | **SP:** 15 | **Gate PO:** aprovação dos 5 cards antes de Fase 2

### Entradas

- `KB/aiops/AIOPS_TEAM_BASELINE.md` — papéis, requisitos e modelo-alvo
- `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md` — ações e critérios de pronto

### Entrega por agente

Cada `agent_card` deve conter:

| Campo | Descrição |
|---|---|
| `missão` | O que o agente faz e para que existe |
| `domínio` | Área de responsabilidade exclusiva |
| `ferramentas_permitidas` | Lista explícita de ferramentas que pode usar |
| `ferramentas_proibidas` | O que está fora do seu escopo |
| `skills` | Skills ativos por papel |
| `workflows` | Fluxos padrão por papel |
| `entrada` | Que tipos de tarefa aceita |
| `saída` | Formato e destino do resultado |
| `limites_autonomia` | O que pode decidir sem escalar |
| `escala_ao_po` | Quando e como escala ao PO |
| `modelo_preferido` | Runtime/modelo/provedor por padrão |
| `fallback` | Alternativa quando o modelo primário falha |
| `política_custo` | Critério de uso de recursos |

### Agent cards a produzir

| Papel | Story | Domínio principal |
|---|---|---|
| Cindy | ST-S3-01 | Orquestração, triagem, roteamento, escala ao PO |
| Builder | ST-S3-02 | Código, automações, refatoração, pipelines |
| Reviewer | ST-S3-03 | QA, validação semântica, compliance, auditoria |
| Documenter | ST-S3-04 | Documentação técnica, contratos, KB, material operacional |
| PlatformOps | ST-S3-05 | Infra, IoT, runtime, telemetria, n8n, ThingsBoard |

### Critério de pronto

- [ ] 5 `agent_card` produzidos e revisados
- [ ] Cada card tem missão, domínio, ferramentas, entrada/saída, limites e escala ao PO
- [ ] Nenhum papel tem sobreposição de responsabilidade não resolvida
- [ ] Roteamento por capacidade é possível com base nos cards
- [ ] **Gate PO:** PO aprova os 5 cards antes de avançar

---

## Fase 2 — ACP/Redis Mesh governado + logging mínimo

**Stories:** ST-S3-07, ST-S3-08, ST-S3-09 | **SP:** 15 | **Gate PO:** nenhum — execução contínua

> **Atenção:** o logging mínimo de tarefa é entrega obrigatória desta fase. Nenhum worker da Fase 3 entra em execução sem rastreabilidade funcionando.

### Entradas

- Agent cards aprovados (Fase 1)
- `KB/aiops/AIOPS_TEAM_BASELINE.md` seção ACP
- Redis ativo com namespace `acp:*`

### Entregas

#### 2.1 Capability Registry (ST-S3-07)

Cada agente anuncia no ACP:

```json
{
  "agent": "builder",
  "domain": "code",
  "tools": ["opencode", "git", "terminal"],
  "skills": ["coder", "tester"],
  "limits": { "max_autonomy": "refactoring", "always_escalate": ["architecture", "cost"] }
}
```

#### 2.2 Task Lifecycle (ST-S3-08)

Estados formais:

```
queued → claimed → running → blocked → review → done
                                    ↘ failed
                                    ↘ escalated
```

Cada transição de estado registra:
- `task_id` — UUID único da tarefa
- `trace_id` — ID de rastreamento da cadeia de handoffs
- `agent` — quem executou a transição
- `timestamp` — UTC ISO 8601
- `resultado` ou `motivo_falha`

#### 2.3 Handoffs formais (ST-S3-09)

Mensagem de handoff carrega:

```json
{
  "task_id": "...",
  "trace_id": "...",
  "from_agent": "cindy",
  "to_agent": "builder",
  "task": "...",
  "context": "...",
  "artifact_ref": "...",
  "deadline": "...",
  "resposta_esperada": "...",
  "motivo_escala": null
}
```

#### 2.4 Logging mínimo obrigatório

- Toda transição de estado gravada em log estruturado (JSON)
- Cada handoff registra `trace_id` propagado
- Consultável via Redis CLI ou log local
- Formato: `acp:log:<task_id>` com histórico de transições

### Critério de pronto

- [ ] Capability registry funcionando — agentes anunciam capacidades no ACP
- [ ] Task lifecycle implementado com todos os estados e transições
- [ ] Handoffs formais com `task_id`, `trace_id` e campos obrigatórios
- [ ] **Logging mínimo validado:** qualquer tarefa ACP gera trace legível com origem, destino, estado e resultado
- [ ] Gate interno: validar com tarefa de teste ponta a ponta antes de Fase 3

---

## Fase 3 — Workers dos especialistas

**Stories:** (derivado de Fase 1+2) | **SP:** incluído no escopo da S3 | **Gate PO:** nenhum

### Entradas

- Agent cards (Fase 1)
- ACP mesh + logging funcionando (Fase 2)

### Entregas por agente

Cada worker deve:

- Consumir filas/streams do ACP continuamente
- Operar com contexto isolado (memória privada)
- Publicar resultado, artifacts e status de volta ao ACP
- Respeitar `agent_card` como contrato de execução

### Estrutura por agente

```
/workers/
  cindy/      → orquestração, triagem, handoff para especialistas
  builder/    → consome tarefas de código, chama OpenCode
  reviewer/   → consome tarefas de QA, valida artifacts
  documenter/ → consome tarefas de documentação
  platformops/ → consome tarefas de infra e runtime
```

### Critério de pronto

- [ ] Cada worker consome e devolve tarefas via ACP sem intervenção manual da Cindy em cada passo
- [ ] Contexto e memória isolados por agente
- [ ] Trace de tarefa ponta a ponta: PO envia → Cindy roteia → worker executa → resultado no ACP

---

## Fase 4 — Integração OpenCode

**Stories:** ST-S3-10, ST-S3-11 | **SP:** 13 | **Gate PO:** nenhum

### Entradas

- Workers operacionais (Fase 3)
- `run_opencode.bat` disponível

### Perfis OpenCode a criar

| Perfil | Usado por | Função |
|---|---|---|
| `planner` | Cindy | Planejamento de sprint e decomposição de tarefas |
| `coder` | Builder | Implementação de código |
| `reviewer` | Reviewer | Revisão semântica e auditoria de código |
| `tester` | Reviewer | Geração e execução de testes |
| `docs-writer` | Documenter | Produção de documentação técnica |
| `sre-debugger` | PlatformOps | Diagnóstico de runtime e incidentes |
| `context-scout` | Cindy / qualquer | Leitura e síntese de contexto longo |

### Fluxo de execução

```
Cindy (ou agente) cria tarefa no ACP
  → worker do agente alvo consume a tarefa
    → worker chama OpenCode com perfil correto
      → OpenCode executa no contexto delimitado
        → resultado + artifacts voltam ao ACP com status
          → Cindy consolida ou escala ao PO quando necessário
```

### Critério de pronto

- [ ] 7 perfis OpenCode criados com regras, permissões e MCPs por perfil
- [ ] Workers chamam OpenCode corretamente e devolvem resultado ao ACP
- [ ] OpenCode não assume papel de barramento — apenas executa tarefas delimitadas
- [ ] Tarefas complexas isoladas em worktree ou sandbox

---

## Fase 5 — Observabilidade completa + Validação automatizada

**Stories:** ST-S3-12, ST-S3-13, ST-S3-14, ST-S3-15 | **SP:** 19 | **Gate PO:** aprovação da política de gates antes de fechar

### Entregas

#### 5.1 Observabilidade (ST-S3-15)

- Timeline de handoffs por tarefa
- Métricas por ciclo de sprint: throughput, falhas, retrabalho
- Log de intervenção humana (quando e por que o PO entrou)
- Critérios de qualidade por ciclo (alvo mínimo: 80/100)

#### 5.2 Playwright Validation Suite (ST-S3-12)

- Smoke tests de handoff entre agentes
- Smoke tests de task lifecycle (queued → done)
- Testes de fallback e recuperação de falha

#### 5.3 SonarCloud (ST-S3-13)

- **Bloqueado:** depende de credenciais (ST-S2-04)
- Não bloqueia as demais entregas desta fase

#### 5.4 PO Gate Definition (ST-S3-14)

Documentar formalmente quando o PO entra:

| Gate | Quando | O PO faz |
|---|---|---|
| G1 — Sprint | Criação ou ajuste de sprint | Aprova escopo e backlog |
| G2 — Plano | Antes de executar fase | Aprova plano da fase |
| G3 — Decisão | Escopo, arquitetura, custo ou risco relevante | Decide e registra |
| G4 — Aceite final | Fim de entrega | Valida e fecha |

### Critério de pronto

- [ ] Timeline de handoffs operacional via log ACP
- [ ] Playwright smoke tests passando
- [ ] Política de gates do PO documentada e aplicada
- [ ] Observabilidade suficiente para operar o time sem inspeção manual de cada tarefa

---

## Fase 6 — Adoção Microsoft Agent Framework

**Story:** ST-S3-06 | **SP:** 8 | **Gate PO:** aprovação de trilha de adoção

### Entradas

- Time operacional (Fases 1–5 concluídas)

### Entregas

- Avaliação formal do Microsoft Agent Framework como plataforma de gestão
- Agent Governance Toolkit mapeado como modelo de guardrails
- Trilha de adoção incremental documentada
- Decisão registrada sobre Azure DevOps / Azure Monitor para fase posterior

### Critério de pronto

- [ ] Microsoft Agent Framework avaliado com ambiente de desenvolvimento configurado
- [ ] Trilha de adoção aprovada pelo PO
- [ ] Componentes Microsoft pagos adiados até ROI demonstrado

---

## Gates do PO — resumo

| Gate | Fase | O que aprova |
|---|---|---|
| G-F1 | Fim da Fase 1 | 5 agent cards antes de iniciar ACP |
| G-F5a | Durante Fase 5 | Política de gates formais do PO |
| G-F6 | Fase 6 | Trilha de adoção Microsoft Agent Framework |
| G-sprint | A qualquer momento | Ajuste de escopo, risco ou arquitetura relevante |

---

## Bloqueios externos

| ID | Descrição | Impacto | Responsável |
|---|---|---|---|
| ST-S2-04 | Credenciais SonarCloud | Bloqueia ST-S3-13 — não bloqueia demais fases | PO fornece |
| ST-S2-05 | Porta 11434 Ollama bloqueada para WSL2 | Builder não usa Ollama local | Usuário libera firewall |

---

## Definição de pronto (DoD global)

Para qualquer story ser considerada concluída:

- [ ] Entrega funciona conforme critério de pronto da fase
- [ ] Rastreabilidade registrada em `Dev_Tracking_S3.md`
- [ ] Bug ou evidência de teste em `tests/bugs_log.md` quando aplicável
- [ ] Nenhum commit/push sem ordem expressa do PO

---

## Stack aprovado

| Camada | Componente |
|---|---|
| Coordenação | Cindy + Microsoft Agent Framework (plataforma de gestão) |
| Mesh | ACP via Redis — namespace `acp:*` |
| Executor | OpenCode (perfis especializados por papel) |
| Rastreabilidade | Logging mínimo ACP (Fase 2) → Observabilidade completa (Fase 5) |
| Validação | Playwright + SonarCloud (quando desbloqueado) |
| Runtime | Hermes `v0.9.0` — canal Telegram |
| Memória | KB canônica + Dev_Tracking + memória privada/compartilhada por agente |
| Modelo de pensamento | Codex — raciocínio profundo, validação e verificação contra SoT |

---

## Referências

- `Dev_Tracking_S3.md` — sprint ativa e backlog
- `KB/aiops/AIOPS_TEAM_BASELINE.md` — estado real e arquitetura alvo
- `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md` — plano de ação detalhado
- `KB/aiops/AGENT_TRANSITION_BOARD.md` — decisões e bloqueios
- `KB/aiops/HANDOFF_S3_2026-04-14.md` — passagem de bastão operacional
- `tests/bugs_log.md` — bugs e evidências
- `docs/ARCHITECTURE.md` — arquitetura canônica

---

*Documento criado em 2026-04-14. Atualizar conforme fases forem concluídas.*
