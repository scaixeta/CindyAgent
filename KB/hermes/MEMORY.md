## Cindy Agent — Fatos persistentes

### Workspace e stack

- Projeto: Cindy Agent
- `workspace_root`: `C:\CindyAgent` | `C:\cindyagent`
- Workspace em WSL: `/mnt/c/CindyAgent`
- Stack operacional: Hermes + Telegram
- Runtime principal de acompanhamento: Hermes via gateway no Telegram

### Git e repositório

- Remote oficial: `https://github.com/scaixeta/CindyAgent`
- Branch principal: `main`
- `.scr/.env` é segredo local e não deve ser versionado

### Regras operacionais

- O Hermes deve ser iniciado por rotina simples no Windows e ficar pronto no Telegram.
- Telegram é o canal principal de interação operacional quando o gateway estiver ativo.
- `acorde` é uma retomada lógica; não é wake-on-LAN.
- Se a máquina estiver desligada, suspensa ou sem gateway, o Telegram não inicia o Hermes sozinho.
- Git oficial para autenticação e operações de publicação no GitHub deve usar o Windows quando houver dependência de login/credencial gráfica.
- Quando `git push` falhar no WSL por credencial, o procedimento preferencial é executar `git push` no repositório Windows correspondente.
- Para execução automatizada do push pelo Codex/Cline no Windows, preferir o Git do Windows em modo não interativo, evitando TTY e prompts gráficos bloqueantes.
- Procedimento validado: usar `cmd.exe` no repositório Windows com `GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=never`, `credential.interactive=never` e `credential.modalprompt=false`.
- Commit e push apenas sob ordem explícita do PO.
- Não expor segredos.
- Não inventar resultados nem conteúdo de arquivos.
- Priorizar respostas objetivas, leitura sob demanda, status claro e execução controlada.
- A Cindy deve operar com postura executiva no Telegram: organizar trabalho, tornar possibilidades visíveis, destacar bloqueios e conduzir próximos passos.
- Ao responder, deve reduzir a necessidade de coordenação manual do PO.
- A referência canônica para a evolução do time multiagente é `KB/aiops/AIOPS_TEAM_BASELINE.md`.
- O plano de ação desta linha de evolução está em `KB/aiops/AIOPS_TEAM_ACTION_PLAN.md`.
- O estado real atual do time: Fases 1 a 4 da S3 foram materializadas em código local (`.agents/scripts/`). Cindy é operacional localmente, o Mesh ACP em Redis foi codificado, os Workers de cada papel (Builder, Reviewer, Documenter, PlatformOps) foram estruturados com isolamento de contexto OpenCode.
- A direção aprovada (e parcialmente implementada) é operar num time em mesh governado, com agentes independentes por domínio e o PO atuando como HITL por gates.
- A solução arquitetural aprovada segue princípio `Microsoft first`, mas com adoção incremental e compatível com restrições de licença.
- Microsoft Agent Framework é a plataforma de gestão approved — não é mais apenas referência de arquitetura.
- ACP/Redis continua como mesh interno durante a transição para Microsoft Agent Framework.
- OpenCode permanece como executor técnico dos especialistas.
- Nomes dos agentes são baseados em papel: Cindy (coordenação), Builder (execução), Reviewer (validação), Documenter (documentação), PlatformOps (infra). Nenhum papel está atrelado a modelo ou provedor específico.
- Codex é o modelo de pensamento e validação do time — usado para raciocínio profundo, planejamento e verificação de fatos contra o SoT.

### Guardas de idioma

- Responder sempre em português do Brasil, com acentuação correta.
- Nunca usar formas de português europeu, como `ficheiros`, `activo`, `directa`, `planeamento`, `arquitectura` ou `utilizador`.
- Preferir termos brasileiros, como `arquivos`, `atual`, `direta`, `planejamento` e `arquitetura`.
- Zero caracteres asiáticos sem solicitação explícita do usuário.
- Nunca remover diacríticos de conteúdo em PT-BR sem autorização explícita do PO.

### Aprendizados recentes — Sentivis SIM

#### S3 — Mock Telemetry Validation

- 18 histórias, 68 SP, todas concluídas.
- Documentação canônica reorganizada em `SETUP`, `ARCHITECTURE`, `DEVELOPMENT` e `OPERATIONS`.
- Cirrus Lab conectado com 4 dispositivos reais: `NIMBUS-AERO`, `ATMOS-WIND`, `ATMOS-LINK` e `NIMBUS-ECHO-R1`.
- Integração com Jira consolidada para sincronização operacional.
- Gate F0 testado e aprovado.
- Documentos extras criados: `TELEMETRY_CONTRACT`, `DEVICE_PROFILE_MODELING`, `DASHBOARD_BASELINE`, `RULE_ENGINE_EVALUATION`, `TRILHA_EVIDENCIA` e `HARDWARE_BASELINE`.

#### Falhas conhecidas e prevenção

| Falha | Prevenção |
|---|---|
| Subagente gera informação incorreta | Verificar fatos contra o SoT antes de aceitar |
| Estado de sprint perdido na memória | Registrar fatos de sprint em `MEMORY.md` |
| Commit sem autorização do PO | Gate obrigatório em todo commit |
| Referência a arquivo inexistente | Ler o arquivo antes de citá-lo |
| Remoção de acentos em PT-BR | Manter `ptbr-orthography` como fonte da verdade |

#### Incidente de idioma

- Houve tentativa indevida de remover acentos de arquivos em PT-BR.
- Houve contaminação do runtime com termos de português europeu em `USER.md` e `MEMORY.md`.
- A correção obrigatória é sincronizar a KB canônica antes de cada ativação da Cindy.

#### Ajuste de personalidade

- A Cindy deve ser mais executiva e mais orientada a condução operacional no Telegram.
- Deve comunicar não só o que fez, mas também o que pode fazer, o que está travando e quais caminhos práticos estão disponíveis.

### Infra Sentivis

- ThingsBoard CE: `204.168.202.5:8080` com tenant `sentivis@sentivis.com.br`
- n8n Railway: `stvsiaopsdevice-api-production.up.railway.app`
- Cirrus Lab: 4 dispositivos ativos
- Jira STVIA: espelho operacional, não source of truth

### Validações pendentes

- [ ] Renovar o JWT do Cirrus Lab após expiração
- [x] Definir o backlog de S4 para Sentivis SIM
- [x] Corrigir o erro de strip NFKD para manter diacríticos em PT-BR
- [x] Refatorar nomes de agentes de modelo-marcados para baseados em papel
- [x] Promover Microsoft Agent Framework para plataforma de gestão approved

### Hermes Runtime — Configuração validada em 2026-04-14

| Campo | Valor |
|---|---|
| Versão Hermes | `v0.9.0 (2026.4.13)` |
| Modelo principal | `MiniMax-M2.7` |
| Provider principal | `minimax` |
| Fallback provider | `openai-codex` |
| Fallback model | `gpt-5.3-codex` |
| Fallback base_url | `https://chatgpt.com/backend-api/codex` |
| Login Codex | Válido por subscription |
| Serviço gateway | `hermes-gateway.service` (systemd de sistema) — `active (running)` |

**Nota sobre `systemd (user)`:** o `hermes status` pode mostrar "stopped" no manager `systemd (user)`, mas o serviço real em uso é o systemd de sistema, que está ativo.

**Nota sobre update:** a alteração local em `cron/scheduler.py` foi preservada antes do update do Hermes via stash `pre-update-backup-2026-04-14` e patch local `.update-backup-cron-scheduler.patch`.

**Fontes:** `KB/hermes/RUNTIME_EXPORT.md`
