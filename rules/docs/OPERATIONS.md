# OPERATIONS

## Proposito

Orientar como operar, validar e manter a Cindy.

## Natureza operacional

A Cindy e um repositorio-base de governanca, skills e workflows. Ela opera principalmente em ambiente local para:

- leitura de contexto
- execucao de skills
- validacao estrutural DOC2.5
- manutencao de tracking, bugs e testes
- higiene de contexto para reduzir desperdicio de tokens

## Rotinas operacionais

### 0. Gate de etapa

Antes de agir, a Cindy deve declarar em qual etapa esta operando:

- `analysis`
- `planning`
- `execution`
- `validation`
- `report`

Sem essa declaracao, a Cindy deve permanecer em leitura e sintese.

Comando curto como `execute` nao deve ser interpretado como autorizacao imediata para criar artefatos.

### 1. Validacao estrutural

Conferencias minimas:

- `README.md` presente e coerente com a sprint ativa
- `docs/` com os 4 arquivos canonicos
- `rules/WORKSPACE_RULES.md` presente
- `Dev_Tracking.md` e `Dev_Tracking_SX.md` ativo coerentes
- `tests/bugs_log.md` atualizado
- gate manual `doc25-preflight` executado antes de alegar conformidade

Para projetos derivados recem-criados:

- usar `Templates/` como base oficial de bootstrap documental
- validar se o resultado final reproduz os artefatos canonicos esperados
- nao considerar aceitavel um projeto cuja estrutura exista, mas cujo `README.md` ou tracking inicial nao reflitam o baseline definido pela Cindy

### 2. Audit DOC2.5

Conduzir auditoria manual com foco em:

- estrutura canonica obrigatoria
- coerencia entre `README.md`, tracking, regras e `tests/bugs_log.md`
- ausencia de artefatos legados fora do baseline atual
- consistencia de naming, idioma e `Timestamp UTC`

### 2.1 Gate de contexto

Usar para:

- medir o custo contextual da etapa atual
- listar apenas os arquivos necessarios
- resumir pendencias da sprint ativa
- alertar sobre reprocessamento desnecessario

Tambem usar para:

- impedir expansao precoce para execucao
- justificar por que a leitura atual e suficiente
- separar contexto permanente, ativo e temporario antes de agir

### 3. Verificacao de espelho de skills

Ao adicionar ou portar skills, validar coerencia entre:

- `.agents/skills/` (Canonical SoT Antigravity)
- `.cline/skills/` (Counterpart)
- `.codex/skills/` (Counterpart)

### 4. Verificacao de workflows

- manter apenas workflows DOC2.5 genericos na Cindy pura
- remover workflows especificos de outros projetos
- manter referencias coerentes com `README.md`, tracking e regras vigentes

### 5. Verificacao de tracking

- apenas um `Dev_Tracking_SX.md` ativo na raiz
- `Sprint/` so recebe sprints arquivadas
- `Timestamp UTC` deve refletir os eventos relevantes do projeto
- fechamento de sprint e proibido sem ordem explicita do PO
- referencias de testes e roadmap devem permanecer coerentes entre artefatos

### 6. Politica de remotes e push

- identificar os remotes reais com `git remote -v`
- se houver apenas um remote configurado, operar em `single remote`
- se houver mais de um remote, nao assumir push dual automaticamente
- `dual remote` so vale quando o PO determinar explicitamente
- se nao houver remote identificavel, interromper e perguntar antes de qualquer commit/push

## Seguranca operacional

- nunca versionar credenciais
- nunca documentar segredos
- mascarar valores sensiveis
- respeitar gate do PO para alteracoes e commits

## Resposta a falhas

1. confirmar contexto em `Dev_Tracking_SX.md` ativo
2. interromper o fluxo que falhou
3. registrar bug ou teste em `tests/bugs_log.md`
4. corrigir o artefato minimo necessario
5. atualizar `Timestamp UTC`
6. revalidar docs, skills ou workflows afetados
7. executar passe editorial minimo e autoauditoria antes do relatorio final

Falha operacional inclui:

- comando invalido
- repeticao de erro equivalente
- loop ate interrupcao manual

Nesses casos, a Cindy deve trocar de estrategia e nao insistir no mesmo padrao de comando.

## Disciplina de verdade canonica

- arquitetura sugerida permanece hipotese ate evidencia ou aprovacao do PO
- stack tecnica permanece pendente ate definicao explicita
- integracoes externas nao devem ser tratadas como reais sem prova documental
- templates sao fonte de geracao, nao autorizacao para bootstrap automatico

## Referencias

- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `Dev_Tracking_SX.md`
- `tests/bugs_log.md`
