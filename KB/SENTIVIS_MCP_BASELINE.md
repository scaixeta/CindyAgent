# Baseline SentivisMCP — Mapeamento CRUD Domains

**Sprint:** S3
**Item:** ST-S3-20
**Criado:** 2026-04-10

---

## Visão Geral

Baseline que documenta o estado atual do servidor MCP ThingsBoard (`mcp-thingsboard/`) e o mapeamento completo dos domínios CRUD validados na Sprint S3. Este documento serve como referência para evolução do MCP e para o roadmap de replicação DOC2.5.

**Host ThingsBoard:** `http://204.168.202.5:8080`
**MCP Server:** `mcp-thingsboard/` (Node.js, TypeScript, stdio transport)
**Path:** `C:\01 - Sentivis\Sentivis SIM\mcp-thingsboard`

---

## Arquitetura do MCP

```
mcp-thingsboard/
├── src/
│   ├── index.ts        — servidor MCP (stdio transport)
│   ├── tb-api.ts       — client HTTP ThingsBoard API
│   └── debug-users.ts  — utilitário de debug
├── dist/               — build TypeScript → JS
├── package.json
└── README.md
```

### Transporte
- stdio (Server-Sent Events over stdin/stdout)
- IDEs compatíveis: Cline, VS Code, Gemini CLI

### Build
```bash
npm run build    # tsc
npm start        # node dist/index.js
npm run dev      # ts-node src/index.ts
```

---

## Tools Disponíveis (MCP)

### list_customers
Lista customers do tenant.
```json
{ "pageSize": 100, "page": 0 }
```

### list_devices
Lista todos os dispositivos do tenant.
```json
{ "pageSize": 100, "page": 0, "type": "default" }
```

### list_customer_devices
Lista dispositivos de um customer específico.
```json
{ "customerId": "<uuid>", "pageSize": 100, "page": 0 }
```

### list_users
Lista usuários (responsáveis) do tenant.
```json
{ "pageSize": 100, "page": 0 }
```

---

## Mapeamento CRUD Domains

### Auth
| Operacao | Via MCP | Via REST | Status |
|----------|---------|----------|--------|
| Login (JWT) | Nao | POST /api/auth/login | Validado |
| Refresh token | Nao | POST /api/auth/refresh | Nao validado |
| Logout | Nao | POST /api/auth/logout | Nao validado |

### Customers
| CRUD | Via MCP | Via REST | Status |
|------|---------|----------|--------|
| Create | Nao | POST /api/customer | Validado |
| Read (list) | list_customers | GET /api/customers | Validado |
| Read (id) | Nao | GET /api/customer/{id} | Validado |
| Update | Nao | PUT /api/customer/{id} | **405 GAP** |
| Delete | Nao | DELETE /api/customer/{id} | Validado |

### Devices
| CRUD | Via MCP | Via REST | Status |
|------|---------|----------|--------|
| Create | Nao | POST /api/device | Validado |
| Read (list) | list_devices | GET /api/tenant/deviceInfos | Validado |
| Read (id) | Nao | GET /api/device/{id} | Validado |
| Update | Nao | PUT /api/device | Validado |
| Delete | Nao | DELETE /api/device/{id} | Validado |
| Get credentials | Nao | GET /api/device/{id}/credentials | Validado |

### Customer Devices
| CRUD | Via MCP | Via REST | Status |
|------|---------|----------|--------|
| Read (list) | list_customer_devices | GET /api/customer/{id}/devices | Validado |

### Users (Tenant)
| CRUD | Via MCP | Via REST | Status |
|------|---------|----------|--------|
| Create | Nao | POST /api/user | **500 GAP** |
| Read (list) | list_users | GET /api/users | Validado |
| Read (id) | Nao | GET /api/user/{id} | Validado |
| Update | Nao | PUT /api/user/{id} | **405 GAP** |
| Delete | Nao | DELETE /api/user/{id} | Nao disponivel |

### Telemetry
| Operacao | Via MCP | Via REST | Status |
|----------|---------|----------|--------|
| Enviar (device token) | Nao | POST /api/v1/{token}/telemetry | Validado |
| Consultar (JWT) | Nao | GET /api/plugins/telemetry/DEVICE/{id}/values/timeseries | Validado |

### Device Profiles
| CRUD | Via MCP | Via REST | Status |
|------|---------|----------|--------|
| Read (list) | Nao | GET /api/deviceProfiles | Validado |
| Read (id) | Nao | GET /api/deviceProfile/{id} | Validado |
| Create | Nao | POST /api/deviceProfile | Nao validado |

---

## Gaps do MCP Atual

1. **Sem tool de auth** — o MCP não expõe login JWT; relies on external token management
2. **Sem create/update/delete** — only read operations (list_*)
3. **Sem telemetry** — não expõe envio ou consulta de telemetria
4. **Sem asset management** — não há tool para assets
5. **Sem RPC** — não expõe chamada remota a devices

---

## Dependências

- `../.scr/.env` com `TB_URL`, `TB_USERNAME`, `TB_PASSWORD`
- Node.js >= 18
- TypeScript e ts-node (dev)
- Pacotes: `@modelcontextprotocol/sdk`, `axios`

---

## Integração com IDEs

### Cline / VS Code MCP
```json
{
  "mcpServers": {
    "thingsboard": {
      "command": "node",
      "args": ["c:/01 - Sentivis/Sentivis SIM/mcp-thingsboard/dist/index.js"],
      "env": {}
    }
  }
}
```

---

## Roadmap Sugerido

### Fase 1 — Estável (atual)
- Manter as 4 tools de leitura (list_customers, list_devices, list_customer_devices, list_users)
- Build e dist funcionando

### Fase 2 — Completude CRUD
- Adicionar tool de create para Customers e Devices
- Adicionar tool de delete para Devices
- Adicionar tool de auth (login/refresh)

### Fase 3 — Telemetria
- Adicionar tool de envio de telemetry
- Adicionar tool de consulta de timeseries

### Fase 4 — Assets e RPC
- Adicionar tool de assets
- Adicionar tool de RPC (two-way, one-way)

---

## Referências

- `KB/SwaggerTB.md` — referência completa da API REST
- `docs/PROCESSOS_OPERACIONAIS_CATEGORY_A.md` — processos operacionais Category A
- `mcp-thingsboard/README.md` — README do servidor MCP
- `knowledge/thingsboard/ce/runbooks/` — runbooks operacionais
