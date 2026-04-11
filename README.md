# Cindy Agent

Repositorio-base local da Cindy no workspace `C:\CindyAgent`, usado para manter a governanca DOC2.5, a documentacao canonica, a persona operacional da Cindy no Hermes e os artefatos de referencia que serao replicados para outros projetos do ecossistema.

## Estado atual

- **Sprint ativa:** `S1` — permanece aberta
- **Runtime principal:** Hermes em WSL (`Ubuntu`), com runtime vivo em `/root/.hermes`
- **Canal operacional principal:** Telegram, via Hermes Gateway
- **Tool de raciocinio:** OpenCode CLI com MiniMax M2.7 (Coding Plan)
- **KB canonica da Cindy para Hermes:** `KB/hermes/`
- **Sincronizacao viva do runtime:** `/root/.hermes/SOUL.md`, `/root/.hermes/memories/USER.md`, `/root/.hermes/memories/MEMORY.md`
- **Branch principal deste repositorio:** `main`
- **Segredo local protegido:** `.scr/.env` permanece fora de versionamento

## Sprint S1 — Estado

| Estorias | Total | Done | Pending |
|---|---|---|---|
| Backlog | 16 | 16 | 0 |

Sprint permanece aberta aguardando ordem de encerramento do PO.

## Escopo atual da S1

- estabilizar o runtime Hermes + Telegram
- consolidar a persona Cindy em KB canonica e runtime vivo
- integrar OpenCode CLI como tool de raciocinio profundo
- manter a documentacao DOC2.5 aderente ao estado real do projeto
- registrar o portfolio principal da Cindy para replicacao futura

## Projetos principais da Cindy

O arquivo `Replicar.md` deve ser lido como o mapa dos **projetos principais da Cindy** no estado atual.

Alvos registrados:

1. `C:\Cindy-OC`
2. `C:\01 - Sentivis\Sentivis IA Code`
3. `C:\01 - Sentivis\Sentivis SIM`
4. `C:\Users\sacai\OneDrive\Documentos\FinTechN8N`
5. `C:\01- Astronomus Brasilis\Astro AI Br`
6. `C:\MCP-Projects`
7. `C:\Project Health`
8. `C:\Cindy`

**Repositorio principal de trabalho no momento:** `C:\01 - Sentivis\Sentivis SIM`

> A replicacao entre esses projetos continua como atividade planejada. Nao deve ser executada sem validacao por repositorio, confirmacao de branch/remote e tracking individual.

## Operacao rapida

### Subir Hermes + Cindy no Telegram

```powershell
.\start_hermes_cindy_telegram.bat
```

### OpenCode — usar reasoning profundo

```batch
.\run_opencode.bat "prompt aqui"
```

Modelo padrao: `minimax/MiniMax-M2.7`

## Estrutura canonica

- `README.md` — entry point do projeto
- `Dev_Tracking.md` — indice de sprints
- `Dev_Tracking_S1.md` — sprint ativa
- `docs/SETUP.md` — ambiente, instalacao e preparo operacional
- `docs/ARCHITECTURE.md` — arquitetura atual
- `docs/DEVELOPMENT.md` — fluxo de evolucao e backlog
- `docs/OPERATIONS.md` — operacao corrente do runtime Hermes
- `tests/bugs_log.md` — bugs, testes e evidencias
- `Replicar.md` — mapa dos projetos principais da Cindy e alvos de replicacao

## Leitura recomendada

1. `rules/WORKSPACE_RULES.md`
2. `Cindy_Contract.md`
3. `README.md`
4. `docs/SETUP.md`
5. `docs/ARCHITECTURE.md`
6. `docs/DEVELOPMENT.md`
7. `docs/OPERATIONS.md`
8. `Dev_Tracking.md`
9. `Dev_Tracking_S1.md`
10. `Replicar.md`

---

## Cindy — Orquestradora

A Cindy e o agente principal do projeto. Em cada run, ela identifica o orchestrator ativo (Cline/Codex/Antigravity), a superficie de execucao (VSCode/CLI) e o workspace root; em seguida, descobre e seleciona as skills/workflows disponiveis no contexto atual, respeitando os gates DOC2.5 (plano aprovado antes de execucao; commit/push apenas sob ordem explicita do PO).

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy — Orquestradora" width="220" />
</p>
