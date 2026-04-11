Relatório técnico consolidado com base nas páginas oficiais espelhadas do ThingsBoard CE presentes no workspace (`knowledge/thingsboard/ce`), cobrindo HTTP Device API, REST API administrativa, Swagger UI, telemetry, attributes e consulta de dados armazenados. Não houve implementação, commit, push nem exposição de credenciais.

# Relatório técnico — Validação prévia da API do ThingsBoard CE para o Sentivis IAOps

## 1. Entendimento

O ecossistema de API do ThingsBoard CE, conforme a documentação oficial, é composto por **duas camadas principais** relevantes para o nosso MVP:

### 1.1 Device API
É a camada usada pelo **dispositivo** para se comunicar com a plataforma. No recorte desta análise, a trilha mais importante é a **HTTP Device API**.

Ela permite, entre outros:
- enviar telemetry do device para a plataforma;
- enviar client-side attributes;
- consultar shared attributes e client-side attributes;
- receber updates de shared attributes por polling HTTP;
- executar fluxos de RPC e provisioning.

Na HTTP Device API, a autenticação é feita por **Access Token do device**, embutido na URL da requisição.

### 1.2 Administrative REST API
É a camada usada por **usuários/automações administrativas** para gerenciar entidades e consultar dados da plataforma.

Ela permite:
- autenticar usuário;
- gerenciar devices e outras entidades;
- consultar atributos e telemetry persistidos;
- explorar schemas e endpoints via Swagger UI.

Na REST API administrativa, a autenticação é feita por **JWT Bearer** (documentado) e também por **API Key** nas versões/documentação em que esse recurso aparece.

---

## 2. Estrutura da API

### 2.1 Onde encontrar a estrutura da API
A documentação oficial indica dois pontos principais:

- **HTTP Device API**: documentação específica do protocolo em `reference/http-api`;
- **REST API administrativa**: documentação geral em `reference/rest-api`.

Além disso, a consulta de dados de telemetry/attributes aparece documentada nas páginas funcionais de:
- `user-guide/telemetry`;
- `user-guide/attributes`;
- `user-guide/ui/devices`.

### 2.2 Papel do Swagger UI
A documentação oficial informa que o ThingsBoard inclui documentação interativa baseada em **Swagger UI** para a REST API.

Funções confirmadas do Swagger UI:
- navegar endpoints disponíveis;
- inspecionar request/response schemas;
- testar chamadas diretamente no navegador;
- autenticar como usuário específico.

### 2.3 URL do Swagger UI
A página oficial de REST API documenta que cada instância hospeda o Swagger em:

```text
http://$THINGSBOARD_HOST:PORT/swagger-ui.html
```

Para o ambiente local do projeto, isso implica estruturalmente:

```text
http://204.168.202.5:8080/swagger-ui.html
```

> Isso é consistente com a documentação oficial; a validação manual no ambiente real ainda deve ser executada antes de promover esse acesso como evidência operacional concluída.

### 2.4 Como a autenticação funciona por camada

#### Device API (HTTP)
Autenticação por **Access Token do device** na própria URL:

```text
/api/v1/$ACCESS_TOKEN/...
```

#### REST API administrativa
Autenticação documentada por login em:

```text
/api/auth/login
```

com retorno de:

```json
{"token":"$YOUR_JWT_TOKEN", "refreshToken":"$YOUR_JWT_REFRESH_TOKEN"}
```

Depois disso, as chamadas usam header:

```text
X-Authorization: Bearer $YOUR_JWT_TOKEN
```

A doc também registra suporte a API key via:

```text
X-Authorization: ApiKey $YOUR_API_KEY_VALUE
```

---

## 3. Fluxo de dados

### 3.1 Como um device envia telemetry
Na HTTP Device API, o endpoint oficial para envio de telemetry é:

```text
POST /api/v1/$ACCESS_TOKEN/telemetry
```

Exemplo documentado sem timestamp explícito:

```json
{"temperature":42,"humidity":73}
```

Exemplo documentado com timestamp explícito:

```json
{
  "ts": 1451649600512,
  "values": {
    "temperature": 42.2,
    "humidity": 70
  }
}
```

Comportamento confirmado pela documentação:
- se o payload não trouxer `ts`, o servidor atribui o timestamp do lado servidor;
- se o payload trouxer `ts`, o valor é tratado como timestamp da telemetry.

### 3.2 Como attributes diferem de telemetry
A documentação oficial diferencia claramente:

