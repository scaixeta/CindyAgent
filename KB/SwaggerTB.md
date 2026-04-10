# Swagger ThingsBoard CE - Referência de API REST

## Visão Geral

Este documento descreve os principais endpoints da API REST do ThingsBoard CE disponíveis em `http://204.168.202.5:8080/swagger-ui/index.html`.

**Base URL**: `http://204.168.202.5:8080`

**Host validado**: `204.168.202.5:8080` (Sprint S3 — TEST-S3-16)

**Autenticação**: JWT Token (Bearer) ou Device Access Token

---

## Category A - Domínios Administrativos

> Validado na Sprint S3 via TEST-S3-16 (curl real).

| Domínio | Create | Read | Update | Delete | Notas |
|---------|--------|-------|--------|--------|-------|
| **Auth** | POST /api/auth/login | — | — | — | JWT OK |
| **Tenant Admin scope** | — | GET /api/customers, /api/users | — | — | Escopo confirmado |
| **Tenants CRUD** | HTTP 403 | HTTP 403 | HTTP 403 | HTTP 403 | Fora do escopo TENANT_ADMIN |
| **Customers CRUD** | POST /api/customer | GET /api/customers, GET /api/customer/{id} | HTTP 405 | DELETE /api/customer/{id} | Update=405 (gap API CE) |
| **Customer Users CRUD** | HTTP 500 (SMTP) | GET /api/customer/{id}/users | HTTP 405 | — | SMTP não configurado |
| **Users CRUD** | — | GET /api/users, GET /api/user/{id} | HTTP 405 | — | Update=405 (gap API CE) |

### Gaps Consolidados (Category A)

| Gap | Endpoint | HTTP | Classificação | Workaround |
|-----|----------|------|--------------|------------|
| Update Customer | `PUT /api/customer/{id}` | 405 | Gap API REST CE | UI do ThingsBoard |
| Update User | `PUT /api/user/{id}` | 405 | Gap API REST CE | UI do ThingsBoard |
| Create Customer User | `POST /api/user` + customerId | 500 | Configuração TB (SMTP) | UI do ThingsBoard |
| List Devices | `GET /api/devices` | 400 | Parâmetro obrigatório (deviceIds) | `GET /api/tenant/deviceInfos` |
| Tenants API | `GET/POST /api/tenants` | 403 | Perfil TENANT_ADMIN | N/A (restrição de escopo) |

### Leitura operacional por domínio

- **Auth**: primeiro passo para qualquer validação. `POST /api/auth/login` confirmou JWT funcional no host `204.168.202.5`.
- **Tenant Admin scope**: leitura de `customers` e `users` está habilitada; `tenants` permanece fora do escopo do perfil.
- **Customers**: `create`, `read` e `delete` estão validados; `update` via `PUT` retorna `405`, então o workaround prático é a UI do ThingsBoard.
- **Customer Users**: `read` via `GET /api/customer/{id}/users` está validado; `create` depende de SMTP e `update/delete` não ficaram disponíveis como fluxo REST efetivo nesta versão.
- **Users**: leitura por `GET /api/users` e `GET /api/user/{id}` está validada; `PUT /api/user/{id}` retorna `405`.
- **Devices**: `GET /api/devices` exige `deviceIds`; para listagem operacional use `GET /api/tenant/deviceInfos`.

### Referências operacionais

- `knowledge/thingsboard/ce/manifests/topic_index.md`
- `knowledge/thingsboard/ce/runbooks/rest-api-auth.md`
- `knowledge/thingsboard/ce/runbooks/check-device-token.md`
- `knowledge/thingsboard/ce/runbooks/troubleshooting-ingestion.md`

---

## Autenticação

### Login (Obter JWT Token)


```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "scaixeta@gmail.com",
  "password": "<senha>"
}
```

**Resposta**:
```json
{
  "token": "<jwt_token>",
  "refreshToken": "<refresh_token>"
}
```

**Headers subsequentes**:
```
X-Authorization: Bearer <jwt_token>
```

---

## Devices (Dispositivos)

### Listar Dispositivos

```http
GET /api/devices?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

**Parâmetros Query**:
- `pageSize`: número de items por página
- `page`: número da página (0-indexed)
- `textSearch`: busca por nome
- `sortProperty`: propriedade para ordenação
- `sortOrder`: ASC ou DESC

### Criar Device

```http
POST /api/device
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "name": "Sentivis | 0001",
  "deviceProfileId": {
    "id": "<device_profile_id>",
    "entityType": "DEVICE_PROFILE"
  },
  "type": "default"
}
```

### Obter Device por ID

```http
GET /api/device/{deviceId}
X-Authorization: Bearer <jwt_token>
```

### Atualizar Device

```http
PUT /api/device
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "id": {"id": "<deviceId>"},
  "name": "Novo Nome",
  "type": "default"
}
```

### Deletar Device

```http
DELETE /api/device/{deviceId}
X-Authorization: Bearer <jwt_token>
```

### Buscar Device por Nome

```http
GET /api/tenant/devices?textSearch=<nome>
X-Authorization: Bearer <jwt_token>
```

---

## Telemetria

### Enviar Telemetria (Device API - Access Token)

```http
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

