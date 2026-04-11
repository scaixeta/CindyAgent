#!/usr/bin/env python3
"""
S5 Redis Operational Memory — Sentivis IAOps

Camada mínima de memória operacional com Redis.
Valida se Redis melhora o state persistence de curto prazo
para o workflow de microclima.

Uso:
    python scripts/s5_redis_memory.py --mode check|write|read|window|compare
"""

import argparse
import json
import sys
from datetime import datetime, timezone
import socket

REDIS_HOST = "localhost"
REDIS_PORT = 6379
DEVICE = "NIMBUS-AERO"
TTL_SECONDS = 3600

KEY_LATEST = f"microclimate:{DEVICE}:latest"
KEY_WINDOW = f"microclimate:{DEVICE}:window"
KEY_MEMORY = f"microclimate:{DEVICE}:memory_state"


def get_redis_conn():
    """Ligar ao Redis. Retorna None se indisponível."""
    try:
        import redis
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=3, socket_connect_timeout=3)
    except Exception:
        return None


def redis_ok(conn) -> bool:
    """Verifica se a ligação ao Redis está activa."""
    if conn is None:
        return False
    try:
        conn.ping()
        return True
    except Exception:
        return False


def write_latest_state(conn, state: dict) -> bool:
    """Escreve latest state snapshot para Redis."""
    if conn is None:
        return False
    try:
        conn.setex(KEY_LATEST, TTL_SECONDS, json.dumps(state, ensure_ascii=False))
        return True
    except Exception:
        return False


def read_latest_state(conn) -> dict | None:
    """Lê latest state do Redis."""
    if conn is None:
        return None
    try:
        raw = conn.get(KEY_LATEST)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def write_window(conn, records: list[dict], max_size: int = 20) -> bool:
    """Escreve rolling window de registros no Redis."""
    if conn is None:
        return False
    try:
        # Mantém apenas os últimos max_size registos
        window = json.dumps(records[-max_size:], ensure_ascii=False)
        conn.setex(KEY_WINDOW, TTL_SECONDS, window)
        return True
    except Exception:
        return False


def read_window(conn) -> list[dict] | None:
    """Lê rolling window do Redis."""
    if conn is None:
        return None
    try:
        raw = conn.get(KEY_WINDOW)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def write_memory_state(conn, marker: str, value: dict) -> bool:
    """Escreve estado de processamento/memória operacional."""
    if conn is None:
        return False
    try:
        key = f"{KEY_MEMORY}:{marker}"
        conn.setex(key, TTL_SECONDS * 2, json.dumps(value, ensure_ascii=False))
        return True
    except Exception:
        return False


def read_memory_state(conn, marker: str) -> dict | None:
    """Lê estado operacional guardado."""
    if conn is None:
        return None
    try:
        key = f"{KEY_MEMORY}:{marker}"
        raw = conn.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def check_redis() -> dict:
    """Verifica disponibilidade e configuração do Redis."""
    conn = get_redis_conn()
    ok = redis_ok(conn)
    result = {"redis_disponivel": ok, "host": REDIS_HOST, "port": REDIS_PORT}
    if ok:
        info = conn.info("server")
        result["redis_version"] = info.get("redis_version", "desconhecida")
        result["os"] = info.get("os", "desconhecido")
    return result


def run_check():
    """Modo check: verifica Redis."""
    status = check_redis()
    print(f"Redis disponível: {status['redis_disponivel']}")
    if status["redis_disponivel"]:
        print(f"Version: {status['redis_version']}")
        print(f"Host: {status['host']}:{status['port']}")
    else:
        print("Redis não disponível — modo degradado activo")
    return status


