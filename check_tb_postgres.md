# Verificar PostgreSQL no Servidor ThingsBoard

Execute estes comandos no servidor **204.168.202.5** (como root):

## 1. Verificar se PostgreSQL está rodando
```bash
systemctl status postgresql
# ou
ps aux | grep postgres
```

## 2. Verificar portas em uso
```bash
ss -tlnp | grep postgres
# ou
netstat -tlnp | grep 5432
```

## 3. Verificar config do PostgreSQL
```bash
# Localize o arquivo postgresql.conf
find /etc -name "postgresql.conf" 2>/dev/null

# Mostre listen_addresses
grep listen_addresses /etc/postgresql/*/main/postgresql.conf
```

## 4. Verificar pg_hba.conf
```bash
cat /etc/postgresql/*/main/pg_hba.conf | grep -v "^#"
```

## 5. Testar conexão local
```bash
# Como usuário postgres
su - postgres -c "psql -c 'SELECT version();'"

# Ou como thingsboard
psql -U thingsboard -d thingsboard -c "SELECT 1;"
```

---

**Retorne a saída de cada comando para que eu possa analisar e fornecer os próximos passos.**
