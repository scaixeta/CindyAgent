# OPERATIONS.md — Operações

## Visão Geral

Este documento descreve a operação atual do Cindy Agent com Hermes em WSL, Telegram como canal principal e OpenCode CLI como tool de delegação.

## Estado operacional atual

| Item | Estado |
|---|---|
| Runtime Hermes | instalado e funcional |
| Local do runtime | `/root/.hermes` |
| Executável | `/root/.hermes/hermes-agent/venv/bin/hermes` |
| Telegram | configurado e pareado |
| Gateway | funcional, actualmente executado manualmente |
| OpenCode | integrado via wrapper |
| Serviço persistente | ainda não instalado como service |

## Comandos principais

### No Windows

```powershell
# Subir Hermes + Cindy no Telegram
.\start_hermes_cindy_telegram.bat

# Usar OpenCode (raciocínio profundo)
.\run_opencode.bat "pergunta aqui"
```

### No WSL / Hermes

```powershell
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes status
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway status
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway run
```

## Semântica operacional da Cindy

- **Canal principal:** Telegram, quando o gateway está ativo
- **`acorde`:** retomada lógica da sessão/contexto
- **Não significa:** ligar máquina, acordar WSL ou iniciar Hermes do zero automaticamente
- **Commit/push:** somente com autorização explícita do PO
- **Selecção de reasoning engine:** tarefas simples/rápidas usam OpenCode (MiniMax M2.7); tarefas complexas de planeamento/arquitectura usam Codex (OpenAI gpt-5.2-codex, Reasoning Effort: High, Context 400K)
- **OpenCode:** tool de delegação — usado para raciocínio profundo em código, não substitui o Hermes

## Procedimento padrão de subida

1. iniciar o gateway Hermes
2. ativar/reaplicar a persona Cindy no runtime vivo
3. verificar o status do gateway
4. operar pelo Telegram ou CLI conforme disponibilidade

## Monitoramento rápido

| Verificação | Comando |
|---|---|
| Status geral do Hermes | `hermes status` |
| Status do gateway | `hermes gateway status` |
| Teste rápido do OpenCode | `cd /d C:\cindyagent && opencode run --model minimax/MiniMax-M2.7 "echo hello"` |

## Troubleshooting actual

| Problema | Causa provável | Correção mínima |
|---|---|---|
| Telegram não responde | gateway parado | subir/reiniciar o gateway |
| OpenCode retorna "invalid api key" | MINIMAX_API_KEY expirada ou inválida | verificar chave em `.scr/.env` |
| Warnings de `.env` no WSL | arquivo com `CRLF` | normalizar para `LF` |
| Caracteres quebrados no terminal Windows | encoding do console | usar terminal UTF-8 / PowerShell com code page adequada |

## Operação como serviço

Ainda opcional e não consolidada como padrão deste projeto.

Comandos disponíveis:

```powershell
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway install
wsl -d Ubuntu --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway uninstall
```

## Referência cruzada

- `docs/SETUP.md` — preparo e inicialização
- `Dev_Tracking_S1.md` — estado da sprint aberta
- `Replicar.md` — projetos principais da Cindy e replicação planejada
