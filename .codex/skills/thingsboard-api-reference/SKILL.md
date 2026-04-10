---
name: thingsboard-api-reference
description: Use when the user needs ThingsBoard CE REST API or Device API commands, Swagger-based endpoint lookup, JWT login flow, device token operations, telemetry, attributes, RPC, dashboards, assets, alarms, users, webhooks, OTA, or wants to troubleshoot HTTP requests against ThingsBoard. Do not use for n8n node design itself, Railway deployment management, or generic MQTT guidance.
---

# Skill: ThingsBoard API Reference

Use esta skill quando o pedido envolver consultar, montar, revisar ou executar chamadas HTTP para qualquer instancia ThingsBoard compativel com a REST API e a Device API descritas no Swagger local.

Esta skill foi criada para funcionar como base de conhecimento operacional em `.cline`, com foco em comandos prontos, padroes de autenticacao e mapeamento rapido de endpoints.

## Objetivo

Permitir que qualquer tarefa envolvendo ThingsBoard seja respondida com:

- endpoint correto
- headers corretos
- comando `curl` pronto
- distincao clara entre JWT administrativo e Device Access Token
- referencia rapida ao trecho certo do Swagger local

## Escopo

Esta skill cobre a documentacao consolidada em `KB/SwaggerTB.md`, usando essa base como referencia para chamadas aplicaveis a qualquer servidor ThingsBoard compativel, incluindo:

- autenticacao
- devices
- telemetria
- atributos
- device credentials
- device profiles
- dashboards
- assets
- customers
- RPC
- rule engine
- alarms
- users
- webhooks
- OTA updates
- headers comuns
- codigos HTTP
- rate limiting

## Fontes

- `KB/SwaggerTB.md`
- `references/swagger-command-cookbook.md`
- `references/source-map.md`

## Como usar

1. Confirmar se a operacao usa JWT administrativo ou Device Access Token.
2. Identificar a familia de endpoint no Swagger local.
3. Reaproveitar os comandos da referencia `swagger-command-cookbook.md`.
4. Se faltar um detalhe, localizar o grupo correspondente em `KB/SwaggerTB.md`.
5. Responder sempre com comando pronto e observacoes objetivas sobre headers, parametros e formato de payload.

## Regras de decisao

- Use `POST /api/auth/login` quando a operacao for administrativa.
- Use `/api/v1/{deviceToken}/...` quando a operacao for de dispositivo.
- Para consulta de telemetria armazenada, use JWT e endpoints em `/api/plugins/telemetry/...`.
- Para credenciais de device, use endpoints de `device credentials`, nunca assuma que o access token atual continua valido.
- Ao responder, prefira variaveis reutilizaveis de shell em vez de valores fixos.
- Quando houver mais de um caminho valido, explique qual serve para admin e qual serve para device.
- Se o usuario pedir "todos os comandos", priorize o cookbook e a estrutura por categoria.

## Variaveis padrao

Use estas variaveis nas respostas e exemplos:

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

## Workflow recomendado

### 1. Login administrativo

Quando a operacao for administrativa:

```bash
curl -sS -X POST "$TB_BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$TB_USERNAME\",
    \"password\": \"$TB_PASSWORD\"
  }"
```

Guardar o `token` retornado e usar:

```bash
export TB_JWT="jwt-retornado-no-login"
```

### 2. Padrao de header JWT

```bash
-H "X-Authorization: Bearer $TB_JWT"
```

### 3. Padrao de Device API

```bash
$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/telemetry
$TB_BASE_URL/api/v1/$TB_DEVICE_TOKEN/attributes
```

### 4. Escolha do grupo correto

- `Devices`: CRUD e busca
- `Telemetry`: envio e consulta de series temporais
- `Attributes`: shared, client e server
- `Device Credentials`: inspecao e rotacao de token
- `RPC`: comandos one-way e two-way
- `Dashboards`, `Assets`, `Customers`, `Users`: entidades administrativas
- `Rule Engine`, `Alarms`, `Webhooks`, `OTA`: operacoes de plataforma

## Estrategia de resposta

Ao responder pedidos de ThingsBoard:

1. Nomear rapidamente o grupo da API.
2. Dizer se usa JWT ou device token.
3. Fornecer o comando `curl`.
4. Informar payload minimo e parametros obrigatorios.
5. Se fizer sentido, citar o arquivo de referencia complementar.

## Limites

- Esta skill nao substitui validacao real do ambiente.
- Esta skill nao cobre modelagem interna de workflows n8n.
- Esta skill nao presume credenciais validas.
- Esta skill nao deve inventar endpoints fora do Swagger local consolidado.

## Done when

- a resposta aponta o endpoint correto
- a autenticacao correta foi distinguida
- o comando foi entregue em formato executavel
- o usuario consegue localizar a categoria certa no Swagger local
- os detalhes adicionais ficam organizados nas referencias da skill

## Referencias

- `references/swagger-command-cookbook.md`
- `references/source-map.md`
