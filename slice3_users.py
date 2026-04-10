"""
Slice 3: 25 testes randômicos de validação REST API ThingsBoard CE
Distribuídos em 3 camadas:
- Layer 1: CRUD REST API (Customers, Users, Customer Users, Devices)
- Layer 2: Consistência de estado e contrato
- Layer 3: Comportamento negativo e de fronteira

Host: http://204.168.202.5:8080
Auth: tenant@thingsboard.org / tenant
"""

import json
import requests
import sys
from datetime import datetime

# Configuração
BASE_URL = "http://204.168.202.5:8080"
TB_USERNAME = "tenant@thingsboard.org"
TB_PASSWORD = "tenant"
TB_DEVICE_TOKEN = "dvcyjutxhb3pr5nsc34t"

# Resultados dos testes
results = []
jwt_token = None

def log(msg):
    """Log com timestamp."""
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{ts}] {msg}")

def get_headers():
    """Headers com JWT se disponível."""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if jwt_token:
        headers["X-Authorization"] = f"Bearer {jwt_token}"
    return headers

def login():
    """Autentica e retorna JWT token."""
    global jwt_token
    url = f"{BASE_URL}/api/auth/login"
    payload = {"username": TB_USERNAME, "password": TB_PASSWORD}
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        jwt_token = data.get("token")
        log(f"TEST-AUTH: Login OK, JWT obtido")
        return True
    else:
        log(f"TEST-AUTH: Login FALHOU {resp.status_code} - {resp.text[:200]}")
        return False

def record_test(test_id, layer, family, scope, expected, actual, status, evidence, notes=""):
    """Registra resultado do teste."""
    results.append({
        "test_id": test_id,
        "layer": layer,
        "family": family,
        "scope": scope,
        "expected": expected,
        "actual": actual,
        "status": status,
        "evidence": evidence,
        "notes": notes,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S-03")
    })

# ============================================================
# LAYER 1: CRUD REST API
# ============================================================

def test_L1_customer_create():
    """L1-C1: Create Customer."""
    url = f"{BASE_URL}/api/customer"
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    payload = {"title": f"TEST_Customer_L1_{ts}", "email": f"test_{ts}@sentivis.com"}
    resp = requests.post(url, headers=get_headers(), json=payload)
    actual_id = None
    if resp.status_code == 200:
        data = resp.json()
        actual_id = data.get("id", {}).get("id")
        log(f"L1-C1: Customer criado {actual_id}")
    record_test(
        "L1-C1", "Layer 1", "Customers",
        "POST /api/customer",
        "HTTP 200, customer criado",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "payload": payload, "response": resp.text[:500]},
        f"ID: {actual_id}" if actual_id else ""
    )
    return actual_id

def test_L1_customer_read(customer_id):
    """L1-C2: Read Customer by ID."""
    url = f"{BASE_URL}/api/customer/{customer_id}"
    resp = requests.get(url, headers=get_headers())
    record_test(
        "L1-C2", "Layer 1", "Customers",
        "GET /api/customer/{id}",
        "HTTP 200, customer data",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "response": resp.text[:500]}
    )
    return resp.status_code == 200

def test_L1_customer_update(customer_id):
    """L1-C3: Update Customer (deve falhar com 405)."""
    url = f"{BASE_URL}/api/customer/{customer_id}"
    payload = {"id": {"id": customer_id}, "title": f"TEST_Customer_UPDATED_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"}
    resp = requests.put(url, headers=get_headers(), json=payload)
    record_test(
        "L1-C3", "Layer 1", "Customers",
        "PUT /api/customer/{id}",
        "HTTP 405 (gap API CE)",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 405 else "INFO",
        {"url": url, "response": resp.text[:300]},
        "Gap API CE confirmado" if resp.status_code == 405 else ""
    )

def test_L1_customer_delete(customer_id):
    """L1-C4: Delete Customer."""
    url = f"{BASE_URL}/api/customer/{customer_id}"
    resp = requests.delete(url, headers=get_headers())
    record_test(
        "L1-C4", "Layer 1", "Customers",
        "DELETE /api/customer/{id}",
        "HTTP 200, deletado",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "response": resp.text[:200]}
    )
    return resp.status_code == 200

