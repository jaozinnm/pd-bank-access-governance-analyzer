<div align="center">

# 🛡️ PD Bank

### Access & Governance Analyzer

**Inteligência em governança de acessos, proteção de dados e segurança no uso de inteligência artificial.**

Projeto acadêmico de análise de governança desenvolvido para um cenário bancário fictício. A plataforma transforma datasets estruturados em **achados rastreáveis, indicadores de risco e recomendações para revisão humana**.

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Suportado-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Status:** Em desenvolvimento · **Versão do backend:** v0.4.0 · **Interface:** React + TypeScript

</div>

---

## 📌 Sobre o projeto

O **PD Bank Access & Governance Analyzer** é uma plataforma web de apoio à auditoria e à governança de um banco fictício. O sistema recebe datasets em formatos estruturados, executa regras determinísticas e apresenta resultados para investigação, priorização e tomada de decisão.

O foco não é realizar operações financeiras, mas **identificar possíveis desvios de controle** em três dimensões: 
- identidade e acesso, 
- proteção de dados, 
- governança de IA.

> **Diferencial:** cada achado pode apresentar regra acionada, severidade, evidência, origem na planilha, impacto e recomendação. O resultado auxilia a revisão humana; não revoga permissões nem modifica os dados auditados automaticamente.

## 🎯 Objetivos

- Identificar permissões fora do baseline RBAC e conflitos de segregação de funções (SoD).
- Detectar acessos indevidos, temporários vencidos e revisões pendentes.
- Avaliar classificação, propriedade, compartilhamento e retenção de dados.
- Verificar controles, fontes e níveis de autonomia em casos de uso de IA.
- Oferecer importação de datasets, execução de análises, indicadores e relatórios.
- Manter rastreabilidade dos achados para apoiar investigação e revisão humana.

## 🧩 Módulos do sistema

| Módulo | Responsabilidade |
|---|---|
| **Dashboard executivo** | Indicadores, distribuições e visão geral dos achados |
| **Datasets** | Importação e validação de arquivos XLSX, CSV e ZIP |
| **Análises** | Execução do motor de regras e histórico de resultados |
| **Achados** | Consulta, filtros, severidades, evidências e recomendações |
| **Governança de acessos** | RBAC, SoD, acessos de usuários e revisões |
| **Proteção de dados** | Classificação, responsáveis, compartilhamento e retenção |
| **Governança de IA** | Guardrails, aprovação, fontes de dados e autonomia |
| **Relatórios** | Exportação dos resultados em JSON e CSV |

## 🔍 Motor de regras

| Regra | Análise |
|---|---|
| **R01** | Permissões acima do baseline RBAC |
| **R02** | Conflitos de segregação de funções (SoD) |
| **R03** | Ativos sem classificação ou responsável |
| **R04** | Compartilhamento ou retenção inadequados |
| **R05** | Controles e guardrails insuficientes em IA |
| **R06** | Autonomia excessiva em casos de uso de IA |
| **R07** | Usuários inativos ou desligados com acesso remanescente |
| **R08** | Acessos temporários vencidos |
| **R09** | Revisões de acesso pendentes, vencidas ou reprovadas |

O motor considera exceções válidas, situações de informação insuficiente e cobertura de avaliação por regra. Os resultados **não substituem uma auditoria humana**.

## 🏗️ Arquitetura

```text
┌───────────────────────────────────────────────────┐
│              FRONTEND — React + Vite              │
│ Dashboard · Datasets · Análises · Achados         │
│           http://localhost:5173                   │
└─────────────────────────┬─────────────────────────┘
                          │ HTTP / JSON
                          ▼
┌───────────────────────────────────────────────────┐
│                BACKEND — Flask API                │
│ Importação · Validação · Regras R01–R09           │
│           http://localhost:8080                   │
└─────────────────────────┬─────────────────────────┘
                          │ SQLAlchemy
                          ▼
┌───────────────────────────────────────────────────┐
│             SQLite (local) / PostgreSQL           │
└───────────────────────────────────────────────────┘
```

O frontend e o backend são executados separadamente e se comunicam pela API REST. A interface não implementa regras de negócio nem cria endpoints próprios.

## 🛠️ Tecnologias

| Camada | Tecnologias |
|---|---|
| Frontend | React 18, TypeScript 5.7, Vite 6 |
| Estilização e UI | Tailwind CSS, Lucide React |
| Gráficos | Recharts |
| Navegação | React Router |
| Backend | Python 3.10+, Flask |
| Persistência | SQLAlchemy, SQLite, PostgreSQL |
| Testes | Pytest / unittest |
| Infraestrutura | Docker, Docker Compose |
| Versionamento | Git e GitHub |

