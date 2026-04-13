# CindyAgent — Pacote de Replicação

**Versão:** 1.0
**Data:** 2026-04-13
**Origem:** WSL2 Ubuntu (machine name: `CINDY-WIN`, hostname: `cindy-win`)

## O que está neste pacote

```
REPLICAR_PACKAGE/
├── README.md                        # Este arquivo
├── scripts/
│   ├── 00_setup_wsl.sh              # Pré-requisitos do WSL2
│   ├── 01_install_hermes.sh         # Instalação do Hermes Agent
│   ├── 02_configure_env.sh          # Configuração de variáveis de ambiente
│   ├── 03_install_redis.sh          # Instalação do Redis
│   ├── 04_install_opencode.sh       # Instalação do OpenCode CLI
│   ├── 05_install_codex.sh          # Instalação do Codex CLI (opcional)
│   ├── 06_sync_kb.sh                # Sincronização da KB canônica
│   ├── 07_install_ollama.sh         # GLM-5.1 via Ollama (opcional)
│   ├── 08_setup_acp.sh              # Configuração do ACP via Redis
│   └── 99_activate.sh               # Ativação final
├── configs/
│   ├── config.yaml.template         # Template do config.yaml do Hermes
│   ├── .env.template                # Template do .env (sem segredos)
│   ├── SOUL.md.template             # Persona canônica da Cindy
│   ├── USER.md.template             # Preferências do operador
│   ├── MEMORY.md.template           # Memória operacional da Cindy
│   └── dual_model_gate.py          # Gate de roteamento para 5 agentes
├── runtime_export/                  # Exportação do runtime vivo
│   ├── config.runtime.yaml          # Config.yaml exportado (sem segredos)
│   ├── auth.export.json             # Auth providers (tokens censurados)
│   ├── skills_list.txt             # Lista de skills instaladas
│   ├── redis_dump.redis            # Dump do Redis (opcional)
│   └── system_info.txt             # Info do sistema original
└── docs/
    ├── REPLICAR.md                  # Guia de replicação
    ├── CHECKLIST.md                 # Checklist de validação
    └── TROUBLESHOOT.md             # Problemas comuns
```

## Fluxo de instalação

```bash
# 1. No WSL2 destino, clonar ou copiar este pacote
cp -r /mnt/c/CindyAgent/REPLICAR_PACKAGE ~/

# 2. Executar em ordem
cd ~/REPLICAR_PACKAGE
bash scripts/00_setup_wsl.sh        # Pré-requisitos
bash scripts/03_install_redis.sh    # Redis
bash scripts/01_install_hermes.sh   # Hermes
bash scripts/02_configure_env.sh    # .env e config.yaml
bash scripts/04_install_opencode.sh # OpenCode CLI
bash scripts/06_sync_kb.sh          # KB canônica
bash scripts/08_setup_acp.sh        # Scripts ACP
bash scripts/99_activate.sh         # Validação final
```

## O que cada script faz

| Script | O que instala/configura |
|---|---|
| `00_setup_wsl.sh` | Pacotes base: git, curl, build-essential, python3.11, python3-pip, redis-server |
| `01_install_hermes.sh` | Clona hermes-agent repo, cria venv, instala dependências |
| `02_configure_env.sh` | Copia templates, solicita API keys, valida configuração |
| `03_install_redis.sh` | Instala e configura Redis 7.0+ |
| `04_install_opencode.sh` | Instala OpenCode CLI, configura MINIMAX_API_KEY |
| `05_install_codex.sh` | Instala Codex CLI via npm (opcional) |
| `06_sync_kb.sh` | Copia KB canônica para ~/.hermes/ |
| `07_install_ollama.sh` | Instala Ollama e modelo glm-5.1:cloud (opcional) |
| `08_setup_acp.sh` | Copia scripts ACP para .agents/scripts/ |
| `99_activate.sh` | Testa conectividade, valida ambiente |

## Pré-requisitos do sistema destino

- **WSL2** com Ubuntu 20.04+ ou Debian 12+
- **Windows 10/11** com WSL2 habilitado
- **20 GB** de espaço em disco
- **8 GB RAM** recomendado
- **Acesso à internet** para download de pacotes

## API Keys necessárias

| Provider | Variável | Como obter |
|---|---|---|
| MiniMax | `MINIMAX_API_KEY` | Coding Plan em minimax.io |
| Telegram | `TELEGRAM_BOT_TOKEN` | @BotFather no Telegram |
| GitHub | `GITHUB_TOKEN` | GitHub Settings → Developer Settings |

## Validação pós-instalação

```bash
# Testar Hermes
hermes --version

# Testar Redis
redis-cli PING
# Esperado: PONG

# Testar OpenCode
opencode --version

# Testar ACP
python3 .agents/scripts/test_acp_multi_agent.py

# Testar gate de roteamento
python .agents/skills/dual-model-orchestrator/scripts/dual_model_gate.py "monitorar thingsboard"
# Esperado: SENTIVIS

# Ativar Cindy
cd ~/CindyAgent
python3 KB/hermes/activate_cindy_runtime.py
```

## Replicação para outro projeto

Depois de instalar neste WSL2, para replicar a estrutura para outro projeto:

1. Copiar a pasta `.agents/` e `docs/` para o novo repo
2. Copiar `rules/WORKSPACE_RULES.md` e `Cindy_Contract.md`
3. Ajustar paths e nomes nos arquivos copiados
4. Registrar no `Dev_Tracking.md` do novo projeto

## Origem do pacote

Este pacote foi gerado a partir do ambiente:

- **Machine:** `CINDY-WIN` (Windows + WSL2)
- **WSL:** `Ubuntu 24.04` via `wsl --install Ubuntu`
- **Python:** `3.11.15` (venv: `/root/.hermes/hermes-agent/venv`)
- **Node:** `v22.22.2`
- **Redis:** `7.0.15`
- **Hermes Agent:** `v0.8.0` (git tag `RELEASE_v0.8.0.md`)
- **Runtime path:** `/root/.hermes/`
- **Config path:** `~/.hermes/config.yaml`
- **Repo principal:** `https://github.com/scaixeta/cindy-oc`

## Suporte

Para problemas, consulte `DOCS/TROUBLESHOOT.md` ou use:

```bash
hermes doctor
redis-cli INFO
python3 .agents/scripts/test_acp_multi_agent.py
```
