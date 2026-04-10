# SETUP.md — Configuração do Ambiente

## Visão Geral

O projeto opera sobre **Windows + WSL2 + Ubuntu + Hermes**, com Telegram como canal operacional principal e OpenCode CLI como tool de raciocínio profundo.

## Ambiente atual confirmado

| Item | Estado atual |
|---|---|
| Sistema operacional host | Windows 11 |
| Subsistema Linux | WSL2 |
| Distro principal | Ubuntu |
| Workspace Windows | `C:\CindyAgent` |
| Workspace em WSL | `/mnt/c/CindyAgent` |
| Runtime Hermes vivo | `/root/.hermes` |
| OpenCode CLI | `run_opencode.bat` (wrapper) |
| Modelo OpenCode | `minimax/MiniMax-M2.7` |

## Pré-requisitos operacionais

- Windows com WSL2 funcional
- distro Ubuntu instalada
- Hermes instalado dentro do WSL
- credenciais do Telegram já configuradas no runtime Hermes
- MINIMAX_API_KEY do Coding Plan em `.scr/.env` (nunca versionar)
- OpenCode CLI acessível via `run_opencode.bat`

## Estrutura relevante do runtime Hermes

```
/root/.hermes/
├── SOUL.md
├── memories/
│   ├── USER.md
│   └── MEMORY.md
├── config.yaml
├── .env
└── hermes-agent/
    └── venv/bin/hermes
```

## KB canônica da Cindy neste repositório

```
KB/hermes/
├── README.md
├── SOUL.md
├── USER.md
└── MEMORY.md
```

Essa KB é a origem canônica para a persona da Cindy no Hermes. O runtime vivo em `/root/.hermes` deve permanecer coerente com esse conteúdo.

## Inicialização prática

### Subir Hermes + Cindy no Telegram

```powershell
.\start_hermes_cindy_telegram.bat
```

Esse launcher:
1. reinicia o gateway do Hermes
2. sobe o gateway em janela separada
3. reativa a persona Cindy no runtime
4. mostra o status do gateway

### Usar OpenCode para raciocínio profundo

```batch
.\run_opencode.bat "prompt aqui"
```

O wrapper lê `MINIMAX_API_KEY` do `.scr/.env` e passa ao OpenCode via PowerShell (resolve problema de scoping do `set` no cmd.exe).

## Validação mínima do ambiente

```powershell
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes status
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway status
```

## Regras importantes de setup

- `.scr/.env` é segredo local e não deve ser versionado
- o runtime atual do Hermes está vinculado ao usuário `root` no WSL
- Telegram é canal principal **somente** quando o gateway está ativo
- `acorde` deve ser interpretado como retomada lógica, não wake da máquina
- OpenCode é tool de delegação — não substitui o Hermes

## Pendências conhecidas

| Item | Status |
|---|---|
| Gateway como serviço persistente | Opcional / ainda não implantado |
| Replicação para outros projetos da Cindy | Planejada (ST-S1-16) |
| GSD (Get Shit Done) | Não faz parte deste projeto |

## Referência

Consulte `docs/OPERATIONS.md` para os comandos operacionais correntes.