#### Telemetry
- é **time-series data**;
- representa leituras ao longo do tempo;
- é modelada como pares chave-valor com timestamp;
- serve para histórico, latest values, agregação e dashboarding temporal.

#### Attributes
- são **key-value pairs não orientados a série temporal histórica** no mesmo sentido da telemetry;
- guardam propriedades estáticas ou semi-estáticas;
- existem em três tipos:
  - `server-side`;
  - `shared`;
  - `client-side`.

Resumo funcional:
- **temperature** e **humidity** para o MVP devem ser tratadas como **telemetry**;
- parâmetros de configuração do device devem tender a **shared attributes**;
- estado semi-estático do device pode ir em **client-side attributes**;
- configurações administrativas/metadata tendem a **server-side attributes**.

### 3.3 O que acontece com temperature e humidity na plataforma
Para o fluxo do MVP:
1. o device/mock envia `temperature` e `humidity` via HTTP Device API;
2. o ThingsBoard recebe a mensagem;
3. a mensagem entra no pipeline da plataforma / Rule Engine;
4. a telemetry é persistida como time-series data;
5. os valores passam a aparecer em áreas como:
   - **Latest telemetry** do device;
   - dashboards/widgets;
   - APIs de consulta de latest e histórico.

A documentação também registra que a Rule Engine pode:
- validar telemetry antes de persistir;
- enriquecer mensagens;
- gerar alarmes;
- salvar time-series.

---

## 4. Consulta e retorno de dados

### 4.1 Como dados armazenados podem ser consultados
A documentação oficial da Telemetry/Data Query API expõe endpoints REST administrativos do tipo:

#### Listar chaves de telemetry
```text
GET /api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries
```

#### Obter latest telemetry
```text
GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries?keys=key1,key2,key3
```

#### Obter telemetry histórica
```text
GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries?keys=key1,key2,key3&startTs=...&endTs=...&interval=...&limit=...&agg=AVG
```

Parâmetros históricos confirmados:
- `keys`
- `startTs`
- `endTs`
- `interval`
- `agg` (`MIN`, `MAX`, `AVG`, `SUM`, `COUNT`, `NONE`)
- `limit`

### 4.2 O que “latest telemetry” significa
Pela documentação de UI e telemetry:
- “Latest telemetry” representa os **últimos valores conhecidos** de determinadas chaves de telemetry para a entidade;
- não é a série histórica inteira;
- é a visão operacional do último estado observado para cada key.

No caso do MVP, isso equivale a algo como:
- último `temperature` recebido;
- último `humidity` recebido.

### 4.3 Que APIs ou áreas da UI expõem esses valores
Os valores aparecem em:

#### UI
- **Entities > Devices > [device] > Latest telemetry**;
- dashboards/widgets configurados para latest values ou histórico.

#### REST API administrativa
- endpoints `/api/plugins/telemetry/.../values/timeseries`;
- endpoints de attributes em `/api/plugins/telemetry/.../values/attributes/...`.

#### Swagger UI
A doc afirma que a API de consulta de telemetry/attributes está disponível via Swagger UI.

---

## 5. Aplicação no Sentivis

### 5.1 Qual é o caminho correto de API para a Fase 1
Para a fase atual do projeto — **mock-based validation**, sem hardware real e sem n8n ainda — o caminho correto e mais simples é:

```text
HTTP Device API -> POST /api/v1/$ACCESS_TOKEN/telemetry
```

Payload mínimo aderente ao escopo atual:

```json
{
  "temperature": 25,
  "humidity": 60
}
```

Ou, se quisermos controlar timestamp explicitamente:

```json
{
  "ts": 1451649600512,
  "values": {
    "temperature": 25,
    "humidity": 60
  }
}
```

### 5.2 HTTP Device API é a primeira etapa correta?
**Sim.** Para a Fase 1 do Sentivis, a HTTP Device API é a trilha mais adequada porque:
- trabalha no nível do device/mock;
- usa Access Token do device, evitando complexidade administrativa inicial;
- permite validar o backbone mínimo `mock -> ThingsBoard -> Latest telemetry`;
- mantém baixo acoplamento;
- é consistente com o objetivo atual de validar apenas temperature e humidity.

