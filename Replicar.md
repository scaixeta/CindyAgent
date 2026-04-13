# Replicacao Cindy DOC2.5 — Alvos

Repos locais a sincronizar com ajustes atuais (skills, workflows, docs, GSD):

1) `C:\CindyAgent\` — repo: scaixeta/CindyAgent (agente operacional Cindy)
2) `C:\Cindy\` — repo: scaixeta/Cindy (agente antigo, histórico, intocado)
3) `C:\SentivisAIOps\Sentivis SIM\` — repo: scaixeta/Sentivis-AIOps (N8N + orquestração fazendas)

Repos removidos (pessoais — fora do escopo de replicacao):

- `C:\01 - Sentivis\Sentivis IA Code` (pessoal)
- `C:\Users\sacai\OneDrive\Documentos\FinTechN8N` (pessoal)
- `C:\01- Astronomus Brasilis\Astro AI Br` (pessoal)
- `C:\Project Health` (pessoal)
- `C:\MCP-Projects` (pessoal)
- `C:\Cindy-OC` (redundante — mesmo repo do CindyAgent)

Repos remanejados:

- `Cindy-OC` → movido para CindaAgent (repo unificado)
- `Sentivis SIM` → movido para C:\SentivisAIOps\Sentivis SIM

Proximos passos (planejar antes de executar):
- Validar se cada repo esta limpo (git status).
- Confirmar branch/remote de destino.
- Definir escopo de copia: skills, docs canonicos, Prompt, Cindy_Contract, rules.
- Registrar tracking individual em cada repo antes de alterar.
