# Contrato da API (para React/TypeScript)

Base: `http://localhost:8080`. JSON UTF-8. Erros: `{ "error": string }` (+ `validation` no 422) com HTTP 400/401/404/405/413/422/500.
Gerar tipos a partir da especificação: `npx openapi-typescript http://localhost:8080/openapi.json -o src/api/schema.d.ts`.
CORS: defina `CORS_ORIGINS=http://localhost:5173`. Se `API_KEY` estiver definido, envie `X-API-Key` (exceto `/api/health`, `/openapi.json`, `/docs`).

## Endpoints

| Método e rota | Descrição | Sucesso | Erros |
|---|---|---|---|
| `GET /api/health` | Saúde + banco | 200 / 503 | |
| `GET /api/rules` | Catálogo R01–R09 | 200 `Rule[]` | |
| `GET /api/roles` | Catálogo funcional proposto (papéis, responsabilidades, incompatibilidades e elevação) | 200 `RoleCatalog` | |
| `POST /api/datasets/import` | multipart, campo `file` (.xlsx/.csv/.zip, ≤50 MB) | 201 `ImportResponse` | 400, 413 |
| `POST /api/datasets/validate` | `{ tables: Record<string, object[]> }` | 200 `ValidationResult` | 400 |
| `GET /api/datasets` | Datasets importados (mais recente primeiro) | 200 `Dataset[]` | |
| `GET /api/datasets/{id}` | Dataset + validação | 200 | 404 |
| `POST /api/analyses` | `{ dataset_id: number, reference_date?: "AAAA-MM-DD" }` | 201 `Analysis` | 400, 404, 422 |
| `GET /api/analyses` | Histórico (sem `findings`) | 200 `Analysis[]` | |
| `GET /api/analyses/{id}` | Detalhe com `findings` e `coverage` | 200 `Analysis` | 404 |
| `GET /api/analyses/{id}/export?format=json\|csv` | Download | 200 | 400, 404 |
| `GET /api/findings` | Filtros abaixo; total em `X-Total-Count` | 200 `Finding[]` | 400 |
| `GET /api/findings/{id}` | Detalhe | 200 `Finding` | 404 |
| `GET /api/indicators` | Resumo da última análise | 200 `Indicators` | |

Filtros de `/api/findings`: `analysis_id`, `domain` (igualdade exata), `rule_id` (R01–R09, case-insensitive), `severity` (`critical|high|medium|low`), `status`, `exception_status` (`none|valid|expired|future`), `q` (trecho de `object_ref`), `limit` (1–1000, padrão 200), `offset`. Valor inválido → 400. Para paginar, leia o cabeçalho `X-Total-Count` (exposto via CORS).

### Catálogo funcional de papéis (`GET /api/roles`)

Retorna um objeto `RoleCatalog` versionado com `status`, `source_notes`, lista `roles` e `separation_constraints`. Cada papel inclui identificador, nome, área de origem, perfil macro, finalidade, responsabilidades, incompatibilidades e `elevated_access` (necessidade, modo, permanência e justificativa). Os papéis R01–R14 preservam os IDs, nomes e áreas da aba `catalogo_papeis` do dataset oficial; as responsabilidades e controles são propostas para discussão. Os papéis `EXT-*` são personas externas de cliente do briefing e não integram o catálogo de funcionários nem o baseline interno. O endpoint é informativo: não atribui, revoga ou autoriza acessos.

## Tipos TypeScript

