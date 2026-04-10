# Source Map

## Fonte principal

- `KB/SwaggerTB.md`

## Estrutura do Swagger local consolidado

- Autenticacao
- Devices
- Telemetria
- Atributos
- Device Credentials
- Device Profiles
- Dashboards
- Assets
- Customers
- RPC
- Rule Engine
- Alarms
- Users
- Webhooks
- OTA Updates
- Codigos HTTP
- Headers comuns
- Rate limiting

## Como esta skill foi organizada

- `SKILL.md`: contrato de uso, escopo, fluxo e regras
- `references/swagger-command-cookbook.md`: comandos `curl` prontos por categoria
- `references/source-map.md`: mapa de origem e cobertura

## Quando expandir esta skill

Expandir quando houver necessidade de:

- adicionar endpoints novos do Swagger
- registrar exemplos reais de payload de ambientes clientes, mantendo a skill neutra
- adicionar troubleshooting de erros comuns por endpoint
- espelhar a mesma skill para `.codex/skills` e `.agents/skills`

## Quando nao expandir aqui

Nao usar esta skill para:

- regras internas de n8n
- deploy Railway
- modelagem MQTT fora do escopo HTTP/REST do Swagger consolidado
