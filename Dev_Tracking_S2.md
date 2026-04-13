# Dev_Tracking_S2.md — Sprint 2 (Ativa)

## Identificação

| Campo | Valor |
|---|---|
| Sprint | S2 |
| Status | **Planejada** — aguardando kickoff do PO |
| Início | 2026-04-13 |
| Versão | 1.0 |
| PO | Aprovado pelo PO em — |

## Escopo

Operacionalizar a plataforma Sentivis SIM (ThingsBoard CE + n8n Railway) e consolidar o stack de ferramentas de desenvolvimento da CindyAgent (TTS, MCP, Playwright, SonarCloud, Whisper STT).

**Track A — Ferramentas CindyAgent**
Stack padrão de ferramentas disponíveis para qualquer projeto: TTS MiniMax hd, MCP MiniMax, Playwright, SonarCloud, Whisper STT (via Ollama).

**Track B — Sentivis SIM**
ThingsBoard CE local, n8n Railway, dashboards, alarms, integrações de dispositivos reais (Cirrus Lab).

---

## Backlog

### Track A — Ferramentas CindyAgent

| ID | Estória | SP | Dependência | Status |
|---|---|---|---|---|
| ST-S2-01 | TTS MiniMax: fazer upgrade de `speech-02-turbo` para `speech-2.8-hd` para PT-BR mais natural | 2 | — | Pending |
| ST-S2-02 | MiniMax MCP: integrar `minimax-mcp-js` (npm) no Hermes via native-mcp em modo REST | 5 | API key configurada | Pending |
| ST-S2-03 | Playwright: instalar como ferramenta padrão e validar browser automation no WSL | 3 | Node.js 22 | **Concluída** |
| ST-S2-04 | SonarCloud: configurar SonarScanner apontando para `scaixeta/cindy-oc` via GitHub OAuth | 3 | GitHub OAuth | Pending |
| ST-S2-05 | Whisper STT: instalar e configurar via Ollama (pendente liberação de porta 11434 WSL2→Windows) | 5 | Liberação de porta 11434 | **Pendente (acesso WSL2)** |
| ST-S2-06 | Testar pipeline completo: áudio Telegram → STT Whisper → resposta Cindy → TTS → Telegram | 8 | ST-S2-05 | Pending |

### Track B — Sentivis SIM

| ID | Estória | SP | Dependência | Status |
|---|---|---|---|---|
| ST-S2-10 | ThingsBoard CE: validar acesso e estado dos dispositivos Cirrus Lab (4 dispositivos reais) | 3 | — | Pending |
| ST-S2-11 | ThingsBoard CE: configurar dashboards para os 4 dispositivos reais | 5 | ST-S2-10 | Pending |
| ST-S2-12 | ThingsBoard CE: configurar alarms para thresholds críticos | 5 | ST-S2-10 | Pending |
| ST-S2-13 | n8n Railway: operacionalizar workflows de automação Sentivis | 8 | ST-S2-10 | Pending |
| ST-S2-14 | Integração dispositivo real: validar telemetria NIMBUS-AERO e ATMOS-WIND | 5 | ST-S2-10 | Pending |
| ST-S2-15 | Documentar arquitetura Sentivis SIM em `docs/ARCHITECTURE_SIM.md` | 3 | ST-S2-13 | Pending |

---

## Decisões Registradas

| ID | Descrição | Data |
|---|---|---|
| D-S2-01 | MiniMax NÃO oferece STT — transcrição de áudio requer Whisper (local) ou outra API | 2026-04-13 |
| D-S2-02 | `minimax-mcp-js` (npm v0.0.17) integra TTS, imagem, vídeo, voice cloning, music, voice design — MCP mode: REST na porta 3000 | 2026-04-13 |
| D-S2-03 | MiniMax MCP host API: `https://api.minimaxi.chat` (com "i") — diferente do endpoint `/anthropic/v1/messages` usado diretamente | 2026-04-13 |
| D-S2-04 | Whisper STT fica pendente — usuário vai liberar porta 11434 do Ollama (Windows) para WSL2 via Norton/firewall | 2026-04-13 |
| D-S2-05 | TTS MiniMax atual usa `speech-02-turbo` — upgrade para `speech-2.8-hd` melhora qualidade para PT-BR | 2026-04-13 |
| D-S2-06 | Playwright instalado via pip + npm + browsers — ambiente Python preferencial: venv Hermes `/root/.hermes/venv/bin/python` | 2026-04-13 |

---

## Gates (pré-abertura)

- [ ] PO aprova backlog S2
- [ ] Escopo S2 confirmado com PO
- [ ] Dependências externas (liberação porta Ollama, credenciais SonarCloud) identificadas

---

## Timestamp UTC (planejado)

| Event | Start | Finish | Status |
|---|---|---|---|
| Kickoff S2 | — | — | Pending |
| ST-S2-01 | — | — | Pending |
| ST-S2-02 | — | — | Pending |
| ST-S2-03 | — | — | Pending |
| ST-S2-04 | — | — | Pending |
| ST-S2-05 | — | — | Pending |
| ST-S2-06 | — | — | Pending |
| ST-S2-10 | — | — | Pending |
| ST-S2-11 | — | — | Pending |
| ST-S2-12 | — | — | Pending |
| ST-S2-13 | — | — | Pending |
| ST-S2-14 | — | — | Pending |
| ST-S2-15 | — | — | Pending |
| Sprint close | — | — | Pending |

---

## Notas Técnicas

- **WSL2 hostname:** `cindy-win`
- **Git remote:** `https://github.com/scaixeta/cindy-oc.git`
- **Ollama Windows:** `C:\Users\sacai\AppData\Local\Programs\Ollama\ollama.exe` — processo `ollama.exe` rodando no Windows
- **Porta Ollama:** 11434 (localhost Windows) — inacessível do WSL2 por bloqueio de firewall/antivírus
- **npm global path:** `/root/.hermes/node/lib/node_modules`
- **RAM disponível:** 9.7 GiB / **Disco disponível:** 950 GB
- **Node.js:** v22.22.2 / **Python:** 3.12.3
- **Playwright venv Python:** `/root/.hermes/venv/bin/python` (venv Hermes é o ambiente preferencial para scripts Python com Playwright)
- **Playwright browsers:** Chromium, Firefox, WebKit — todos instalados via `playwright install --with-deps`
- **Playwright versão:** v1.58.0 (pip) / v1.54.1 (npm)
