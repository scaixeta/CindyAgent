import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent


WSL_DISTRO = "Ubuntu-22.04"
WSL_USER = "root"
REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DIR = REPO_ROOT / "KB" / "hermes"
CANONICAL_TO_RUNTIME = {
    CANONICAL_DIR / "SOUL.md": "/root/.hermes/SOUL.md",
    CANONICAL_DIR / "USER.md": "/root/.hermes/memories/USER.md",
    CANONICAL_DIR / "MEMORY.md": "/root/.hermes/memories/MEMORY.md",
}
ACTIVATION_REFERENCES = {
    "rules/WORKSPACE_RULES.md": REPO_ROOT / "rules" / "WORKSPACE_RULES.md",
    ".clinerules/WORKSPACE_RULES_GLOBAL.md": REPO_ROOT / ".clinerules" / "WORKSPACE_RULES_GLOBAL.md",
    ".clinerules/workflows/init.md": REPO_ROOT / ".clinerules" / "workflows" / "init.md",
    ".clinerules/workflows/dev-doc25.md": REPO_ROOT / ".clinerules" / "workflows" / "dev-doc25.md",
    ".clinerules/workflows/commit-doc25.md": REPO_ROOT / ".clinerules" / "workflows" / "commit-doc25.md",
    ".clinerules/workflows/docs-doc25.md": REPO_ROOT / ".clinerules" / "workflows" / "docs-doc25.md",
    ".cline/skills/doc25-rules-policy/SKILL.md": REPO_ROOT / ".cline" / "skills" / "doc25-rules-policy" / "SKILL.md",
    ".cline/skills/workflow-patterns/SKILL.md": REPO_ROOT / ".cline" / "skills" / "workflow-patterns" / "SKILL.md",
    ".cline/skills/doc25-context-check/SKILL.md": REPO_ROOT / ".cline" / "skills" / "doc25-context-check" / "SKILL.md",
    ".cline/skills/doc25-governance/SKILL.md": REPO_ROOT / ".cline" / "skills" / "doc25-governance" / "SKILL.md",
    ".cline/skills/doc25-orchestrator/SKILL.md": REPO_ROOT / ".cline" / "skills" / "doc25-orchestrator" / "SKILL.md",
    ".cline/skills/doc25-workflows/SKILL.md": REPO_ROOT / ".cline" / "skills" / "doc25-workflows" / "SKILL.md",
}
PTBR_BLOCKED_FORMS = {
    "ficheiros": "arquivos",
    "activo": "ativo",
    "activa": "ativa",
    "directa": "direta",
    "directo": "direto",
    "planeamento": "planejamento",
    "arquitectura": "arquitetura",
    "utilizador": "usuário",
    "actual": "atual",
    "actualmente": "atualmente",
    "aceite": "aceito",
}
RUNTIME_TEXT_PATCHES = {
    "  personality: kawaii": "  personality: technical",
    "    voice: en-US-AriaNeural": "    voice: pt-BR-FranciscaNeural",
}


def resolve_wsl_command() -> str:
    for candidate in ("wsl", "wsl.exe", "/mnt/c/Windows/System32/wsl.exe"):
        if shutil.which(candidate) or Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Não foi possível localizar o executável do WSL.")


