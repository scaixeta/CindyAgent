# Cindy Agent

Repositório-base local da Cindy no workspace `C:\CindyAgent`, usado para manter a governança DOC2.5, a documentação canônica, a persona operacional da Cindy no Hermes e os artefatos de referência que serão replicados para outros projetos do ecossistema.

## Estado atual

- **Sprint ativa:** `S1` — permanece aberta
- **Runtime principal:** Hermes em WSL (`Ubuntu`), com runtime vivo em `/root/.hermes`
- **Canal operacional principal:** Telegram, via Hermes Gateway
- **KB canônica da Cindy para Hermes:** `KB/hermes/`
- **Sincronização viva do runtime:** `/root/.hermes/SOUL.md`, `/root/.hermes/memories/USER.md`, `/root/.hermes/memories/MEMORY.md`
- **Branch principal deste repositório:** `main`
- **Segredo local protegido:** `.scr/.env` permanece fora de versionamento

## Escopo atual da S1

- estabilizar o runtime Hermes + Telegram
- consolidar a persona Cindy em KB canônica e runtime vivo
- manter a documentação DOC2.5 aderente ao estado real do projeto
- registrar o portfólio principal da Cindy para replicação futura

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

**Repositório principal de trabalho no momento:** `C:\01 - Sentivis\Sentivis SIM`

> A replicação entre esses projetos continua como atividade planejada. Não deve ser executada sem validação por repositório, confirmação de branch/remote e tracking individual.

## Operação rápida

### Subir Hermes + Cindy no Telegram

```powershell
.\start_hermes_cindy_telegram.bat
```

### Reativar apenas a persona Cindy no runtime atual

```powershell
python KB\hermes\activate_cindy_runtime.py
```

## Estrutura canônica

- `README.md` — entry point do projeto
- `Dev_Tracking.md` — índice de sprints
- `Dev_Tracking_S1.md` — sprint ativa
- `docs/SETUP.md` — ambiente, instalação e preparo operacional
- `docs/ARCHITECTURE.md` — arquitetura atual
- `docs/DEVELOPMENT.md` — fluxo de evolução e backlog
- `docs/OPERATIONS.md` — operação corrente do runtime Hermes
- `tests/bugs_log.md` — bugs, testes e evidências
- `Replicar.md` — mapa dos projetos principais da Cindy e alvos de replicação

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

A Cindy é a agente principal do ecossistema. Neste repositório, ela opera como camada de continuidade operacional entre documentação, runtime Hermes, regras locais, rastreabilidade de sprint e futuros processos de replicação entre projetos.

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy — Orquestradora" width="220" />
</p>
