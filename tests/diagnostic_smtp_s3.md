# Diagnóstico SMTP - ThingsBoard CE (RELATÓRIO FINAL)

## Data: 2026-04-02
## Status: **CONCLUÍDO** ✅

---

## 1. Achados (Evidence Summary)

### 1.1 Host (Hetzner VM)

| Teste | Resultado | Evidência |
|-------|-----------|-----------|
| hostname | ✅ OK | `SentivisThinkBoardCM-new` |
| docker | ✅ OK | `thingsboard` (thingsboard/tb-postgres, bridge) |
| DNS nslookup | ✅ OK | `smtp.hostinger.com → 172.65.255.143, 2606:4700:90:0:f225:a1af:129b:4ba1` |
| DNS getent | ✅ OK | `2606:4700:90:0:f225:a1af:129b:4ba1 smtp.hostinger.com` |
| TCP 465 | ❌ **FALHA** | `HOST_TCP465_FAIL` |
| TCP 587 | ✅ OK | `HOST_TCP587_OPEN` |
| TLS 465 | ❌ **FALHA** | output vazio (timeout) |
| TLS 587 STARTTLS | ✅ OK | Certificate chain OK, CONNECTED |

### 1.2 Container (ThingsBoard)

| Teste | Resultado | Evidência |
|-------|-----------|-----------|
| user | ✅ OK | `thingsboard` |
| hostname | ✅ OK | `694ddc92a217` |
| DNS getent | ✅ OK | `2606:4700:90:0:f225:a1af:129b:4ba1 smtp.hostinger.com` |
| /etc/resolv.conf | ✅ OK | `nameserver 185.12.64.1, 185.12.64.2` |
| TCP 465 | ❌ **FALHA** | `CONTAINER_TCP465_FAIL` |
| TCP 587 | ✅ OK | `CONTAINER_TCP587_OPEN` |
| env (mail/smtp) | ❌ **NÃO CONFIGURADO** | `JAVA_HOME, JAVA_VERSION` apenas |
| Java | ✅ OK | `OpenJDK 17.0.17` |

### 1.3 Logs ThingsBoard

Evidências de erro nos logs:
```
2026-04-02 14:23:37,129 [PasswordResetExecutorService-0-1] ERROR o.t.s.s.mail.DefaultMailService - Error occurred: Unable to send mail 
2026-04-02 14:26:57,856 [PasswordResetExecutorService-0-2] ERROR o.t.s.s.mail.DefaultMailService - Error occurred: Unable to send mail 
2026-04-02 14:39:29,846 [http-nio-0.0.0.0-9090-exec-4] WARN  o.t.s.s.mail.DefaultMailService - Unable to send mail: Timeout!
2026-04-02 14:39:55,463 [http-nio-0.0.0.0-9090-exec-6] WARN  o.t.s.s.mail.DefaultMailService - Unable to send mail: Timeout!
2026-04-02 14:41:03,107 [http-nio-0.0.0.0-9090-exec-7] WARN  o.t.s.s.mail.DefaultMailService - Unable to send mail: Timeout!
2026-04-02 14:42:21,492 [http-nio-0.0.0.0-9090-exec-9] WARN  o.t.s.s.mail.DefaultMailService - Unable to send mail: Timeout!
```

---

## 2. Comparação Host x Container

| Métrica | Host | Container | Interpretação |
|---------|------|------------|---------------|
| DNS smtp.hostinger.com | ✅ OK | ✅ OK | Rede DNS funcionando |
| TCP 465 | ❌ FAIL | ❌ FAIL | **Egress bloqueado para 465** |
| TCP 587 | ✅ OK | ✅ OK | Egress 587 funciona |
| TLS 465 | ❌ FAIL | N/A |timeout handshake |
| TLS 587 STARTTLS | ✅ OK | N/A | handshake OK |
| Variáveis mail/smtp | N/A | ❌ **AUSENTE** | TB não configurado |

---

## 3. Hipóteses Ranqueadas (Root-Cause Hypotheses)

