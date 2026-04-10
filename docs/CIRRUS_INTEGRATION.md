# Integração Cirrus - Documento de Design

## Visão Geral

Integração da estação meteorológica Cirrus Lab (NIMBUS-AERO) como device externo no ecossistema Sentivis via ThingsBoard CE.

---

## Arquitetura

```
Cirrus Lab Cloud (portal.cirrus-lab.com)
  |
  | JWT Bearer Authentication
  | GET /api/plugins/telemetry/DEVICE/{id}/values/timeseries
  v
Python Collector (scripts/cirrus_collector.py)
  |
  | Normalizar payload
  | temperature -> air_temperature
  | humidity -> air_humidity
  v
ThingsBoard CE (204.168.202.5:8080)
  |
  | POST /api/v1/{device_token}/telemetry
  v
Device: Sentivis | CIRRUS-NIMBUS-AERO
  (cdb2a970-3506-11f1-86b7-01315d8eb3e7)
```

---

## Device Cirrus

| Campo | Valor |
|---|---|
| Device ID | 27ad32e0-c0d3-11f0-a562-d9639f025684 |
| Nome | NIMBUS-AERO 1-09821699 |
| Tipo | WeatherStation |
| Localização | SP, Brasil (-22.59467, -48.80054) |
| Telemetria | temperature, humidity |

---

## Device TB Local

| Campo | Valor |
|---|---|
| Device ID | cdb2a970-3506-11f1-86b7-01315d8eb3e7 |
| Nome | Sentivis | CIRRUS-NIMBUS-AERO |
| Device Token | EMlf0gDIPJp9nn4CFvkF |
| Tipo | WeatherStation |

---

## Normalização de Payload

| Chave Cirrus | Chave Interna | Unidade |
|---|---|---|
| temperature | air_temperature | C |
| humidity | air_humidity | % |
| latitude | latitude | degrees |
| longitude | longitude | degrees |

Campos adicionais injetados:
- source_station: "CIRRUS-NIMBUS-AERO"

---

## Script Collector

`scripts/cirrus_collector.py`

Uso:
```bash
python3 scripts/cirrus_collector.py --device nimbus_aero --iterations 12 --interval 300
python3 scripts/cirrus_collector.py --device nimbus_aero --dry-run
```

Argumentos:
- --device: nimbus_aero, atmos_wind, atmos_link, nimbus_echo
- --iterations: número de coletas (padrão: 12)
- --interval: segundos entre coletas (padrão: 300)
- --dry-run: apenas leitura, sem persistência
- --device-token: sobrescrever token do device TB

---

## Batch Backfill

Para backfill de dados históricos, usar endpoint de telemetria batch:
```python
batch = [{"ts": p["ts"], "values": {"air_humidity": str(p["value"])}} for p in hums]
POST /api/v1/{device_token}/telemetry  # com array JSON no body
```

Nota: TB CE 3.x não suporta /api/plugins/telemetry/{id}/telemetry com parâmetro scope.
Usar endpoint de device access token para escritas em batch.

---

## Problemas Conhecidos

1. Temperature sensor: apenas 1 point histórico no Cirrus para NIMBUS-AERO — possível problema de hardware
2. Lacuna histórica: 2025-12-17 a 2026-02-20 (~65 dias sem dados humidity)
3. Humidity shift: salto de 64 para 88 às 18:09 observado na janela de teste
