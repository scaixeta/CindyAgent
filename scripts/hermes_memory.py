#!/usr/bin/env python3
"""
Hermes Redis Memory — Sentivis SIM
Camada de memória persistente em Redis para:
- Histórico de conversa
- Memória de contexto do projeto
- Estado da sessão activa
- Preferências do utilizador

Uso:
    python scripts/hermes_memory.py --op store_memory --key project_context --value "..."
    python scripts/hermes_memory.py --op get_memory --key project_context
    python scripts/hermes_memory.py --op append_conversation --role user --content "..."
    python scripts/hermes_memory.py --op get_conversation --limit 10
    python scripts/hermes_memory.py --op get_state
    python scripts/hermes_memory.py --op status
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REDIS_HOST = "localhost"
REDIS_PORT = 6379
TTL_SHORT = 1800    # 30 min — sessão
TTL_MEDIUM = 86400  # 1 dia — memória projeto
TTL_LONG = 604800   # 7 dias — histórico

PREFIX = "hermes"
SESSION_KEY = f"{PREFIX}:session:active"
MEMORY_KEY = f"{PREFIX}:memory"
CONVERSATION_KEY = f"{PREFIX}:conversation"
USER_KEY = f"{PREFIX}:user"


def get_redis():
    try:
        import redis
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=3, socket_connect_timeout=3)
    except Exception:
        return None


def redis_ok(conn) -> bool:
    if conn is None:
        return False
    try:
        conn.ping()
        return True
    except Exception:
        return False


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# --- SESSION ---

def store_session(conn, session_id: str, metadata: dict) -> bool:
    if conn is None:
        return False
    try:
        key = f"{SESSION_KEY}:{session_id}"
        conn.setex(key, TTL_SHORT, json.dumps({**metadata, "session_id": session_id, "updated_at": now_iso()}))
        # Session activa mais recente
        conn.setex(SESSION_KEY, TTL_SHORT, session_id)
        return True
    except Exception:
        return False


def get_active_session(conn) -> tuple[str | None, dict | None]:
    if conn is None:
        return None, None
    try:
        session_id = conn.get(SESSION_KEY)
        if session_id is None:
            return None, None
        session_id = session_id.decode() if isinstance(session_id, bytes) else session_id
        raw = conn.get(f"{SESSION_KEY}:{session_id}")
        if raw is None:
            return session_id, {}
        data = json.loads(raw)
        return session_id, data
    except Exception:
        return None, {}


def get_all_sessions(conn) -> list[str]:
    if conn is None:
        return []
    try:
        keys = conn.keys(f"{SESSION_KEY}:*")
        return [k.decode() if isinstance(k, bytes) else k for k in keys if k.decode() != SESSION_KEY]
    except Exception:
        return []


# --- PROJECT / CONTEXT MEMORY ---

def store_memory(conn, key: str, value: str, ttl: int = TTL_MEDIUM) -> bool:
    if conn is None:
        return False
    try:
        full_key = f"{MEMORY_KEY}:{key}"
        payload = json.dumps({
            "key": key,
            "value": value,
            "stored_at": now_iso(),
            "ttl_seconds": ttl
        })
        conn.setex(full_key, ttl, payload)
        return True
    except Exception:
        return False


def get_memory(conn, key: str) -> dict | None:
    if conn is None:
        return None
    try:
        raw = conn.get(f"{MEMORY_KEY}:{key}")
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def list_memories(conn) -> list[dict]:
    if conn is None:
        return []
    try:
        keys = conn.keys(f"{MEMORY_KEY}:*")
        result = []
        for k in keys:
            raw = conn.get(k)
            if raw:
                result.append(json.loads(raw))
        return result
    except Exception:
        return []


def delete_memory(conn, key: str) -> bool:
    if conn is None:
        return False
    try:
        conn.delete(f"{MEMORY_KEY}:{key}")
        return True
    except Exception:
        return False


# --- CONVERSATION HISTORY ---

def append_message(conn, role: str, content: str) -> bool:
    """Adiciona uma mensagem ao histórico da sessão activa."""
    if conn is None:
        return False
    try:
        session_id, _ = get_active_session(conn)
        if session_id is None:
            session_id = str(uuid.uuid4())
            store_session(conn, session_id, {"created_at": now_iso()})

        key = f"{CONVERSATION_KEY}:{session_id}"
        msg = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "ts": now_iso()
        }
        conn.rpush(key, json.dumps(msg, ensure_ascii=False))
        conn.expire(key, TTL_LONG)
        # Contador de mensagens
        conn.setex(f"{CONVERSATION_KEY}:{session_id}:count", TTL_LONG, conn.llen(key))
        return True
    except Exception:
        return False


def get_conversation(conn, session_id: str | None = None, limit: int = 20) -> list[dict]:
    if conn is None:
        return []
    try:
        if session_id is None:
            session_id, _ = get_active_session(conn)
        if session_id is None:
            return []
        key = f"{CONVERSATION_KEY}:{session_id}"
        raw_list = conn.lrange(key, -limit, -1)
        return [json.loads(m) for m in raw_list]
    except Exception:
        return []


def get_full_conversation(conn, session_id: str | None = None) -> list[dict]:
    if conn is None:
        return []
    try:
        if session_id is None:
            session_id, _ = get_active_session(conn)
        if session_id is None:
            return []
        key = f"{CONVERSATION_KEY}:{session_id}"
        raw_list = conn.lrange(key, 0, -1)
        return [json.loads(m) for m in raw_list]
    except Exception:
        return []


def clear_conversation(conn, session_id: str | None = None) -> bool:
    if conn is None:
        return False
    try:
        if session_id is None:
            session_id, _ = get_active_session(conn)
        if session_id is None:
            return False
        key = f"{CONVERSATION_KEY}:{session_id}"
        conn.delete(key)
        conn.delete(f"{CONVERSATION_KEY}:{session_id}:count")
        return True
    except Exception:
        return False


def search_conversation(conn, query: str, session_id: str | None = None) -> list[dict]:
    """Busca mensagens que contenham a query."""
    if conn is None:
        return []
    msgs = get_conversation(conn, session_id, limit=500)
    return [m for m in msgs if query.lower() in m.get("content", "").lower()]


# --- USER PREFERENCES ---

def store_user_pref(conn, user_id: str, key: str, value: str) -> bool:
    if conn is None:
        return False
    try:
        full_key = f"{USER_KEY}:{user_id}:{key}"
        conn.setex(full_key, TTL_MEDIUM, json.dumps({"key": key, "value": value, "updated_at": now_iso()}))
        return True
    except Exception:
        return False


def get_user_pref(conn, user_id: str, key: str) -> dict | None:
    if conn is None:
        return None
    try:
        raw = conn.get(f"{USER_KEY}:{user_id}:{key}")
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def list_user_prefs(conn, user_id: str) -> list[dict]:
    if conn is None:
        return []
    try:
        pattern = f"{USER_KEY}:{user_id}:*"
        keys = conn.keys(pattern)
        result = []
        for k in keys:
            raw = conn.get(k)
            if raw:
                result.append(json.loads(raw))
        return result
    except Exception:
        return []


# --- STATUS ---

def status(conn) -> dict:
    if not redis_ok(conn):
        return {
            "redis": "indisponivel",
            "modo": "degradado — toda a memória fica em memória Python local"
        }
    try:
        info = conn.info("server")
        session_id, session_data = get_active_session(conn)
        memories = list_memories(conn)
        total_sessions = len(get_all_sessions(conn))
        return {
            "redis": "activo",
            "version": info.get("redis_version", "?"),
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "active_session": session_id,
            "session_data": session_data,
            "total_sessions": total_sessions,
            "stored_memories": len(memories),
            "memories": memories,
        }
    except Exception as e:
        return {"redis": f"erro: {e}"}


# --- MAIN CLI ---

def main():
    parser = argparse.ArgumentParser(description="Hermes Redis Memory")
    parser.add_argument("--op", required=True,
                        choices=["status", "store_memory", "get_memory", "list_memories",
                                 "delete_memory", "append_conversation", "get_conversation",
                                 "get_full_conversation", "clear_conversation", "search_conversation",
                                 "store_session", "get_state", "store_user_pref", "get_user_pref"])
    parser.add_argument("--key", help="Chave da memória")
    parser.add_argument("--value", help="Valor da memória")
    parser.add_argument("--ttl", type=int, default=TTL_MEDIUM, help="TTL em segundos")
    parser.add_argument("--role", help="Papel na conversa (user/assistant/system)")
    parser.add_argument("--content", help="Conteúdo da mensagem")
    parser.add_argument("--session", help="ID da sessão")
    parser.add_argument("--limit", type=int, default=20, help="Limite de mensagens")
    parser.add_argument("--query", help="Query de busca")
    parser.add_argument("--user", default="sentivis_ai", help="ID do utilizador")
    args = parser.parse_args()

    conn = get_redis()

    if args.op == "status":
        st = status(conn)
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return

    if not redis_ok(conn):
        print("Redis indisponivel — modo degradado activo", file=sys.stderr)
        sys.exit(1)

    if args.op == "store_memory":
        if not args.key or not args.value:
            print("--key e --value são obrigatórios", file=sys.stderr)
            sys.exit(1)
        ok = store_memory(conn, args.key, args.value, args.ttl)
        print(f"Memoria '{args.key}': {'OK' if ok else 'FALHOU'}")

    elif args.op == "get_memory":
        if not args.key:
            print("--key é obrigatório", file=sys.stderr)
            sys.exit(1)
        result = get_memory(conn, args.key)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Chave '{args.key}' não encontrada")

    elif args.op == "list_memories":
        mems = list_memories(conn)
        print(f"Memórias guardadas: {len(mems)}")
        for m in mems:
            print(f"  [{m['key']}] {m['stored_at']}")

    elif args.op == "delete_memory":
        if not args.key:
            print("--key é obrigatório", file=sys.stderr)
            sys.exit(1)
        ok = delete_memory(conn, args.key)
        print(f"Apagar '{args.key}': {'OK' if ok else 'FALHOU'}")

    elif args.op == "store_session":
        if not args.session:
            print("--session é obrigatório", file=sys.stderr)
            sys.exit(1)
        meta = json.loads(args.value) if args.value else {}
        ok = store_session(conn, args.session, meta)
        print(f"Sessão '{args.session}': {'OK' if ok else 'FALHOU'}")

    elif args.op == "get_state":
        sid, data = get_active_session(conn)
        print(f"Sessão activa: {sid}")
        print(json.dumps(data, indent=2, ensure_ascii=False) if data else "Nenhuma sessão activa")

    elif args.op == "append_conversation":
        if not args.role or not args.content:
            print("--role e --content são obrigatórios", file=sys.stderr)
            sys.exit(1)
        ok = append_message(conn, args.role, args.content)
        print(f"Mensagem [{args.role}]: {'OK' if ok else 'FALHOU'}")

    elif args.op == "get_conversation":
        msgs = get_conversation(conn, args.session, args.limit)
        print(f"Mensagens ({len(msgs)}):")
        for m in msgs:
            print(f"  [{m['role']}] {m['ts']}: {m['content'][:80]}")

    elif args.op == "get_full_conversation":
        msgs = get_full_conversation(conn, args.session)
        print(f"Mensagens ({len(msgs)}):")
        for m in msgs:
            print(f"  [{m['role']}] {m['ts']}: {m['content'][:100]}")

    elif args.op == "clear_conversation":
        ok = clear_conversation(conn, args.session)
        print(f"Limpar conversa: {'OK' if ok else 'FALHOU'}")

    elif args.op == "search_conversation":
        if not args.query:
            print("--query é obrigatório", file=sys.stderr)
            sys.exit(1)
        msgs = search_conversation(conn, args.query, args.session)
        print(f"Resultados para '{args.query}': {len(msgs)}")
        for m in msgs:
            print(f"  [{m['role']}] {m['ts']}: {m['content'][:120]}")

    elif args.op == "store_user_pref":
        if not args.key or not args.value:
            print("--key e --value são obrigatórios", file=sys.stderr)
            sys.exit(1)
        ok = store_user_pref(conn, args.user, args.key, args.value)
        print(f"Pref '{args.key}': {'OK' if ok else 'FALHOU'}")

    elif args.op == "get_user_pref":
        if not args.key:
            print("--key é obrigatório", file=sys.stderr)
            sys.exit(1)
        result = get_user_pref(conn, args.user, args.key)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Pref '{args.key}' não encontrada")


if __name__ == "__main__":
    main()
