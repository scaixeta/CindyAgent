"""
cirrus_collector.py — Cirrus-Lab External Station Collector
S4: Sentivis IAOps

Lê telemetria do Cirrus-Lab via JWT, normaliza para o contrato interno,
e persiste no ThingsBoard local via POST /api/v1/{token}/telemetry.

Uso:
    python scripts/cirrus_collector.py [--device-id <id>] [--iterations <n>] [--interval <seconds>]

Parametros:
    --device-id   Cirrus device UUID (default: 27ad32e0-c0d3-11f0-a562-d9639f025684)
    --iterations   Numero de coletas (default: 12)
    --interval     Intervalo em segundos (default: 300 = 5 min)
    --dry-run      Apenas simula sem persistir

Credential source: .scr/.env
    THINGSBOARD_CIRRUS_JWT_Token
    TB_CIRRUS_DEVICE_TOKEN
    TB_HOST, TB_PORT

Normalizacao:
    temperature  -> air_temperature
    humidity     -> air_humidity
    latitude     -> latitude
    longitude    -> longitude
    source_station -> CIRRUS-NIMBUS-AERO
"""

import urllib.request
import urllib.error
import json
import time
import re
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
ENV_FILE = SCRIPT_DIR / '.scr' / '.env'

# Cirrus device registry
CIRRUS_DEVICES = {
    'nimbus_aero': {
        'id': '27ad32e0-c0d3-11f0-a562-d9639f025684',
        'name': 'NIMBUS-AERO',
        'label': 'Sentivis | CIRRUS-NIMBUS-AERO',
        'type': 'WeatherStation',
    },
    'atmos_wind': {
        'id': '9c5178a0-6d58-11f0-bf1e-9f28a6572bf1',
        'name': 'ATMOS-WIND',
        'label': 'Sentivis | CIRRUS-ATMOS-WIND',
        'type': 'WeatherStation',
    },
    'atmos_link': {
        'id': 'bdda85a0-6dd2-11f0-bf1e-9f28a6572bf1',
        'name': 'ATMOS-LINK',
        'label': 'Sentivis | CIRRUS-ATMOS-LINK',
        'type': 'WeatherStation',
    },
    'nimbus_echo': {
        'id': 'cbec4881-067b-11f1-ab6c-212e5827054d',
        'name': 'NIMBUS-ECHO-R1',
        'label': 'Sentivis | CIRRUS-NIMBUS-ECHO-R1',
        'type': 'WeatherStation',
    },
}


def load_env():
    env = {}
    if not ENV_FILE.exists():
        print(f'[WARN] {ENV_FILE} not found')
        return env
    content = ENV_FILE.read_text(encoding='utf-8')
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def get_cirrus_jwt(env):
    raw = env.get('THINGSBOARD_CIRRUS_JWT_Token', '')
    if raw.startswith('Bearer '):
        return raw[7:]
    return raw


def get_tb_credentials(env):
    return {
        'host': env.get('TB_HOST', '204.168.202.5'),
        'port': env.get('TB_PORT', '8080'),
        'url': env.get('TB_URL', 'http://204.168.202.5:8080'),
        'device_token': env.get('TB_CIRRUS_DEVICE_TOKEN', 'EMlf0gDIPJp9nn4CFvkF'),
        'tenant_user': env.get('TB_TENANT_USERNAME', ''),
        'tenant_pass': env.get('TB_TENANT_PASSWORD', ''),
    }


def read_cirrus_telemetry(env, device_id, keys='temperature,humidity,latitude,longitude', limit=5):
    """Read telemetry from Cirrus-Lab via JWT Bearer token."""
    jwt = get_cirrus_jwt(env)
    now_ms = int(time.time() * 1000)
    url = (
        f'https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}'
        f'/values/timeseries?keys={keys}&startTs=0&endTs={now_ms}&limit={limit}'
    )
    req = urllib.request.Request(url, headers={'X-Authorization': 'Bearer ' + jwt})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_latest_telemetry(raw_telemetry):
    """
    Extract the latest value for each key from Cirrus telemetry response.
    Response format: {"temperature": [{"ts": ..., "value": "25"}], ...}
    Returns: {key: (ts_ms, value_string)}
    """
    result = {}
    for key, entries in raw_telemetry.items():
        if not entries:
            continue
        latest = sorted(entries, key=lambda x: x['ts'], reverse=True)[0]
        result[key] = (latest['ts'], latest['value'])
    return result


