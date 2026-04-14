# KB — Knowledge Base do CindyAgent

Fonte de conhecimento canônico do projeto. Organizada por domínio.

## Estrutura

```
KB/
  aiops/      — Estratégia, plano de execução e documentos da Sprint S3 (time AIOps multiagente)
  hermes/     — Runtime Hermes: memória, persona, exportes e diagnósticos do gateway
  meta/       — Status de repositórios e metadados gerais do projeto
```

> Conteúdo do ecossistema Sentivis fica em `C:\01 - Sentivis\Sentivis SIM\KB\`.

## aiops/

| Arquivo | Descrição |
|---|---|
| `S3_EXECUTION_PLAN.md` | **Documento oficial de execução da S3** — guia autoritativo por fase |
| `AIOPS_TEAM_BASELINE.md` | Estado real do time, lacunas e arquitetura alvo |
| `AIOPS_TEAM_ACTION_PLAN.md` | Plano de ação detalhado em 6 fases |
| `AGENT_TRANSITION_BOARD.md` | Board de decisões, bloqueios e pontos de validação |
| `HANDOFF_S3_2026-04-14.md` | Passagem de bastão — estado ao fim do ciclo operacional 2026-04-14 |

## hermes/

| Arquivo | Descrição |
|---|---|
| `MEMORY.md` | Memória operacional da Cindy no runtime Hermes |
| `SOUL.md` | Persona e valores da Cindy |
| `USER.md` | Perfil do PO |
| `RUNTIME_EXPORT.md` | Exportação do estado do runtime |
| `README.md` | Guia de uso dos arquivos Hermes |
| `fallback_diagnosis.md` | Diagnóstico do fallback MiniMax (BUG-S3-01) |
| `runtime_export/` | Snapshots de configuração e estado do runtime |

## meta/

| Arquivo | Descrição |
|---|---|
| `REPOSITORIES_STATUS.md` | Status dos repositórios do ecossistema Cindy |
