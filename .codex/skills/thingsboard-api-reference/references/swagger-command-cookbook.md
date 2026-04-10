# ThingsBoard CE Swagger Command Cookbook

Este arquivo transforma o conteudo de `KB/SwaggerTB.md` em comandos operacionais reutilizaveis para qualquer instancia ThingsBoard compativel.

## 1. Preparacao

```bash
export TB_BASE_URL="https://your-thingsboard-host"
export TB_USERNAME="tenant@company.com"
export TB_PASSWORD="change-me"
export TB_JWT="seu-jwt"
export TB_DEVICE_ID="uuid-do-device"
export TB_DEVICE_TOKEN="access-token-do-device"
export TB_DEVICE_PROFILE_ID="uuid-do-device-profile"
export TB_DASHBOARD_ID="uuid-do-dashboard"
export TB_ASSET_ID="uuid-do-asset"
export TB_CUSTOMER_ID="uuid-do-customer"
export TB_USER_ID="uuid-do-user"
```

## 2. Autenticacao

### Login JWT

```bash
curl -sS -X POST "$TB_BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$TB_USERNAME\",
    \"password\": \"$TB_PASSWORD\"
  }"
```

### Exemplo com `jq` para capturar o token

```bash
export TB_JWT="$(
  curl -sS -X POST "$TB_BASE_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"$TB_USERNAME\",
      \"password\": \"$TB_PASSWORD\"
    }" | jq -r '.token'
)"
```

## 3. Devices

### Listar dispositivos

```bash
curl -sS "$TB_BASE_URL/api/devices?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Listar dispositivos com busca por nome

```bash
curl -sS "$TB_BASE_URL/api/devices?pageSize=100&page=0&textSearch=ExampleDevice" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar device

```bash
curl -sS -X POST "$TB_BASE_URL/api/device" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"name\": \"Example Device 0001\",
    \"deviceProfileId\": {
      \"id\": \"$TB_DEVICE_PROFILE_ID\",
      \"entityType\": \"DEVICE_PROFILE\"
    },
    \"type\": \"default\"
  }"
```

### Obter device por ID

```bash
curl -sS "$TB_BASE_URL/api/device/$TB_DEVICE_ID" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Atualizar device

```bash
curl -sS -X PUT "$TB_BASE_URL/api/device" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"id\": {\"id\": \"$TB_DEVICE_ID\"},
    \"name\": \"Novo Nome\",
    \"type\": \"default\"
  }"
```

### Deletar device

```bash
curl -sS -X DELETE "$TB_BASE_URL/api/device/$TB_DEVICE_ID" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Buscar device por nome

```bash
curl -sS "$TB_BASE_URL/api/tenant/devices?textSearch=ExampleDevice" \
  -H "X-Authorization: Bearer $TB_JWT"
```

## 4. Telemetria

### Enviar telemetria com timestamp e values

```bash
curl -sS -X POST "$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/telemetry" \
  -H "Content-Type: application/json" \
  -d '{
    "ts": 1646925123000,
    "values": {
      "temperature": 25.5,
      "humidity": 60.0
    }
  }'
```

### Enviar telemetria em formato simplificado

```bash
curl -sS -X POST "$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/telemetry" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25.5,
    "humidity": 60.0,
    "ts": 1646925123000
  }'
```

### Consultar telemetria por keys e janela de tempo

```bash
curl -sS "$TB_BASE_URL/api/plugins/telemetry/DEVICE/$TB_DEVICE_ID/values/timeseries?keys=temperature,humidity&startTs=1646925123000&endTs=1647011523000" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Consultar telemetria com agregacao

```bash
curl -sS "$TB_BASE_URL/api/plugins/telemetry/DEVICE/$TB_DEVICE_ID/values/timeseries?keys=temperature&startTs=1646925123000&endTs=1647011523000&interval=60000&limit=100&agg=AVG" \
  -H "X-Authorization: Bearer $TB_JWT"
```

## 5. Atributos

### Enviar atributos do device

```bash
curl -sS -X POST "$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/attributes" \
  -H "Content-Type: application/json" \
  -d '{
    "shared": {
      "firmware_version": "1.0.0",
      "location": "sala"
    },
    "client": {
      "connection_status": "connected"
    }
  }'
```

### Consultar atributos shared

```bash
curl -sS "$TB_BASE_URL/api/plugins/telemetry/DEVICE/$TB_DEVICE_ID/values/attributes?keys=firmware_version,location&types=SHARED_SCOPE" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Consultar atributos server-side