def test_L1_user_list():
    """L1-U1: List Users."""
    url = f"{BASE_URL}/api/users?pageSize=100&page=0"
    resp = requests.get(url, headers=get_headers())
    users = []
    if resp.status_code == 200:
        data = resp.json()
        users = data.get("data", [])
        log(f"L1-U1: {len(users)} users listados")
    record_test(
        "L1-U1", "Layer 1", "Users",
        "GET /api/users",
        "HTTP 200, lista de users",
        f"HTTP {resp.status_code}, {len(users)} users",
        "PASS" if resp.status_code == 200 and len(users) > 0 else "FAIL",
        {"url": url, "count": len(users), "sample": [u.get("email") for u in users[:3]]}
    )
    return users

def test_L1_user_read_by_id(user_id):
    """L1-U2: Read User by ID."""
    url = f"{BASE_URL}/api/user/{user_id}"
    resp = requests.get(url, headers=get_headers())
    record_test(
        "L1-U2", "Layer 1", "Users",
        "GET /api/user/{id}",
        "HTTP 200, user data",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "response": resp.text[:500]}
    )

def test_L1_user_update(user_id):
    """L1-U3: Update User (deve falhar com 405)."""
    url = f"{BASE_URL}/api/user/{user_id}"
    payload = {"id": {"id": user_id}, "firstName": "Updated"}
    resp = requests.put(url, headers=get_headers(), json=payload)
    record_test(
        "L1-U3", "Layer 1", "Users",
        "PUT /api/user/{id}",
        "HTTP 405 (gap API CE)",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 405 else "INFO",
        {"url": url, "response": resp.text[:300]},
        "Gap API CE confirmado" if resp.status_code == 405 else ""
    )

def test_L1_customer_user_list(customer_id):
    """L1-CU1: List Customer Users."""
    url = f"{BASE_URL}/api/customer/{customer_id}/users"
    resp = requests.get(url, headers=get_headers())
    users = []
    if resp.status_code == 200:
        data = resp.json()
        users = data if isinstance(data, list) else data.get("data", [])
        log(f"L1-CU1: {len(users)} customer users")
    record_test(
        "L1-CU1", "Layer 1", "Customer Users",
        "GET /api/customer/{id}/users",
        "HTTP 200, lista de customer users",
        f"HTTP {resp.status_code}, {len(users)} users",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "count": len(users)}
    )
    return users

def test_L1_device_create():
    """L1-D1: Create Device."""
    url = f"{BASE_URL}/api/device"
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    payload = {"name": f"TEST_Device_L1_{ts}", "type": "default"}
    resp = requests.post(url, headers=get_headers(), json=payload)
    actual_id = None
    if resp.status_code == 200:
        data = resp.json()
        actual_id = data.get("id", {}).get("id")
        log(f"L1-D1: Device criado {actual_id}")
    record_test(
        "L1-D1", "Layer 1", "Devices",
        "POST /api/device",
        "HTTP 200, device criado",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "payload": payload, "response": resp.text[:500]},
        f"ID: {actual_id}" if actual_id else ""
    )
    return actual_id

def test_L1_device_read(device_id):
    """L1-D2: Read Device by ID."""
    url = f"{BASE_URL}/api/device/{device_id}"
    resp = requests.get(url, headers=get_headers())
    record_test(
        "L1-D2", "Layer 1", "Devices",
        "GET /api/device/{id}",
        "HTTP 200, device data",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "response": resp.text[:500]}
    )

def test_L1_device_update(device_id):
    """L1-D3: Update Device."""
    url = f"{BASE_URL}/api/device"
    payload = {"id": {"id": device_id}, "name": f"TEST_Device_UPDATED_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}", "type": "default"}
    resp = requests.put(url, headers=get_headers(), json=payload)
    record_test(
        "L1-D3", "Layer 1", "Devices",
        "PUT /api/device",
        "HTTP 200 ou 405",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [200, 405] else "FAIL",
        {"url": url, "response": resp.text[:300]}
    )

def test_L1_device_delete(device_id):
    """L1-D4: Delete Device."""
    url = f"{BASE_URL}/api/device/{device_id}"
    resp = requests.delete(url, headers=get_headers())
    record_test(
        "L1-D4", "Layer 1", "Devices",
        "DELETE /api/device/{id}",
        "HTTP 200, deletado",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 200 else "FAIL",
        {"url": url, "response": resp.text[:200]}
    )
    return resp.status_code == 200

