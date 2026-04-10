# ThingsBoard Integration Guide (Sentivis SIM)

Este documento detalha como operar a integração do ThingsBoard CE no ambiente Sentivis SIM, incluindo autenticação, dispositivos e telemetria.

## 1. Ambiente
- **Host**: `http://204.168.202.5:8080`
- **Tenant Admin**: Consultar `.scr/.env` (`TB_USERNAME`, `TB_PASSWORD`)
- **Mail From padrão**: `sentivis@sentivis.com.br`

## 2. Dispositivos Críticos
| Device Name | Device ID | Access Token |
|-------------|-----------|--------------|
| `Sentivis | 0001` | `415037d0-cbe6-11ef-9c4c-7d9fc39bb2d2` | consultar `.scr/.env` |

## 3. Fluxo de Autenticação (REST API)
Sempre use a skill `thingsboard-api-reference` para estas operações.

1. **Obter JWT**:
   ```bash
   curl -X POST http://204.168.202.5:8080/api/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$TB_USERNAME\", \"password\":\"$TB_PASSWORD\"}"
   ```

2. **Consultar Token de Device**:
   ```bash
   curl -X GET http://204.168.202.5:8080/api/device/{DEVICE_ID}/credentials \
        -H "X-Authorization: Bearer {JWT}"
   ```

## 4. Envio de Telemetria (Device API)
O envio via n8n ou scripts locais deve usar o endpoint de telemetria com o Access Token:
- **URL**: `http://204.168.202.5:8080/api/v1/{ACCESS_TOKEN}/telemetry`
- **Method**: POST
- **Payload**: `{"temperature": 25, "humidity": 60}`

## 5. Mail Server
Quando a configuração exigir remetente padrão do projeto, usar `sentivis@sentivis.com.br` no campo `Mail From` do ThingsBoard.

## 6. Troubleshooting (BUG-S3-03)
Se receber `401 Unauthorized`:
1. Valide se o `ACCESS_TOKEN` no n8n coincide com o valor guardado em `.scr/.env`.
2. Verifique se o dispositivo não foi deletado ou se o token foi resetado no dashboard do ThingsBoard.
