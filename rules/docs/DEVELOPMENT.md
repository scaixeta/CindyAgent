# DEVELOPMENT

## Proposito

Descrever como o desenvolvimento deve ser conduzido na Cindy seguindo DOC2.5.

## Principios

- uma sprint ativa por vez
- tracking obrigatorio
- mudanca minima necessaria
- governanca antes de execucao
- sem estruturas paralelas fora do modelo canonico
- `rules/WORKSPACE_RULES.md` e fonte operacional obrigatoria, nao contexto opcional
- preflight DOC2.5 e validacao de contexto devem acontecer antes de alegar conformidade

## Fluxo geral

### 1. Ler contexto

- `README.md`
- `rules/WORKSPACE_RULES.md` e `.agents/rules`
- `.clinerules/WORKSPACE_RULES_GLOBAL.md` (Cline) ou `~/.gemini/GEMINI.md` (Antigravity Global)
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md` ativo
- `tests/bugs_log.md`
- gate `doc25-context-check`

### 2. Planejar antes de editar

- resumir entendimento
- propor plano claro
- obter aprovacao explicita do PO

### 3. Executar

- aplicar a menor mudanca possivel
- atualizar backlog em tabela `Status | Estoria`
- registrar decisoes como `[D-SX-YY] - descricao`
- referenciar bugs e testes em `tests/bugs_log.md`
- se houver mudanca estrutural, registrar pelo menos 1 teste estrutural no `tests/bugs_log.md`
- evitar linguagem de encerramento prematuro sem ordem explicita do PO

### 4. Atualizar rastreabilidade

- refletir o trabalho em `Dev_Tracking_SX.md` ativo
- atualizar `Dev_Tracking.md` se o estado da sprint mudar
- atualizar docs canonicos e templates quando a realidade da base mudar
- resumir no `Dev_Tracking_SX.md` os testes estruturais executados
- manter coerencia entre `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md`

### 5. Preflight, editorial pass e autoauditoria

- executar o gate manual `doc25-preflight` antes de reportar conclusao
- validar `Timestamp UTC` como gate bloqueante
- executar passe editorial minimo: typos, nomes de arquivo, mistura PT-BR/EN e wording simples
- incluir autoauditoria final: o que mudou, coerencia dos artefatos, pendencias de governanca e dependencias do PO

## Politica de leitura vs alteracao

### Leitura permitida

- `git status`
- `git log`
- `git show`
- `git branch`
- leitura de arquivos

### Alteracao exige gate do PO

- `git add`
- `git commit`
- `git push`
- criacao/remocao de arquivos
- instalacao de dependencias

## Skills e workflows

- Skills canonicas devem estar coerentes entre `.agents/`, `.cline/` e `.codex/`
- Workflows DOC2.5 ficam em `.clinerules/workflows/` e `.agents/workflows/`
- O uso de skills deve preceder improviso ou duplicacao de logica
- Processos de IA/ML (modelagem, classificação, RAG) exigem obrigatoriamente a orquestração via skill `crisp-dm-workflow-doc25`, mapeando todo o ciclo de vida à estrutura de controle e logging do DOC2.5 sem criar dependências de governança paralelas.

## Tests e bugs

- `tests/bugs_log.md` e o log centralizado
- `Dev_Tracking_SX.md` ativo recebe apenas resumo e referencias cruzadas
- `Timestamp UTC` deve refletir os eventos relevantes ja executados
- validacao cruzada curta deve substituir reprocessamento completo quando nao houver mudancas em artefatos estaveis

## Referencias

- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `tests/bugs_log.md`
- `rules/WORKSPACE_RULES.md`