def normalize_payload(latest_values, source_device_id, source_device_name):
    """
    Normalize Cirrus telemetry to internal Sentivis contract.

    Cirrus -> Internal:
        temperature  -> air_temperature
        humidity     -> air_humidity
        latitude     -> latitude
        longitude    -> longitude
        source_station -> CIRRUS-<name>-<short_id>
    """
    short_id = source_device_id.split('-')[0]

    normalized = {
        'ts': int(time.time() * 1000),
        'source_station': f'CIRRUS-{source_device_name}-{short_id}',
        'source_device_id': source_device_id,
    }

    key_map = {
        'temperature': 'air_temperature',
        'humidity': 'air_humidity',
        'latitude': 'latitude',
        'longitude': 'longitude',
    }

    for cirrus_key, normalized_key in key_map.items():
        if cirrus_key in latest_values:
            ts, val = latest_values[cirrus_key]
            try:
                normalized[normalized_key] = float(val)
            except (ValueError, TypeError):
                normalized[normalized_key] = val

    return normalized


def persist_to_tb(tb_cfg, normalized_payload, dry_run=False):
    """Persist normalized telemetry to ThingsBoard local via Device API."""
    if dry_run:
        print(f'[DRY-RUN] Would persist: {json.dumps(normalized_payload, indent=2)}')
        return True

    url = f"{tb_cfg['url']}/api/v1/{tb_cfg['device_token']}/telemetry"
    payload = json.dumps(normalized_payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
        }
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status in (200, 201)


def collection_summary(iteration, max_iterations, interval_sec, status, latest_values, normalized, persisted):
    now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    temp = latest_values.get('temperature', (None, None))
    hum = latest_values.get('humidity', (None, None))
    lat = latest_values.get('latitude', (None, None))
    lon = latest_values.get('longitude', (None, None))
    return {
        'collection': iteration,
        'timestamp_utc': now_utc,
        'status': status,
        'temperature_raw': temp[1] if temp[0] else None,
        'humidity_raw': hum[1] if hum[0] else None,
        'latitude_raw': lat[1] if lat[0] else None,
        'longitude_raw': lon[1] if lon[0] else None,
        'normalized': normalized,
        'persisted': persisted,
    }


def run_collection(device_key, iterations, interval_sec, dry_run=False, log_callback=None):
    """
    Run the collection loop.

    Args:
        device_key: key in CIRRUS_DEVICES dict
        iterations: number of collections
        interval_sec: seconds between collections
        dry_run: if True, skip persistence
        log_callback: function(row_dict) called after each collection
    """
    env = load_env()
    tb_cfg = get_tb_credentials(env)

    device = CIRRUS_DEVICES.get(device_key)
    if not device:
        print(f'[ERROR] Unknown device key: {device_key}')
        return []

    results = []

    for i in range(1, iterations + 1):
        status = 'SUCCESS'
        error_msg = ''
        latest_values = {}
        normalized = {}
        persisted = False

        try:
            raw = read_cirrus_telemetry(env, device['id'])
            latest_values = get_latest_telemetry(raw)
            normalized = normalize_payload(latest_values, device['id'], device['name'])
            if not dry_run:
                persisted = persist_to_tb(tb_cfg, normalized)
            else:
                persisted = True
        except Exception as e:
            status = 'FAIL'
            error_msg = str(e)

        row = collection_summary(i, iterations, interval_sec, status, latest_values, normalized, persisted)
        if error_msg:
            row['error'] = error_msg

        results.append(row)

        ts_display = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f"[{ts_display}] Collection {i}/{iterations}: {status} | "
              f"Temp={latest_values.get('temperature', (None,''))[1]} "
              f"Hum={latest_values.get('humidity', (None,''))[1]} "
              f"Persisted={persisted}")

        if log_callback:
            log_callback(row)

        if i < iterations:
            time.sleep(interval_sec)

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cirrus-Lab Collector for S4')
    parser.add_argument('--device', default='nimbus_aero',
                        choices=list(CIRRUS_DEVICES.keys()),
                        help='Cirrus device to collect from')
    parser.add_argument('--iterations', type=int, default=12,
                        help='Number of collections (default: 12)')
    parser.add_argument('--interval', type=int, default=300,
                        help='Interval in seconds (default: 300 = 5 min)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simulate without persisting to TB')
    args = parser.parse_args()

    print(f'=== Cirrus Collector S4 ===')
    print(f'Device: {CIRRUS_DEVICES[args.device]["name"]}')
    print(f'Iterations: {args.iterations}, Interval: {args.interval}s')
    print(f'Dry-run: {args.dry_run}')
    print()

    results = run_collection(
        device_key=args.device,
        iterations=args.iterations,
        interval_sec=args.interval,
        dry_run=args.dry_run,
    )

    success = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    print()
    print(f'=== Collection Complete ===')
    print(f'Total: {len(results)} | Success: {success} | Failed: {failed}')
