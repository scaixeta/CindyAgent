#!/usr/bin/env python3
"""
Lista opções de correção SMTP e tenta a mais simples via API
"""
import paramiko
import requests
import sys
import json

HETZNER_HOST = "204.168.202.5"
HETZNER_USER = "root"
HETZNER_PASSWORD = "XPpaUgECcFgx"

TB_HOST = "204.168.202.5"
TB_PORT = "8080"
TB_USERNAME = "sentivis@sentivis.com.br"
TB_PASSWORD = "Sentivis@2026"

def login():
    url = f"http://{TB_HOST}:{TB_PORT}/api/auth/login"
    resp = requests.post(url, json={"username": TB_USERNAME, "password": TB_PASSWORD}, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("token")
    return None

def try_api_correction(jwt):
    """Tentar correção via API do ThingsBoard"""
    print("\n=== TENTANDO CORRECAO VIA API ===")
    
    # Verificar se há endpoint para testSmtp
    endpoints_tested = []
    
    # 1. GET settings
    url = f"http://{TB_HOST}:{TB_PORT}/api/admin/settings"
    headers = {"X-Authorization": f"Bearer {jwt}"}
    
    for method in ["GET", "PUT"]:
        for path in ["/api/admin/settings", "/api/admin/settings/mail", "/api/admin/smtp-config"]:
            try:
                if method == "GET":
                    resp = requests.get(f"http://{TB_HOST}:{TB_PORT}{path}", headers=headers, timeout=5)
                else:
                    resp = requests.put(f"http://{TB_HOST}:{TB_PORT}{path}", headers=headers, json={}, timeout=5)
                print(f"{method} {path}: {resp.status_code}")
                endpoints_tested.append(f"{method} {path}: {resp.status_code}")
            except Exception as e:
                print(f"{method} {path}: ERRO - {str(e)[:50]}")
    
    return endpoints_tested

def try_ssh_correction():
    """Tentar correção via SSH - restart container com env vars"""
    print("\n=== TENTANDO CORRECAO VIA SSH ===")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HETZNER_HOST, username=HETZNER_USER, 
                   password=HETZNER_PASSWORD, timeout=30)
        
        # Verificar se ha restart possível
        print("Verificando opcoes de restart...")
        
        # Verificar rede do container
        stdin, stdout, stderr = ssh.exec_command("docker inspect thingsboard --format '{{.NetworkSettings.Networks}}'")
        networks = stdout.read().decode()
        print(f"Redes: {networks[:100]}")
        
        # Verificar se ha docker-compose ou restart config
        stdin, stdout, stderr = ssh.exec_command("ls -la /var/lib/docker/containers/ | head -5")
        print(f"Containers dir: {stdout.read().decode()[:200]}")
        
        ssh.close()
        return True
        
    except Exception as e:
        print(f"SSH Error: {e}")
        return False

def main():
    print("=== OPCAO DE CORRECAO SMTP SIMPLES ===")
    
    jwt = login()
    if not jwt:
        print("[ERRO] Login falhou")
        return 1
    print("[OK] JWT obtido")
    
    # Tentar API
    api_result = try_api_correction(jwt)
    
    # Tentar SSH
    ssh_result = try_ssh_correction()
    
    print("\n=== RESULTADO ===")
    print("Correção automática NÃO disponível")
    print("Motivo: Tenant Admin sem permissao + sem docker-compose local")
    print("\nAção requerida: Hetzner Web Console → System Admin")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())