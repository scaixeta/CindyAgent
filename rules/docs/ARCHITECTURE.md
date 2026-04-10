# ARCHITECTURE

## Proposito

Descrever a arquitetura da Cindy como base portatil de governanca, skills e workflows para Cline, Codex e Antigravity.

## Visao geral

A Cindy e organizada em camadas:

- governanca DOC2.5
- runtimes de skills
- workflows operacionais
- documentacao canonica
- templates e contratos de runtime

Ela funciona como base pura. Nao importa engines ou estruturas especificas de outros projetos.

## Camadas principais

### 1. Governanca

- `.agents/rules` (Workspace Rules)
- `rules/WORKSPACE_RULES.md`
- `.clinerules/WORKSPACE_RULES_GLOBAL.md` e `~/.gemini/GEMINI.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md` ativo
- `tests/bugs_log.md`

`rules/WORKSPACE_RULES.md` e a fonte operacional obrigatoria. Os demais artefatos de runtime devem herdar sua interpretacao, nunca relativiza-la.

### 2. Skills

- `.agents/skills/` (Canonical Authoring SoT)
- `.cline/skills/` (Mirror Runtime)
- `.codex/skills/` (Mirror Runtime)

As skills comuns devem permanecer coerentes entre os runtimes.

### 3. Workflows

- `.clinerules/workflows/`
- `.agents/workflows/`

Os workflows canônicos da Cindy sao os DOC2.5 genericos de init, docs, dev e commit.

### 4. Documentacao

- `README.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/OPERATIONS.md`
- `Templates/`

### 5. Branding e contrato

- `.brand/` para identidade visual
- `Cindy_Contract.md` como contrato canonico de orquestracao, subordinado a `rules/WORKSPACE_RULES.md` na operacao cotidiana

## Fluxo arquitetural principal

1. identificar o orchestrator ativo
2. carregar regras globais e locais
3. localizar a sprint ativa
4. consultar skills e workflows
5. propor plano e aguardar aprovacao
6. executar o minimo necessario
7. registrar tracking, bugs, testes e `Timestamp UTC`
8. executar `doc25-preflight` antes de alegar conformidade
9. usar `doc25-context-check` para evitar releituras desnecessarias

## Fronteiras da arquitetura

- Nao importar `skills-src/` de outros projetos
- Nao manter workflows especificos de projetos terceiros na Cindy pura
- Nao manter referencias quebradas ou artefatos redundantes
- Nao introduzir caminhos paralelos fora do modelo canonico
- O ciclo de vida de IA/ML (CRISP-DM) é reconhecido formalmente, mas seus processos habitam estritamente o modelo canônico das 4 pastas documentais e o workflow DOC2.5 aprovado. Modelos não dão permissão ao agenciamento paralelo de Git ou docs estruturais soltos.

## Relacao com outros artefatos

- `rules/WORKSPACE_RULES.md`: precedencia operacional obrigatoria
- `Cindy_Contract.md`: contrato canonico, subordinado a regra operacional na execucao cotidiana
- `docs/DEVELOPMENT.md`: fluxo de execucao
- `docs/OPERATIONS.md`: validacao e manutencao
- `Dev_Tracking_SX.md`: sprint ativa
- `tests/bugs_log.md`: evidencias tecnicas

## Mapa de Dependencias

- `rules/WORKSPACE_RULES.md` governa todos os demais artefatos e define precedencia, estrutura canonica e gates
- `Cindy_Contract.md` depende de `rules/WORKSPACE_RULES.md` para discovery e despacho, sem sobrepor a regra local
- `README.md` depende de `rules/WORKSPACE_RULES.md`, `Cindy_Contract.md`, `Dev_Tracking.md` e `Dev_Tracking_SX.md` para orientar leitura e estado atual
- `docs/SETUP.md` depende de `README.md`, `rules/WORKSPACE_RULES.md`, tracking e templates para preparar contexto e bootstrap documental
- `docs/DEVELOPMENT.md` depende de `SETUP`, `ARCHITECTURE`, regras e tracking para orientar mudanca, colaboracao e rastreabilidade
- `docs/OPERATIONS.md` depende de todos os docs canonicos, tracking e `tests/bugs_log.md` para validar coerencia e manutencao
- `Dev_Tracking.md` depende de `README.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md` para manter o indice sincronizado
- `Dev_Tracking_SX.md` depende das regras, do trabalho executado e das evidencias em `tests/bugs_log.md`
- `Templates/` depende da realidade consolidada em `README.md`, docs canonicos, tracking e regras para continuar gerando artefatos coerentes
