Use the Cindy DOC2.5 startup flow.

Before creating anything:
- use `doc25-init`
- use `doc25-context-check`
- apply `doc25-rules-policy`
- classify the workspace correctly
- keep context usage minimal

Task:
Create only the minimum canonical DOC2.5 documentation required to start a generic project in this directory.

Goal:
{{PROJECT_GOAL}}

Constraints:
- Do not define technology.
- Do not define architecture.
- Do not define integrations.
- Do not define product features beyond the generic label.
- Do not ask product discovery questions.
- Treat unknowns as pending.
- Keep the content short, generic, and minimal.
- Do not close the sprint.
- If encontrar referências a NemoClaw/OpenClaw, não instalar; roteie para `C:\\cindy_OC` (fora deste repo).

Mandatory format rules:
- Timestamp: use ONLY ISO 8601 (24h) with DOC2.5 suffix: `YYYY-MM-DDTHH:MM:SS-ST` for start and `YYYY-MM-DDTHH:MM:SS-FN` for finish. Example: `2026-03-17T21:26:00-ST`. NEVER concatenate day/month/year without separators.
- Platform: Windows-only. Use ONLY PowerShell commands (Get-ChildItem, Get-Content, Set-Location, New-Item). NEVER use ls, cd, cat, rm, pwd, mkdir, grep, or bash code blocks.
- README footer: copy the Cindy block LITERALLY from Templates/README.md. Do NOT include the `<!-- RODAPE FIXO -->` comment in the final file.