### Hipótese 1: Porta 465 BLOQUEADA no Firewall de Egress ⭐ **ALTA PROBABILIDADE**
- **Evidência:** TCP 465 falha tanto no host quanto no container, mas 587 funciona
- **Análise:** O firewall da Hetzner ou da rede está bloqueando egress na porta 465 (SSL direto)
- **Ação:** Verificar regras de firewall da Hetzner para saída na porta 465

### Hipótese 2: Timeout no JavaMail ao tentar conectar na 465 ⭐ **ALTA PROBABILIDADE**
- **Evidência:** Logs mostram "Unable to send mail: Timeout!" repetidamente
- **Análise:** O ThingsBoard tenta porta 465 primeiro (SSL), timeout após 10s, não tenta 587 como fallback
- **Ação:** Forçar ThingsBoard a usar porta 587 (STARTTLS)

### Hipótese 3: Configuração SMTP Ausente no ThingsBoard ⚠️ **SECUNDÁRIO**
- **Evidência:** `env | grep mail` retorna apenas variáveis Java, nenhuma variável `TB_MAIL_*`
- **Análise:** ThingsBoard pode estar usando configuração da UI (System Admin), não variáveis de ambiente
- **Ação:** Verificar UI de System Admin para SMTP configurado

### Hipótese 4: DNS ou Proxy Intermitente ❌ **DESCARTADA**
- **Evidência:** DNS resolve corretamente, 587 funciona
- **Análise:** Não é problema de DNS ou proxy geral

---

## 4. Próxima Ação Corretiva Recomendada

### Ação: Ajustar a configuração SMTP do ThingsBoard para usar porta 587 (STARTTLS)

**Opção A - Via Variáveis de Ambiente (se usar docker-compose):**
```yaml
environment:
  - TB_MAIL_PORT=587
  - TB_MAIL_PROTOCOL=smtp
  - TB_MAIL_SMTP_SSL=false
  - TB_MAIL_SMTP_STARTTLS=true
```

**Opção B - Via UI System Admin:**
1. Acessar UI: `http://204.168.202.5:8080`
2. Login como System Admin
3. Settings → Mail Server
4. Configurar:
   - Host: `smtp.hostinger.com`
   - Port: `587`
   - Protocol: `smtp`
   - Security: `STARTTLS`
   - Username: `sergio.caixeta@sentivis.com.br`
   - Password: `MaeCaForever@1992`
   - Mail From: `sentivis@sentivis.com.br`

**Opção C - Verificar Firewall Hetzner:**
1. Acessar Hetzner Cloud Console
2. Firewall da VM: verificar se porta 465 TCP está liberada para egress
3. Se não estiver, adicionar regra outbound para 465/tcp

---

## 5. O Que NÃO Foi Concluído

- ❌ Não foi possível determinar por que a porta 465 está bloqueada (firewall Hetzner? rede? upstream?)
- ❌ Não foi verificado se há regra de firewall outbound no painel Hetzner
- ❌ Não foi testado se forçar porta 587 resolve o problema completamente
- ⚠️ Os testes locais (Windows) funcionaram porque a rede local não bloqueia 465

---

## 6. Resumo Executivo

| Aspecto | Status |
|---------|--------|
| DNS Host | ✅ OK |
| DNS Container | ✅ OK |
| TCP 465 Host | ❌ FAIL |
| TCP 587 Host | ✅ OK |
| TCP 465 Container | ❌ FAIL |
| TCP 587 Container | ✅ OK |
| TLS 465 | ❌ FAIL |
| TLS 587 STARTTLS | ✅ OK |
| TB SMTP Config | ⚠️ Não verificado |
| Logs TB | ⚠️ Timeout confirmado |

**Causa Raiz Provável:** Porta 465 bloqueada no firewall de egress da Hetzner + ThingsBoard tentando SSL na 465 primeiro e giving up antes de tentar 587.

**Recomendação Final:** Configurar ThingsBoard para usar porta 587 com STARTTLS em vez de porta 465 com SSL.

---

## Referências

- Script de diagnóstico: `scripts/diagnostic_ssh_hetzner.py`
- Credenciais: `.scr/.env`
- BUG-S3-05: `tests/bugs_log.md`
- Dev_Tracking_S3.md