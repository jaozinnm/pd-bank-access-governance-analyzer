"""Especificação OpenAPI 3.0 (fonte para gerar tipos TypeScript: openapi-typescript)."""
from __future__ import annotations

from .rules import RULE_IDS
from .summary import SEVERITIES, STATUSES


def _ref(name): return {"$ref": f"#/components/schemas/{name}"}
def _json(schema, desc="OK"): return {"description": desc, "content": {"application/json": {"schema": schema}}}
def _err(desc): return _json(_ref("Error"), desc)
def _arr(name): return {"type": "array", "items": _ref(name)}
def _qp(name, schema, desc): return {"name": name, "in": "query", "required": False, "schema": schema, "description": desc}
def _id(name="id"): return {"name": name, "in": "path", "required": True, "schema": {"type": "integer", "minimum": 1}}


def build_spec(version: str) -> dict:
    nullable_str = {"type": "string", "nullable": True}
    schemas = {
        "Error": {"type": "object", "required": ["error"], "properties": {"error": {"type": "string"}, "validation": _ref("ValidationResult")}},
        "Dataset": {"type": "object", "required": ["id", "name", "created_at", "table_counts"], "properties": {
            "id": {"type": "integer"}, "name": {"type": "string"}, "created_at": {"type": "string", "format": "date-time"},
            "table_counts": {"type": "object", "additionalProperties": {"type": "integer", "nullable": True}}}},
        "ValidationResult": {"type": "object", "required": ["valid", "errors", "warnings"], "properties": {
            "valid": {"type": "boolean"},
            "errors": {"type": "array", "items": {"type": "object", "properties": {"table": nullable_str, "row": {"type": "integer", "nullable": True}, "message": {"type": "string"}}}},
            "warnings": {"type": "array", "items": {"type": "string"}},
            "recognized_sheets": {"type": "array", "items": {"type": "object", "properties": {"source_name": {"type": "string"}, "canonical_name": {"type": "string"}}}},
            "unknown_sheets": {"type": "array", "items": {"type": "string"}},
            "records_total": {"type": "integer"}, "records_accepted": {"type": "integer"}, "records_rejected": {"type": "integer"},
            "tables": {"type": "object", "additionalProperties": {"type": "integer", "nullable": True}}}},
        "ImportResponse": {"type": "object", "required": ["dataset", "validation", "import"], "properties": {
            "dataset": _ref("Dataset"), "validation": _ref("ValidationResult"),
            "import": {"type": "object", "properties": {"warnings": {"type": "array", "items": {"type": "string"}},
                                                          "sources": {"type": "array", "items": {"type": "object", "properties": {
                                                              "file": {"type": "string"}, "sheet": {"type": "string"}, "table": {"type": "string"}, "rows": {"type": "integer"}}}}}}}},
        "Finding": {"type": "object", "properties": {
            "id": {"type": "integer"}, "analysis_id": {"type": "integer"}, "rule_id": {"type": "string", "enum": list(RULE_IDS)},
            "category": {"type": "string"}, "domain": {"type": "string", "description": "Igual a category."},
            "severity": {"type": "string", "enum": list(SEVERITIES)}, "status": {"type": "string", "enum": list(STATUSES)},
            "exception_status": {"type": "string", "enum": ["none", "valid", "expired", "future"]},
            "object_ref": {"type": "string"}, "finding_type": nullable_str, "subject_id": nullable_str, "related_id": nullable_str,
            "source_sheet": nullable_str, "source_row": {"type": "integer", "nullable": True},
            "evidence": {"type": "string"}, "description": {"type": "string"}, "impact": {"type": "string"},
            "recommendation": {"type": "string"}, "reviewer": nullable_str}},
        "Summary": {"type": "object", "properties": {
            "total": {"type": "integer"}, "by_severity": {"type": "object", "additionalProperties": {"type": "integer"}},
            "by_status": {"type": "object", "additionalProperties": {"type": "integer"}},
            "by_rule": {"type": "object", "additionalProperties": {"type": "integer"}},
            "by_type": {"type": "object", "additionalProperties": {"type": "integer"}}, "expired_exceptions": {"type": "integer"}}},
        "RuleCoverage": {"type": "object", "properties": {"evaluated": {"type": "boolean"}, "reason": nullable_str,
                                                          "records_checked": {"type": "integer"}, "notes": {"type": "array", "items": {"type": "string"}}}},
        "Analysis": {"type": "object", "properties": {
            "id": {"type": "integer"}, "analysis_id": {"type": "integer"}, "dataset_id": {"type": "integer"},
            "status": {"type": "string"}, "created_at": {"type": "string", "format": "date-time"},
            "reference_date": nullable_str, "summary": _ref("Summary"),
            "coverage": {"type": "object", "nullable": True, "additionalProperties": _ref("RuleCoverage"),
                         "description": "Por regra (R01–R09) e EXCEPTIONS: avaliada ou pulada (com motivo)."},
            "findings": _arr("Finding")}},
        "Rule": {"type": "object", "properties": {"rule_id": {"type": "string"}, "title": {"type": "string"}}},
        "Role": {"type": "object", "required": ["role_id", "name", "area", "macro_profile", "responsibilities", "incompatibilities", "elevated_access"],
                 "properties": {"role_id": {"type": "string"}, "name": {"type": "string"}, "area": {"type": "string"},
                                "macro_profile": {"type": "string"}, "catalog_status": {"type": "string"}, "purpose": {"type": "string"},
                                "responsibilities": {"type": "array", "items": {"type": "string"}},
                                "incompatibilities": {"type": "array", "items": {"type": "string"}},
                                "elevated_access": {"type": "object", "properties": {
                                    "required": {"type": "boolean"}, "mode": {"type": "string"},
                                    "permanent": {"type": "boolean"}, "rationale": {"type": "string"}}}}},
        "SeparationConstraint": {"type": "object", "required": ["constraint_id", "roles", "activities", "rationale", "status"],
                                 "properties": {"constraint_id": {"type": "string"}, "roles": _arr("RoleId"),
                                                "activities": {"type": "array", "items": {"type": "string"}},
                                                "rationale": {"type": "string"}, "status": {"type": "string"}}},
        "RoleId": {"type": "string"},
        "RoleCatalog": {"type": "object", "required": ["version", "status", "roles", "separation_constraints"],
                        "properties": {"version": {"type": "string"}, "status": {"type": "string"},
                                       "source_notes": {"type": "array", "items": {"type": "string"}},
                                       "roles": _arr("Role"), "separation_constraints": _arr("SeparationConstraint")}},
    }
    filters = [
        _qp("analysis_id", {"type": "integer", "minimum": 1}, "Filtra por análise"), _qp("domain", {"type": "string"}, "Categoria/domínio (igualdade exata)"),
        _qp("rule_id", {"type": "string", "enum": list(RULE_IDS)}, "R01–R09"), _qp("severity", {"type": "string", "enum": list(SEVERITIES)}, "Severidade"),
        _qp("status", {"type": "string", "enum": list(STATUSES)}, "Situação"),
        _qp("exception_status", {"type": "string", "enum": ["none", "valid", "expired", "future"]}, "Estado da exceção"),
        _qp("q", {"type": "string"}, "Busca por trecho em object_ref"),
        _qp("limit", {"type": "integer", "minimum": 1, "maximum": 1000, "default": 200}, "Página"),
        _qp("offset", {"type": "integer", "minimum": 0, "default": 0}, "Deslocamento"),
    ]
    return {
        "openapi": "3.0.3",
        "info": {"title": "PD Bank Access & Governance Analyzer API", "version": version,
                 "description": "Sem autenticação por padrão; defina API_KEY para exigir o cabeçalho X-API-Key. CORS via CORS_ORIGINS."},
        "servers": [{"url": "/"}],
        "components": {"schemas": schemas, "securitySchemes": {"ApiKey": {"type": "apiKey", "in": "header", "name": "X-API-Key"}}},
        "paths": {
            "/api/health": {"get": {"summary": "Health check", "responses": {"200": _json({"type": "object"}), "503": _json({"type": "object"}, "Banco indisponível")}}},
            "/api/rules": {"get": {"summary": "Catálogo de regras", "responses": {"200": _json(_arr("Rule"))}}},
            "/api/roles": {"get": {"summary": "Catálogo funcional de papéis proposto", "description": "R01–R14 reproduzem IDs, nomes e áreas do dataset oficial; responsabilidades, incompatibilidades e elevação são propostas. O endpoint não concede permissões.", "responses": {"200": _json(_ref("RoleCatalog"))}}},
            "/api/datasets/import": {"post": {"summary": "Importar XLSX, CSV ou ZIP (multipart, campo 'file')",
                "requestBody": {"required": True, "content": {"multipart/form-data": {"schema": {"type": "object", "required": ["file"], "properties": {"file": {"type": "string", "format": "binary"}}}}}},
                "responses": {"201": _json(_ref("ImportResponse"), "Importado"), "400": _err("Arquivo inválido/malicioso/formato não suportado"), "413": _err("Acima de 50 MB")}}},
            "/api/datasets/validate": {"post": {"summary": "Validar tabelas JSON",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object", "required": ["tables"], "properties": {"tables": {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "object"}}}}}}}},
                "responses": {"200": _json(_ref("ValidationResult")), "400": _err("Corpo inválido")}}},
            "/api/datasets": {"get": {"summary": "Listar datasets importados", "responses": {"200": _json(_arr("Dataset"))}}},
            "/api/datasets/{id}": {"get": {"summary": "Detalhe do dataset + validação", "parameters": [_id()],
                "responses": {"200": _json({"type": "object", "properties": {"dataset": _ref("Dataset"), "validation": _ref("ValidationResult")}}), "404": _err("Não encontrado")}}},
            "/api/analyses": {
                "get": {"summary": "Histórico de análises (sem findings)", "responses": {"200": _json(_arr("Analysis"))}},
                "post": {"summary": "Executar análise de um dataset",
                    "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object", "required": ["dataset_id"], "properties": {
                        "dataset_id": {"type": "integer", "minimum": 1}, "reference_date": {"type": "string", "format": "date", "description": "Data usada para vigência de exceções/prazos; padrão: dataset_info.data_referencia; se ausente, hoje (America/Sao_Paulo)."}}}}}},
                    "responses": {"201": _json(_ref("Analysis")), "400": _err("Parâmetros inválidos"), "404": _err("Dataset não encontrado"), "422": _err("Dataset estruturalmente inválido")}}},
            "/api/analyses/{id}": {"get": {"summary": "Detalhe da análise com achados e cobertura", "parameters": [_id()], "responses": {"200": _json(_ref("Analysis")), "404": _err("Não encontrada")}}},
            "/api/analyses/{id}/public-cases": {"get": {"summary": "Comparar a análise com casos_teste_publicos (match/divergent/unmatched/computed)",
                "parameters": [_id()], "responses": {"200": _json({"type": "object"}), "404": _err("Análise não encontrada")}}},
            "/api/analyses/{id}/export": {"get": {"summary": "Exportar JSON ou CSV (CSV neutraliza injeção de fórmula)",
                "parameters": [_id(), _qp("format", {"type": "string", "enum": ["json", "csv"], "default": "json"}, "Formato")],
                "responses": {"200": {"description": "Arquivo para download"}, "400": _err("Formato inválido"), "404": _err("Não encontrada")}}},
            "/api/findings": {"get": {"summary": "Listar/filtrar achados (total no cabeçalho X-Total-Count)", "parameters": filters,
                "responses": {"200": {"description": "OK", "headers": {"X-Total-Count": {"schema": {"type": "integer"}}}, "content": {"application/json": {"schema": _arr("Finding")}}}, "400": _err("Filtro inválido")}}},
            "/api/findings/{id}": {"get": {"summary": "Detalhe do achado", "parameters": [_id()], "responses": {"200": _json(_ref("Finding")), "404": _err("Não encontrado")}}},
            "/api/indicators": {"get": {"summary": "Indicadores da última análise", "responses": {"200": _json({"type": "object", "properties": {
                "datasets_count": {"type": "integer"}, "analyses_count": {"type": "integer"}, "latest_analysis_id": {"type": "integer", "nullable": True}, "latest": _ref("Summary")}})}}},
        },
    }
