# DEVELOPMENT - Sentivis IAOps

## Proposito

Descrever como a evolucao do projeto deve ser conduzida seguindo DOC2.5.

## 1. Principios de desenvolvimento

- Uma sprint ativa por vez
- Tracking obrigatorio
- Mudanca minima necessaria
- Plano antes de execucao
- Sem estruturas paralelas fora do modelo canonico
- Fato, inferencia e pendencia devem permanecer separados

## 2. Estado actual de desenvolvimento

| Item | Valor |
|---|---|
| Fase actual | S3 Encerrada |
| Sprint activa | Nenhuma |
| Escopo aprovado | Mock telemetry validation + Cirrus Lab hardware real |
| Fora do escopo | Integracao Cirrus->TB local, LoRa, ESP32 |

## 3. Estimativas (Fibonacci 1-21)

| Pontos | Regra pratica |
|---:|---|
| 1 | Operacao atomica, baixo risco, 1 passo |
| 2 | Pequeno ajuste com 1 verificacao |
| 3 | Mudanca pequena com 2+ passos/arquivos |
| 5 | Decisao + ajuste + validacao |
| 8 | Integracao/fluxo com superficie maior |
| 13 | Coordenacao/incerteza |
| 21 | Alto risco/abrangencia; fatiamento recomendado |

## 4. Fluxo de desenvolvimento

### 4.1 Ler contexto

1. `README.md`
2. `Dev_Tracking.md`
3. Sprint activa ou arquivada mais recente
4. `docs/SETUP.md`
5. `docs/ARCHITECTURE.md`
6. `docs/OPERATIONS.md`

### 4.2 Planejar

- Resumir entendimento
- Propor plano numerado
- Aguardar aprovacao explicita do PO antes de executar

### 4.3 Executar

- Actualizar backlog em `Dev_Tracking_SX.md`
- Registrar decisoes como `[D-SX-YY]`
- Referenciar bugs e testes em `tests/bugs_log.md`
- Aplicar a menor mudanca necessaria

### 4.4 Actualizar rastreabilidade

- Manter `Dev_Tracking_SX.md` coerente
- Actualizar `Dev_Tracking.md` quando necessario
- Manter coerencia entre `README.md`, docs, tracking e `bugs_log`

## 5. Backlog e instrumentacao da sprint

```
| Estado | SP | Jira | Estoria |
|---|---|---|---|
| To-Do | 8 | STVIA-45 | ST-S0-03 - Definir contrato de mock telemetry |
| Done | 13 | STVIA-46 | ST-S0-04 - Mapear device/profile modeling |
```

**Estados permitidos:** `To-Do`, `Doing`, `Done`, `Accepted`, `Pending-SX`

**Decisoes:** `[D-SX-YY] - descricao`

**Timestamp UTC:** `ST-SX-YY | YYYY-MM-DDTHH:MM:SS-ST | YYYY-MM-DDTHH:MM:SS-FN | Done`

## 6. Politica de leitura vs alteracao

### Leitura permitida

- `git status`
- `git log`
- `git show`
- Leitura de arquivos

### Alteracao exige gate

- `git add`
- `git commit`
- `git push`
- Criacao/remocao de arquivos
- Instalacao de dependencias

## 7. Tests e bugs

- Log centralizado em `tests/bugs_log.md`
- `Timestamp UTC` nas tabelas
- `Dev_Tracking_SX.md` recebe referencias cruzadas
- Quando nao houver automacao, registrar a validacao manual executada

## 8. Referencias minimas

- `README.md`
- `Dev_Tracking.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/OPERATIONS.md`
- `tests/bugs_log.md`
