# ThingsBoard CE - Modelagem Sentivis para MLE

## Objetivo

Este documento consolida uma proposta pratica para modelar o dominio Sentivis no ThingsBoard CE, usando apenas capacidades suportadas pela documentacao local e pelo ambiente validado no workspace.

O foco aqui e:

- representar Sentivis como tenant principal;
- organizar estados, cidades, fazendas, sedes regionais e regioes de influencia;
- separar controle de acesso de modelagem de negocio;
- indicar quais CRUDs e operacoes sao viaveis;
- indicar o que pode ser administrado por automacao/MCP;
- deixar claro o que e limitacao do ThingsBoard CE e o que e decisao de modelagem.

## Premissas

- Sentivis e o `Tenant`.
- Os dados operacionais entram no tenant da Sentivis.
- Clientes finais, cooperativas, fazendas e outras entidades do dominio podem nao coincidir com a fronteira de permissao.
- Uma fazenda pode:
  - ser cliente;
  - nao ser cliente;
  - ter multiplas sedes;
  - estar associada a mais de uma cidade/regiao de influencia;
  - participar de uma ou mais cooperativas.

## Base documental usada

- `knowledge/thingsboard/ce/user-guide/entities-and-relations.md`
- `knowledge/thingsboard/ce/user-guide/attributes.md`
- `knowledge/thingsboard/ce/user-guide/ui/assets.md`
- `knowledge/thingsboard/ce/user-guide/ui/customers.md`
- `knowledge/thingsboard/ce/user-guide/ui/users.md`
- `knowledge/thingsboard/ce/user-guide/ui/tenants.md`
- `knowledge/thingsboard/ce/user-guide/ui/devices.md`
- `knowledge/thingsboard/ce/user-guide/entity-views.md`
- `knowledge/thingsboard/ce/user-guide/asset-profiles.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/OPERATIONS.md`
- `KB/SwaggerTB.md`

## O que o ThingsBoard CE faz bem aqui

Pelos manuais, o ThingsBoard CE suporta muito bem:

- `Tenant` como entidade-raiz de negocio.
- `Customers` como fronteira de acesso/visibilidade.
- `Users` em tres niveis:
  - `SYS_ADMIN`
  - `TENANT_ADMIN`
  - `CUSTOMER_USER`
- `Assets` para representar objetos abstratos:
  - fazenda
  - sede regional
  - cidade
  - estado
  - cooperativa
  - regiao de influencia
- `Devices` para sensores, gateways, tratores conectados, estacoes climaticas etc.
- `Relations` direcionais entre entidades do mesmo tenant.
- `Attributes` para metadata e configuracao.
- `Dashboards` para operacao e visualizacao.
- `Entity Views` para compartilhar apenas parte dos dados de um asset/device para clientes especificos.

## Limites reais do CE

Os limites mais importantes para o seu caso sao:

- `Customer` no CE nao deve ser tratado como subestrutura organizacional arbitraria.
- `Customer User` nao cria subcustomers no CE.
- `Entity Groups` e certas opcoes avancadas de ownership/grupos sao PE, nao CE.
- Algumas rotas REST via `PUT` nao sao o caminho correto nesta instancia:
  - update de user foi validado via `POST /api/user` com `id`;
  - `PUT /api/user/{id}` retorna `405` e nao deve ser usado como metodo principal.
- Configuracoes globais exigem `SYS_ADMIN`.

## Principio de modelagem recomendado

A recomendacao central e esta:

- use `Customer` para `acesso e contrato`;
- use `Asset` para `dominio de negocio e geografia`;
- use `Relation` para representar a malha real, inclusive quando ela nao for uma arvore simples;
- use `Entity View` quando um mesmo ativo/dispositivo precisar ser visto por mais de um cliente com recorte parcial;
- use `Attributes` para tags, classificacao, identificadores externos e parametros operacionais.

Em outras palavras:

- geografia e estrutura operacional nao devem ser empurradas para `Customer`;
- `Customer` deve existir quando fizer sentido de permissao, comercial ou segregacao de visualizacao;
- fazenda, cidade, estado, sede e cooperativa devem existir como entidades do dominio, preferencialmente `Assets`.

## Modelo recomendado para a Sentivis