```bash
curl -sS "$TB_BASE_URL/api/plugins/telemetry/DEVICE/$TB_DEVICE_ID/values/attributes?keys=firmware_version,location&types=SERVER_SCOPE" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Consultar atributos client-side

```bash
curl -sS "$TB_BASE_URL/api/plugins/telemetry/DEVICE/$TB_DEVICE_ID/values/attributes?keys=connection_status&types=CLIENT_SCOPE" \
  -H "X-Authorization: Bearer $TB_JWT"
```

## 6. Device Credentials

### Obter credentials do device

```bash
curl -sS "$TB_BASE_URL/api/device/$TB_DEVICE_ID/credentials" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Atualizar credentials do device

```bash
curl -sS -X POST "$TB_BASE_URL/api/device/$TB_DEVICE_ID/credentials" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "credentialsType": "ACCESS_TOKEN",
    "credentialsId": "novo-device-token"
  }'
```

### Criar access token

```bash
curl -sS -X POST "$TB_BASE_URL/api/device-with-credentials" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"device\": {
      \"name\": \"Example Device 0002\",
      \"deviceProfileId\": {
        \"id\": \"$TB_DEVICE_PROFILE_ID\",
        \"entityType\": \"DEVICE_PROFILE\"
      },
      \"type\": \"default\"
    },
    \"credentials\": {
      \"credentialsType\": \"ACCESS_TOKEN\",
      \"credentialsId\": \"token-novo-0002\"
    }
  }"
```

## 7. Device Profiles

### Listar device profiles

```bash
curl -sS "$TB_BASE_URL/api/deviceProfiles?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Obter device profile por ID

```bash
curl -sS "$TB_BASE_URL/api/deviceProfile/$TB_DEVICE_PROFILE_ID" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar device profile

```bash
curl -sS -X POST "$TB_BASE_URL/api/deviceProfile" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "name": "Example Device Profile",
    "type": "DEFAULT",
    "transportType": "DEFAULT",
    "profileData": {
      "configuration": {
        "type": "DEFAULT"
      },
      "transportConfiguration": {
        "type": "DEFAULT"
      }
    }
  }'
```

## 8. Dashboards

### Listar dashboards

```bash
curl -sS "$TB_BASE_URL/api/tenant/dashboards?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Obter dashboard por ID

```bash
curl -sS "$TB_BASE_URL/api/dashboard/$TB_DASHBOARD_ID" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar dashboard

```bash
curl -sS -X POST "$TB_BASE_URL/api/dashboard" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "title": "Example Dashboard",
    "configuration": {
      "widgets": {},
      "states": {
        "default": {
          "name": "Default"
        }
      }
    }
  }'
```

### Atualizar dashboard

```bash
curl -sS -X PUT "$TB_BASE_URL/api/dashboard" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"id\": {\"id\": \"$TB_DASHBOARD_ID\"},
    \"title\": \"Example Dashboard Updated\",
    \"configuration\": {
      \"widgets\": {},
      \"states\": {
        \"default\": {
          \"name\": \"Default\"
        }
      }
    }
  }"
```

## 9. Assets

### Listar assets

```bash
curl -sS "$TB_BASE_URL/api/tenant/assets?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar asset

```bash
curl -sS -X POST "$TB_BASE_URL/api/asset" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "name": "Planta A",
    "type": "facility"
  }'
```

### Associar device a asset

```bash
curl -sS -X POST "$TB_BASE_URL/api/relation" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"from\": {
      \"id\": \"$TB_ASSET_ID\",
      \"entityType\": \"ASSET\"
    },
    \"to\": {
      \"id\": \"$TB_DEVICE_ID\",
      \"entityType\": \"DEVICE\"
    },
    \"type\": \"Contains\",
    \"typeGroup\": \"COMMON\"
  }"
```

## 10. Customers

### Listar customers

```bash
curl -sS "$TB_BASE_URL/api/customers?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar customer

```bash
curl -sS -X POST "$TB_BASE_URL/api/customer" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "title": "Example Customer",
    "country": "BR",
    "city": "Belo Horizonte"
  }'
```

## 11. RPC

### Enviar RPC two-way

```bash
curl -sS -X POST "$TB_BASE_URL/api/plugins/rpc/twoway/$TB_DEVICE_ID" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "method": "reboot",
    "params": {
      "delay": 5
    }
  }'
```

### Enviar RPC one-way

```bash
curl -sS -X POST "$TB_BASE_URL/api/plugins/rpc/oneway/$TB_DEVICE_ID" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "method": "setMode",
    "params": {
      "mode": "eco"
    }
  }'
```

## 12. Rule Engine

### Listar rules