### 5.3 O que deve esperar para depois
Deve ficar para etapa posterior:
- integração n8n remota;
- automação administrativa mais ampla via REST API de gestão;
- modelagem expandida de atributos/configuração complexa;
- hardware real;
- fluxos avançados de RPC, provisioning e rule chains mais sofisticadas;
- consultas históricas complexas e agregações operacionais mais pesadas, depois da validação mínima de ingestão.

---

## 6. Confirmado vs Pendente

### Confirmado
Com base na documentação oficial espelhada consultada:

- O ThingsBoard CE separa **Device API** e **REST API administrativa**.
- A **HTTP Device API** usa autenticação por **Access Token** do device.
- O endpoint oficial para envio de telemetry por HTTP é:
  ```text
  /api/v1/$ACCESS_TOKEN/telemetry
  ```
- A HTTP Device API aceita payload simples sem timestamp e payload com `ts` + `values`.
- O endpoint oficial para publicação de client-side attributes por HTTP é:
  ```text
  /api/v1/$ACCESS_TOKEN/attributes
  ```
- O endpoint oficial para requisição de attributes pelo device é:
  ```text
  /api/v1/$ACCESS_TOKEN/attributes?clientKeys=...&sharedKeys=...
  ```
- O ThingsBoard distingue `server-side`, `shared` e `client-side` attributes.
- `shared attributes` são voltados a configuração do device do lado servidor para o device.
- `client-side attributes` podem ser publicados pelo device.
- A REST API administrativa usa autenticação JWT via `/api/auth/login` e header `X-Authorization: Bearer ...`.
- A documentação oficial também descreve exploração da API via **Swagger UI**.
- O Swagger UI da instância é documentado em `/swagger-ui.html`.
- A Data Query API administrativa usa endpoints sob `/api/plugins/telemetry/...`.
- “Latest telemetry” é a visão dos últimos valores conhecidos por chave.
- A UI do device expõe abas de **Attributes** e **Latest telemetry**.

### Inferido
Inferências razoáveis, mas ainda dependentes de validação operacional no ambiente do projeto:

- Para o Sentivis Phase 1, o fluxo mais seguro é `mock HTTP -> device token -> telemetry ingest -> Latest telemetry`.
- `temperature` e `humidity` devem ser modeladas como telemetry, não como attributes.
- O endpoint do Swagger do host do projeto provavelmente é:
  ```text
  http://204.168.202.5:8080/swagger-ui.html
  ```
- A trilha inicial de validação manual pode ser feita primeiro só com `temperature` e `humidity`, sem necessidade de rule chain custom inicial.

### Pendente de validação
Itens que **não devem ser promovidos a verdade operacional final** sem teste manual no ambiente real:

- se a instância atual do projeto está com Swagger UI habilitado e acessível externamente;
- se o device `Sentivis | 0001` já possui Access Token pronto para uso operacional nesta fase;
- se a instância atual aplica alguma regra de validação/transformação no Rule Engine que altere o comportamento padrão da ingestão;
- qual é o formato final de resposta observado na prática para queries específicas no ambiente atual;
- quais constraints de retenção/TTL estão ativos na instância do projeto;
- se haverá necessidade de timestamps explícitos no mock desde o primeiro teste, ou se o timestamp de servidor é suficiente para a Fase 1.

---

## 7. Recomendação

A próxima etapa técnica segura para o projeto é:

### Etapa recomendada
**Validação manual controlada da HTTP Device API**, sem n8n e sem simulador completo ainda.

### Sequência sugerida
1. confirmar o Access Token do device de teste;
2. executar um `POST /api/v1/$ACCESS_TOKEN/telemetry` com payload mínimo de `temperature` e `humidity`;
3. verificar o resultado em **Latest telemetry** na UI do device;
4. validar, em seguida, a consulta administrativa de latest values via REST API;
5. só depois disso avançar para desenho do workflow remoto em n8n.

### Justificativa
Essa sequência:
- reduz acoplamento;
- valida primeiro o backbone real da plataforma;
- separa ingestão de device da automação administrativa;
- evita introduzir n8n antes de entender o comportamento confirmado da API.

## Fontes oficiais consultadas no espelho local
- `knowledge/thingsboard/ce/api/http-api.md`
- `knowledge/thingsboard/ce/api/rest-api.md`
- `knowledge/thingsboard/ce/user-guide/telemetry.md`
- `knowledge/thingsboard/ce/user-guide/attributes.md`
- `knowledge/thingsboard/ce/user-guide/ui/devices.md`
- `knowledge/thingsboard/ce/user-guide/access-token.md`