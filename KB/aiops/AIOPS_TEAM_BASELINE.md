# AIOPS_TEAM_BASELINE.md

## Objetivo

Este documento registra o estado real atual do time CindyAgent, a direção desejada para o time AIOps multiagente e os gaps que ainda precisam ser fechados.

Ele deve servir como referência de arquitetura operacional e de priorização para a materialização do time de desenvolvimento real orquestrado pela Cindy, com o PO atuando como human-in-the-loop apenas nos gates adequados.

## Estado real confirmado hoje

### Runtime e canais ativos

- Workspace Windows: `C:\CindyAgent`
- Workspace WSL: `/mnt/c/CindyAgent`
- Runtime vivo Hermes: `/root/.hermes` — versão `v0.9.0 (2026.4.13)`
- Serviço ativo do gateway: `hermes-gateway.service` (systemd, enabled, `Restart=always`)
- Modo de inicialização: **WSL2 + systemd** — não mais via `.bat` Windows
- Fix permanente de bytecode: `ExecStartPre` no unit file limpa `.pyc` e `__pycache__` em todo start
- Serviço ativo de backbone: `redis-server.service`
- Canal operacional principal: Telegram
- API server Hermes: porta `127.0.0.1:8642`
- Healthcheck: `curl http://127.0.0.1:8642/health` → `{"status": "ok", "platform": "hermes-agent"}`

### Ferramentas disponíveis hoje

#### 1. Hermes

- Runtime principal da Cindy
- Sessões persistidas em `/root/.hermes`
- Gateway ativo para Telegram
- API server OpenAI-compatible via `8642`
- Base atual do modelo padrão: MiniMax

### 2. Telegram

- Canal principal de interação operacional com a Cindy
- Diretório de canais mostra DM ativa `Sentivis AI`
- Depende do gateway Hermes ativo

### 3. Redis

- Backbone local disponível em `localhost:6379`
- Namespace `hermes:*` em uso pelo runtime
- Namespace `acp:*` disponível para comunicação entre agentes

### 4. ACP via Redis

- Biblioteca local: `.agents/scripts/acp_redis.py`
- Script de teste: `.agents/scripts/test_acp_multi_agent.py`
- Streams existentes confirmados:
  - `acp:stream:minimax`
  - `acp:stream:sentivis`
- Há mensagens persistidas de teste nos streams

### 5. OpenCode

- Wrapper local disponível: `run_opencode.bat`
- Função atual: raciocínio profundo e tarefas de código
- Modelo operacional documentado: `MiniMax-M2.7`
- Deve evoluir para executor técnico dos agentes especialistas, não para barramento do sistema

### 6. Codex

- Presença operacional confirmada no ambiente
- Papel atual: advisor para tarefas mais complexas de planejamento, arquitetura e validação
- Não é o modelo padrão do runtime Hermes neste momento

### 7. KB canônica

- Fonte de verdade comportamental em `KB/hermes/`
- Sincronizada com o runtime vivo da Cindy

## O que o sistema ainda não é

Apesar de a documentação do projeto já descrever a equipe de 5 agentes, o runtime real ainda não opera como um time multiagente autônomo completo.

### Não confirmado como operação contínua hoje

- agentes independentes rodando continuamente por papel
- consumidores autônomos permanentes por stream ACP
- comunicação peer-to-peer real e recorrente entre todos os agentes
- execução paralela contínua de tarefas entre especialistas
- mesh de descoberta de capacidades em produção
- workflow de sprint automatizado ponta a ponta com gates explícitos do PO

## Leitura correta do estado atual

Hoje o sistema funciona, na prática, como:

`PO -> Cindy -> Hermes + ferramentas + delegação + Redis`

Ou seja:

- Cindy é o agente realmente operacional
- Hermes fornece runtime, memória, gateway e API
- Redis e ACP existem como infraestrutura e prova de conceito
- Codex e OpenCode existem como capacidades de apoio
- a equipe de 5 agentes ainda está parcialmente materializada, não plenamente operacional

## Direção desejada aprovada

O objetivo é transformar esse estado em um time AIOps/de desenvolvimento real.

### Princípios desejados

- Cada agente deve ter independência operacional dentro do seu domínio
- Cada agente deve possuir ferramentas, skills, workflows e regras próprias
- Os agentes devem operar em mesh, com consciência mútua de capacidades e responsabilidades
- A Cindy deve atuar como orquestradora e coordenadora, não como gargalo de cada microdecisão
- O PO deve ser o HITL do sistema, mas por gates, não por passo operacional

