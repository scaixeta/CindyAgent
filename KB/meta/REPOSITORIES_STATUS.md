# REPOSITORIES_STATUS.md — Estado dos Repositorios

**Gerado:** 2026-04-10
**Atualizado:** 2026-04-14 (reconciliacao de remote e contexto da sprint ativa)
**Contexto:** Repositorios ativos do portfolio Cindy via Replicar.md
**Workspace:** `C:\cindyagent` / `github.com/scaixeta/CindyAgent`

---

## Resumo

Escopo reduzido para 3 repos: CindyAgent, Sentivis SIM (principal) e Cindy. Repos pessoais removidos: Sentivis IA Code, FinTechN8N, Astro AI Br, Project Health e MCP-Projects.

---

## Inventario por Repositorio

### 1. CindyAgent
| Campo | Valor |
|---|---|
| **Caminho** | `C:\Cindy-OC` |
| **Branch** | `master` |
| **Remote** | `github.com/scaixeta/CindyAgent` |
| **Changes** | 1.084 arquivos |
| **Cindy_Contract** | Presente |
| **Dev_Tracking** | Presente |
| **Prompt.md** | Presente (copiado 2026-04-10) |
| **SKILLS_INDEX.md** | Presente (copiado 2026-04-10) |
| **KB/** | Presente |
| **docs/** | Presente |
| **.clinerules/** | Presente |
| **rules/** | Presente |
| **.scr/** | Presente |
| **Git** | OK |

### 2. Sentivis SIM (PRINCIPAL)
| Campo | Valor |
|---|---|
| **Caminho** | `C:\01 - Sentivis\Sentivis SIM` |
| **Branch** | `main` |
| **Remote** | `github.com/scaixeta/sentivis-iaops` |
| **Changes** | 161 arquivos |
| **Cindy_Contract** | Presente |
| **Dev_Tracking** | Presente |
| **Prompt.md** | Presente |
| **SKILLS_INDEX.md** | Presente |
| **KB/** | Presente |
| **docs/** | Presente |
| **.clinerules/** | Presente |
| **rules/** | Presente |
| **.scr/** | Presente |
| **Git** | OK |

### 3. Cindy
| Campo | Valor |
|---|---|
| **Caminho** | `C:\Cindy` |
| **Branch** | `main` |
| **Remote** | `github.com/scaixeta/Cindy` |
| **Changes** | 262 arquivos |
| **Cindy_Contract** | Presente |
| **Dev_Tracking** | Presente |
| **Prompt.md** | Presente |
| **SKILLS_INDEX.md** | Presente |
| **KB/** | Presente |
| **docs/** | Presente |
| **.clinerules/** | Presente |
| **rules/** | Presente |
| **.scr/** | Presente |
| **Git** | OK |

---

## Tabela Comparativa

| Repo | Cindy_Contract | Dev_Tracking | Prompt | SKILLS_INDEX | KB | docs | .clinerules | rules | .scr | Git |
|---|---|---|---|---|---|---|---|---|---|---|
| CindyAgent | X | X | X | X | X | X | X | X | X | OK |
| Sentivis SIM | X | X | X | X | X | X | X | X | X | OK |
| Cindy | X | X | X | X | X | X | X | X | X | OK |

**3/3 repos com estrutura completa.**

---

## Scores de Maturidade (0-5)

| Repo | Codigo | Docs | Governance | KB | Operations |
|---|---|---|---|---|---|
| CindyAgent | 4 | 3 | 4 | 4 | 3 |
| Sentivis SIM | 4 | 4 | 5 | 4 | 4 |
| Cindy | 3 | 3 | 4 | 4 | 3 |

---

## Correcoes Aplicadas 2026-04-10

- `Prompt.md` copiado para CindyAgent (via Sentivis SIM)
- `SKILLS_INDEX.md` copiado para CindyAgent
- `KB/USER.md` copiado para CindyAgent (espelhamento KB/hermes)
- MCP-Projects, Sentivis IA Code, FinTechN8N, Astro AI Br, Project Health removidos do Replicar.md


---

## Metas

### Curto Prazo (sprint ativa S3)
- Manter README e docs canonicos coerentes com o estado real do runtime Hermes
- Verificar mudancas pendentes (1.084 no Cindy-OC, 161 no Sentivis SIM, 262 no Cindy)
- Validar o backlog da S3 antes de expandir automacoes multiagente

### Medio Prazo (30 dias)
- Consolidar branches dos 3 repos ativos
- Garantir que todos estejam com git status limpo antes de trabalho pesado
- Replicar KB/hermes atualizada para CindyAgent KB

### Longo Prazo (90 dias)
- 3/3 repos com estrutura DOC2.5 identica e sincronizada
- Replicacao como processo recorrente entre os 3

---

## Proximos Passos

1. **[PO]** Confirmar a priorizacao do backlog da S3
2. **[PO]** Decidir sobre changes pendentes nos 3 repos (git stash? commit?)
3. **[AUTO]** Atualizar KB/REPOSITORIES_STATUS.md apos decisoes de git

---

*Documento gerado via analise direta dos repositorios ativos do portfolio Cindy.*