def run_write_sample(conn, records: list[dict]):
    """Escreve estado actual para Redis."""
    if conn is None:
        print("Redis indisponível — sem escrita")
        return False

    # Latest state
    latest = records[-1] if records else {}
    latest_ok = write_latest_state(conn, latest)
    print(f"Latest state: {'OK' if latest_ok else 'FALHOU'}")

    # Window
    window_ok = write_window(conn, records)
    print(f"Rolling window: {'OK' if window_ok else 'FALHOU'}")

    # Memory state
    mem_state = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "records_count": len(records),
    }
    mem_ok = write_memory_state(conn, "last_run", mem_state)
    print(f"Memory state: {'OK' if mem_ok else 'FALHOU'}")

    return latest_ok and window_ok and mem_ok


def run_read_sample(conn):
    """Lê e mostra estado do Redis."""
    latest = read_latest_state(conn)
    window = read_window(conn)
    mem = read_memory_state(conn, "last_run")

    print("\n--- Estado no Redis ---")
    print(f"Latest: {latest}")
    print(f"Window ({len(window) if window else 0} registos): {window[-3:] if window else None}")
    print(f"Memory: {mem}")
    return latest, window, mem


def run_compare(records: list[dict]):
    """Compara estado com e sem Redis."""
    conn = get_redis_conn()
    print("\n=== COMPARAÇÃO DE ESTADO ===")
    print(f"Registos locais: {len(records)} ponto(s)")
    print(f"Último: {records[-1] if records else 'nenhum'}")

    if redis_ok(conn):
        latest = read_latest_state(conn)
        window = read_window(conn)
        mem = read_memory_state(conn, "last_run")
        print(f"\nCom Redis:")
        print(f"  Latest: {latest}")
        print(f"  Window: {len(window) if window else 0} registos")
        print(f"  Memory: {mem}")
        print("\nMelhoria: Redis permite recall de estado entre execuções.")
        print("         Sem Redis, cada execução começa do zero.")
    else:
        print("\nSem Redis: cada execução é stateless.")
        print("          Não há melhoria sem Redis activo.")


def parse_minimal_records() -> list[dict]:
    """Lê os 12 pontos do collection_log.txt da S4."""
    log_path = "artifacts/s4-cirrus/2026-04-10/collection_log.txt"
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    records = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "Timestamp UTC" in line or "---" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        try:
            num = parts[1].strip()
            if not num.isdigit():
                continue
            records.append({
                "iter": int(num),
                "ts": parts[2].strip(),
                "temperature_c": float(parts[3].strip()),
                "humidity_pct": float(parts[4].strip()),
            })
        except (ValueError, IndexError):
            continue
    return records


def main():
    parser = argparse.ArgumentParser(description="S5 Redis Operational Memory")
    parser.add_argument("--mode", default="check",
                        choices=["check", "write", "read", "window", "compare"])
    args = parser.parse_args()

    print(f"[S5 Redis] Modo: {args.mode}")
    print(f"[S5 Redis] Início: {datetime.now(timezone.utc).isoformat()}")

    if args.mode == "check":
        run_check()
        return

    conn = get_redis_conn()

    if args.mode == "compare":
        records = parse_minimal_records()
        run_compare(records)
        return

    if args.mode == "write":
        records = parse_minimal_records()
        if not records:
            print("Erro: nenhum registo encontrado")
            sys.exit(1)
        ok = run_write_sample(conn, records)
        print(f"\nEscrita Redis: {'SUCESSO' if ok else 'MODO DEGRADADO'}")
        sys.exit(0 if ok else 1)

    if args.mode == "read":
        if not redis_ok(conn):
            print("Redis indisponível")
            sys.exit(1)
        run_read_sample(conn)
        return

    if args.mode == "window":
        records = parse_minimal_records()
        if not records:
            print("Erro: nenhum registo encontrado")
            sys.exit(1)
        if not redis_ok(conn):
            print("Redis indisponível — saltando teste de janela")
            sys.exit(1)
        write_window(conn, records)
        window = read_window(conn)
        print(f"Janela guardada: {len(window)} registos")
        print(f"Últimos 3: {window[-3:] if window else None}")
        sys.exit(0)


if __name__ == "__main__":
    main()
