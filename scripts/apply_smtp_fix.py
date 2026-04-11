#!/usr/bin/env python3
"""
Aplica correção SMTP via variáveis de ambiente no container Docker
"""
import paramiko
import sys

HETZNER_HOST = "204.168.202.5"
HETZNER_USER = "root"
HETZNER_PASSWORD = "XPpaUgECcFgx"

def main():
    print("=== APLICANDO CORRECAO SMTP ===")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HETZNER_HOST, username=HETZNER_USER, 
                   password=HETZNER_PASSWORD, timeout=30)
        print("[OK] SSH conectado")
        
        # Verificar se o ThingsBoard tem variáveis de ambiente SMTP
        stdin, stdout, stderr = ssh.exec_command(
            "docker exec thingsboard env | grep -i MAIL || echo NO_MAIL_VARS"
        )
        current_vars = stdout.read().decode()
        print(f"Variaveis de ambiente MAIL atuais: {current_vars[:200] if current_vars else '(vazio)'}")
        
        # Não é possível setar variáveis de ambiente em container em execução
        # A correção requer restart do container ou configuração via UI
        print("\n[INFO] Variaveis de ambiente nao podem ser setadas em container em execucao")
        print("[INFO] Opcoes de correcao:")
        print("  1. Reiniciar o container com novas variaveis")
        print("  2. Configurar via UI de System Admin")
        
        ssh.close()
        print("\n[RESULTADO] SMTP nao pode ser corrigido automaticamente via API ou env")
        print("[PROXIMO PASSO] Acao manual necessaria via Hetzner Web Console")
        
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())