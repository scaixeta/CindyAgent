"""
API de testes FastAPI - Modulo principal
Autor: CindyAgent
Provedor: MiniMax M2.7 via OpenCode CLI
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, List, Optional
import uvicorn

app = FastAPI(title="API de Testes", version="1.0.0")

# Memoria para armazenar os registros
registros: List[dict] = []
proximo_id: int = 1


class RegistroEntrada(BaseModel):
    """Modelo de entrada para registro"""
    nome: str
    valor: Any


class RegistroSaida(BaseModel):
    """Modelo de saida para registro"""
    id: int
    nome: str
    valor: Any


@app.post("/registrar", response_model=RegistroSaida)
async def registrar(dados: RegistroEntrada):
    """
    Registra um novo item em memoria.
    Recebe: { "nome": str, "valor": any }
    Retorna: { "id": int, "nome": str, "valor": any }
    """
    global proximo_id
    registro = {
        "id": proximo_id,
        "nome": dados.nome,
        "valor": dados.valor
    }
    registros.append(registro)
    print(f"[LOG] Registro criado: id={proximo_id}, nome={dados.nome}")
    proximo_id += 1
    return registro


@app.get("/registros", response_model=List[RegistroSaida])
async def listar_registros():
    """
    Retorna todos os registros armazenados em memoria.
    """
    print(f"[LOG] Listando registros: total={len(registros)}")
    return registros


@app.delete("/encerrar")
async def encerrar():
    """
    Retorna relatorio final com todos os dados e limpa a memoria.
    """
    global registros, proximo_id
    relatorio = {
        "total_registros": len(registros),
        "registros": list(registros)
    }
    print(f"[LOG] Encerrando: {len(registros)} registros processados")
    # Limpa os dados
    registros = []
    proximo_id = 1
    return relatorio


if __name__ == "__main__":
    print("[INFO] Iniciando API de testes na porta 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
