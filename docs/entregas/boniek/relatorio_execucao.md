# Entrega técnica — Boniek

Data: 24/11/2026. Destinatárias: Larysse (QA/pacote final) e Letícia (documentação).
Base: `jaozinnm/pd-bank-access-governance-analyzer`, commit `eb9c083`, backend v0.4.0.
Branch de trabalho: `feat/boniek-entrega-executavel`.

## Decisão de entrega

**SQLite + Vite é o caminho oficial da demonstração acadêmica.** Instalação e
roteiro completos estão no README raiz e em `frontend/README.md`. Docker/PostgreSQL
foi validado como alternativa, com frontend separado. Os serviços da demonstração
usam localhost; a API do Compose foi limitada a 127.0.0.1 no host.

## Alterações

- READMEs com comandos Linux/macOS e PowerShell, URLs, Excel oficial, exportações,
  build/preview, variáveis, empacotamento e troubleshooting.
- `.env.example` esclarece que Python local não carrega `.env`; Compose e Vite têm
  configurações separadas. Compose passa também limite de upload e fuso horário.
- Exclusões de credenciais locais, dependências, caches e build no Git/Docker.
- `scripts/smoke_test.py`: 30 verificações HTTP com o Excel oficial e saída JSON opcional.
- `npm run smoke:api`: 9 verificações usando os módulos reais do cliente frontend em Node.
- Testes PostgreSQL agora isolam cada caso em schema temporário. A primeira execução
  revelou dois testes contaminados pelos registros dos anteriores; a correção foi
  validada com os seis testes ativados, sem alterar regras de negócio ou o Excel.

## Execução e evidências

Ambiente: Linux, Python 3.14.10, Node.js 24.21.0, npm 11.19.0, Docker Engine 29.9.3,
Compose 5.7.0. Container da API: Python 3.12-slim; banco: PostgreSQL 16-alpine.
As versões Python instaladas estão em `ambiente_python.txt` (registro da execução,
não substitui `requirements.txt`).

| Verificação | Resultado | Evidência neste diretório |
|---|---|---|
| venv novo + instalação de requirements | OK | `ambiente_python.txt` e execução da suíte |
| Pytest com SQLite e PostgreSQL exclusivo de testes | 138 passaram, nenhum pulado | `evidencia_testes.txt` |
| API SQLite por HTTP | 30 verificações passaram | `evidencia_sqlite.json` |
| Build Docker, healthchecks e API PostgreSQL por HTTP | 30 verificações passaram | `evidencia_postgres.json` |
| `npm ci` e `npm run build` | OK, TypeScript e Vite | `evidencia_build.txt` |
| Cliente frontend real contra a API | 9 verificações passaram | `evidencia_frontend.json` |
| Instalação, testes e build após extrair o ZIP | OK: 132 testes + 6 PostgreSQL opcionais pulados; build e integração passaram | `evidencia_pacote.json` |

O Excel original foi importado em ambos os bancos: **20 abas, 1.890 registros,
431 achados**, referência **2026-11-05**. Por regra: R01=16, R02=5, R03=7, R04=65,
R05=25, R06=3, R07=19, R08=4, R09=287. Severidades: 44 críticos, 119 altos,
142 médios e 126 baixos. O JSON exportado foi comparado ao registro relido do banco;
o CSV teve suas 431 linhas e colunas de rastreabilidade conferidas.

Foram conferidos preflight OPTIONS, origem permitida, `X-API-Key` permitido e
exposição de `X-Total-Count` e `Content-Disposition`. Os testes da suíte também
cobrem autenticação opcional e CORS desligado/ativado. Nenhuma chave real foi
incluída nas evidências.

Durante a integração, Flask e Vite estavam ativos em 8080 e 5173. O HTML e o módulo
HTTP da aplicação foram servidos pelo Vite; o teste frontend carregou os módulos
reais via Vite SSR em Node. O Compose usou um projeto isolado
`pdbank-boniek-validacao`, portas 18080/15432, senha temporária fora do repositório
e um banco `pd_bank_test` separado do banco da demonstração.

## Limitações e pendências para QA

- **Revisão visual no navegador pendente:** Maestri Portal recusou conexão e o host
  de navegador do ambiente estava indisponível. O teste em Node não executa a UI,
  não aplica a política CORS do browser e não testa o clique de download. Larysse
  deve seguir o roteiro dos READMEs para conferir esses pontos antes da entrega final.
- Comandos Windows/macOS foram documentados, mas a execução ocorreu somente em Linux.
- `npm audit` retornou **2 alertas moderados** em `react-router`/`react-router-dom`,
  sem altos/críticos; veja `evidencia_npm_audit.json`. O registro indica correção
  via migração principal para 7.18.7. A migração não foi feita nesta entrega de execução.
- As dependências Python usam intervalos de versão; reinstalações futuras podem
  resolver outras versões. O lockfile npm existente foi preservado.
- SQLite não exige autenticação por padrão nesta demonstração local. Chaves `VITE_*`
  são públicas; este pacote acadêmico não é uma implantação de produção.
- As inconsistências conhecidas da planilha e decisões de interpretação permanecem
  documentadas nas entregas de César e no relatório v0.4.0.

## Pacote e encaminhamento

O ZIP de código-fonte fica fora do repositório, em `../entrega-boniek/`, sem `.git`,
bancos, `.env` reais, venv, dependências instaladas, caches ou `dist/`. Inclui os dois
`.env.example`, lockfile, frontend, testes, Excel oficial, READMEs e estas evidências.

O pacote final inclui a mesma implementação validada na extração e o relatório
consolidado depois do teste. Após o commit, `git archive` (comando no README) permite
gerar novamente o pacote. O SHA-256 do ZIP fica no arquivo `SHA256SUMS.txt` ao lado dele.