## 🚀 Instalação oficial: SQLite + frontend

Use dois terminais, sempre partindo da raiz do projeto. 
Requer: Python 3.10+, Node.js 20+ com npm e Git.
A execução foi validada em Linux com Python 3.14 e Node.js 24; 
Detalhes e limitações estão disponíveis no [Relatório de Execução Front-end + Back-end](docs/entregas/boniek/relatorio_execucao.md).

```bash
git clone https://github.com/jaozinnm/pd-bank-access-governance-analyzer.git
cd pd-bank-access-governance-analyzer
```

### 1. Backend — terminal 1

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABASE_URL=sqlite:///pd_bank_analyzer.db
export CORS_ORIGINS=http://localhost:5173
export API_KEY=""
python app.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DATABASE_URL = "sqlite:///pd_bank_analyzer.db"
$env:CORS_ORIGINS = "http://localhost:5173"
$env:API_KEY = ""
python app.py
```

O SQLite é criado automaticamente na raiz; não precisa instalar um servidor de banco.

A API inicia em **http://localhost:8080**. Saúde: **http://localhost:8080/api/health**;
Swagger: **http://localhost:8080/docs**; contrato: **http://localhost:8080/openapi.json**.

O Swagger carrega recursos de uma CDN e requer internet.

### 2. Frontend — terminal 2

```bash
cd frontend
npm ci
npm run dev
```

Abra **http://localhost:5173**. Os padrões já apontam para a API local, sem criar `.env`.

Para configurar outra API, copie `frontend/.env.example` para `frontend/.env.local`
(`cp` no Linux/macOS ou `Copy-Item` no PowerShell), ajuste os valores e reinicie o Vite.

Consulte o [README do frontend](frontend/README.md).

### 3. Demonstração com o Excel oficial

1. Em **Datasets**, selecione `tests/data/PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx`.
2. Aguarde a validação e clique em **Importar dataset**. A base tem 20 abas e 1.890 registros.
3. Clique na ação **Executar análise** do dataset ou abra **Nova análise** e selecione-o.
4. Deixe a data de referência vazia, clique em **Revisar configuração** e **Confirmar execução**.
5. Confira **431 achados**, com referência **2026-11-05**, consulte a paginação e abra um achado.
6. Use os botões **JSON** e **CSV** no resultado, ou abra **Relatórios** para exportar.

Esses totais são o snapshot da v0.4.0 para o arquivo oficial original; não use a
planilha corrigida de César para reproduzi-los. 
A base tem inconsistências conhecidas(como AI07) e o sistema não as corrige automaticamente. 
Veja a [nota de qualidade](docs/entregas/cesar/nota_qualidade_dados.md).

Com a API ativa, este teste reproduz upload, análise, consulta e as duas exportações
por HTTP, conferindo também CORS e conteúdo dos arquivos. Cria **um novo dataset e
uma nova análise por execução**; use uma instância de demonstração:

```bash
python scripts/smoke_test.py --out /tmp/pdbank-smoke.json
```

No Windows, use `--out "$env:TEMP/pdbank-smoke.json"`.
Exemplos de consulta (substitua `1` pelo ID retornado, `curl.exe` no PowerShell):

```bash
curl -f http://localhost:8080/api/health
curl -f "http://localhost:8080/api/findings?analysis_id=1&limit=20&offset=0"
curl -f "http://localhost:8080/api/analyses/1/export?format=json" -o analysis-1.json
curl -f "http://localhost:8080/api/analyses/1/export?format=csv" -o analysis-1.csv
```

Se `API_KEY` estiver configurada, adicione `-H "X-API-Key: SUA_CHAVE_LOCAL"` ao curl;
o teste de fumaça lê `API_KEY` do ambiente.

### Variáveis de ambiente

**`python app.py` não lê `.env` automaticamente.** Exporte as variáveis no terminal.
O Compose lê o `.env` raiz; o Vite lê `frontend/.env.local`. Não misture esses arquivos.

| Variável | Padrão / finalidade |
|---|---|
| `DATABASE_URL` | `sqlite:///pd_bank_analyzer.db`; caminho relativo ao diretório de execução |
| `CORS_ORIGINS` | Vazio desliga CORS; use `http://localhost:5173` para este guia. Várias origens separadas por vírgula |
| `API_KEY` | Vazia desliga autenticação local. Se definida, exige `X-API-Key` em `/api/*`, exceto saúde |
| `HOST` / `PORT` | `127.0.0.1` / `8080` na execução Python local |
| `FLASK_DEBUG` | Desligado; `1` ativa debug apenas para desenvolvimento |
| `MAX_UPLOAD_MB` | `50`; frontend também limita upload a 50 MB |
| `APP_TIMEZONE` | `America/Sao_Paulo` |
| `VITE_API_BASE_URL` | `http://localhost:8080`; URL acessível pelo navegador, sem `/api` ao final |
| `VITE_API_KEY` | Opcional; mesma chave da API para demonstração. É pública no bundle do navegador |
| `VITE_APP_VERSION` | `1.0.0`, versão da interface; backend permanece v0.4.0 |
| `POSTGRES_DB` / `POSTGRES_USER` | `pd_bank` no Compose |
| `POSTGRES_PASSWORD` | Obrigatória no Compose; somente letras, números, `-` e `_` para compor a URL |
| `POSTGRES_PORT` / `API_PORT` | `5432` / `8080` no host do Compose |