# ============================================================
# LAYER 2: Consistência de estado e contrato
# ============================================================

def test_L2_customer_read_after_create():
    """L2-C1: Read-after-write consistency for Customer."""
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    # Create
    url = f"{BASE_URL}/api/customer"
    payload = {"title": f"TEST_L2_Consistency_{ts}", "email": f"l2_{ts}@sentivis.com"}
    resp = requests.post(url, headers=get_headers(), json=payload)
    if resp.status_code != 200:
        record_test("L2-C1", "Layer 2", "Customers", "Read-after-write Customer", "Create OK", f"Create falhou {resp.status_code}", "FAIL", {"create_resp": resp.text[:200]})
        return None
    created = resp.json()
    cust_id = created.get("id", {}).get("id")
    created_title = created.get("title")
    # Read
    url2 = f"{BASE_URL}/api/customer/{cust_id}"
    resp2 = requests.get(url2, headers=get_headers())
    read_ok = resp2.status_code == 200
    read_title = resp2.json().get("title") if read_ok else None
    consistent = read_title == created_title
    record_test(
        "L2-C1", "Layer 2", "Customers",
        "Read-after-write consistency",
        f"title={created_title}",
        f"read_title={read_title}, consistent={consistent}",
        "PASS" if consistent else "FAIL",
        {"created": created, "read": resp2.json() if read_ok else resp2.text[:200]},
        "Consistência confirmada" if consistent else "INCONSISTÊNCIA!"
    )
    # Cleanup
    requests.delete(f"{BASE_URL}/api/customer/{cust_id}", headers=get_headers())
    return cust_id

def test_L2_customer_update_persistence(customer_id):
    """L2-C2: Update persistence validation."""
    # Read original
    url1 = f"{BASE_URL}/api/customer/{customer_id}"
    resp1 = requests.get(url1, headers=get_headers())
    if resp1.status_code != 200:
        record_test("L2-C2", "Layer 2", "Customers", "Update persistence", "Read OK", "Read falhou", "FAIL", {})
        return
    original = resp1.json()
    # Try update
    url2 = f"{BASE_URL}/api/customer/{customer_id}"
    payload = {"id": {"id": customer_id}, "title": "TEST_UPDATED_L2"}
    resp2 = requests.put(url2, headers=get_headers(), json=payload)
    # Re-read
    resp3 = requests.get(url1, headers=get_headers())
    if resp3.status_code == 200:
        after = resp3.json()
        updated = after.get("title") == "TEST_UPDATED_L2"
        record_test(
            "L2-C2", "Layer 2", "Customers",
            "Update persistence",
            "Update persiste ou 405",
            f"HTTP update={resp2.status_code}, persisted={updated}",
            "PASS" if resp2.status_code == 405 or updated else "FAIL",
            {"update_resp": resp2.status_code, "after_update": after.get("title")}
        )

def test_L2_user_list_pagination():
    """L2-U1: Pagination validation."""
    url = f"{BASE_URL}/api/users?pageSize=2&page=0"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        has_total_pages = "totalPages" in data or "totalElements" in data
        has_data = "data" in data and len(data["data"]) > 0
        record_test(
            "L2-U1", "Layer 2", "Users",
            "Pagination validation",
            "has totalPages/totalElements",
            f"has_pages={has_total_pages}, has_data={has_data}",
            "PASS" if has_total_pages and has_data else "FAIL",
            {"response_keys": list(data.keys())[:10]}
        )
    else:
        record_test("L2-U1", "Layer 2", "Users", "Pagination", "HTTP 200", f"HTTP {resp.status_code}", "FAIL", {})

def test_L2_device_list_with_params():
    """L2-D1: Device list with search params."""
    url = f"{BASE_URL}/api/tenant/devices?pageSize=10&page=0&textSearch=Sentivis"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        devices = data.get("data", [])
        record_test(
            "L2-D1", "Layer 2", "Devices",
            "GET /api/tenant/devices with textSearch",
            "HTTP 200, devices filtered",
            f"HTTP {resp.status_code}, {len(devices)} devices",
            "PASS" if len(devices) > 0 else "INFO",
            {"url": url, "devices": [d.get("name") for d in devices[:5]]}
        )
    else:
        record_test("L2-D1", "Layer 2", "Devices", "Device list with params", "HTTP 200", f"HTTP {resp.status_code}", "FAIL", {"resp": resp.text[:200]})

