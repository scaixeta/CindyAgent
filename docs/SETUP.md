# SETUP.md — Configuração do Ambiente

## Visão Geral

O projeto opera hoje sobre **Windows + WSL2 + Ubuntu + Hermes**, com Telegram como canal operacional principal quando o gateway está ativo.

## Ambiente atual confirmado

| Item | Estado atual |
|---|---|
| Sistema operacional host | Windows 11 |
| Subsistema Linux | WSL2 |
| Distro principal | `Ubuntu` |
| Workspace Windows | `C:\CindyAgent` |
| Workspace em WSL | `/mnt/c/CindyAgent` |
| Runtime Hermes vivo | `/root/.hermes` |
| Executável principal do Hermes | `/root/.hermes/hermes-agent/venv/bin/hermes` |

## Pré-requisitos operacionais

- Windows com WSL2 funcional
- distro Ubuntu instalada
- Hermes instalado dentro do WSL
- credenciais do Telegram já configuradas no runtime Hermes
- `.scr/.env` preservado localmente e **fora do versionamento**

## Estrutura relevante do runtime Hermes

```text
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

```text
KB/hermes/
├── README.md
├── SOUL.md
├── USER.md
└── MEMORY.md
```

Essa KB é a origem canônica para a persona da Cindy no Hermes. O runtime vivo em `/root/.hermes` deve permanecer coerente com esse conteúdo.

## Inicialização prática

### Subida recomendada no Windows

```powershell
.\start_hermes_cindy_telegram.bat
```

Esse launcher:

1. reinicia o gateway do Hermes
2. sobe o gateway em janela separada
3. reativa a persona Cindy no runtime
4. mostra o status do gateway

### Reativação isolada da Cindy

```powershell
python KB\hermes\activate_cindy_runtime.py
```

## Validação mínima do ambiente

```powershell
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes status
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway status
python KB\hermes\activate_cindy_runtime.py
```

## Regras importantes de setup

- `.scr/.env` é segredo local e não deve ser versionado
- o runtime atual do Hermes está vinculado ao usuário `root` no WSL
- Telegram é canal principal **somente** quando o gateway está ativo
- `acorde` deve ser interpretado como retomada lógica, não wake da máquina

## Pendências conhecidas

| Item | Status |
|---|---|
| Gateway como serviço persistente | Opcional / ainda não implantado |
| Padronização de encoding do terminal Windows | Pendente |
| Replicação para outros projetos da Cindy | Planejada |

## Referência

Consulte `docs/OPERATIONS.md` para os comandos operacionais correntes.