### 1. Raiz

- `Tenant`: `Sentivis`

Tudo fica dentro do tenant da Sentivis.

### 2. Entidades de negocio como Assets

Recomendo criar `Asset Profiles` para padronizar o dominio:

- `State`
- `City`
- `Farm`
- `RegionalOffice`
- `InfluenceRegion`
- `Cooperative`
- `Parcel` ou `OperationalArea` se houver necessidade de granularidade intra-fazenda
- `GatewaySite` ou `TelemetryHub` se fizer sentido operacional

### 3. Devices

Use `Devices` para tudo que produz telemetria ou recebe comando:

- sensor de umidade
- estacao meteorologica
- gateway LoRa/WiFi/4G
- medidor
- atuador
- tracker

Cada device deve ficar ligado por relacao ao asset de negocio relevante.

### 4. Customers

Use `Customers` somente quando houver necessidade concreta de acesso segregado, por exemplo:

- fazenda-cliente que precisa ver seus dados;
- cooperativa que precisa ver um subconjunto de fazendas;
- parceiro regional com acesso limitado;
- municipio/secretaria com acesso apenas a certas entidades.

Se a fazenda for cliente, ela pode existir como:

- `Asset` do tipo `Farm` para representar o dominio;
- `Customer` para representar a fronteira de acesso.

Essas duas coisas nao precisam ser a mesma entidade conceitual.

## Como representar o dominio Sentivis

### Opcao recomendada

#### Estrutura base

- `State` -> asset
- `City` -> asset
- `Farm` -> asset
- `RegionalOffice` -> asset
- `InfluenceRegion` -> asset
- `Cooperative` -> asset
- `Device` -> device

#### Relacoes sugeridas

Use relacoes direcionais com tipos semanticamente claros:

- `Contains`
- `LocatedIn`
- `ManagedBy`
- `MemberOf`
- `Influences`
- `OperatesIn`
- `HasHeadquarters`
- `MonitoredBy`

Exemplo:

- `State` `Contains` `City`
- `City` `Contains` `Farm`
- `Farm` `HasHeadquarters` `RegionalOffice`
- `Farm` `MemberOf` `Cooperative`
- `InfluenceRegion` `Influences` `Farm`
- `Farm` `Contains` `Device`
- `RegionalOffice` `Manages` `Farm`

### Por que isso e melhor que usar Customer para tudo

Porque o seu dominio nao e uma hierarquia de acesso pura.

Voce descreveu situacoes como:

- fazenda em mais de uma cidade;
- fazenda com mais de uma sede;
- cooperativas com regioes de influencia;
- decisoes parciais sobre quais fazendas entram.

Isso e melhor modelado como grafo de entidades com relacoes, nao como arvore fixa de clientes.

## Como tratar casos especiais

### Caso 1 - Fazenda e cliente ao mesmo tempo

Modelo recomendado:

- `Farm` como `Asset`
- `Farm Customer` como `Customer`
- ligacao por atributo ou relacao de referencia

Exemplo de server-side attributes no asset `Farm`:

```json
{
  "farmCode": "FARM-001",
  "crmCustomerCode": "CUST-001",
  "isCustomer": true,
  "primaryCustomerName": "Fazenda Boa Vista"
}
```

### Caso 2 - Fazenda em mais de uma cidade ou regiao

Nao force arvore unica.

Use relacoes multiplas:

- `Farm` `LocatedIn` `City A`
- `Farm` `LocatedIn` `City B`
- `InfluenceRegion X` `Influences` `Farm`

Se houver uma cidade principal, guarde isso em atributo:

```json
{
  "primaryCityId": "CITY-123",
  "multiCity": true
}
```

### Caso 3 - Fazenda com varias sedes regionais

Modelo recomendado:

- `Farm` como asset principal
- cada sede como asset `RegionalOffice`
- relacao `Farm` `HasHeadquarters` `RegionalOffice`

### Caso 4 - Cooperativa com visao parcial

Modelo recomendado:

- cooperativa como `Asset`
- se precisar acesso segregado, cooperativa tambem pode existir como `Customer`
- para compartilhar apenas parte dos dados de certos devices/assets, use `Entity Views`

## Uso recomendado de atributos