Variáveis `VITE_*` são incorporadas no build. Após alterá-las, reinicie `npm run dev`
ou gere um novo build. Não coloque credenciais de produção no frontend.

### Alternativa: Docker + PostgreSQL

Requer Docker Engine/Desktop ativo com Compose. O frontend continua no terminal 2.
Copie o exemplo para `.env` na raiz (`Copy-Item .env.example .env` no PowerShell):

```bash
cp .env.example .env
```

Edite `POSTGRES_PASSWORD` com uma senha local própria antes de iniciar. O exemplo
já contém `CORS_ORIGINS=http://localhost:5173`. Pare a API SQLite antes de usar a
mesma porta, ou altere `API_PORT` e `VITE_API_BASE_URL` em conjunto.

```bash
docker compose up --build -d --wait
docker compose ps
curl -f http://localhost:8080/api/health
python scripts/smoke_test.py
docker compose down
```

O último comando preserva o volume do banco. `docker compose down -v` **apaga os
dados do projeto**: use apenas se quiser reiniciar a demonstração do zero.
O caminho oficial continua SQLite; o resultado do teste Docker está no relatório.

## 🧪 Testes, build e pacote

Com o ambiente Python ativado, na raiz:

```bash
python -m pytest -q
```

Os testes PostgreSQL são opcionais e requerem `TEST_POSTGRES_URL` apontando para um
**banco exclusivo de teste**, com permissão para criar schemas. Cada teste cria e
remove seu próprio schema; não use o banco da demonstração.

No diretório `frontend/`:

```bash
npm ci
npm run build
npm run preview -- --port 5173
```

O preview acima usa a mesma origem já permitida pela API. Sem `--port 5173`, o
preview deste projeto usa **3000**: adicione essa origem a `CORS_ORIGINS` para usá-lo.
`dist/` é gerado localmente e não faz parte do código entregue.

Depois de revisar e fazer commit das alterações, gere um ZIP apenas dos arquivos
versionados (execute na raiz; o ZIP fica fora do projeto):

```bash
git archive --format=zip --prefix=pd-bank-access-governance-analyzer/ -o ../pd-bank-v0.4.0-boniek.zip HEAD
```

Extraia em uma pasta nova e repita a instalação, testes, build e demonstração acima.
Não inclua `.env`, `.env.local`, banco, `.venv`, `node_modules`, `dist`, caches ou `.git`.
Os arquivos `.env.example` são modelos e devem permanecer. As evidências da entrega
estão em [`docs/entregas/boniek/`](docs/entregas/boniek/).

## 🔧 Troubleshooting

| Sintoma | Como resolver |
|---|---|
| `npm ci` falha | Execute em `frontend/`, com o `package-lock.json` entregue e Node 20+. Confira rede/registro npm |
| PowerShell bloqueia `Activate.ps1` | Use `.\.venv\Scripts\python.exe` no lugar de `python`, sem ativar o ambiente |
| Porta 8080 ocupada | Pare a outra API ou ajuste `PORT` (local) / `API_PORT` (Compose) e `VITE_API_BASE_URL` |
| Porta 5173 ocupada | O Vite falha por `strictPort`; libere a porta ou ajuste a porta e `CORS_ORIGINS` juntos |
| Saúde responde, mas tela não carrega dados | Confira a URL da API e CORS; `localhost` e `127.0.0.1` são origens diferentes |
| HTTP 401 | Configure a mesma `API_KEY` no backend e `VITE_API_KEY` no frontend; reinicie o Vite |
| CORS no preview | Use `npm run preview -- --port 5173` ou permita `http://localhost:3000` no backend |
| Variável no `.env` não surte efeito | Python local requer exportação no terminal; o `.env` raiz só é lido pelo Compose |
| Banco SQLite não abre | Inicie na raiz e use um diretório gravável; não inclua o arquivo `.db` no PR |
| HTTP 413 | Arquivo excede `MAX_UPLOAD_MB`; o frontend aceita no máximo 50 MB |
| Docker não inicia | Confira daemon, acesso ao socket, senha no `.env`, portas livres e `docker compose logs api db` |
| Achados diferentes de 431 | Use o Excel original e deixe a data vazia; outras bases/datas podem mudar o resultado |

