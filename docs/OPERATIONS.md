# OPERATIONS.md — Operacoes

## Visao Geral

Este documento descreve a operacao atual do Cindy Agent com Hermes em WSL, Telegram como canal principal e OpenCode CLI como tool de delegacao.

## Estado operacional atual

| Item | Estado |
|---|---|
| Runtime Hermes | instalado e funcional |
| Local do runtime | `/root/.hermes` |
| Executavel | `/root/.hermes/hermes-agent/venv/bin/hermes` |
| Telegram | configurado e pareado |
| Gateway | funcional, actualmente executado manualmente |
| OpenCode | integrado via wrapper |
| Servico persistente | ainda nao instalado como service |

## Comandos principais

### No Windows

```powershell
# Subir Hermes + Cindy no Telegram
.\start_hermes_cindy_telegram.bat

# Usar OpenCode (raciocinio profundo)
.\run_opencode.bat "pergunta aqui"
```

### No WSL / Hermes

```powershell
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes status
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway status
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway run
```

## Semantica operacional da Cindy

- **Canal principal:** Telegram, quando o gateway esta ativo
- **`acorde`:** retomada logica da sessao/contexto
- **Nao significa:** ligar maquina, acordar WSL ou iniciar Hermes do zero automaticamente
- **Commit/push:** somente com autorizacao explicita do PO
- **Seleccao de reasoning engine:** tarefas simples/rapidas usam OpenCode (MiniMax M2.7); tarefas complexas de planeamento/arquitectura usam Codex (OpenAI gpt-5.2-codex, Reasoning Effort: High, Context 400K)
- **OpenCode:** tool de delegacao — usado para raciocinio profundo em codigo, nao substitui o Hermes

## Procedimento padrao de subida

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
| Teste ACP (multi-agente) | `python3 .agents/scripts/test_acp_multi_agent.py` |
| Keys ACP no Redis | `redis-cli KEYS "acp:*"` |
| Stream de um agente | `redis-cli XLEN acp:stream:sentivis` |

## Troubleshooting actual

| Problema | Causa provavel | Correcao minima |
|---|---|---|
| Telegram nao responde | gateway parado | subir/reiniciar o gateway |
| OpenCode retorna "invalid api key" | MINIMAX_API_KEY expirada ou invalida | verificar chave em `.scr/.env` |
| Warnings de `.env` no WSL | arquivo com `CRLF` | normalizar para `LF` |
| Caracteres quebrados no terminal Windows | encoding do console | usar terminal UTF-8 / PowerShell com code page adequada |

## Operacao como servico

Ainda opcional e nao consolidada como padrao deste projeto.

Comandos disponiveis:

```powershell
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway install
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway uninstall
```

## Operações da equipe de agentes

### Enviar tarefa via ACP
```python
python3 -c "
import sys
sys.path.insert(0, '.agents/scripts')
from acp_redis import ACPRedis
acp = ACPRedis()
acp.publish(to='sentivis', msg_type='TASK', action='check_device_status', payload={'device':'NIMBUS-AERO'}, from_agent='cindy')
print('Tarefa enviada')
"
```

### Gate de classificação (5 agentes)
```bash
python .agents/skills/dual-model-orchestrator/scripts/dual_model_gate.py "monitorar thingsboard"
# Retorna: SENTIVIS
```

## Limite de iteração

- 3-5 ciclos Discussão→Execução→Validação
- Após limite: escalar para PO via Cindy

## Referências da equipe

- `docs/AGENT_TEAM_MODEL.md` — modelo operacional
- `docs/ACP_PROTO.md` — especificação ACP
- `docs/SETUP.md` — configuração do ambiente