### Leitura prática do HITL do PO

O PO entra em:

- definição e ajuste da sprint
- aprovação de plano
- decisões grandes de escopo, risco, custo ou arquitetura
- aceite final

O PO não deve precisar entrar em:

- handoffs normais entre agentes
- validações intermediárias de rotina
- coordenação de execução diária da sprint

## Modelo-alvo do time

### Nomes baseados em papel — rationale

Nomes de agente atrelados a um modelo ou provedor específico criamfragilidade:

- se o modelo muda, o nome perde o sentido
- se o provedor muda, a identidade do agente precisa mudar junto
- a equipe não deveria precisar renomear-se quando a estratégia de runtime muda

Nomes baseados em papel são estáveis porque:

- o papel existe independentemente do modelo que o executa
- qualquer provedor pode atuar em qualquer papel conforme a tarefa
- a identidade da equipe permanece consistente ao longo de múltiplas mudanças de stack

### Papéis-alvo (role-based)

- `Cindy`: orquestração, triagem, gestão de dependências, consolidação, escala ao PO
- `Builder`: código, lógica de aplicação, automações, refatorações, pipelines
- `Reviewer`: validação semântica, QA, revisão, compliance, auditoria
- `Documenter`: documentação técnica, contratos, dashboards, material operacional
- `PlatformOps`: IoT, infraestrutura, telemetria, integrações de campo, n8n, ThingsBoard, runtime, observabilidade

**Importante:** nenhum papel está vinculado a um modelo ou provedor específico. Qualquer papel pode usar OpenAI, Codex, GPT-5.x, MiniMax, GLM ou outro provedor dependendo da tarefa, do custo e da disponibilidade.

### Requisitos de independência por agente

Cada agente deve ter:

- missão clara
- fronteira de atuação
- skills próprias
- ferramentas permitidas
- workflows próprios
- critérios de entrada e saída
- regras de escala
- memória privada de trabalho
- acesso controlado à memória compartilhada

## Arquitetura-alvo recomendada

### 1. Mesh governado

O modelo recomendado para este projeto não é swarm puro sem governança.

O modelo mais coerente é:

- mesh de comunicação entre especialistas
- Cindy como coordenadora leve
- PO como gate de decisão

### Avaliação do mesh via ACP

O `mesh governado` pode ser implementado sobre o ACP interno via Redis, desde que o ACP evolua de prova de conceito para protocolo operacional completo.

#### O que o ACP atual já sustenta

- publicação de mensagens estruturadas
- streams persistidos por agente
- separação de namespace em `acp:*`
- prova de comunicação entre agentes simulados

#### O que o ACP ainda precisa ganhar

- `agent_card` ou registro de capacidades por agente
- heartbeat e presença
- ciclo de vida formal de tarefa
- artefatos e referências de saída
- `trace_id`, `task_id`, `session_id` e correlação
- política de retry, timeout, lease e dead-letter
- estado de aprovação humana

Conclusão: o ACP atual é base viável para o mesh interno, mas ainda não é o mesh completo.

### 2. Capability registry

Cada agente deve anunciar:

- nome
- domínio
- ferramentas
- skills
- workflows
- limites
- critérios de escala

Esse registro deve permitir roteamento por capacidade, não apenas por palavra-chave.

### 3. Memória em camadas

- memória privada por agente
- memória compartilhada do time
- memória de sprint
- memória de decisão do PO
- memória operacional de incidentes e aprendizados

### 4. Comunicação orientada a tarefa

Mensagens entre agentes devem carregar:

- tarefa
- contexto
- artefatos
- dependências
- status
- resposta esperada
- deadline ou SLA
- motivo de escala quando existir

### 5. Observabilidade obrigatória

O time precisa rastrear:

- quem recebeu a tarefa
- quem delegou
- que ferramenta foi usada
- quais artefatos foram gerados
- por que houve falha
- quando houve intervenção humana

## Ferramentas e capacidades que faltam materializar

### Princípio de stack

O direcionamento aprovado é `Microsoft first`, mas sem dependência inicial de produtos com licenciamento alto ou acoplamento prematuro ao stack pago.

Na prática:

- priorizar tecnologia Microsoft open source ou com tier gratuito viável
- usar ferramentas pagas apenas quando houver ganho operacional claro
- preservar OpenCode, Redis e documentação canônica como ativos já disponíveis

### Coordenação

