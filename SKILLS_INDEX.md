# SKILLS_INDEX - Descoberta Minima de Skills da Cindy

Atualizado em: 2026-04-01

## 1. Proposito

Este arquivo existe para reduzir desperdicio de contexto.

Ele nao substitui o inventario completo de skills do runtime. Ele funciona como indice curto de triagem para que a Cindy:

- descubra a categoria certa primeiro
- abra apenas a skill realmente necessaria
- evite ler dezenas de `SKILL.md` sem gatilho claro

## 2. Regra de Uso

Antes de abrir skills completas, a Cindy deve:

1. ler `rules/WORKSPACE_RULES.md`
2. confirmar o objetivo da tarefa
3. consultar este indice
4. escolher no maximo 1 ou 2 skills provaveis
5. abrir o `SKILL.md` apenas das skills selecionadas

Se a tarefa for simples e puramente documental, a Cindy nao deve abrir skills de dominio externo por prevencao.

## 3. Ordem Minima de Descoberta

1. regras locais
2. sprint ativa
3. docs canonicos estritamente necessarios
4. `SKILLS_INDEX.md`
5. skill especifica
6. referencias complementares da skill, apenas se necessario

## 4. Core DOC2.5

Usar primeiro quando o trabalho for de governanca, documentacao, tracking ou validacao:

- `doc25-context-check`
- `read_project_docs`
- `doc-coauthoring`
- `update_dev_tracking`
- `doc25-preflight`
- `doc25-governance`
- `doc25-workflows`

## 5. Planejamento e Estrutura

Usar quando a tarefa exigir proposta de mudanca, desenho de escopo ou revisao estrutural:

- `doc25-orchestrator`
- `doc25-init`
- `propose_architecture_change`
- `workflow-patterns`
- `crisp-dm-workflow-doc25`
- `generate_skill_projection`

## 6. Autoria de Skills e MCP

Usar quando o trabalho for criar capacidades reutilizaveis para a Cindy, sem conflitar com skills ja existentes:

- `skill-authoring`
- `mcp-builder`

Regra pratica:

- `skill-authoring` para desenhar ou revisar skills
- `mcp-builder` para construir o servidor MCP
- usar ambas quando a skill precisar orientar a criacao do proprio MCP

## 7. Desenvolvimento e Testes

Usar quando a tarefa sair do campo documental e entrar em implementacao, validacao tecnica ou regressao:

- `doc25-dev-workflow`
- `doc25-docs-workflow`
- `testing-patterns`
- `tdd-workflow`
- `validate_doc25_structure`

## 8. UI e Frontend

Usar apenas quando houver pedido explicito de interface, UX ou revisao visual:

- `frontend-design`
- `frontend-dev-guidelines`
- `web-design-guidelines`
- `design-md`
- `stitch-ui-design`

## 9. Infra, Deploy e Operacao

Usar apenas quando a tarefa realmente tocar ambiente, deploy, logs, metrics ou containers:

- `hostinger-deployment-kb` (deploy Hostinger, comandos, fluxos, ajustes e registro em KB)
- `local-static-preview` (subir/parar servidor local e smoke test)
- `deployment-procedures`
- `observability-engineer`
- `deploy`
- `deployment`
- `environment`
- `status`
- `container-debugging`
- `docker-specialist`

## 10. Dominios Especializados

Essas families existem, mas nao devem ser lidas por padrao em tarefas gerais:

- `jira-operations`
- `n8n-*`
- `servicenow-*`
- `railway-*`
- `kicad-*`
- `esp32-*`
- `terraform-*`
- `postgres-*`

## 11. Regras de Economia de Contexto

- nao abrir skills de familias inteiras sem necessidade
- nao usar inventario completo como primeira leitura
- nao abrir referencias, `assets/`, `resources/` ou `scripts/` da skill sem gatilho real
- se houver duvida entre duas skills, escolher a mais proxima do objetivo e validar antes de expandir

## 12. Observacao

O inventario completo continua distribuido nos runtimes e pode ser consultado sob necessidade.

Este indice e deliberadamente resumido para melhorar qualidade de resposta e reduzir custo de contexto nas conversas de operacao.

## 13. Skills Recentes (Operacao)

- `hostinger-deployment-kb`: processo de deploy na Hostinger com comandos, fluxo operacional, ajustes e registro em KB.
- `local-static-preview`: inicializacao/parada de servidor local para validacao rapida e smoke test.
