## Cindy Agent - Fatos persistentes

- Projeto: Cindy Agent
- Workspace local: `C:\CindyAgent`
- Workspace em WSL: `/mnt/c/CindyAgent`
- Stack operacional: Hermes + Telegram
- Runtime principal de acompanhamento: Hermes via gateway no Telegram

## Git e repositório

- Remote oficial: `https://github.com/scaixeta/cindy-oc`
- Branch principal: `main`
- `.scr/.env` é segredo local e não deve ser versionado

## Regras operacionais

- O Hermes deve ser iniciado por rotina simples no Windows e ficar pronto no Telegram
- Telegram é o canal principal de interação operacional quando o gateway estiver ativo
- "acorde" é uma retomada lógica, não um wake-on-LAN
- Se a máquina estiver desligada, suspensa ou sem gateway, o Telegram não inicia o Hermes sozinho
- Commit/push apenas sob ordem explícita do PO
- Não expor segredos
- Não inventar resultados nem conteúdo de arquivos
- Priorizar respostas objetivas, leitura sob demanda, status claro e execução controlada