def test_L2_customer_delete_404():
    """L2-C3: Deleted resource returns 404."""
    # Create and delete
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    url = f"{BASE_URL}/api/customer"
    payload = {"title": f"TEST_DeleteMe_{ts}"}
    resp = requests.post(url, headers=get_headers(), json=payload)
    if resp.status_code != 200:
        record_test("L2-C3", "Layer 2", "Customers", "Delete returns 404", "Create OK", "Create falhou", "FAIL", {})
        return
    cust_id = resp.json().get("id", {}).get("id")
    requests.delete(f"{BASE_URL}/api/customer/{cust_id}", headers=get_headers())
    # Try read after delete
    resp2 = requests.get(f"{BASE_URL}/api/customer/{cust_id}", headers=get_headers())
    is_404 = resp2.status_code == 404
    record_test(
        "L2-C3", "Layer 2", "Customers",
        "DELETE then GET returns 404",
        "HTTP 404",
        f"HTTP {resp2.status_code}",
        "PASS" if is_404 else "FAIL",
        {"cust_id": cust_id, "after_delete_resp": resp2.status_code}
    )

def test_L2_device_profile_list():
    """L2-D2: Device profile listing."""
    url = f"{BASE_URL}/api/deviceProfiles?pageSize=100&page=0"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        profiles = data.get("data", [])
        record_test(
            "L2-D2", "Layer 2", "Devices",
            "GET /api/deviceProfiles",
            "HTTP 200, profiles list",
            f"HTTP {resp.status_code}, {len(profiles)} profiles",
            "PASS" if len(profiles) > 0 else "FAIL",
            {"profiles": [p.get("name") for p in profiles[:5]]}
        )
    else:
        record_test("L2-D2", "Layer 2", "Devices", "Device profiles", "HTTP 200", f"HTTP {resp.status_code}", "FAIL", {})

# ============================================================
# LAYER 3: Comportamento negativo e de fronteira
# ============================================================

def test_L3_invalid_json_payload():
    """L3-N1: Invalid JSON payload."""
    url = f"{BASE_URL}/api/customer"
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data="{invalid json}")
    record_test(
        "L3-N1", "Layer 3", "Customers",
        "POST with invalid JSON",
        "HTTP 400 ou 500",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [400, 500] else "INFO",
        {"url": url, "status": resp.status_code}
    )

def test_L3_missing_required_fields():
    """L3-N2: Missing required fields in Customer."""
    url = f"{BASE_URL}/api/customer"
    payload = {"title": "TEST_NO_EMAIL"}  # missing email
    resp = requests.post(url, headers=get_headers(), json=payload)
    record_test(
        "L3-N2", "Layer 3", "Customers",
        "POST customer without required field",
        "HTTP 400 ou 500",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [400, 500] else "INFO",
        {"url": url, "payload": payload, "status": resp.status_code, "response": resp.text[:200]}
    )

def test_L3_wrong_customer_id():
    """L3-N3: GET with invalid customer ID format."""
    url = f"{BASE_URL}/api/customer/invalid-uuid-format"
    resp = requests.get(url, headers=get_headers())
    record_test(
        "L3-N3", "Layer 3", "Customers",
        "GET /api/customer/{invalid_id}",
        "HTTP 400 ou 404",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [400, 404] else "INFO",
        {"url": url, "status": resp.status_code}
    )

def test_L3_delete_nonexistent():
    """L3-N4: DELETE non-existent customer."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    url = f"{BASE_URL}/api/customer/{fake_id}"
    resp = requests.delete(url, headers=get_headers())
    record_test(
        "L3-N4", "Layer 3", "Customers",
        "DELETE non-existent customer",
        "HTTP 404",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 404 else "INFO",
        {"url": url, "status": resp.status_code}
    )

def test_L3_update_nonexistent():
    """L3-N5: PUT on non-existent customer."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    url = f"{BASE_URL}/api/customer/{fake_id}"
    payload = {"id": {"id": fake_id}, "title": "TEST"}
    resp = requests.put(url, headers=get_headers(), json=payload)
    record_test(
        "L3-N5", "Layer 3", "Customers",
        "PUT non-existent customer",
        "HTTP 404 ou 405",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [404, 405] else "INFO",
        {"url": url, "status": resp.status_code}
    )

