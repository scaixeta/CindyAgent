# Abrir Porta 5432 no Servidor ThingsBoard

## Objetivo
Permitir acesso remoto ao PostgreSQL do ThingsBoard para operações de DB.

## Credenciais
- **Host:** 204.168.202.5
- **Port:** 5432
- **User:** thingsboard
- **Password:** `<obter do .scr/.env>`
- **DB:** thingsboard

---

## Instruções

### 1. Acesse o servidor
```bash
ssh root@204.168.202.5
```

### 2. Firewall do SO

**Ubuntu/Debian:**
```bash
sudo ufw allow 5432/tcp
sudo ufw reload
```

**CentOS/RHEL:**
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload
```

### 3. Configurar PostgreSQL

Edite `/etc/postgresql/*/main/postgresql.conf`:
```properties
listen_addresses = '*'
```

Edite `/etc/postgresql/*/main/pg_hba.conf`:
```host
host all all 0.0.0.0/0 md5
host all all ::0/0 md5
```

### 4. Reiniciar PostgreSQL
```bash
sudo systemctl restart postgresql
```

### 5. Verificar
```bash
ss -tlnp | grep 5432
```

---

## Após abrir a porta

Retorne aqui para que eu possa:
1. Testar a conexão
2. Executar schema introspection
3. Aplicar update seguro no usuário
