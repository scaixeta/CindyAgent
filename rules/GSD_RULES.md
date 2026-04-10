# GSD_RULES.md - Integração de Inteligência Tática

## Objetivo
Estabelecer o framework GSD (Get Shit Done) como o motor oficial de execução e especificação técnica para o projeto Cindy-OC, mantendo a compatibilidade com a governança DOC2.5.

## Regras de Operação Híbrida

### 1. Invocação de Workflows
Sempre que a Cindy identificar uma nova fase de desenvolvimento ou uma tarefa complexa, ela deve delegar a parte técnica ao GSD.
- Comandos GSD para planejamento: `/gsd:new-project`, `/gsd:plan-phase`.
- Comandos GSD para execução: `/gsd:execute-phase`, `/gsd:quick`.

### 2. Dualidade de Persistência
- **Filtro Governança (Humano):** `Dev_Tracking_SX.md` e `PROJECT.md` são os documentos oficiais para o PO.
- **Filtro Técnico (IA):** A pasta `.planning/` e os documentos `CONTEXT.md` / `PLAN.md` são a memória de longo prazo para a IA.

### 3. Padrão de Sincronização
Ao concluir uma fase no GSD (`/gsd:execute-phase`), a Cindy deve atualizar o `Dev_Tracking_SX.md` com as evidências do que foi construído, respeitando a Regra 7 (Timestamp UTC) do DOC2.5.

### 4. Mapeamento de Contexto
A Cindy deve manter o mapeamento de codebase (`/gsd:map-codebase`) atualizado sempre que houver mudanças estruturais (novas bibliotecas, novos serviços, refatoração de arquitetura).

## Comandos Rápidos
- `/gsd:help` - Lista todos os super-poderes GSD disponíveis para a Cindy.
- `/gsd:stats` - Visão geral do progresso técnico das fases.
