---
name: autoresearch
description: Loop autonômico (Karpathy/Goenka) adaptado ao DOC2.5 para iterar com métrica mecânica, rollback e guardas locais.
version: 0.1.0-codex
---

# Autoresearch (Codex · DOC2.5)

Implementa o padrão de iteração automática (modificar → verificar → manter/reverter → repetir) inspirado em:

- Karpathy/autoresearch (630 linhas, foco em ML)
- uditgoenka/autoresearch (skill/plug-in com subcomandos)

## Quando usar
- Precisa otimizar um objetivo mensurável com loops curtos.
- Deseja rodar “/autoresearch” ou subcomandos equivalentes em modo assistido, respeitando os gates DOC2.5.

## Guardas DOC2.5 (obrigatório)
1) Sem `git commit/push` sem ordem do PO.  
2) Sempre definir: Goal, Scope editável, Metric numérica, Direction, Verify (comando) e Guard opcional.  
3) Iterações devem ser **bounded** neste workspace; evitar “loop infinito”.  
4) Sem criação de diretórios externos de relatório sem aprovação.  
5) Respeitar paths canônicos; não alterar docs/tracking sem gate específico.

## Subconjunto suportado (Codex)
- `/autoresearch` (loop principal, Iterations: N requerido aqui)
- `/autoresearch:plan` (wizard para Goal/Scope/Metric/Verify)
- `/autoresearch:debug` e `/autoresearch:fix` (modo leitura/planejamento; sem auto-fixar sem autorização)
- `/autoresearch:learn` (somente leitura por padrão; geração de docs exige gate)
Outros subcomandos devem ser tratados como leitura/planejamento até novo aval.

## Uso rápido (exemplo seguro)
```
/autoresearch:plan Goal: aumentar cobertura Scope: src/**/*.ts Metric: cobertura% Direction: higher Verify: npm test -- --coverage | findstr "All files" Guard: npm test
```
Depois valide o plano com o PO antes de iniciar o loop.

## Referências
- README upstream: https://github.com/uditgoenka/autoresearch
- README original: https://github.com/karpathy/autoresearch
- Protocolos detalhados: references/upstream-links.md

## Portabilidade (pendente)
- Copiar esta skill para `.agents/skills/autoresearch` e `.cline/skills/autoresearch` após teste local.
