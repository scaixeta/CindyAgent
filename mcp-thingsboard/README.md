# ThingsBoard MCP Server (Sentivis SIM)

Este é um servidor Model Context Protocol (MCP) para interfacear com a API REST do ThingsBoard CE.

## Funcionalidades (Tools)

- `list_customers`: Lista os clientes cadastrados.
- `list_devices`: Lista todos os dispositivos do tenant.
- `list_customer_devices`: Lista dispositivos de um cliente específico.
- `list_users`: Lista os usuários (responsáveis).

## Configuração

O servidor utiliza as credenciais localizadas em `../.scr/.env`. Certifique-se de que `TB_URL`, `TB_USERNAME` e `TB_PASSWORD` estão configurados.

## Como Executar

Para rodar o servidor em modo `stdio`:
```bash
npm start
```

## Integração com IDEs (Cline/Gemini)

Adicione a seguinte configuração ao seu arquivo de patches/configurações de MCP:

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