- registry vivo de capacidades por agente
- roteamento por capability
- handoff formal entre agentes
- status de tarefa por agente
- política de gates do PO
- política de autonomia por agente e por tipo de tarefa

### Execução

- workers independentes por papel
- consumo contínuo de filas/streams
- isolamento de contexto por agente
- workflows versionados por papel
- integração do OpenCode como executor dos especialistas
- sandboxes ou worktrees por tarefa complexa

### Governança

- gates formais do PO
- política de autonomia por tipo de tarefa
- limites de custo, risco e escopo
- auditoria das decisões

### Observabilidade

- tracing por tarefa multiagente
- timeline de handoffs
- métricas de throughput, falhas e retrabalho
- avaliação humana e automática por sprint

## Ferramentas recomendadas por camada

### Obrigatórias para materializar o time

- Hermes como runtime da Cindy
- Redis como barramento do mesh
- ACP evoluído como protocolo interno
- OpenCode como executor dos especialistas
- documentação canônica em `docs/`
- sprint e backlog em `Dev_Tracking*.md`
- KB compartilhada e memória privada por agente

### Fortemente recomendadas na próxima fase

- capability registry por agente
- artifact store por tarefa
- tracing multiagente
- runbooks por workflow
- locks e leases para evitar dupla execução

### Microsoft-first recomendada

- **Microsoft Agent Framework como plataforma de gestão aprovada** — é agora a referência oficial de arquitetura e gestão de agentes para o CindyAgent
- Agent Governance Toolkit como referência de guardrails
- Azure DevOps Boards/Pipelines apenas se o custo operacional fizer sentido
- Azure Monitor/Application Insights em fase posterior para observabilidade centralizada

### Solução Microsoft-first recomendada

### Objetivo da solução

Adotar Microsoft Agent Framework como plataforma de gestão de agentes approved, com adoção incremental e sem bloqueio por licenças. O ACP/Redis permanece como mesh/bus interno durante a transição. OpenCode permanece como executor técnico dos especialistas.

### Princípios da solução

- Microsoft Agent Framework é agora a **plataforma de gestão approved** — não mais apenas referência futura
- a adoção é **incremental**: produtos Microsoft pagos não são obrigatórios na primeira fase
- a abordagem permanece **portátil e interoperável** — o framework é aberto e o runtime é desacoplado de escolhas de modelo
- preservar a documentação canônica e o `Dev_Tracking` como fonte de verdade
- preservar o ACP via Redis como barramento interno do time durante a transição
- usar OpenCode como executor técnico dos especialistas
- adiar produtos Microsoft pagos até existir maturidade operacional suficiente

### Stack-alvo por camada

#### 1. Coordination layer

- Cindy como coordenadora
- **Microsoft Agent Framework como plataforma de gestão approved**
- Agent Governance Toolkit como modelo de guardrails de runtime

#### 2. Mesh layer

- ACP interno sobre Redis
- capability registry por agente
- task lifecycle, artifacts, trace e handoff
- semântica inspirada em A2A para descoberta de capacidade e coordenação

#### 3. Knowledge layer

- `docs/` como documentação canônica
- `Dev_Tracking*.md` como fonte de verdade da sprint
- `KB/` como memória operacional e baseline arquitetural
- memória privada por agente e memória compartilhada de time

#### 4. Execution layer

- OpenCode como runtime de execução dos especialistas
- agentes especializados por papel
- worktrees ou sandboxes por tarefa

#### 5. Tool layer

- MCP para ferramentas e contexto externo
- integrações Microsoft quando agregarem valor real
- integração não-Microsoft mantida quando já for funcional e mais econômica

#### 6. Observability layer

- tracing e métricas locais no curto prazo
- evolução posterior para Azure Monitor / Application Insights

### Decisão prática de adoção

#### Entrar agora

- Microsoft Agent Framework como referência arquitetural
- Agent Governance Toolkit como referência de segurança e governança
- Redis + ACP como barramento
- OpenCode como executor
- documentação e tracking locais como source of truth

#### Entrar em fase posterior

- Azure DevOps Boards
- Azure Pipelines
- Azure Monitor / Application Insights
- Entra ID ou identidade centralizada para agentes, se a complexidade justificar

#### Adiar

- Azure SRE Agent como núcleo inicial
- Copilot Enterprise como dependência principal do time
- qualquer componente Microsoft com custo recorrente sem ganho comprovado

### Interpretação do Microsoft-first neste projeto