**Notas**:
- `ts`: timestamp em milissegundos (opcional, se omitido usa timestamp atual)
- `values`: objeto com pares key-value

**Formato alternativo**:
```json
{
  "temperature": 25.5,
  "humidity": 60.0,
  "ts": 1646925123000
}
```

### Consultar Telemetria (com JWT)

```http
GET /api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries?keys=temperature,humidity&startTs=1646925123000&endTs=1647011523000
X-Authorization: Bearer <jwt_token>
```

**Parâmetros Query**:
- `keys`: keys separadas por vírgula
- `startTs`: timestamp inicial em milissegundos
- `endTs`: timestamp final em milissegundos
- `interval`: intervalo de agregação em milissegundos
- `limit`: limite de registros
- `agg`: tipo de agregação (MIN, MAX, AVG, SUM, COUNT, NONE)

**Resposta**:
```json
{
  "temperature": [
    {"ts": 1646925123000, "value": "25.5"},
    {"ts": 1646926000000, "value": "26.0"}
  ],
  "humidity": [
    {"ts": 1646925123000, "value": "60.0"},
    {"ts": 1646926000000, "value": "59.5"}
  ]
}
```

---

## Atributos

### Enviar Atributos do Device (Device API - Access Token)

```http
POST /api/v1/{deviceToken}/attributes
Content-Type: application/json

{
  "shared": {
    "firmware_version": "1.0.0",
    "location": "sala"
  },
  "client": {
    "connection_status": "connected"
  }
}
```

### Consultar Atributos (com JWT)

```http
GET /api/plugins/telemetry/DEVICE/{deviceId}/values/attributes?keys=firmware_version,location&types=SHARED_SCOPE
X-Authorization: Bearer <jwt_token>
```

**Parâmetros Query**:
- `keys`: keys separadas por vírgula
- `types`: SHARED_SCOPE, CLIENT_SCOPE, SERVER_SCOPE

### Atributos do Lado Servidor

```http
GET /api/plugins/telemetry/DEVICE/{deviceId}/values/attributes?keys=<keys>&types=SERVER_SCOPE
X-Authorization: Bearer <jwt_token>
```

---

## Device Credentials

### Obter Credentials do Device

```http
GET /api/device/{deviceId}/credentials
X-Authorization: Bearer <jwt_token>
```

### Atualizar Credentials do Device

```http
POST /api/device/{deviceId}/credentials
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "credentialsType": "ACCESS_TOKEN",
  "credentialsId": "<device_access_token>",
  "credentialsValue": "<novo_token>"
}
```

### Criar Access Token

```http
POST /api/device/{deviceId}/credentials
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "credentialsType": "ACCESS_TOKEN"
}
```

**Resposta**:
```json
{
  "credentialsId": "<access_token>",
  "credentialsType": "ACCESS_TOKEN"
}
```

---

## Device Profiles

### Listar Device Profiles

```http
GET /api/deviceProfiles?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Obter Device Profile por ID

```http
GET /api/deviceProfile/{deviceProfileId}
X-Authorization: Bearer <jwt_token>
```

### Criar Device Profile

```http
POST /api/deviceProfile
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "name": "Default Profile",
  "type": "DEFAULT",
  "transportType": "DEFAULT",
  "provisioningStrategy": "CHECK_PROVISIONING_RESPONSE",
  "profileData": {
    "configuration": {
      "type": "DEFAULT"
    },
    "transportConfiguration": {
      "type": "DEFAULT"
    }
  }
}
```

---

## Dashboards

### Listar Dashboards

```http
GET /api/dashboards?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Obter Dashboard por ID

```http
GET /api/dashboard/{dashboardId}
X-Authorization: Bearer <jwt_token>
```

### Criar Dashboard

```http
POST /api/dashboard
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "title": "Meu Dashboard",
  "configuration": {}
}
```

### Atualizar Dashboard

```http
PUT /api/dashboard
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "id": {"id": "<dashboardId>"},
  "title": "Dashboard Atualizado"
}
```

---

## Assets

### Listar Assets

```http
GET /api/assets?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar Asset

```http
POST /api/asset
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "name": "Asset 1",
  "type": "default"
}
```

### Associar Device a Asset

```http
POST /api/relations
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "from": {"id": "<assetId>", "entityType": "ASSET"},
  "to": {"id": "<deviceId>", "entityType": "DEVICE"},
  "type": "Contains"
}
```

---

## Customers

### Listar Customers

```http
GET /api/customers?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar Customer

```http
POST /api/customer
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "title": "Customer 1",
  "email": "cliente@exemplo.com"
}
```

---

## RPC (Remote Procedure Call)

### Enviar RPC para Device (Two-Way)

```http
POST /api/plugins/rpc/twoway/{deviceId}
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "method": "getTime",
  "params": {},
  "timeout": 5000
}
```

### Enviar RPC para Device (One-Way)

```http
POST /api/plugins/rpc/oneway/{deviceId}
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "method": "sendNotification",
  "params": {"message": "Alerta!"}
}
```

---

## Rule Engine