```ts
export type RuleId = "R01"|"R02"|"R03"|"R04"|"R05"|"R06"|"R07"|"R08"|"R09";
export type Severity = "critical"|"high"|"medium"|"low";
export type FindingStatus = "non_compliant"|"insufficient_information"|"valid_exception"|"compliant";
export type ExceptionStatus = "none"|"valid"|"expired"|"future";
export interface RoleCatalog {
  version: string; status: "proposed"; source_notes: string[];
  roles: Array<{
    role_id: string; name: string; area: string; macro_profile: string;
    catalog_status: string; purpose: string; responsibilities: string[];
    incompatibilities: string[];
    elevated_access: { required: boolean; mode: string; permanent: boolean; rationale: string };
  }>;
  separation_constraints: Array<{
    constraint_id: string; roles: string[]; activities: string[]; rationale: string; status: string;
  }>;
}

export interface Dataset { id: number; name: string; created_at: string; table_counts: Record<string, number | null>; }

export interface ValidationResult {
  valid: boolean;
  errors: { table: string | null; row: number | null; message: string }[];
  warnings: string[];
  recognized_sheets: { source_name: string; canonical_name: string }[];
  unknown_sheets: string[];
  records_total: number; records_accepted: number; records_rejected: number;
  tables: Record<string, number | null>;
}
export interface ImportResponse {
  dataset: Dataset; validation: ValidationResult;
  import: { warnings: string[]; sources: { file: string; sheet: string; table: string; rows: number }[] };
}
export interface Finding {
  id: number; analysis_id: number; rule_id: RuleId;
  category: string; domain: string;            // domain == category
  severity: Severity; status: FindingStatus; exception_status: ExceptionStatus;
  object_ref: string;
  source_sheet: string | null; source_row: number | null;   // null em achados de bancos antigos
  evidence: string; description: string; impact: string; recommendation: string;
  reviewer: string | null;                     // sempre null nesta versão
}
export interface Summary {
  total: number; by_severity: Record<Severity, number>; by_status: Record<FindingStatus, number>;
  by_rule: Record<RuleId, number>; expired_exceptions: number;
}
export interface RuleCoverage { evaluated: boolean; reason: string | null; records_checked: number; notes: string[]; }
export interface Analysis {
  id: number; analysis_id: number; dataset_id: number; status: string; created_at: string;
  reference_date: string | null; summary: Summary | null;
  coverage: (Record<RuleId | "EXCEPTIONS", RuleCoverage>) | null;   // null em análises antigas
  findings?: Finding[];                         // ausente no histórico
}
export interface Indicators { datasets_count: number; analyses_count: number; latest_analysis_id: number | null; latest: Summary; }
```

## Exemplos

```bash
curl -F "file=@dados.zip" localhost:8080/api/datasets/import
curl -X POST -H "Content-Type: application/json" -d '{"dataset_id":1}' localhost:8080/api/analyses
curl "localhost:8080/api/findings?analysis_id=1&rule_id=R01&limit=50"
curl -OJ "localhost:8080/api/analyses/1/export?format=csv"
```

```ts
const res = await fetch(`${API}/api/findings?analysis_id=${id}&limit=50&offset=${page * 50}`);
const items: Finding[] = await res.json();
const total = Number(res.headers.get("X-Total-Count"));
```

## Notas para o frontend

* **Mostre `coverage`**: regra `evaluated: false` significa "não avaliada" (com `reason`), não "sem problemas".
* `status === "insufficient_information"` pede revisão humana; `valid_exception` é risco aceito (a evidência cita a exceção).
* `source_sheet`/`source_row` apontam a linha da planilha original (linha 1 = cabeçalho) para o link "ver origem".
* CSV exportado neutraliza fórmulas (`=`, `+`, `-`, `@` iniciais ganham `'`).
* Datasets e análises são imutáveis; reanalisar cria nova análise (histórico preservado).


## v0.4.0 — novidades de contrato

* **Achado** ganha `finding_type` (vocabulário de `casos_teste_publicos.expected_category`, ex.: `Excesso_de_Privilegio`,
  `Conflito_SoD`, `Conta_Desligada`, `Acesso_Expirado`, `Retencao_Ausente`, `Guardrail_Ausente`, `Agencia_Excessiva`,
  `Risco_Integrado`), `subject_id` (usuário, ativo `DAxx`, caso de IA `AIxx` ou compartilhamento `SHxxx`) e `related_id`
  (recurso/ativo/regra relacionados). `domain` (= `category`) passa a ter: Identidade e acesso, Segregação de funções,
  Governança de dados, Compartilhamento, Retenção, Governança de IA, Revisão de acesso, Integrado.
* **Resumo** ganha `by_type`. **Cobertura** ganha as chaves `EXCEPTIONS` (inclui exceções sem achado associado) e `META`
  (data de referência e sua fonte).
* **Data de referência**: `reference_date` do corpo > `dataset_info.data_referencia` > hoje.
* `GET /api/analyses/{id}/public-cases` → `{analysis_id, available, reference_date, summary{total,match,divergent,unmatched,computed},
  cases[{test_case_id, verdict, expected, actual, matched_findings, extra_findings, explanation}]}`.
* Exportação CSV inclui `finding_type`, `subject_id`, `related_id`.