Contrato da API: [`docs/API.md`](docs/API.md). Validação anterior da versão:
[`docs/v0.4.0-relatorio.md`](docs/v0.4.0-relatorio.md).

## 📂 Estrutura do repositório

```text
pd-bank-access-governance-analyzer/
├── frontend/               # Aplicação React + TypeScript
│   ├── src/api/            # Cliente HTTP e adaptadores
│   ├── src/components/     # Componentes visuais reutilizáveis
│   ├── src/pages/          # Páginas da aplicação
│   └── package.json
├── pdbank/                 # Regras, importação, API e persistência
├── tests/                  # Testes do backend
├── scripts/                # Ferramentas de validação
├── docs/                   # Contratos, relatórios e decisões técnicas
├── app.py                  # Entrada da aplicação Flask
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## 👥 Equipe

| Integrante | Papel no projeto |
|---|---|
| Abrão Filipi dos Santos | Decisões dos casos públicos e validação das premissas |
| Caio Cesar Leandro Amorim | Qualidade do dataset e interpretação dos resultados |
| Danilo Gabriel Diniz e Silva | Apoio à execução técnica e integração do sistema |
| Boniek Araújo dos Santos Júnior | Execução técnica, README e pacote executável |
| João Rafael Morato Uchoa Cavalcanti | Frontend e integração visual com a API |
| Alice Maria Sena Pereira | Catálogo e revisão das regras de governança |
| Mateus Valerino Barros de Santana | Apoio ao plano e à execução dos testes |
| Matheus do Nascimento Gomes Vaz | Plano e execução dos testes formais |
| Maria Larysse Yasmin Lira Pereira | QA final e montagem do ZIP de entrega |
| Letícia Gomes da Silva | Documentação acadêmica e Security & Governance Playbook |
| Marcio Aureliano Pedro da Silva | Slides e apresentação do projeto |



## 🤝 Colaboração e fluxo de trabalho

1. Crie uma issue para a tarefa ou escolha uma já existente.
2. Abra uma branch a partir de `main`, por exemplo `feat/dashboard-indicadores` ou `fix/importacao-xlsx`.
3. Faça commits pequenos e descritivos.
4. Execute os testes relacionados à alteração.
5. Abra um Pull Request explicando o que mudou e como validar.
6. Aguarde a revisão antes de mesclar na `main`.

**Sugestões de labels:** `frontend`, `backend`, `bug`, `testes`, `documentacao`, `integracao`, `prioridade-alta`, `good-first-issue`.

## 🔐 Segurança e limitações

- O projeto utiliza **dados fictícios** para fins acadêmicos.
- Não envie `.env`, credenciais, tokens ou bancos locais ao GitHub.
- O backend pode executar sem autenticação em desenvolvimento; **não o exponha publicamente dessa forma**.
- A análise é baseada em regras e recomendações; não executa alterações automáticas em permissões ou dados.
- A compatibilidade e o funcionamento completo devem ser revalidados após cada integração relevante.

## 📄 Licenciamento e créditos

Projeto acadêmico em desenvolvimento. A licença de distribuição será definida após confirmar a autoria e as permissões de reutilização dos componentes incorporados. Contribuições e materiais de terceiros devem manter os créditos e avisos de licença aplicáveis.

---

<div align="center">

### 🛡️ PD Bank — Access & Governance Analyzer

**Da evidência à decisão: governança mais clara, riscos mais visíveis.**

</div>


## Entrega técnica final — Residência em Software & IA

- [Índice da entrega](docs/entrega-final/01_Indice_da_Entrega.md)
- [Documentação de IA](docs/entrega-final/02_Documentacao_IA.pdf)
- [Catálogo de prompts reconstruídos](docs/prompts/README.md)
- [Prompts que falharam](docs/entrega-final/03_Prompts_Que_Falharam.pdf)

A IA foi utilizada durante a engenharia de software. O motor de análise é determinístico e não exige chaves de serviços de LLM. As variáveis API_KEY e VITE_API_KEY referem-se à API do próprio sistema; não exponha segredos no frontend. Consulte os exemplos de ambiente existentes. Não há URL de deploy público confirmada neste pacote.