### Server-side attributes

Pelos manuais, server-side attributes sao adequados para:

- metadata administrativa;
- geocodigos;
- classificacao territorial;
- ids externos;
- parametros de integracao;
- flags de elegibilidade;
- configuracoes de alarme;
- atributos de negocio.

Exemplos uteis para o seu caso:

```json
{
  "externalCode": "REG-001",
  "ibgeCode": "3550308",
  "isCustomer": true,
  "riskTier": "high",
  "cropType": "soy",
  "lat": -22.123,
  "lon": -47.456,
  "cooperativeCode": "COOP-09"
}
```

### Shared attributes

Somente para `Device`.
Use para configuracao que o servidor envia ao device:

- thresholds
- target firmware
- polling interval
- feature flags de dispositivo

### Client-side attributes

Somente para `Device`.
Use para o que o device reporta como estado semi-estatico:

- firmware atual
- versao de configuracao
- modo de operacao

## Telemetria vs metadata

Use esta regra:

- se muda no tempo e precisa historico: `Telemetry`
- se e classificacao/configuracao/metadata: `Attributes`

Para o dominio Sentivis:

- umidade do solo: telemetry
- precipitacao: telemetry
- bateria do sensor: telemetry ou client attribute conforme uso
- codigo da fazenda: server-side attribute
- municipio principal: server-side attribute
- cooperativa associada: server-side attribute ou relation

## Entity Views no seu caso

Os manuais deixam claro que `Entity Views` servem para expor somente parte dos dados de `Device` ou `Asset` a um `Customer`.

Isso e util quando:

- a cooperativa pode ver apenas alguns indicadores;
- a fazenda ve apenas seus ativos;
- o municipio ve agregados ou um subconjunto de telemetria;
- a Sentivis precisa manter debug/operacao ocultos do cliente.

Use `Entity Views` quando:

- o ativo fisico e o mesmo;
- mas a visao de dados muda por cliente;
- e voce nao quer duplicar devices/assets.

## Dashboards recomendados

Sugestao minima:

- `Dashboard Operacional Tenant`
  - visao completa Sentivis
- `Dashboard Customer - Farm`
  - visao por fazenda cliente
- `Dashboard Customer - Cooperative`
  - visao parcial por cooperativa
- `Dashboard Territorial`
  - visao por estado/cidade/regiao

Os dashboards devem usar:

- aliases por asset/device/customer;
- mapas;
- cards por alarme;
- tabelas por relacao;
- filtros temporais;
- graficos de telemetria agregada.

## CRUDs e operacoes viaveis

### Com `TENANT_ADMIN`

Ja validado ou compativel com a documentacao:

- Customers:
  - create
  - read
  - delete
- Customer Users:
  - create
  - read
  - update via `POST /api/user` com `id`
  - delete
- Users do tenant:
  - read
  - update via `POST /api/user` com `id`
- Devices:
  - create
  - read
  - delete
  - update conforme endpoint suportado da entidade
- Assets:
  - create
  - read
  - relations
  - attributes
- Dashboards:
  - create
  - read
  - update
- Attributes:
  - leitura e escrita via REST API nas entidades suportadas
- Relations:
  - criar e apagar via `/api/relations`

### Com `SYS_ADMIN`

Necessario para:

- Tenants
  - create
  - edit
  - delete
- Tenant admins
  - create
  - edit
  - disable/enable
  - login as tenant admin
- Mail Server global
- Security settings globais
- configuracoes administrativas globais

## O que pode ser administrado via MCP

Se o MCP expuser os endpoints corretos e usar as credenciais corretas, entao e viavel administrar:

### Com contexto `TENANT_ADMIN`

- CRUD de customers
- CRUD de customer users
- CRUD de users no tenant
- CRUD de devices
- CRUD de assets
- leitura/escrita de attributes
- criacao e remocao de relations
- dashboards
- consultas operacionais

### Com contexto `SYS_ADMIN`

- Mail Server
- Security settings
- tenant administration
- validacoes globais da instancia

### Limite importante

MCP nao elimina:

- limitacoes da API CE;
- diferencas entre metodo correto e metodo aparentemente intuitivo;
- necessidade de usar `SYS_ADMIN` para configuracao global.

