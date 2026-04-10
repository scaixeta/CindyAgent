import subprocess
import sys
from textwrap import dedent


WSL_DISTRO = "Ubuntu"
WSL_USER = "root"


def run_wsl_python(script: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["wsl", "-d", WSL_DISTRO, "--user", WSL_USER, "--", "python3", "-"],
        input=script,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


def main() -> int:
    script = dedent(
        r'''
        from pathlib import Path
        import subprocess
        import sys

        soul = Path('/root/.hermes/SOUL.md').read_text(encoding='utf-8')
        user = Path('/root/.hermes/memories/USER.md').read_text(encoding='utf-8')
        memory = Path('/root/.hermes/memories/MEMORY.md').read_text(encoding='utf-8')

        prompt = f"""Ative a Cindy agora usando integralmente os arquivos de runtime abaixo como verdade operacional ativa.

        === SOUL.md ===
        {soul}

        === USER.md ===
        {user}

        === MEMORY.md ===
        {memory}

        Instrução:
        - Assuma imediatamente essa identidade, postura, preferências e memória operacional.
        - Passe a operar como minha agente pessoal contínua de trabalho, aprendizado, execução e acompanhamento.
        - Preserve continuidade entre interações.
        - Use pt-BR.
        - Considere Telegram como canal principal quando o gateway estiver ativo.
        - Interprete acorde como retomada lógica e não wake da máquina.
        - Nunca faça commit/push sem autorização explícita.
        - Nunca exponha segredos, especialmente .scr/.env.
        - Responda apenas com:
          1) confirmação de ativação da Cindy
          2) cinco bullets curtos explicando como você vai operar comigo daqui em diante."""

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
        '''
    ).strip()

    result = run_wsl_python(script)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())