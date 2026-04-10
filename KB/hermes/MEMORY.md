## Cindy Agent - Fatos persistentes

### Workspace e stack

- Projeto: Cindy Agent
- workspace_root: `C:\CindyAgent` | `C:\cindyagent` (case-sensitive no Windows)
- workspace em WSL: `/mnt/c/cindyagent`
- Stack operacional: Hermes + Telegram
- Runtime principal de acompanhamento: Hermes via gateway no Telegram

### Git e repositorio

- Remote oficial: `https://github.com/scaixeta/cindy-oc`
- Branch principal: `main`
- `.scr/.env` e segredo local e nao deve ser versionado

### Regras operacionais

- O Hermes deve ser iniciado por rotina simples no Windows e ficar pronto no Telegram
- Telegram e o canal principal de interacao operacional quando o gateway estiver ativo
- "acorde" e uma retomada logica, nao um wake-on-LAN
- Se a maquina estiver desligada, suspensa ou sem gateway, o Telegram nao inicia o Hermes sozinho
- Commit/push apenas sob ordem explcita do PO
- Nao expor segredos
- Nao inventar resultados nem conteudo de arquivos
- Priorizar respostas objetivas, leitura sob demanda, status claro e execucao controlada

---

## Sprint Learnings  Sentivis SIM

### S3  Mock Telemetry Validation (Encerrada 2026-04-11)

**Entregas:**
- 18 estorias, 68 SP, todas Done
- Docs canonicos reestruturados para DOC2.5 (Objectivo, Constraints, Progress, Relevant Files, Next Steps, Critical Context)
- PT-BR sem acentos aplicado em 14 ficheiros (strip NFKD)
- Cirrus Lab conectado  4 devices reais (NIMBUS-AERO, ATMOS-WIND, ATMOS-LINK, NIMBUS-ECHO-R1)
- Jira integration consolidada  sync, reconcile, sprint assign, sprint dates
- Gate F0 testado e aprovado
- 6 docs extras criados: TELEMETRY_CONTRACT, DEVICE_PROFILE_MODELING, DASHBOARD_BASELINE, RULE_ENGINE_EVALUATION, TRILHA_EVIDENCIA, HARDWARE_BASELINE

**Learnings:**
- Subagentes (Codex) geraram informacao incorreta sobre DASHBOARD_BASELINE (referencia inexistente)  risco de hallucination em delegation
- Memory falha: contexto de S3 encerrada nao foi retido entre sessoes  MEMORY.md precisa de fatos de sprint
- DOC2.5 CHECK foi executado via subagente, nao automaticamente  precisa ser paso de prompt
- Commits exigem preflight documentado e autorizacao PO  nunca
- Dev_Tracking e o unico SoT de estado de sprint  nao confiar em memoria
- KB files podem existir em localizacoes diferentes das esperadas (ex: THINGSBOARD_INTEGRATION.md movido para KB/)
- PT-BR audit precisa de tooling automatizado (strip NFKD)  correcao manual propensa a erro

### Padroes de falha conhecidos

| Falha | Prevencao |
|---|---|
| Subagente gera informacao incorreta | Verificar facts contra SoT antes de aceitar |
| Estado de sprint perdido na memoria | Registrar fatos de sprint em MEMORY.md |
| Commits sem autorizacao PO | Gate obrigatorio em todo commit |
| Reference a ficheiro inexistente | Ler o ficheiro antes de referencia-lo |
| Caracteres nao-ASCII em docs PT-BR | Usar strip NFKD antes de escrever |

### Infra Sentivis (referencia persistente)

- ThingsBoard CE: `204.168.202.5:8080` (tenant: sentivis@sentivis.com.br)
- n8n Railway: `stvsiaopsdevice-api-production.up.railway.app`
- Cirrus Lab: 4 devices ativos, JWT exp 2026-04-10 (renovar)
- Jira STVIA: espelho operacional, nao SoT

---

## Pending validations

- [ ] Cirrus Lab JWT renovado apos expiracao 2026-04-10
- [ ] S4 backlog definido para Sentivis SIM
- [ ] PT-BR strip automatizado testado
