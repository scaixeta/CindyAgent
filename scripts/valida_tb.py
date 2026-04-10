import urllib.request, json, time

TB_HOST = "http://204.168.202.5:8080"

try:
    # Login
    login_data = json.dumps({"username": "sentivis@sentivis.com.br", "password": "Sentivis@2026"}).encode()
    req = urllib.request.Request(f"{TB_HOST}/api/auth/login", data=login_data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=10)
    token = json.loads(resp.read())["token"]
    print(f"LOGIN: OK ({token[:20]}...)")

    # Publish test telemetry
    device_token = "EMlf0gDIPJp9nn4CFvkF"
    payload = json.dumps({"air_humidity": 72.00, "air_temperature": 22.5}).encode()
    req2 = urllib.request.Request(f"{TB_HOST}/api/v1/{device_token}/telemetry", data=payload, headers={"Content-Type": "application/json"})
    resp2 = urllib.request.urlopen(req2, timeout=10)
    print(f"PUBLISH: {resp2.read()}")

    # Query back
    device_id = "cdb2a970-3506-11f1-86b7-01315d8eb3e7"
    now_ms = int(time.time() * 1000)
    url = f"{TB_HOST}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys=air_humidity,air_temperature&startTs=0&endTs={now_ms}&limit=3"
    headers = {"X-Authorization": f"Bearer {token}"}
    req3 = urllib.request.Request(url, headers=headers)
    resp3 = urllib.request.urlopen(req3, timeout=10)
    data = json.loads(resp3.read())

    print("TELEMETRIA RECENTE:")
    for key in ["air_humidity", "air_temperature"]:
        points = data.get(key, [])
        if points:
            latest = points[-1]
            ts = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(latest["ts"]/1000))
            print(f"  {key}: {latest['value']} @ {ts}")
        else:
            print(f"  {key}: SEM DADOS")

    print("VALIDACAO: OK")
except Exception as e:
    print(f"ERRO: {e}")
    import traceback; traceback.print_exc()
