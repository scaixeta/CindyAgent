#!/usr/bin/env python3
"""
opencode_executor.py — Integração com OpenCode como executor técnico dos especialistas

Executa tarefas técnicas via OpenCode usando perfis especializados por papel.
O OpenCode NÃO é o barramento do mesh — é apenas o executor de trabalho técnico.

Uso:
    from opencode.opencode_executor import OpenCodeExecutor
    executor = OpenCodeExecutor(profile="coder")
    result = executor.run(instruction="...", context="...", files=["..."])
"""

import subprocess
import json
import os
import tempfile
import logging
from pathlib import Path
from typing import Optional
from opencode.profiles import PROFILES, OpenCodeProfile

log = logging.getLogger("opencode.executor")

# Caminho do wrapper OpenCode no ambiente
OPENCODE_CMD_WIN = r"C:\CindyAgent\run_opencode.bat"
OPENCODE_CMD_WSL = "/mnt/c/CindyAgent/run_opencode.bat"
WORKSPACE_WIN    = r"C:\CindyAgent"
WORKSPACE_WSL    = "/mnt/c/CindyAgent"


class OpenCodeExecutor:
    """
    Executor de tarefas técnicas via OpenCode com perfil especializado.
    
    Cada chamada:
      1. Seleciona o perfil correto (regras, permissões, MCPs)
      2. Monta o prompt com instrução + contexto
      3. Executa o OpenCode headless
      4. Parseia e retorna o resultado estruturado
    """

    def __init__(self, profile: str = "coder", timeout: int = 300):
        if profile not in PROFILES:
            raise ValueError(f"Perfil desconhecido: '{profile}'. Disponíveis: {list(PROFILES.keys())}")
        self.profile_name = profile
        self.profile: OpenCodeProfile = PROFILES[profile]
        self.timeout = timeout
        log.info("[OpenCode] Executor iniciado com perfil=%s", profile)

    def run(
        self,
        instruction: str,
        context:     Optional[str] = None,
        files:       Optional[list[str]] = None,
        cwd:         Optional[str] = None,
    ) -> dict:
        """
        Executa uma instrução via OpenCode e retorna resultado estruturado.

        Returns:
            {
              "summary":      str,        # resumo do resultado
              "artifact_ref": str | None, # caminho do artefato gerado
              "failed":       bool,
              "output":       str,        # output bruto do OpenCode
            }
        """
        prompt = self._build_prompt(instruction, context, files)
        log.info("[OpenCode] profile=%s instruction=%s...", self.profile_name, instruction[:60])

        try:
            result = self._execute_opencode(prompt, cwd or WORKSPACE_WIN)
            return self._parse_result(result, instruction)
        except subprocess.TimeoutExpired:
            log.error("[OpenCode] Timeout após %ds para perfil=%s", self.timeout, self.profile_name)
            return {
                "summary":      f"OpenCode timeout após {self.timeout}s",
                "artifact_ref": None,
                "failed":       True,
                "output":       "",
            }
        except Exception as e:
            log.error("[OpenCode] Erro ao executar profile=%s: %s", self.profile_name, e, exc_info=True)
            return {
                "summary":      f"Erro no OpenCode: {e}",
                "artifact_ref": None,
                "failed":       True,
                "output":       str(e),
            }

    # ─── Internos ───────────────────────────────────────────────────

    def _build_prompt(self, instruction: str, context: Optional[str], files: Optional[list[str]]) -> str:
        parts = []

        # Injetando regras e restrições do perfil
        if self.profile.rules:
            parts.append(f"# Regras do perfil {self.profile_name}\n{self.profile.rules}\n")

        # Contexto do agente
        if context:
            parts.append(f"# Contexto\n{context}\n")

        # Arquivos relevantes
        if files:
            parts.append(f"# Arquivos alvo\n" + "\n".join(f"- {f}" for f in files) + "\n")

        # Instrução principal
        parts.append(f"# Instrução\n{instruction}")

        return "\n".join(parts)

    def _execute_opencode(self, prompt: str, cwd: str) -> str:
        """
        Executa OpenCode em modo headless com o prompt.
        
        Tenta:
          1. OpenCode CLI direto (se disponível no PATH)
          2. Via run_opencode.bat no Windows
          3. Simulação (quando OpenCode não está disponível — retorna placeholder)
        """
        # Grava prompt em arquivo temporário
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(prompt)
            prompt_file = f.name

        try:
            # Tenta OpenCode CLI
            cmd = self._build_command(prompt_file)
            proc = subprocess.run(
                cmd,
                shell      = True,
                cwd        = cwd,
                capture_output=True,
                text       = True,
                timeout    = self.timeout,
                encoding   = "utf-8",
                errors     = "replace",
            )
            return proc.stdout or proc.stderr or ""
        finally:
            try:
                os.unlink(prompt_file)
            except OSError:
                pass

    def _build_command(self, prompt_file: str) -> str:
        """Constrói o comando OpenCode correto para o ambiente."""
        # Tenta detectar opencode no PATH
        if os.path.exists(OPENCODE_CMD_WIN):
            return f'"{OPENCODE_CMD_WIN}" --model {self.profile.model} --prompt-file "{prompt_file}"'
        # Fallback: usa hermes chat como proxy (compatível com a API local 8642)
        return (
            f'wsl -d Ubuntu -u root -- bash -c '
            f'"hermes chat -Q --source opencode --model {self.profile.model} '
            f'-q \\"$(cat {prompt_file})\\" 2>&1"'
        )

    def _parse_result(self, raw_output: str, instruction: str) -> dict:
        """Parseia a saída do OpenCode e extrai informações estruturadas."""
        artifact_ref = self._extract_artifact_ref(raw_output)
        failed       = self._detect_failure(raw_output)
        summary      = self._extract_summary(raw_output, instruction)

        return {
            "summary":      summary,
            "artifact_ref": artifact_ref,
            "failed":       failed,
            "output":       raw_output[:3000],  # Limita para o ACP
        }

    def _extract_artifact_ref(self, output: str) -> Optional[str]:
        """Extrai caminhos de arquivo mencionados no output do OpenCode."""
        import re
        # Padrões comuns: "saved to X", "wrote X", "created X"
        patterns = [
            r'(?:saved?|wrote?|created?|output(?:ted)?) (?:to )?[`"]?([^\s`"]+\.\w+)[`"]?',
            r'File:\s*([^\s]+\.\w+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                candidate = match.group(1)
                if len(candidate) > 3 and "/" in candidate or "\\" in candidate or "." in candidate:
                    return candidate
        return None

    def _detect_failure(self, output: str) -> bool:
        failure_keywords = ["error:", "traceback", "failed:", "exception:", "could not", "not found"]
        lower = output.lower()
        return any(kw in lower for kw in failure_keywords)

    def _extract_summary(self, output: str, instruction: str) -> str:
        if not output.strip():
            return f"OpenCode executou: {instruction[:80]}"
        # Última linha não vazia como summary
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        return lines[-1][:200] if lines else output[:200]
