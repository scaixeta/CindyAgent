# SETUP

## Proposito

Este documento orienta como preparar o ambiente local para trabalhar com a Cindy.

## Requisitos minimos

- Git
- Bash ou PowerShell
- Editor de texto ou IDE

## Requisitos opcionais

- Runtime local compativel com o orchestrator em uso (`Cline`, `Codex` ou `Antigravity`)
- Ferramentas de shell para inspecao local (`git`, `rg`, `bash` ou `PowerShell`)

## Instalacao

### 1. Clonar o repositorio

```bash
git clone https://github.com/scaixeta/Cindy
cd Cindy
```

### 2. Validar a estrutura base

```bash
ls
ls docs
ls rules
ls tests
```

### 3. Conferir a trilha canonica

Arquivos minimos esperados:

- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md` ativo
- `tests/bugs_log.md`
- `rules/WORKSPACE_RULES.md`

Na Cindy atual, o arquivo ativo e `Dev_Tracking_S1.md`.

### 4. Executar validacoes locais, se necessario

Validacao estrutural minima:

- conferir `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` ativo, `rules/WORKSPACE_RULES.md` e `tests/bugs_log.md`
- confirmar presenca dos 4 docs canonicos em `docs/`
- validar coerencia cruzada entre tracking, regras e documentacao

Gates operacionais:

- `doc25-preflight` como gate manual antes de alegar conclusao ou conformidade
- `doc25-context-check` para leitura incremental e higiene de contexto
- workflows em `.clinerules/workflows/` para inicializacao, docs, desenvolvimento e commit

### 5. Inicializar um projeto derivado da Cindy

A inicializacao de um novo projeto DOC2.5 derivado da Cindy deve ser feita a partir dos templates canônicos em `Templates/`, reproduzindo os artefatos obrigatorios:

- `README.md` com rodape completo da Cindy
- `Dev_Tracking.md` e `Dev_Tracking_S0.md` coerentes e sem encerramento prematuro
- `tests/bugs_log.md` inicial
- `Cindy_Contract.md` adaptado ao projeto derivado
- `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md` e `docs/OPERATIONS.md`
- `rules/WORKSPACE_RULES.md` alinhado ao contexto do projeto derivado

## Estrutura atual do projeto

```
Cindy/
├── .agents/
├── .brand/
├── .cline/
├── .clinerules/
├── .codex/
├── README.md
├── Cindy_Contract.md
├── Dev_Tracking.md
├── Dev_Tracking_S1.md
├── docs/
├── rules/
├── Templates/
├── tests/
└── Sprint/
```

## Proximos passos

- Ler `docs/ARCHITECTURE.md`
- Ler `docs/DEVELOPMENT.md`
- Ler `docs/OPERATIONS.md`
