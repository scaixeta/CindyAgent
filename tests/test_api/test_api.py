"""
Testes para API de registros
Autor: CindyAgent
"""
import asyncio
import json
import httpx
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"
RESULTADO_FILE = Path(__file__).parent / "resultado_teste.json"


async def run_tests():
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10.0) as client:
        # 1. Registrar 3 itens
        itens = [
            {"nome": "item_teste_1", "valor": 100},
            {"nome": "item_teste_2", "valor": "texto qualquer"},
            {"nome": "item_teste_3", "valor": {"chave": "objeto"}},
        ]
        ids = []
        for item in itens:
            r = await client.post("/registrar", json=item)
            r.raise_for_status()
            dados = r.json()
            ids.append(dados["id"])
            print(f"[OK] Registrado id={dados['id']}, nome={dados['nome']}")

        # 2. Extrair todos via GET e validar 3 itens
        r = await client.get("/registros")
        r.raise_for_status()
        registros = r.json()
        assert len(registros) == 3, f"Esperado 3 registros, obtido {len(registros)}"
        print(f"[OK] GET /registros retornou {len(registros)} itens")

        # 3. Chamar DELETE /encerrar e validar contagem
        r = await client.delete("/encerrar")
        r.raise_for_status()
        relatorio = r.json()
        assert relatorio["total_registros"] == 3, f"Relatorio com contagem errada: {relatorio}"
        print(f"[OK] DELETE /encerrar - relatorio: {relatorio['total_registros']} registros")

    # 4. Montar evidencia
    resultado = {
        "sucesso": True,
        "testes": [
            {"nome": "registrar_3_itens", "status": "pass", "ids_registrados": ids},
            {"nome": "get_registros", "status": "pass", "quantidade": 3},
            {"nome": "delete_encerrar", "status": "pass", "total_relatorio": 3},
        ],
        "dados": {
            "itens_enviados": itens,
            "registros_retornados": registros,
            "relatorio_final": relatorio,
        },
    }

    with open(RESULTADO_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"[OK] Evidencia guardada em {RESULTADO_FILE}")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    return resultado


if __name__ == "__main__":
    asyncio.run(run_tests())