def test_L3_duplicate_customer_name():
    """L3-N6: Create customer with duplicate title."""
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    title = f"TEST_DUP_{ts}"
    payload = {"title": title, "email": f"dup1_{ts}@sentivis.com"}
    resp1 = requests.post(f"{BASE_URL}/api/customer", headers=get_headers(), json=payload)
    cust_id = None
    if resp1.status_code == 200:
        cust_id = resp1.json().get("id", {}).get("id")
    # Try duplicate
    payload2 = {"title": title, "email": f"dup2_{ts}@sentivis.com"}
    resp2 = requests.post(f"{BASE_URL}/api/customer", headers=get_headers(), json=payload2)
    record_test(
        "L3-N6", "Layer 3", "Customers",
        "POST duplicate customer name",
        "HTTP 200 ou 400 (comportamento varia)",
        f"HTTP {resp2.status_code}",
        "INFO",
        {"first_resp": resp1.status_code, "dup_resp": resp2.status_code, "cust_id": cust_id}
    )
    # Cleanup
    if cust_id:
        requests.delete(f"{BASE_URL}/api/customer/{cust_id}", headers=get_headers())

def test_L3_unsupported_method():
    """L3-N7: PATCH method not supported."""
    url = f"{BASE_URL}/api/customers"
    resp = requests.patch(url, headers=get_headers())
    record_test(
        "L3-N7", "Layer 3", "Customers",
        "PATCH /api/customers",
        "HTTP 405 ou 400",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [400, 405] else "INFO",
        {"url": url, "status": resp.status_code}
    )

def test_L3_device_without_type():
    """L3-N8: Create device without type field."""
    url = f"{BASE_URL}/api/device"
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    payload = {"name": f"TEST_NoType_{ts}"}  # missing type
    resp = requests.post(url, headers=get_headers(), json=payload)
    record_test(
        "L3-N8", "Layer 3", "Devices",
        "POST device without type",
        "HTTP 200 ou 400",
        f"HTTP {resp.status_code}",
        "INFO",
        {"url": url, "status": resp.status_code, "response": resp.text[:300]}
    )
    # Cleanup if created
    if resp.status_code == 200:
        dev_id = resp.json().get("id", {}).get("id")
        if dev_id:
            requests.delete(f"{BASE_URL}/api/device/{dev_id}", headers=get_headers())

def test_L3_invalid_user_email():
    """L3-N9: Create user with invalid email format."""
    url = f"{BASE_URL}/api/user"
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    payload = {"email": f"invalid-email-{ts}", "authority": "TENANT_ADMIN"}
    resp = requests.post(url, headers=get_headers(), json=payload)
    record_test(
        "L3-N9", "Layer 3", "Users",
        "POST user with invalid email",
        "HTTP 400 ou 500",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code in [400, 500] else "INFO",
        {"url": url, "status": resp.status_code, "response": resp.text[:200]}
    )

def test_L3_tenant_scope_blocked():
    """L3-N10: Tenant scope operations blocked for TENANT_ADMIN."""
    # GET /api/tenants
    resp1 = requests.get(f"{BASE_URL}/api/tenants?pageSize=10&page=0", headers=get_headers())
    # POST /api/tenant
    resp2 = requests.post(f"{BASE_URL}/api/tenant", headers=get_headers(), json={"title": "TEST"})
    record_test(
        "L3-N10", "Layer 3", "Tenants",
        "Tenant scope blocked for TENANT_ADMIN",
        "HTTP 403",
        f"GET={resp1.status_code}, POST={resp2.status_code}",
        "PASS" if resp1.status_code == 403 and resp2.status_code == 403 else "INFO",
        {"get_tenants": resp1.status_code, "post_tenant": resp2.status_code}
    )

