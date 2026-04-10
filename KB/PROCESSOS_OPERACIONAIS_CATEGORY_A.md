# Processos Operacionais — Category A (ThingsBoard CE)

**Sprint:** S3
**Item:** ST-S3-19
**Criado:** 2026-04-10

---

## Visão Geral

Category A abrange os domínios administrativos do ThingsBoard CE validados na Sprint S3. Este documento descreve o processo operacional padrão para cada domínio, incluindo workaround para gaps conhecidos.

**Host:** `http://204.168.202.5:8080`
**Autenticação:** JWT via `POST /api/auth/login`
**Perfil:** Tenant Administrator

---

## Processo 1 — Autenticação

### Obter JWT Token

```
POST /api/auth/login
Content-Type: application/json

{
  "username": "scaixeta@gmail.com",
  "password": "***"
}
```

**Resposta:**
```json
{
  "token": "<jwt_token>",
  "refreshToken": "<refresh_token>"
}
```

**Header para todas as chamadas subsequentes:**
```
X-Authorization: Bearer <jwt_token>
```

### Renovação de Token
```
POST /api/auth/refresh
X-Authorization: Bearer <refresh_token>
```

### Logout
```
POST /api/auth/logout
X-Authorization: Bearer <jwt_token>
```

---

## Processo 2 — Customers CRUD

### Create
```
POST /api/customer
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "title": "<nome_customer>",
  "email": "<email@cliente.com>"
}
```
**Retorno esperado:** HTTP 200 + JSON com `id`
**Gap:** Nenhum

### Read (lista)
```
GET /api/customers?pageSize=100&page=0
X-Authorization: Bearer <token>
```

### Read (individual)
```
GET /api/customer/{customerId}
X-Authorization: Bearer <token>
```

### Update
```
PUT /api/customer/{customerId}
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "title": "<novo_nome>",
  "email": "<novo_email@cliente.com>"
}
```
**Status:** HTTP 405 — GAP API CE
**Workaround:** Usar UI do ThingsBoard em `/api/customer?id=<customerId>`

### Delete
```
DELETE /api/customer/{customerId}
X-Authorization: Bearer <token>
```
**Retorno esperado:** HTTP 200

---

## Processo 3 — Customer Users CRUD

### Create
```
POST /api/user
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "email": "<usuario@cliente.com>",
  "firstName": "<nome>",
  "lastName": "<sobrenome>",
  "customerId": { "id": "<customerId>" }
}
```
**Status:** HTTP 500 — SMTP não configurado no ThingsBoard
**Workaround:** Criar via UI do ThingsBoard

### Read (lista de users de um customer)
```
GET /api/customer/{customerId}/users
X-Authorization: Bearer <token>
```

### Read (individual)
```
GET /api/user/{userId}
X-Authorization: Bearer <token>
```

### Update
```
PUT /api/user/{userId}
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "firstName": "<novo_nome>",
  "lastName": "<novo_sobrenome>"
}
```
**Status:** HTTP 405 — GAP API CE
**Workaround:** UI do ThingsBoard

### Delete
**Não disponível via REST.** Workaround: UI do ThingsBoard.

---

## Processo 4 — Users (Tenant Scope) CRUD

### Read (lista)
```
GET /api/users?pageSize=100&page=0
X-Authorization: Bearer <token>
```

### Read (individual)
```
GET /api/user/{userId}
X-Authorization: Bearer <token>
```

### Update
```
PUT /api/user/{userId}
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "firstName": "<novo_nome>"
}
```
**Status:** HTTP 405 — GAP API CE
**Workaround:** UI do ThingsBoard

### Delete
**Não disponível via REST.** Workaround: UI do ThingsBoard.

---

## Processo 5 — Devices

### Create
```
POST /api/device
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "name": "<nome_device>",
  "deviceProfileId": { "id": "<profileId>", "entityType": "DEVICE_PROFILE" },
  "type": "default"
}
```

### Read (lista — recomendado)
```
GET /api/tenant/deviceInfos?pageSize=100&page=0
X-Authorization: Bearer <token>
```

### Read (por deviceId)
```
GET /api/device/{deviceId}
X-Authorization: Bearer <token>
```

### Update
```
PUT /api/device
Content-Type: application/json
X-Authorization: Bearer <token>

{
  "id": { "id": "<deviceId>" },
  "name": "<novo_nome>",
  "type": "default"
}
```

### Delete
```
DELETE /api/device/{deviceId}
X-Authorization: Bearer <token>
```

### Obter Access Token
```
GET /api/device/{deviceId}/credentials
X-Authorization: Bearer <token>
```

---

## Processo 6 — Telemetria

### Enviar (Device Access Token)
```
POST /api/v1/{deviceToken}/telemetry
Content-Type: application/json

{
  "ts": 1646925123000,
  "values": {
    "temperature": 25.5,
    "humidity": 60.0
  }
}
```

### Consultar (JWT)
```
GET /api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries?keys=temperature,humidity&startTs=<inicio>&endTs=<fim>
X-Authorization: Bearer <token>
```

---

## Resumo de Gaps

| Operacao | Endpoint | HTTP | Workaround |
|----------|----------|------|-----------|
| Update Customer | PUT /api/customer/{id} | 405 | UI ThingsBoard |
| Update User | PUT /api/user/{id} | 405 | UI ThingsBoard |
| Create Customer User | POST /api/user | 500 | UI ThingsBoard |
| Delete User | DELETE /api/user/{id} | N/A | UI ThingsBoard |
| List Devices | GET /api/devices | 400 | GET /api/tenant/deviceInfos |

---

## Referências

- `KB/SwaggerTB.md` — referência completa de API REST
- `mcp-thingsboard/` — servidor MCP com tools para os domínios validados
- `integrators/n8n/` — workflows n8n de integração
- `knowledge/thingsboard/ce/runbooks/` — runbooks operacionais
