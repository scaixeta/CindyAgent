# Política de Gates Formais do PO (AIOps Mesh)

Este documento oficializa o contrato de governança **Human-In-The-Loop (HITL)** para o time multiagente (Cindy, Builder, Reviewer, Documenter, PlatformOps).

O *Product Owner (PO)* atua por exceção e aprovação de fronteiras (Gates), não por microgestão da execução das tarefas.

## 1. Mapeamento de Gates Obrigatórios

Nenhuma fase ou tarefa crítica transpassa as seguintes fronteiras de governança sem a anuência explícita do PO. O registro da intervenção humana deve ficar grafado no Log do Mesh ACP para rastreabilidade de Observabilidade (Fase 5).

| Gate | Momento | O que o PO Faz | Ação Sistêmica Esperada |
|---|---|---|---|
| **G1 — Sprint** | Criação, ajuste ou repriorização de Sprint | Aprova o escopo macro, o objetivo da Sprint e o Backlog de estórias associadas. | Emissão do arquivo `Dev_Tracking_S*.md` com status Validado e congelamento de itens na iteração atual. |
| **G2 — Plano** | Antes de executar qualquer fase ou bloco complexo | Aprova um planejamento consolidado da referida fase (como o plano de ação, contratos ou blueprints). | Geração do `PLAN_<feature>.md` aprovado. |
| **G3 — Decisão** | Mudanças de Escopo, Arquitetura, Custo ou Risco relevante | Lê a análise/draft gerada pelo time multiagente e aprova a direção técnica abordada. | Tarefas bloqueadas no Mesh mudam seu status para `review` / `done`. Registro de `<Decision Record>` em formato markdown. |
| **G4 — Aceite Final**| Fim de entrega ou encerramento de Sprint | Valida a fumaça de testes localmente ou end-to-end, confere o `HANDOFF` report e autoriza o desfecho. | Autorização de Commit/Push e fechamento dos relatórios de Sprint. |

## 2. Padrões de Escalação Semântica para o PO

Quando um Worker (via `EscalateToHuman` exception ou DLQ) precisar do PO para destravar uma etapa:
- O Worker colocará a Task no estado `escalated`.
- O payload de escalação registrará formalmente em log qual gate foi acionado ou qual é a barreira:
   * Erro sistêmico inacessível ao agente.
   * Credenciais ou pagamentos Microsoft faltantes.
   * Dúvida conceitual estrita que altere a regra de negócio do software.

**Referência**: ST-S3-14 (Fase 5 — Observabilidade e Validação)
