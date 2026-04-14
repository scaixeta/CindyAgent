# AIOPS_TEAM_ACTION_PLAN.md

## Objetivo

Transformar o CindyAgent de um runtime centralizado na Cindy com infraestrutura parcial de delegação em um time AIOps/de desenvolvimento multiagente real, com especialistas independentes, mesh governado, OpenCode como executor e PO atuando como human-in-the-loop por gates.

## Premissas confirmadas

- A documentação canônica continua em `docs/`
- O backlog e a sprint continuam em `Dev_Tracking*.md`
- A sprint permanece aberta e não deve ser alterada por este plano
- O runtime real atual ainda é parcial
- O mesh interno será implementado sobre ACP via Redis
- O stack seguirá princípio `Microsoft first`, com pragmatismo de licenças
- O OpenCode será integrado como executor dos especialistas
- Nomes de agente são baseados em papel — não em modelo: Candid, Builder, Reviewer, Documenter, PlatformOps
- Microsoft Agent Framework é a plataforma de gestão approved — não mais referência futura

## Resultado esperado

Ao final da implementação, o sistema deve permitir:

- especialistas independentes por domínio
- comunicação em mesh com governança
- handoffs formais e rastreáveis
- autonomia operacional dentro de limites explícitos
- PO atuando por gates, e não por microgestão
- execução técnica delegada ao OpenCode

## Fase 1 — Consolidar o contrato operacional

### Entregas

- contrato operacional por agente (role-based)
- matriz de capacidades por agente
- política de autonomia por agente
- regras de escala ao PO
- definição de estados de tarefa
- estratégia de modelo/provedor por papel

### Ações

1. Definir `agent_card` para Cindy, Builder, Reviewer, Documenter e PlatformOps
2. Definir ferramentas permitidas e proibidas por agente
3. Definir workflows padrão por agente
4. Definir critérios de entrada, saída e handoff
5. Definir gates do PO
6. Definir para cada papel: modelos preferidos, fallback, provedor estratégia e política de custo/risco/autonomia

### Critério de pronto

- qualquer tarefa consegue ser roteada por capacidade
- cada agente tem missão e fronteira claras
- cada papel tem estratégia de modelo/provedor definida e documentada

## Fase 2 — Evoluir o ACP para mesh governado

### Entregas

- protocolo ACP interno ampliado
- capability registry
- lifecycle formal de tarefas
- heartbeat e presença
- **logging mínimo de tarefa obrigatório** — rastreabilidade antes dos workers entrarem em execução

### Ações

1. Adicionar `agent_card`, `task_id`, `trace_id`, `session_id`, `artifact_ref`
2. Definir estados: `queued`, `claimed`, `running`, `blocked`, `review`, `done`, `failed`, `escalated`
3. Adicionar lock/lease por tarefa
4. Adicionar filas de retry e dead-letter
5. Definir formato de artifact e resposta
6. **Implementar logging mínimo de tarefa:** registrar em cada transição de estado — quem enviou, quem recebeu, `trace_id`, timestamp, resultado ou motivo de falha
7. **Validar rastreabilidade antes de avançar para Fase 3** — nenhum worker deve entrar em execução sem que o trace de tarefa já funcione

### Critério de pronto

- o mesh deixa de ser prova de conceito e vira protocolo operacional confiável
- qualquer tarefa enviada ao ACP gera um trace legível com origem, destino, estado e resultado

## Fase 3 — Materializar os especialistas

### Entregas

- workers independentes por agente
- memória privada por agente
- memória compartilhada do time
- workflows especializados

### Ações

1. Criar worker de cada agente
2. Isolar contexto, memória e ferramentas por papel
3. Criar namespace ou estrutura de storage por agente
4. Definir procedimentos de leitura da fonte canônica
5. Definir política de publicação de resultado no ACP

### Critério de pronto

- cada agente consegue receber, executar e devolver trabalho sem intervenção manual da Cindy em cada passo

## Fase 4 — Integrar o OpenCode

### Entregas

- integração do OpenCode ao mesh
- agentes OpenCode especializados
- execução controlada por perfil

### Ações

1. Criar perfis OpenCode:
   - `planner`
   - `coder`
   - `reviewer`
   - `tester`
   - `docs-writer`
   - `sre-debugger`
   - `context-scout`