## Recomendacao de configuracao para a Sentivis

### Configuracao alvo

- `Tenant`: Sentivis
- `Customers`: apenas fronteiras de acesso/comercial
- `Assets`: dominio real do negocio e da geografia
- `Devices`: fontes de telemetria e comando
- `Relations`: malha de estrutura real
- `Entity Views`: compartilhamento parcial para clientes/cooperativas
- `Dashboards`: por papel e por recorte territorial/operacional

### Estrutura inicial sugerida

#### Asset Profiles

- `State`
- `City`
- `Farm`
- `RegionalOffice`
- `InfluenceRegion`
- `Cooperative`
- `OperationalArea`

#### Device Profiles

- `SoilSensor`
- `WeatherStation`
- `Gateway`
- `Meter`
- `Actuator`

#### Relacoes padrao

- `Contains`
- `LocatedIn`
- `ManagedBy`
- `MemberOf`
- `Influences`
- `HasHeadquarters`

## Decisoes para o MLE

Estas decisoes precisam ser fechadas antes de escalar a modelagem:

### 1. O que e cliente e o que e apenas dominio

Decidir criterios objetivos para criar `Customer`.

Recomendacao:

- criar `Customer` apenas quando houver necessidade real de acesso segregado ou relacao comercial;
- manter fazenda/cooperativa/cidade/estado como `Asset` por padrao.

### 2. Hierarquia ou grafo

Recomendacao:

- usar grafo com `Relations`;
- nao forcar arvore unica para fazendas com pertencimentos multiplos.

### 3. Nivel de granularidade

Decidir se a unidade de negocio operacional e:

- fazenda;
- sede regional;
- talhao/area operacional;
- dispositivo.

Recomendacao:

- comecar em `Farm` + `RegionalOffice` + `Device`;
- abrir `OperationalArea` apenas quando o caso de uso exigir.

### 4. Compartilhamento parcial

Decidir onde `Entity Views` entram.

Recomendacao:

- usar `Entity Views` para cooperativas, parceiros e clientes com recorte parcial;
- nao duplicar assets/devices so para compartilhar subconjuntos.

### 5. Chaves de identificacao

Definir chaves canonicas em attributes:

- `externalCode`
- `erpId`
- `crmId`
- `ibgeCode`
- `farmCode`
- `cooperativeCode`
- `regionalOfficeCode`

## Proposta operacional minima

### Fase 1

- Tenant Sentivis estabilizado
- profiles criados
- assets de territorio e negocio
- devices conectados
- relacoes basicas
- dashboards de tenant

### Fase 2

- customers onde houver segregacao real
- customer users
- entity views para compartilhamento parcial
- dashboards por cliente/cooperativa

### Fase 3

- alarmes por perfil
- atributos de configuracao
- integracoes externas
- automacao MCP completa com `TENANT_ADMIN` e `SYS_ADMIN`

## Minha recomendacao final

Para o caso Sentivis, o melhor desenho no ThingsBoard CE e:

- `Sentivis = Tenant`
- `Fazenda/Cidade/Estado/Cooperativa/Sede/Regiao = Assets`
- `Permissao e acesso = Customers + Users`
- `Sensores e gateways = Devices`
- `Pertencimento e influencia = Relations`
- `Metadata = Server-side attributes`
- `Compartilhamento parcial = Entity Views`

Isso preserva:

- flexibilidade para modelar casos nao-hierarquicos;
- governanca de acesso sem distorcer o dominio;
- compatibilidade com o CE;
- escalabilidade para automacao via MCP.

## O que considero viavel agora

- administrar o tenant Sentivis quase inteiro por API/MCP;
- criar e manter a malha de assets e relations;
- operar customers e customer users;
- expor recortes controlados por entity views;
- manter dashboards por papel;
- separar operacao de negocio de controle de acesso.

## O que eu faria na pratica

1. Fechar o dicionario de entidades do dominio.
2. Criar `Asset Profiles` padrao.
3. Definir relacoes canonicas.
4. Definir atributos obrigatorios por tipo de asset.
5. Mapear quais atores viram `Customer`.
6. Criar dashboards operacionais e externos.
7. Formalizar o que o MCP pode criar, ler, atualizar e apagar por papel.

