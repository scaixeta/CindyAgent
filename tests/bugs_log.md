# bugs_log.md — Log de Bugs, Testes e Evidências

## Sprint S1

### BUG-S1-01 — Warnings no WSL ao ler `.scr/.env` com `CRLF`

- **Data:** 2026-04-09
- **Severidade:** Baixa
- **Evidência:** warnings do tipo `$'\r': command not found` durante ativação do runtime Hermes
- **Impacto:** ruído operacional no bootstrap da Cindy; sem impedir ativação
- **Correção:** normalização do `.scr/.env` local para `LF`
- **Status:** Corrigido

### TEST-S1-01 — Pairing Telegram aprovado

- **Data:** 2026-04-09
- **Escopo:** validar autorização do usuário no Telegram para uso do bot Hermes
- **Resultado:** pairing aprovado com sucesso; usuário reconhecido no próximo contato
- **Status:** Passou

### TEST-S1-02 — Gateway Hermes em execução manual

- **Data:** 2026-04-09
- **Escopo:** subir gateway Hermes e verificar operação fora de service manager
- **Resultado:** gateway em execução manual com PID ativo e status positivo
- **Status:** Passou

### TEST-S1-03 — Ativação da Cindy no runtime Hermes

- **Data:** 2026-04-09
- **Escopo:** enviar prompt de ativação usando `SOUL.md`, `USER.md` e `MEMORY.md` do runtime vivo
- **Resultado:** Cindy ativada com resposta válida e `session_id` gerado
- **Status:** Passou

### TEST-S1-04 — Proteção de `.scr/.env` no Git

- **Data:** 2026-04-09
- **Escopo:** validar remoção do segredo do histórico/versionamento e proteção por `.gitignore`
- **Resultado:** `.scr/.env` removido do histórico enviado ao remote e mantido apenas localmente
- **Status:** Passou

### TEST-S1-05 — API de testes FastAPI com `POST`/`GET`/`DELETE`

- **Data:** 2026-04-10
- **Escopo:** criar API de testes em FastAPI com endpoints `POST /registrar`, `GET /registros` e `DELETE /encerrar`; executar testes automatizados com `httpx.AsyncClient`; guardar evidência em `resultado_teste.json`
- **Resultado:** todos os testes passaram; 3 itens registrados, `GET` retornou 3 registros, `DELETE` devolveu relatório com contagem correta. Evidência guardada em `tests/test_api/resultado_teste.json`
- **Commit:** a8002d3
- **Status:** Passou

### TEST-S1-06 — Integração do Codex CLI

- **Data:** 2026-04-10
- **Escopo:** autenticar o Codex via `codex-cli auth login`, testar resposta do modelo com cálculo simples e configurar `gpt-5.2-codex` como modelo padrão para planejamento e arquitetura
- **Resultado:** autenticação via OAuth web (assinatura ChatGPT) confirmada; teste com `2+2` devolveu `4` com sucesso; modelo `gpt-5.2-codex` (`reasoning effort: high`, contexto: 400K) configurado como padrão para tarefas de planejamento e arquitetura
- **Status:** Passou

---

## Issues abertos

| ID | Descrição | Severidade | Status |
|---|---|---|---|
| ISSUE-S1-01 | Encoding do terminal Windows ainda pode exibir caracteres quebrados na saída do Hermes | Baixa | Aberto |

---

## Notas

- A sprint S1 permanece aberta
- `Replicar.md` passa a ser tratado como mapa dos projetos principais da Cindy
- A replicação entre projetos ainda está em fase de planejamento e não foi executada neste ciclo
- `2026-04-11` — ST-S1-16: escopo Embrapa/café movido para Sentivis SIM (S5) — não pertence ao CindyAgent. Backlog do CindyAgent corrigido para 16 itens (ST-S1-16 renarrada como desalocação de escopo).