def run_wsl_python(script: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [resolve_wsl_command(), "-d", WSL_DISTRO, "--user", WSL_USER, "--", "python3", "-"],
        input=script,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


def safe_write(stream, text: str) -> None:
    if not text:
        return
    data = text.encode("utf-8", errors="replace")
    buffer = getattr(stream, "buffer", None)
    if buffer is not None:
        buffer.write(data)
        buffer.flush()
        return
    stream.write(data.decode("utf-8", errors="replace"))
    stream.flush()


def load_canonical_files() -> dict[Path, str]:
    return {
        source: source.read_text(encoding="utf-8")
        for source in CANONICAL_TO_RUNTIME
    }


def load_activation_references() -> dict[str, str]:
    return {
        label: path.read_text(encoding="utf-8")
        for label, path in ACTIVATION_REFERENCES.items()
    }


def summarize_reference(content: str, *, max_items: int = 8) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    selected: list[str] = []
    for line in lines:
        if (
            line.startswith("#")
            or line.startswith("- ")
            or line.startswith("* ")
            or re.match(r"^\d+[.)]\s", line)
            or line.lower().startswith("description:")
            or line.lower().startswith("name:")
        ):
            selected.append(line)
        if len(selected) >= max_items:
            break
    if not selected:
        selected = lines[:max_items]
    return "\n".join(selected)


def build_reference_digest(references: dict[str, str]) -> str:
    manifest = "\n".join(f"- {label}" for label in references)
    summaries = "\n\n".join(
        f"=== {label} ===\n{summarize_reference(content)}"
        for label, content in references.items()
    )
    return (
        "Manifesto exato dos artefatos relidos nesta ativação:\n"
        f"{manifest}\n\n"
        "Contagem obrigatória da `.cline/skills/`: 6 arquivos.\n"
        "A lista obrigatória inclui `.cline/skills/doc25-workflows/SKILL.md`.\n\n"
        "Digest operacional dos artefatos relidos:\n"
        f"{summaries}"
    )


def validate_ptbr(files: dict[Path, str]) -> list[str]:
    issues: list[str] = []
    for source, content in files.items():
        for blocked, replacement in PTBR_BLOCKED_FORMS.items():
            pattern = rf"(?<!`)\b{re.escape(blocked)}\b(?!`)"
            if re.search(pattern, content, flags=re.IGNORECASE):
                issues.append(
                    f"{source.name}: usar '{replacement}' em vez de '{blocked}'."
                )
    return issues


def sync_runtime_config() -> int:
    script = dedent(
        f"""
        from pathlib import Path
        import json

        path = Path("/root/.hermes/config.yaml")
        content = path.read_text(encoding="utf-8")
        replacements = json.loads({json.dumps(json.dumps(RUNTIME_TEXT_PATCHES, ensure_ascii=False))})

        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)

        path.write_text(content, encoding="utf-8")

        missing = [new for new in replacements.values() if new not in content]
        if missing:
            print("missing::" + ",".join(missing))
            raise SystemExit(2)

        print(f"configured::{{path}}")
        """
    ).strip()

    result = run_wsl_python(script)
    safe_write(sys.stdout, result.stdout)
    safe_write(sys.stderr, result.stderr)
    return result.returncode


def sync_runtime(files: dict[Path, str]) -> int:
    payload = {
        target: files[source]
        for source, target in CANONICAL_TO_RUNTIME.items()
    }
    script = dedent(
        f"""
        from pathlib import Path
        import json

        payload = json.loads({json.dumps(json.dumps(payload, ensure_ascii=False))})

        for target, content in payload.items():
            path = Path(target)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"synced::{{path}}")
        """
    ).strip()

    result = run_wsl_python(script)
    safe_write(sys.stdout, result.stdout)
    safe_write(sys.stderr, result.stderr)
    return result.returncode


def activate_runtime(references: dict[str, str]) -> int:
    reference_blocks = build_reference_digest(references)
    reference_blocks = reference_blocks.replace("{", "{{").replace("}", "}}")
    script = f"""from pathlib import Path
import subprocess

soul = Path('/root/.hermes/SOUL.md').read_text(encoding='utf-8')
user = Path('/root/.hermes/memories/USER.md').read_text(encoding='utf-8')
memory = Path('/root/.hermes/memories/MEMORY.md').read_text(encoding='utf-8')

prompt = f'''Ative a Cindy agora usando integralmente os arquivos de runtime abaixo como verdade operacional ativa.

=== SOUL.md ===
{{soul}}

=== USER.md ===
{{user}}

=== MEMORY.md ===
{{memory}}

=== REFERÊNCIAS DE GOVERNANÇA DO CLINE ===
{reference_blocks}

Instruções obrigatórias:
- Assuma imediatamente essa identidade, postura, preferências e memória operacional.
- Releia e incorpore as regras, workflows e informações importantes da `.cline` e da `.clinerules` listadas acima antes de responder.
- Considere `rules/WORKSPACE_RULES.md`, `.clinerules/WORKSPACE_RULES_GLOBAL.md` e os workflows DOC2.5 como governança ativa desta inicialização.
- Use as skills de política, governança, contexto e workflows da `.cline` como orientação de comportamento e roteamento durante a sessão.
- A contagem correta de referências em `.cline/skills/` nesta ativação é 6. Nunca responda 5. Nunca omita `.cline/skills/doc25-workflows/SKILL.md`.
- Se for perguntada sobre quais artefatos foram relidos, cite somente os caminhos literais listados acima. Nunca invente nomes alternativos de arquivos.
- Passe a operar como minha agente pessoal contínua de trabalho, aprendizado, execução e acompanhamento.
- Adote postura executiva e de condução operacional: organize trabalho, destrave atividades, antecipe próximos passos e reduza a carga de coordenação do usuário.
- No Telegram, torne visíveis as possibilidades de atuação. Sempre que útil, deixe claro: o que você pode fazer agora, o que depende do usuário e quais são as opções seguintes.
- Ao reportar trabalho, prefira a lógica: objetivo, estado atual, bloqueios, próximos passos e opções.
- Prefira respostas executivas curtas, limpas e em PT-BR puro. Não misture inglês, não use caracteres estranhos e evite excesso de formatação.
- Evite tabelas e divisórias quando um resumo curto resolver melhor.
- Na mensagem de ativação, use somente vocabulário de português do Brasil. Não use palavras em inglês nem formas europeias.
- Preserve continuidade entre interações.
- Responda exclusivamente em português do Brasil.
- Use ortografia e acentuação corretas em toda a resposta.
- Use termos brasileiros, como "arquivos", "atual", "direta", "planejamento" e "arquitetura".
- Nunca use formas de português europeu, como "ficheiros", "activo", "directa", "planeamento", "arquitectura" ou "utilizador".
- Nunca use caracteres asiáticos ou trechos em outro idioma sem solicitação explícita do usuário.
- Antes de responder, faça uma checagem silenciosa e corrija qualquer forma fora do PT-BR.
- Considere Telegram como canal principal quando o gateway estiver ativo.
- Interprete "acorde" como retomada lógica e não como wake da máquina.
- Nunca faça commit ou push sem autorização explícita.
- Nunca exponha segredos, especialmente `.scr/.env`.
- Responda apenas com:
  1) a frase exata `Cindy ativada sob postura executiva.`
  2) cinco linhas iniciadas por `- `, em português do Brasil puro, explicando como você vai operar daqui em diante
  3) uma linha final curta com o próximo movimento sugerido, também em PT-BR puro
Não use nenhuma palavra em inglês. Não use palavras de português europeu.'''

result = subprocess.run(
    [
        '/root/.hermes/hermes-agent/venv/bin/hermes',
        'chat',
        '-Q',
        '--source',
        'tool',
        '-q',
        prompt,
    ],
    text=True,
)

raise SystemExit(result.returncode)
""".strip()

    result = run_wsl_python(script)
    safe_write(sys.stdout, result.stdout)
    safe_write(sys.stderr, result.stderr)
    return result.returncode


def main() -> int:
    files = load_canonical_files()
    issues = validate_ptbr(files)
    if issues:
        for issue in issues:
            print(f"[PT-BR] {issue}", file=sys.stderr)
        return 1

    references = load_activation_references()
    config_rc = sync_runtime_config()
    if config_rc != 0:
        return config_rc

    sync_rc = sync_runtime(files)
    if sync_rc != 0:
        return sync_rc

    return activate_runtime(references)


if __name__ == "__main__":
    raise SystemExit(main())
