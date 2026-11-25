"""API Flask. Só conversa com ``Repository`` (sem SQLAlchemy aqui)."""
from __future__ import annotations

import hmac
import json
import logging

from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import HTTPException

from . import __version__
from .config import Settings
from .export import findings_to_csv
from .public_cases import compare_public_cases
from .importer import ImportFailure, import_file, safe_filename
from .openapi import build_spec
from .repository import FINDING_FILTERS, Repository
from .role_catalog import get_role_catalog
from .rules import RULE_IDS, RULE_TITLES, analyze_full
from .summary import SEVERITIES, STATUSES, summarize
from .validation import validate_data
from .values import parse_date

log = logging.getLogger("pdbank")
SERVICE = "PD Bank Access & Governance Analyzer"
EXCEPTION_STATES = ("none", "valid", "expired", "future")


class ApiError(Exception):
    def __init__(self, message: str, code: int = 400, **extra):
        super().__init__(message)
        self.message, self.code, self.extra = message, code, extra


def _json_body() -> dict:
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ApiError("Corpo JSON inválido: envie um objeto JSON com Content-Type: application/json.", 400)
    return body


def _int_arg(name: str, default=None, minimum=0, maximum=None):
    raw = request.args.get(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ApiError(f"Parâmetro '{name}' deve ser um inteiro.", 400) from None
    if value < minimum or (maximum is not None and value > maximum):
        raise ApiError(f"Parâmetro '{name}' fora do intervalo permitido.", 400)
    return value


def _choice_arg(name: str, allowed: tuple, upper=False):
    raw = request.args.get(name)
    if raw is None or raw == "":
        return None
    value = raw.strip().upper() if upper else raw.strip()
    if value not in allowed:
        raise ApiError(f"Valor inválido para '{name}'. Permitidos: {', '.join(allowed)}.", 400)
    return value


def create_app(repository: Repository | None = None, settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    if repository is None:
        from .sql_repository import SqlRepository  # import tardio: SQLAlchemy só quando necessário
        repository = SqlRepository(settings.database_url)
    repository.init()
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = settings.max_upload_mb * 1024 * 1024
    app.config["JSON_AS_ASCII"] = False
    app.json.ensure_ascii = False
    repo = repository

    # ------------------------------------------------------------ CORS / auth
    def _cors_headers(resp: Response) -> Response:
        origin = request.headers.get("Origin")
        if origin and settings.cors_origins and ("*" in settings.cors_origins or origin in settings.cors_origins):
            resp.headers["Access-Control-Allow-Origin"] = "*" if "*" in settings.cors_origins else origin
            resp.headers["Vary"] = "Origin"
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            resp.headers["Access-Control-Expose-Headers"] = "X-Total-Count, Content-Disposition"
        return resp

    @app.before_request
    def _guard():
        if request.method == "OPTIONS":
            return _cors_headers(app.make_default_options_response())
        public = request.path in ("/api/health", "/openapi.json", "/docs")
        if settings.api_key and request.path.startswith("/api/") and not public:
            given = request.headers.get("X-API-Key", "")
            if not hmac.compare_digest(given.encode(), settings.api_key.encode()):
                return _cors_headers(jsonify({"error": "Chave de API ausente ou inválida."})), 401
        return None

    @app.after_request
    def _after(resp):
        return _cors_headers(resp)

    @app.errorhandler(ApiError)
    def _api_error(e: ApiError):
        return jsonify({"error": e.message, **e.extra}), e.code

    @app.errorhandler(HTTPException)
    def _http_error(e: HTTPException):
        messages = {404: "Recurso não encontrado.", 405: "Método HTTP não permitido para este recurso.",
                    413: "Arquivo excede o limite permitido."}
        return jsonify({"error": messages.get(e.code, e.description or e.name)}), e.code

    @app.errorhandler(Exception)
    def _unexpected(e: Exception):
        log.exception("Erro inesperado")
        return jsonify({"error": "Erro interno do servidor."}), 500

    # ------------------------------------------------------------ rotas
    @app.get("/api/health")
    def health():
        ok = repo.ping()
        body = {"status": "ok" if ok else "degraded", "database": "ok" if ok else "unavailable",
                "service": SERVICE, "version": __version__}
        return jsonify(body), (200 if ok else 503)

    @app.get("/api/rules")
    def rules_catalog():
        return jsonify([{"rule_id": r, "title": RULE_TITLES[r]} for r in RULE_IDS])

    @app.get("/api/roles")
    def roles_catalog():
        """Catálogo funcional proposto; não representa permissões concedidas."""
        return jsonify(get_role_catalog())

    @app.post("/api/datasets/import")
    def import_dataset():
        if "file" not in request.files:
            raise ApiError('Envie o arquivo no campo multipart "file".', 400)
        f = request.files["file"]
        if not f.filename:
            raise ApiError("Nome de arquivo ausente.", 400)
        name = safe_filename(f.filename)
        try:
            result = import_file(name, f.read())
        except ImportFailure as exc:
            raise ApiError(str(exc), 400) from exc
        ds = repo.add_dataset(name, result.tables)
        validation = validate_data(result.tables, result.warnings)
        return jsonify({"dataset": ds, "validation": validation,
                        "import": {"warnings": result.warnings, "sources": result.sources}}), 201

    @app.post("/api/datasets/validate")
    def validate_endpoint():
        # Aceita tanto o contrato JSON original quanto o upload multipart do frontend.
        # A validação de arquivo NÃO persiste o dataset.
        if "file" in request.files:
            f = request.files["file"]
            if not f.filename:
                raise ApiError("Nome de arquivo ausente.", 400)
            try:
                result = import_file(safe_filename(f.filename), f.read())
            except ImportFailure as exc:
                raise ApiError(str(exc), 400) from exc
            return jsonify(validate_data(result.tables, result.warnings))
        tables = _json_body().get("tables")
        if not isinstance(tables, dict):
            raise ApiError('Corpo esperado: {"tables": {"nome_da_tabela": [linhas]}}.', 400)
        return jsonify(validate_data(tables))

    @app.get("/api/datasets")
    def datasets():
        return jsonify(repo.list_datasets())

    @app.get("/api/datasets/<int:dataset_id>")
    def dataset_detail(dataset_id: int):
        d = repo.get_dataset(dataset_id)
        if d is None:
            raise ApiError("Dataset não encontrado.", 404)
        tables = d.pop("tables")
        return jsonify({"dataset": d, "validation": validate_data(tables)})

    @app.post("/api/analyses")
    def run_analysis():
        body = _json_body()
        did = body.get("dataset_id")
        if did is None:
            raise ApiError("dataset_id é obrigatório.", 400)
        if isinstance(did, bool) or not isinstance(did, int) or did < 1:
            raise ApiError("dataset_id deve ser um inteiro positivo.", 400)
        ref = None
        if body.get("reference_date") is not None:
            ref = parse_date(body["reference_date"])
            if ref is None:
                raise ApiError("reference_date inválida; use AAAA-MM-DD.", 400)
        ds = repo.get_dataset(did)
        if ds is None:
            raise ApiError("Dataset não encontrado.", 404)
        check = validate_data(ds["tables"])
        if not check["valid"]:
            raise ApiError("Dataset inválido.", 422, validation=check)
        out = analyze_full(ds["tables"], ref)
        saved = repo.add_analysis(did, out.reference_date, out.coverage, summarize(out.findings), out.findings)
        return jsonify(_analysis_payload(saved)), 201

    def _analysis_payload(a: dict, with_findings: bool = True) -> dict:
        payload = {**{k: v for k, v in a.items() if k != "findings"}, "analysis_id": a["id"]}
        if with_findings:
            payload["findings"] = a.get("findings", [])
        return payload

    @app.get("/api/analyses")
    def analyses():
        return jsonify([_analysis_payload(a, with_findings=False) for a in repo.list_analyses()])

    @app.get("/api/analyses/<int:aid>")
    def analysis_detail(aid: int):
        a = repo.get_analysis(aid)
        if a is None:
            raise ApiError("Análise não encontrada.", 404)
        return jsonify(_analysis_payload(a))

    @app.get("/api/analyses/<int:aid>/public-cases")
    def analysis_public_cases(aid: int):
        a = repo.get_analysis(aid)
        if a is None:
            raise ApiError("Análise não encontrada.", 404)
        ds = repo.get_dataset(a["dataset_id"])
        if ds is None:
            raise ApiError("Dataset da análise não encontrado.", 404)
        return jsonify({"analysis_id": aid, **compare_public_cases(ds["tables"], a["findings"])})

    @app.get("/api/findings")
    def list_findings():
        filters = {
            "analysis_id": _int_arg("analysis_id", minimum=1),
            "domain": (request.args.get("domain") or None),
            "rule_id": _choice_arg("rule_id", RULE_IDS, upper=True),
            "severity": _choice_arg("severity", SEVERITIES),
            "status": _choice_arg("status", STATUSES),
            "exception_status": _choice_arg("exception_status", EXCEPTION_STATES),
        }
        assert set(filters) == set(FINDING_FILTERS)
        limit = _int_arg("limit", default=200, minimum=1, maximum=1000)
        offset = _int_arg("offset", default=0, minimum=0)
        items, total = repo.list_findings(filters, limit, offset, request.args.get("q") or None)
        resp = jsonify(items)
        resp.headers["X-Total-Count"] = str(total)
        return resp

    @app.get("/api/findings/<int:fid>")
    def finding_detail(fid: int):
        f = repo.get_finding(fid)
        if f is None:
            raise ApiError("Achado não encontrado.", 404)
        return jsonify(f)

    @app.get("/api/indicators")
    def indicators():
        items = repo.list_analyses()
        latest = items[0] if items else None
        return jsonify({"datasets_count": len(repo.list_datasets()), "analyses_count": len(items),
                        "latest_analysis_id": latest["id"] if latest else None,
                        "latest": latest["summary"] if latest else summarize([])})

    @app.get("/api/analyses/<int:aid>/export")
    def export_analysis(aid: int):
        fmt = (request.args.get("format") or "json").lower()
        if fmt not in ("json", "csv"):
            raise ApiError("Formato inválido; use format=json ou format=csv.", 400)
        a = repo.get_analysis(aid)
        if a is None:
            raise ApiError("Análise não encontrada.", 404)
        if fmt == "csv":
            return Response(findings_to_csv(a["findings"]), mimetype="text/csv; charset=utf-8",
                            headers={"Content-Disposition": f'attachment; filename="analysis-{aid}.csv"'})
        body = json.dumps(_analysis_payload(a), ensure_ascii=False, indent=2).encode("utf-8")
        return Response(body, mimetype="application/json",
                        headers={"Content-Disposition": f'attachment; filename="analysis-{aid}.json"'})

    @app.get("/openapi.json")
    def openapi_spec():
        return jsonify(build_spec(__version__))

    @app.get("/docs")
    def swagger_docs():
        html = ('<!doctype html><html><head><meta charset="utf-8"><title>PD Bank API</title>'
                '<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"></head><body>'
                '<div id="swagger-ui"></div><script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>'
                '<script>SwaggerUIBundle({url:"/openapi.json",dom_id:"#swagger-ui"})</script></body></html>')
        return Response(html, mimetype="text/html")

    return app