### Listar Rules

```http
GET /api/rules?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar Rule

```http
POST /api/rule
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "name": "Nova Rule",
  "processorType": "JS",
  "type": "org.thingsboard.server.common.msg.queue.RuleEngineProcessor"
}
```

---

## Alarms

### Listar Alarms

```http
GET /api/alarms?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar Alarm

```http
POST /api/alarm
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "type": "HIGH_TEMPERATURE",
  "severity": "CRITICAL",
  "status": "ACTIVE",
  "entityType": "DEVICE",
  "entityId": "<deviceId>",
  "assignee": {
    "entityType": "USER",
    "id": "<userId>"
  }
}
```

### Consultar Alarms por Device

```http
GET /api/alarm/entity/{entityType}/{entityId}?status=ACTIVE&severity=CRITICAL
X-Authorization: Bearer <jwt_token>
```

---

## Users

### Listar Users

```http
GET /api/users?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar User

```http
POST /api/user
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "email": "usuario@exemplo.com",
  "firstName": "Nome",
  "lastName": "Sobrenome",
  "authority": "TENANT_ADMIN"
}
```

---

## Webhooks

### Listar Webhooks

```http
GET /api/webhooks?pageSize=100&page=0
X-Authorization: Bearer <jwt_token>
```

### Criar Webhook

```http
POST /api/webhook
Content-Type: application/json
X-Authorization: Bearer <jwt_token>

{
  "name": "Meu Webhook",
  "url": "https://exemplo.com/webhook",
  "enabled": true,
  "type": "WEBHOOK"
}
```

---

## OTA Updates

### Listar Firmwares

```http
GET /api/ota/packages?pageSize=100&page=0&type=DEVICE
X-Authorization: Bearer <jwt_token>
```

### Criar Firmware

```http
POST /api/ota/package
Content-Type: multipart/form-data
X-Authorization: Bearer <jwt_token>

--file--: firmware.bin
--data--: {"version": "1.0.0", "title": "Firmware v1", "type": "DEVICE"}
```

---

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Requisição bem sucedida |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Requisição inválida |
| 401 | Unauthorized - Credenciais inválidas |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro no servidor |

---

## Headers Comuns

### Autenticação JWT
```
X-Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Autenticação Device Token
```
Content-Type: application/json
X-Authorization: Bearer <device_access_token>
```

---

## Rate Limiting

O ThingsBoard CE aplica rate limiting:
- **Sem autenticação**: 100 requests/minuto
- **Com JWT**: 1000 requests/minuto
- **Device API**: 100 requests/minuto por device

---

## Referências

- Swagger UI: `http://204.168.202.5:8080/swagger-ui/index.html`
- Documentação oficial: `https://thingsboard.io/docs/reference/rest-api/`
- Device API: `https://thingsboard.io/docs/reference/http-integration/`

---

## SentivisMCP - Baseline Lógico (Sprint S3)

O **SentivisMCP** (`mcp-thingsboard/`) é o baseline lógico do MCP Server para ThingsBoard CE no projeto Sentivis IAOps.

### Ferramentas Disponíveis (v1.0)

| Tool | Endpoint REST | CRUD | Status |
|------|-------------|------|--------|
| `list_customers` | `GET /api/customers` | Read | Validado ✓ |
| `list_devices` | `GET /api/tenant/deviceInfos` | Read | Validado ✓ |
| `list_customer_devices` | `GET /api/customer/{id}/devices` | Read | Pendente validação |
| `list_users` | `GET /api/users` | Read | Validado ✓ |

### Mapeamento CRUD por Domínio

| Domínio | MCP Tool | Operações Supportadas | Gaps |
|---------|----------|----------------------|------|
| Auth | N/A (manual) | Login JWT | — |
| Customers | `list_customers` | Read | Create/Update/Delete via REST |
| Devices | `list_devices`, `list_customer_devices` | Read | Create/Update/Delete via REST |
| Customer Users | N/A | Read (via REST) | Create/Update via REST |
| Users | `list_users` | Read | Update via REST |

### Notas de Implementação

- O MCP Server lê credenciais de `../.scr/.env` (`TB_URL`, `TB_USERNAME`, `TB_PASSWORD`)
- Ejecuta em modo `stdio` para integração com IDEs (Cline/Gemini)
- A skill `thingsboard-api-reference` (`.cline/skills/`) fornece cookbook de comandos curl
- Physical rename de `mcp-thingsboard/` não faz parte da Sprint S3

### Referências

- `mcp-thingsboard/README.md`
- `mcp-thingsboard/src/` (código fonte TypeScript)
- `.cline/skills/thingsboard-api-reference/SKILL.md`

---

## Notas

1. **CORS**: Verificar configurações de CORS se acessando de frontend
2. **JWT Expiration**: Tokens expiram; implementar refresh token
3. **Device Token**: Usar para dispositivos IoT, não para aplicações server-side
4. **Timestamps**: Usar milissegundos (Unix epoch)
5. **Paginação**: Sempre usar `pageSize` e `page` para listagens
6. **Category A validado**: ver seção "Category A - Domínios Administrativos" para gaps consolidados