2. Definir regras, permissões e MCPs por perfil
3. Implementar chamada do OpenCode pelos workers
4. Devolver output do OpenCode ao ACP com artefatos
5. Isolar tarefas complexas em worktree/sandbox

### Critério de pronto

- especialistas usam OpenCode como executor técnico sem transformar o OpenCode em barramento do sistema

## Fase 5 — Observabilidade e governança

### Entregas

- tracing multiagente
- log de handoffs
- métricas por agente
- auditoria de intervenção humana

### Ações

1. Medir latência, custo, falha, retrabalho e throughput
2. Registrar tool calls e handoffs
3. Registrar onde houve bloqueio ou escala
4. Criar visão de saúde da sprint
5. Definir critérios de qualidade por ciclo

### Critério de pronto

- o time fica auditável e operável como sistema

## Fase 6 — Adoção Microsoft Agent Framework

### Entregas

- trilha de adoção Microsoft Agent Framework como plataforma de gestão approved
- integração incremental de componentes Microsoft

### Ações

1. Usar Microsoft Agent Framework como plataforma de gestão approved — não mais como alvo de arquitetura
2. Avaliar Agent Governance Toolkit para guardrails
3. Avaliar Azure DevOps para boards/pipeline quando houver ganho claro
4. Avaliar Azure Monitor/Application Insights em fase posterior
5. Adiar produtos com custo recorrente alto até a maturidade operacional justificar
6. Manter interoperabilidade com ACP/Redis durante a transição

### Critério de pronto

- a evolução do stack adota Microsoft Agent Framework como plataforma de gestão sem forçar dependência cara antes da hora

## Solução Microsoft-first a implementar

### Núcleo aprovado

- Cindy como coordenação operacional do time
- ACP via Redis como mesh governado durante transição
- OpenCode como executor dos especialistas
- Microsoft Agent Framework como plataforma de gestão approved
- Agent Governance Toolkit como referência de governança

### Sequência de adoção

#### Etapa 1 — agora

- consolidar ACP interno
- materializar especialistas
- integrar OpenCode
- usar Microsoft Agent Framework como guia estrutural

#### Etapa 2 — após estabilização do time

- avaliar Azure DevOps para apoio de board/pipeline
- avaliar Azure Monitor/Application Insights para observabilidade centralizada

#### Etapa 3 — após validação operacional

- avaliar componentes Microsoft pagos que tragam ganho real
- considerar serviços AIOps/SRE mais avançados apenas com ROI claro

### Regra de decisão

Sempre que houver duas opções técnicas equivalentes:

- preferir a opção Microsoft, se:
  - houver viabilidade econômica
  - não houver perda importante de autonomia
  - não houver dependência prematura de licença

Caso contrário:

- manter a solução atual interoperável
- registrar o gap
- adiar a migração para a fase correta

## Ferramentas obrigatórias

- Hermes
- Redis
- ACP evoluído
- OpenCode
- Microsoft Agent Framework como referência de arquitetura
- documentação canônica
- `Dev_Tracking*.md`
- KB compartilhada
- workers especializados

## Ferramentas desejáveis

- artifact store
- tracing centralizado
- capability registry visual
- dashboard operacional do time
- automation de gates e approvals
- Agent Governance Toolkit
- Azure Monitor / Application Insights
- Azure DevOps Boards/Pipelines

## Ferramentas a adiar

- Azure SRE Agent como núcleo inicial
- Copilot Enterprise como dependência central
- products Microsoft pagos sem ROI operacional demonstrado

## Gates do PO

O PO entra em:

- criação e ajuste da sprint
- aprovação do plano
- mudança relevante de escopo, arquitetura, custo ou risco
- aceite final

O PO não entra em:

- handoff rotineiro
- coordenação diária da execução
- revisão intermediária de cada microtarefa

## Ordem recomendada de implementação

1. contrato operacional (agent_cards)
2. ACP ampliado **+ logging mínimo de tarefa** — rastreabilidade é pré-requisito para os workers
3. workers dos especialistas
4. integração OpenCode
5. observabilidade completa (dashboards, métricas, auditoria)
6. adoção Microsoft-first incremental

## Observação final

Este documento é o plano de ação derivado do baseline canônico em `KB/aiops/AIOPS_TEAM_BASELINE.md`. Ele não substitui a documentação DOC2.5 nem altera a sprint ativa.
