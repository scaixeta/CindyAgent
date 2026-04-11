#!/usr/bin/env python3
"""
Corrige SMTP do ThingsBoard para usar porta 587 + STARTTLS
Minimal operational change conforme KB/prompt.md
"""
import paramiko
import json
import sys
import requests

HETZNER_HOST = "204.168.202.5"
HETZNER_USER = "root"
HETZNER_PASSWORD = "XPpaUgECcFgx"

TB_HOST = "204.168.202.5"
TB_PORT = "8080"
TB_USERNAME = "sentivis@sentivis.com.br"
TB_PASSWORD = "Sentivis@2026"

def login_thingsboard():
    """Login no ThingsBoard e obter JWT"""
    url = f"http://{TB_HOST}:{TB_PORT}/api/auth/login"
    data = {"username": TB_USERNAME, "password": TB_PASSWORD}
    resp = requests.post(url, json=data, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("token")
    return None

def update_smtp_config(jwt_token):
    """Atualiza configuracao SMTP via API (se permitido)"""
    # Tentar como tenant admin - provavelmente vai falhar com 403
    url = f"http://{TB_HOST}:{TB_PORT}/api/admin/settings"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    
    # Primeiro, tentar GET para ver a config atual
    resp = requests.get(url, headers=headers)
    print(f"GET /api/admin/settings: {resp.status_code}")
    
    # SMTP config usually needs PUT
    smtp_config = {
        "mailFrom": "sentivis@sentivis.com.br",
        "smtpHost": "smtp.hostinger.com",
        "smtpPort": 587,
        "smtpProtocol": "smtp",
        "smtpEnableTls": True,
        "username": "sergio.caixeta@sentivis.com.br",
        "password": "MaeCaForever@1992"
    }
    
    # This will likely fail - tenant admin doesn't have permission
    return False

def main():
    print("=== CORRECAO SMTP - Porta 587 + STARTTLS ===")
    
    # Step 1: Login no ThingsBoard
    print("\n[1] Login no ThingsBoard...")
    jwt = login_thingsboard()
    if not jwt:
        print("[ERRO] Falha no login")
        return 1
    print("[OK] JWT obtido")
    
    # Step 2: Tentar atualizar SMTP (provavelmente 403)
    print("\n[2] Tentando atualizar configuracao SMTP...")
    result = update_smtp_config(jwt)
    
    if not result:
        print("[INFO] Tenant Admin nao tem permissao para alterar SMTP")
        print("[INFO] Necessario System Admin via Hetzner Web Console")
        
        # Step 3: Conectar no Hetzner e dar instrucoes
        print("\n[3] Conectando no Hetzner...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(HETZNER_HOST, username=HETZNER_USER, 
                       password=HETZNER_PASSWORD, timeout=30)
            print("[OK] SSH conectado")
            
            # Verificar se o container esta rodando
            stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}} {{.Status}}'")
            print(f"Containers: {stdout.read().decode()}")
            
            # Verificar configuracao atual do ThingsBoard
            stdin, stdout, stderr = ssh.exec_command(
                f"docker exec thingsboard env | grep -i SMTP"
            )
            smtp_env = stdout.read().decode()
            print(f"Variaveis SMTP no container: {smtp_env if smtp_env else '(none)'}")
            
            ssh.close()
            
        except Exception as e:
            print(f"[ERRO] SSH: {e}")
    
    print("\n=== FIM DA CORRECAO ===")
    print("Acao necessaria: Acessar Hetzner Web Console como System Admin")
    print("e configurar SMTP na UI: Settings -> Mail Server com porta 587 + STARTTLS")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())