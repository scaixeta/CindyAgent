# ARCHITECTURE.md — Arquitetura

## Visão Geral

Cindy Agent é o repositório-base da Cindy, usado para integrar:

- governança DOC2.5
- runtime Hermes em WSL
- OpenCode CLI como tool de raciocínio profundo
- persona operacional da Cindy
- canal Telegram
- documentação e rastreabilidade
- futura replicação controlada para outros projetos da Cindy

## Arquitetura de Alto Nível

```
┌──────────────────────────────────────────────────────┐
│                    Cindy Agent                       │
│        governanca + docs + KB + tracking             │
└───────────────┬───────────────────────┬─────────────┘
                │                       │
        ┌───────▼────────┐      ┌──────▼────────┐
        │ KB/hermes       │      │ rules/ + DOC2.5│
        │ persona canonica│      │ governanca     │
        └───────┬─────────┘      └──────┬─────────┘
                │                       │
                └──────────┬────────────┘
                           │
                    ┌──────▼────────────────────────┐
                    │ /root/.hermes (runtime vivo)    │
                    │ Hermes + memorias + config       │
                    └──────┬──────────────────────────┘
                           │
                    ┌──────▼─────────┐    ┌──────────────┐
                    │ Telegram Gateway│   │ OpenCode CLI │
                    └────────────────┘    │ (delegacao)  │
                                            └──────────────┘
```

## Componentes principais

### 1. Repositório-base Cindy Agent

Mantém o cânon do projeto:

- `README.md`
- `docs/`
- `Dev_Tracking*.md`
- `tests/bugs_log.md`
- `Cindy_Contract.md`
- `rules/`
- `KB/hermes/`

### 2. OpenCode CLI

Ferramenta de delegação para tarefas que exigem raciocínio profundo sobre código.

- Wrapper: `C:\cindyagent\run_opencode.bat`
- Modelo: `minimax/MiniMax-M2.7`
- Autenticação: `MINIMAX_API_KEY` do Coding Plan em `.scr/.env`
- Invocado pela Cindy via `mcp_delegate_task` com `acp_command=opencode`

### 3. KB canônica da Cindy para Hermes

Local: `KB/hermes/`

Função:
- definir identidade da Cindy
- registrar preferências estáveis do operador
- preservar memória operacional persistente
- orientar a sincronização do runtime vivo do Hermes

### 4. Runtime vivo do Hermes

Local: `/root/.hermes`

Função:
- hospedar o runtime efetivo da Cindy no Hermes
- armazenar `SOUL.md`, `USER.md`, `MEMORY.md`, `config.yaml`, `.env`, `state.db`
- executar o gateway Telegram

### 5. Telegram

É o canal operacional principal quando o gateway está ativo.

Sem gateway ativo, o Telegram não desperta o sistema sozinho.

## Fluxo principal atual

1. ajustar KB canônica no repositório-base
2. sincronizar/reativar o runtime vivo do Hermes
3. subir ou reiniciar o gateway Telegram
4. operar a Cindy via Telegram ou CLI
5. para tarefas complexas de código, delegar ao OpenCode via `mcp_delegate_task`
6. registrar fatos, decisões e pendências na documentação e tracking
7. planejar replicação para outros projetos antes de qualquer alteração externa

## Fronteiras atuais

### Dentro do escopo atual

- Cindy Agent como repositório-base
- Hermes + Telegram funcionando no ambiente local
- OpenCode CLI como tool de delegação (MiniMax M2.7)
- documentação canônica e tracking da sprint S1
- mapa de replicação em `Replicar.md`

### Fora do escopo atual

- replicação automática para todos os projetos listados
- fechamento da sprint S1
- automação completa de deploy/serviço do gateway

## Referência

Consulte `docs/DEVELOPMENT.md` para o fluxo de evolução controlada.
