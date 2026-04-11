#!/usr/bin/env python3
"""
Diagnóstico SMTP - ThingsBoard CE no Hetzner
Executa testes de rede host vs container
"""
import paramiko
import sys
import time

# Credenciais do .scr/.env
HETZNER_HOST = "204.168.202.5"
HETZNER_USER = "root"
HETZNER_PASSWORD = "XPpaUgECcFgx"  # HETZNER_ROOT_PASSWORD_TEMP
CONTAINER_NAME = "thingsboard"

def run_ssh_command(ssh, command, timeout=30):
    """Executa comando SSH e retorna stdout/stderr"""
    print(f"\n>>> Executando: {command}")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    stdout_str = stdout.read().decode('utf-8', errors='replace')
    stderr_str = stderr.read().decode('utf-8', errors='replace')
    return stdout_str, stderr_str

def main():
    print("=" * 60)
    print("DIAGNÓSTICO SMTP - THINGSBOARD CE (HETZNER)")
    print("=" * 60)
    
    # Conectar SSH
    print(f"\n[1] Conectando em {HETZNER_HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HETZNER_HOST, username=HETZNER_USER, password=HETZNER_PASSWORD, 
                    timeout=30, allow_agent=False, look_for_keys=False)
        print("[OK] SSH conectado com sucesso!")
    except Exception as e:
        print(f"[ERRO] Falha ao conectar SSH: {e}")
        return 1
    
    # STEP 1: Host identity e baseline
    print("\n" + "=" * 60)
    print("STEP 1: HOST IDENTITY E BASELINE")
    print("=" * 60)
    
    stdout, stderr = run_ssh_command(ssh, "whoami")
    print(f"whoami: {stdout.strip()}")
    
    stdout, stderr = run_ssh_command(ssh, "hostname")
    print(f"hostname: {stdout.strip()}")
    
    stdout, stderr = run_ssh_command(ssh, "date")
    print(f"date: {stdout.strip()}")
    
    stdout, stderr = run_ssh_command(ssh, "docker ps --format '{{.Names}} {{.Status}}'")
    print(f"docker ps:\n{stdout}")
    
    stdout, stderr = run_ssh_command(ssh, f"docker inspect {CONTAINER_NAME} --format '{{{{.Name}}}} {{{{.Config.Image}}}} {{{{.HostConfig.NetworkMode}}}}'")
    print(f"docker inspect:\n{stdout}")
    
    # STEP 2: Host DNS e TCP reachability
    print("\n" + "=" * 60)
    print("STEP 2: HOST DNS E TCP REACHABILITY")
    print("=" * 60)
    
    stdout, stderr = run_ssh_command(ssh, "nslookup smtp.hostinger.com")
    print(f"nslookup:\n{stdout}")
    
    stdout, stderr = run_ssh_command(ssh, "getent hosts smtp.hostinger.com || true")
    print(f"getent hosts: {stdout.strip()}")
    
    # TCP 465
    stdout, stderr = run_ssh_command(ssh, "timeout 10 bash -lc 'cat < /dev/null > /dev/tcp/smtp.hostinger.com/465' && echo HOST_TCP465_OPEN || echo HOST_TCP465_FAIL")
    print(f"TCP 465: {stdout.strip()}")
    
    # TCP 587
    stdout, stderr = run_ssh_command(ssh, "timeout 10 bash -lc 'cat < /dev/null > /dev/tcp/smtp.hostinger.com/587' && echo HOST_TCP587_OPEN || echo HOST_TCP587_FAIL")
    print(f"TCP 587: {stdout.strip()}")
    
    # STEP 3: Host TLS/STARTTLS handshake
    print("\n" + "=" * 60)
    print("STEP 3: HOST TLS/STARTTLS HANDSHAKE")
    print("=" * 60)
    
    stdout, stderr = run_ssh_command(ssh, "timeout 15 openssl s_client -connect smtp.hostinger.com:465 -servername smtp.hostinger.com </dev/null 2>&1 | head -n 30")
    print(f"TLS 465:\n{stdout}")
    
    stdout, stderr = run_ssh_command(ssh, "timeout 15 openssl s_client -starttls smtp -connect smtp.hostinger.com:587 -servername smtp.hostinger.com </dev/null 2>&1 | head -n 30")
    print(f"STARTTLS 587:\n{stdout}")
    
    # STEP 4-7: Container checks
    print("\n" + "=" * 60)
    print("STEP 4-7: CONTAINER CHECKS")
    print("=" * 60)
    
    # Verificar se bash existe no container
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} which bash 2>/dev/null || echo NO_BASH")
    has_bash = "NO_BASH" not in stdout
    
    # Container identity
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} whoami 2>/dev/null || echo 'exec failed'")
    print(f"Container whoami: {stdout.strip()}")
    
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} hostname 2>/dev/null || echo 'exec failed'")
    print(f"Container hostname: {stdout.strip()}")
    
    # Container DNS
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} getent hosts smtp.hostinger.com 2>/dev/null || docker exec {CONTAINER_NAME} nslookup smtp.hostinger.com 2>/dev/null || echo 'DNS_FAILED'")
    print(f"Container DNS: {stdout.strip()}")
    
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} cat /etc/resolv.conf 2>/dev/null || echo 'resolv.conf failed'")
    print(f"Container /etc/resolv.conf:\n{stdout}")
    
    # Container TCP
    if has_bash:
        cmd_465 = f"docker exec {CONTAINER_NAME} bash -c \"timeout 10 bash -lc 'cat < /dev/null > /dev/tcp/smtp.hostinger.com/465' && echo CONTAINER_TCP465_OPEN || echo CONTAINER_TCP465_FAIL\""
        stdout, stderr = run_ssh_command(ssh, cmd_465)
        print(f"Container TCP 465: {stdout.strip()}")
        
        cmd_587 = f"docker exec {CONTAINER_NAME} bash -c \"timeout 10 bash -lc 'cat < /dev/null > /dev/tcp/smtp.hostinger.com/587' && echo CONTAINER_TCP587_OPEN || echo CONTAINER_TCP587_FAIL\""
        stdout, stderr = run_ssh_command(ssh, cmd_587)
        print(f"Container TCP 587: {stdout.strip()}")
    else:
        # Fallback: usar sh ou netcat
        print("bash não disponível, tentando netcat ou curl...")
        cmd_465 = f"docker exec {CONTAINER_NAME} sh -c \"timeout 10 bash -lc 'cat < /dev/null > /dev/tcp/smtp.hostinger.com/465' && echo CONTAINER_TCP465_OPEN || echo CONTAINER_TCP465_FAIL\" 2>/dev/null || echo 'CONTAINER_TCP465_FAILED'"
        stdout, stderr = run_ssh_command(ssh, cmd_465)
        print(f"Container TCP 465 (fallback): {stdout.strip()}")
    
    # Container env
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} env | grep -i -E 'mail|smtp|proxy|java|tb_' 2>/dev/null || echo 'env grep failed'")
    print(f"Container env (mail/smtp/proxy):\n{stdout}")
    
    stdout, stderr = run_ssh_command(ssh, f"docker exec {CONTAINER_NAME} java -version 2>&1 | head -n 3")
    print(f"Container Java version:\n{stdout}")
    
    # STEP 8: Logs do ThingsBoard
    print("\n" + "=" * 60)
    print("STEP 8: LOGS DO THINGSBOARD")
    print("=" * 60)
    
    stdout, stderr = run_ssh_command(ssh, f"docker logs --tail 500 {CONTAINER_NAME} 2>&1 | grep -i -E 'mail|smtp|timeout|socket|dns|ssl|tls|hostinger|javax.mail|jakarta.mail' | tail -n 100")
    print(f"Logs (mail/smtp/timeout):\n{stdout}")
    
    if not stdout.strip():
        print("(nenhum match encontrado)")
        stdout, stderr = run_ssh_command(ssh, f"docker logs --tail 50 {CONTAINER_NAME} 2>&1")
        print(f"Ultimos 50 logs:\n{stdout}")
    
    # Fechar SSH
    ssh.close()
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO CONCLUIDO")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
