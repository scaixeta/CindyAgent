# DEVELOPMENT.md — Desenvolvimento

## Visão Geral

O desenvolvimento atual do Cindy Agent permanece dentro da **Sprint S1**, ainda aberta, com foco em consolidar o runtime Hermes, a persona Cindy, a documentação DOC2.5 e o planejamento da replicação entre os projetos principais da Cindy.

## Estado atual da sprint

- **Sprint ativa:** `S1`
- **Status:** aberta
- **Escopo corrente:** Hermes + Telegram + KB/hermes + docs canônicos + tracking + planejamento de replicação

## Fluxo DOC2.5 aplicado neste projeto

```text
1. entender o pedido
2. ler contexto mínimo necessário
3. separar fato, inferência e pendência
4. propor caminho proporcional ao impacto
5. executar a menor mudança necessária
6. registrar tracking e evidências
7. validar coerência documental
```

## Gates obrigatórios

| Gate | Regra |
|---|---|
| Planejamento | obrigatório antes de mudanças estruturais ou replicação multi-repo |
| Escrita | somente após entendimento claro do impacto |
| Commit/Push | apenas sob ordem explícita do PO |
| Fechamento de sprint | não permitido sem comando explícito do PO |

## Escopo aprovado agora

### Dentro do escopo atual

- manter o repositório-base Cindy Agent coerente com o estado real do Hermes
- documentar KB/hermes e runtime vivo do Hermes
- documentar operação via Telegram e gateway
- registrar os projetos principais da Cindy via `Replicar.md`
- planejar replicação futura sem executá-la automaticamente

### Fora do escopo atual

- alterar em lote os repositórios listados em `Replicar.md`
- fechar a sprint S1
- automatizar replicação entre todos os projetos sem tracking individual

## Portfólio principal da Cindy

`Replicar.md` deve ser tratado como o mapa atual dos **projetos principais da Cindy**.

Repositório principal de trabalho neste momento:

- `C:\01 - Sentivis\Sentivis SIM`

Planejamento futuro de replicação por repositório deve seguir esta ordem mínima:

1. validar limpeza local (`git status`)
2. confirmar branch e remote
3. definir escopo exato da cópia
4. registrar tracking local antes de alterar

## Escopo de replicação planejado

Itens candidatos a replicação controlada:

- skills relevantes
- docs canônicos
- Prompt / persona Cindy
- `Cindy_Contract.md`
- `rules/`
- workflows e artefatos GSD quando aplicáveis

## Política Git

- `git status`, `git log`, `git show` → leitura permitida
- `git commit` e `git push` → somente com ordem explícita do PO
- não assumir autorização por silêncio

## Rastreabilidade mínima

Toda mudança relevante deve refletir:

- `README.md`
- `docs/`
- `Dev_Tracking.md`
- `Dev_Tracking_S1.md`
- `tests/bugs_log.md` quando houver bug ou teste real

## Qualidade

- alvo mínimo de qualidade interna: **80/100**
- preferir mudança mínima, verificável e reversível
- documentar o estado real em vez de descrever arquitetura aspiracional

## Referência

Consulte `Dev_Tracking_S1.md` para backlog, decisões e pendências da sprint ativa.