```bash
curl -sS "$TB_BASE_URL/api/ruleChains?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar rule chain

```bash
curl -sS -X POST "$TB_BASE_URL/api/ruleChain" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "name": "Example Rule Chain",
    "type": "CORE",
    "root": false,
    "debugMode": false,
    "configuration": null
  }'
```

## 13. Alarms

### Listar alarms

```bash
curl -sS "$TB_BASE_URL/api/alarms?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar alarm

```bash
curl -sS -X POST "$TB_BASE_URL/api/alarm" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d "{
    \"type\": \"HighTemperature\",
    \"originator\": {
      \"id\": \"$TB_DEVICE_ID\",
      \"entityType\": \"DEVICE\"
    },
    \"severity\": \"CRITICAL\",
    \"startTs\": 1646925123000,
    \"status\": \"ACTIVE_UNACK\",
    \"ackTs\": 0,
    \"clearTs\": 0,
    \"details\": {
      \"temperature\": 90
    }
  }"
```

### Consultar alarms por device

```bash
curl -sS "$TB_BASE_URL/api/alarm/DEVICE/$TB_DEVICE_ID?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

## 14. Users

### Listar users

```bash
curl -sS "$TB_BASE_URL/api/users?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar user

```bash
curl -sS -X POST "$TB_BASE_URL/api/user?sendActivationMail=false" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "email": "novo.usuario@sentivis.com",
    "authority": "TENANT_ADMIN",
    "firstName": "Novo",
    "lastName": "Usuario"
  }'
```

## 15. Webhooks

### Listar webhooks

```bash
curl -sS "$TB_BASE_URL/api/webhooks?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar webhook

```bash
curl -sS -X POST "$TB_BASE_URL/api/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "name": "Example Webhook",
    "configuration": {
      "url": "https://example.com/webhook",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }'
```

## 16. OTA Updates

### Listar firmwares

```bash
curl -sS "$TB_BASE_URL/api/otaPackages?pageSize=100&page=0&type=FIRMWARE" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Criar firmware

```bash
curl -sS -X POST "$TB_BASE_URL/api/otaPackage" \
  -H "Content-Type: application/json" \
  -H "X-Authorization: Bearer $TB_JWT" \
  -d '{
    "type": "FIRMWARE",
    "title": "FW 1.0.0",
    "version": "1.0.0",
    "tag": "stable"
  }'
```

## 17. Headers comuns

### Header para JWT

```bash
X-Authorization: Bearer $TB_JWT
```

### Header para Device API

```bash
Content-Type: application/json
```

Observacao: no fluxo por device token, o token vai na URL, nao no header.

## 18. Codigos HTTP

Use esta leitura rapida ao interpretar respostas:

- `200 OK`: operacao concluida
- `201 Created`: recurso criado
- `400 Bad Request`: payload, parametro ou formato invalido
- `401 Unauthorized`: JWT invalido, expirado ou device token incorreto
- `403 Forbidden`: usuario autenticado sem permissao suficiente
- `404 Not Found`: recurso ou endpoint nao encontrado
- `429 Too Many Requests`: limite de requisicoes atingido
- `500 Internal Server Error`: erro interno no ThingsBoard

## 19. Rate limiting

O Swagger consolidado indica presenca de rate limiting. Em lotes de chamadas:

- pagina resultados
- evite loops agressivos
- trate `429`
- use retries com backoff

## 20. Leitura rapida por tipo de autenticacao

### Usa JWT

- `/api/device`
- `/api/devices`
- `/api/device/{deviceId}/credentials`
- `/api/deviceProfile`
- `/api/dashboard`
- `/api/tenant/dashboards`
- `/api/asset`
- `/api/customer`
- `/api/plugins/telemetry/.../values/...`
- `/api/plugins/rpc/...`
- `/api/ruleChain`
- `/api/alarms`
- `/api/users`
- `/api/webhook`
- `/api/otaPackage`

### Usa Device Access Token

- `/api/v1/{deviceToken}/telemetry`
- `/api/v1/{deviceToken}/attributes`

## 21. Atalhos uteis

### Validar rapidamente se o JWT funciona

```bash
curl -sS "$TB_BASE_URL/api/auth/user" \
  -H "X-Authorization: Bearer $TB_JWT"
```

### Validar rapidamente se o device token funciona

```bash
curl -i -X POST "$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/telemetry" \
  -H "Content-Type: application/json" \
  -d '{"ping":1}'
```

### Buscar ID de device a partir do nome

```bash
curl -sS "$TB_BASE_URL/api/tenant/devices?textSearch=Example%20Device%200001&pageSize=10&page=0" \
  -H "X-Authorization: Bearer $TB_JWT"
```