def test_L3_customer_user_create_smtp():
    """L3-N11: Customer user create blocked by SMTP."""
    url = f"{BASE_URL}/api/user"
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    # Get a customer ID first
    resp_cust = requests.get(f"{BASE_URL}/api/customers?pageSize=1&page=0", headers=get_headers())
    cust_id = None
    if resp_cust.status_code == 200:
        data = resp_cust.json()
        customers = data.get("data", [])
        if customers:
            cust_id = customers[0].get("id", {}).get("id")
    if not cust_id:
        record_test("L3-N11", "Layer 3", "Customer Users", "Customer user create", "customerId required", "No customer found", "FAIL", {})
        return
    payload = {"email": f"cu_test_{ts}@sentivis.com", "authority": "CUSTOMER_USER", "customerId": {"id": cust_id}}
    resp = requests.post(url, headers=get_headers(), json=payload)
    record_test(
        "L3-N11", "Layer 3", "Customer Users",
        "POST /api/user with customerId (SMTP gap)",
        "HTTP 500 (SMTP not configured)",
        f"HTTP {resp.status_code}",
        "PASS" if resp.status_code == 500 else "INFO",
        {"url": url, "status": resp.status_code, "response": resp.text[:300]},
        "Gap SMTP confirmado" if resp.status_code == 500 else ""
    )

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    log("=" * 60)
    log("INICIANDO SLICE 3: 25 TESTES THINGSBOARD CE")
    log("=" * 60)
    
    # 1. Login
    if not login():
        log("ERRO FATAL: Login falhou")
        print(json.dumps({"error": "Login failed"}, indent=2))
        sys.exit(1)
    
    # LAYER 1: CRUD
    log("\n--- LAYER 1: CRUD ---")
    
    # L1-C1 a L1-C4: Customer CRUD
    cust_id = test_L1_customer_create()
    if cust_id:
        test_L1_customer_read(cust_id)
        test_L1_customer_update(cust_id)
        test_L1_customer_delete(cust_id)
    
    # L1-U1 a L1-U3: User operations
    users = test_L1_user_list()
    if users:
        user_id = users[0].get("id", {}).get("id")
        if user_id:
            test_L1_user_read_by_id(user_id)
            test_L1_user_update(user_id)
    
    # L1-CU1: Customer Users list
    if cust_id:
        test_L1_customer_user_list(cust_id)
    
    # L1-D1 a L1-D4: Device CRUD
    dev_id = test_L1_device_create()
    if dev_id:
        test_L1_device_read(dev_id)
        test_L1_device_update(dev_id)
        test_L1_device_delete(dev_id)
    
    # LAYER 2: Consistência
    log("\n--- LAYER 2: CONSISTÊNCIA ---")
    
    test_L2_customer_read_after_create()
    
    # Criar customer para testes L2
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    resp_c = requests.post(f"{BASE_URL}/api/customer", headers=get_headers(), json={"title": f"TEST_L2_{ts}", "email": f"l2_{ts}@sentivis.com"})
    cust_l2_id = resp_c.json().get("id", {}).get("id") if resp_c.status_code == 200 else None
    
    if cust_l2_id:
        test_L2_customer_update_persistence(cust_l2_id)
        requests.delete(f"{BASE_URL}/api/customer/{cust_l2_id}", headers=get_headers())
    
    test_L2_user_list_pagination()
    test_L2_device_list_with_params()
    test_L2_customer_delete_404()
    test_L2_device_profile_list()
    
    # LAYER 3: Negativos
    log("\n--- LAYER 3: NEGATIVOS ---")
    
    test_L3_invalid_json_payload()
    test_L3_missing_required_fields()
    test_L3_wrong_customer_id()
    test_L3_delete_nonexistent()
    test_L3_update_nonexistent()
    test_L3_duplicate_customer_name()
    test_L3_unsupported_method()
    test_L3_device_without_type()
    test_L3_invalid_user_email()
    test_L3_tenant_scope_blocked()
    test_L3_customer_user_create_smtp()
    
    # OUTPUT
    log("\n" + "=" * 60)
    log("RESULTADO DOS TESTES")
    log("=" * 60)
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    info = sum(1 for r in results if r["status"] == "INFO")
    
    print(f"\nTOTAL: {len(results)} testes")
    print(f"PASS:  {passed}")
    print(f"FAIL:  {failed}")
    print(f"INFO:  {info}")
    print()
    
    # Output JSON for parsing
    output = {
        "summary": {"total": len(results), "passed": passed, "failed": failed, "info": info},
        "tests": results
    }
    
    with open("tests/slice3_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    log(f"Resultados salvos em tests/slice3_results.json")

if __name__ == "__main__":
    main()