Neste contexto, `Microsoft first` não significa substituir imediatamente tudo por produto Microsoft.

Significa:

- desenhar a arquitetura para convergir ao ecossistema Microsoft
- usar primeiro o que a Microsoft oferece de forma aberta, interoperável ou economicamente viável
- manter interoperabilidade com ferramentas já adotadas enquanto o time amadurece

### Resultado esperado

Ao seguir essa solução:

- o projeto respeita a diretriz Microsoft-first
- não se bloqueia por licença antes da hora
- mantém evolução incremental
- preserva a autonomia dos agentes e a governança do PO

### Ferramentas a adiar

- Azure SRE Agent como núcleo do sistema
- Copilot Enterprise como dependência central do time
- qualquer produto Microsoft com custo recorrente sem ganho operacional já demonstrado

## Integração recomendada do OpenCode

O OpenCode deve ser integrado como motor de execução dos agentes especialistas.

### Papel do OpenCode no sistema

- executar trabalho técnico de código
- operar com agentes especializados por papel
- respeitar instruções, permissões e MCPs por agente
- devolver resultado, artefatos e status ao ACP

### Papel que o OpenCode não deve assumir

- não deve ser o barramento do mesh
- não deve ser a fonte de verdade da sprint
- não deve substituir a Cindy como coordenadora

### Fluxo recomendado

1. Cindy ou outro agente cria uma tarefa no ACP
2. O worker do agente alvo consome a tarefa
3. O worker chama o OpenCode com o agente certo
4. O OpenCode executa no contexto delimitado
5. O resultado volta para o ACP com artefatos, status e evidências
6. Cindy consolida ou escala ao PO quando necessário

### Especialistas OpenCode sugeridos

- `planner`
- `coder`
- `reviewer`
- `tester`
- `docs-writer`
- `sre-debugger`
- `context-scout`

## Padrões de mercado e comunidade que devem guiar a evolução

### Padrões observados

- supervisor + especialistas
- colaboração lateral com handoffs
- memória compartilhada + memória privada
- protocolos abertos de interoperabilidade
- human-in-the-loop por gate
- observabilidade completa de tool calls, trajetórias e decisões

### Fontes externas que embasam esta direção

- Anthropic — arquitetura de agentes e padrões de governança
- LangChain/LangGraph — supervisor, handoffs e redes multiagente
- CrewAI — crews, flows, memória, skills e HITL
- Microsoft Agent Framework — observabilidade, aprovações, MCP e interoperabilidade
- Google A2A — descoberta de capacidade, tarefas, artefatos e interoperabilidade entre agentes
- Azure SRE Agent — exemplo real de AIOps com automação sob guardrails
- Repositórios comunitários de times multiagente de desenvolvimento com planner/coder/reviewer/tester/docs
- OpenCode — agentes especializados, permissões, regras, comandos, MCP e execução headless

## Decisões de orientação para o CindyAgent

- Tratar o time atual como `estado parcial`, não como `estado final`
- Evitar afirmar que a equipe de 5 agentes já opera de forma plenamente autônoma
- Projetar a evolução sobre um modelo de mesh governado
- Adotar a solução `Microsoft first` de forma incremental, pragmática e compatível com restrições de licença
- Preservar Cindy como coordenadora e o PO como gate humano
- Materializar agentes como unidades reais com ferramentas, skills, memória e workflows próprios

## Próximos passos recomendados

1. Definir o contrato operacional de cada agente
2. Definir o registry de capacidades
3. Definir o protocolo de handoff e artefatos
4. Definir as memórias privada, compartilhada e de sprint
5. Definir os gates HITL do PO
6. Implementar workers reais por agente
7. Implementar observabilidade multiagente
8. Atualizar a documentação canônica para refletir o estado real versus o estado-alvo
9. Integrar o OpenCode como executor controlado dos especialistas
10. Avaliar adoção incremental do stack Microsoft-first conforme licença e maturidade

## Status deste documento

- Tipo: baseline canônico de arquitetura operacional
- Uso: orientar planejamento e implementação do time AIOps da Cindy
- Política: atualizar sempre que o estado real do runtime ou da governança mudar
- Observação: este documento não é o plano de ação final; ele é a base confirmada que deve sustentar o plano consolidado ao fim da análise
- Última atualização: `2026-04-14` — runtime Hermes v0.9.0 estável, fix permanente de bytecode aplicado, gateway via systemd, Fase 1 do ACTION_PLAN como próximo passo aguardando OK do PO
