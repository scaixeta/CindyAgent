# ARCHITECTURE.md — Arquitetura

## Visão Geral

Cindy Agent é o repositório-base da Cindy, usado para integrar:

- governança DOC2.5
- runtime Hermes em WSL
- persona operacional da Cindy
- canal Telegram
- documentação e rastreabilidade
- futura replicação controlada para outros projetos da Cindy

## Arquitetura de Alto Nível

```text
┌──────────────────────────────────────────────────────┐
│                    Cindy Agent                      │
│        governança + docs + KB + tracking            │
└───────────────┬───────────────────────┬─────────────┘
                │                       │
                │                       │
        ┌───────▼────────┐      ┌──────▼────────┐
        │ KB/hermes       │      │ rules/ + DOC2.5│
        │ persona canônica│      │ governança     │
        └───────┬─────────┘      └──────┬─────────┘
                │                       │
                └──────────┬────────────┘
                           │
                    ┌──────▼────────────────────────┐
                    │ /root/.hermes (runtime vivo)  │
                    │ Hermes + memórias + config    │
                    └──────┬────────────────────────┘
                           │
                    ┌──────▼─────────┐
                    │ Telegram Gateway│
                    └─────────────────┘
```

## Componentes principais

### 1. Repositório-base Cindy Agent

Mantém o canon do projeto:

- `README.md`
- `docs/`
- `Dev_Tracking*.md`
- `tests/bugs_log.md`
- `Cindy_Contract.md`
- `rules/`
- `KB/hermes/`

### 2. KB canônica da Cindy para Hermes

Local: `KB/hermes/`

Função:

- definir identidade da Cindy
- registrar preferências estáveis do operador
- preservar memória operacional persistente
- orientar a sincronização do runtime vivo do Hermes

### 3. Runtime vivo do Hermes

Local: `/root/.hermes`

Função:

- hospedar o runtime efetivo da Cindy no Hermes
- armazenar `SOUL.md`, `USER.md`, `MEMORY.md`, `config.yaml`, `.env`, `state.db`
- executar o gateway Telegram

### 4. Telegram

É o canal operacional principal quando o gateway está ativo.

Sem gateway ativo, o Telegram não desperta o sistema sozinho; ele apenas volta a funcionar quando o runtime estiver em execução.

## Runtimes relacionados

| Runtime | Papel no ecossistema |
|---|---|
| `.cline/` | runtime Cline |
| `.codex/` | runtime Codex |
| `.agents/` | skills canônicas e base compartilhada |

## Portfólio principal da Cindy

Além deste repositório-base, `Replicar.md` registra os **projetos principais da Cindy** que deverão receber replicação controlada de artefatos, skills, docs e regras.

O principal repositório de trabalho atualmente é:

- `C:\01 - Sentivis\Sentivis SIM`

## Fluxo principal atual

1. ajustar KB canônica no repositório-base
2. sincronizar/reativar o runtime vivo do Hermes
3. subir ou reiniciar o gateway Telegram
4. operar a Cindy via Telegram ou CLI
5. registrar fatos, decisões e pendências na documentação e tracking
6. planejar replicação para outros projetos antes de qualquer alteração externa

## Fronteiras atuais

### Dentro do escopo atual

- Cindy Agent como repositório-base
- Hermes + Telegram funcionando no ambiente local
- documentação canônica e tracking da sprint S1
- mapa de replicação em `Replicar.md`

### Fora do escopo atual

- replicação automática para todos os projetos listados
- fechamento da sprint S1
- automação completa de deploy/serviço do gateway

## Referência

Consulte `docs/DEVELOPMENT.md` para o fluxo de evolução controlada.
