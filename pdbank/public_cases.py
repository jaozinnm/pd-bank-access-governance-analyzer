"""Comparação do resultado da análise com ``casos_teste_publicos`` (sem inventar correspondências).

Cada caso é cruzado com os achados REAIS do motor por (subject_id, related_id) dentro de um escopo de
regras definido pelo domínio do caso. O veredito é uma de:

* ``match``      — categoria, prioridade e decisão esperadas coincidem com o resultado do motor;
* ``divergent``  — há achado da categoria esperada, mas prioridade/decisão diferem (motivo explicado);
* ``unmatched``  — o motor não produziu o achado esperado (ou produziu achado onde se esperava nenhum);
* ``computed``   — o caso pede "Calcular": mostramos o resultado calculado, sem aprovar/reprovar.

Achados da mesma entidade fora do escopo do caso aparecem em ``extra_findings`` e NÃO alteram o veredito.
"""
from __future__ import annotations

from collections import Counter

from .rules import SEV_ORDER, Engine
from .schema import get
from .values import normalize

PRIORITY = {"critico": "critical", "alto": "high", "medio": "medium", "baixo": "low"}
RETENTION_TYPES = {"Retencao_Ausente"}
# domínio do caso -> predicado de escopo sobre um achado
SCOPES = {
    "acesso": lambda f: f["rule_id"] in ("R01", "R02", "R07", "R08"),
    "dados": lambda f: f["rule_id"] == "R03" or f["finding_type"] in RETENTION_TYPES,
    "retencao": lambda f: f["finding_type"] in RETENTION_TYPES,
    "compartilhamento": lambda f: f["rule_id"] == "R04" and f["finding_type"] not in RETENTION_TYPES,
    "ia": lambda f: f["rule_id"] in ("R05", "R06") and f["finding_type"] != "Risco_Integrado",
    "integrado": lambda f: f["finding_type"] == "Risco_Integrado",
}


def _related_ok(f: dict, related) -> bool:
    if not related:
        return True
    r = str(related).lower()
    return r in str(f.get("related_id") or "").lower() or r in str(f.get("evidence") or "").lower()


def _brief(f: dict) -> dict:
    return {"rule_id": f["rule_id"], "finding_type": f["finding_type"], "severity": f["severity"], "status": f["status"],
            "related_id": f.get("related_id"), "source": f"{f['source_sheet']}#{f['source_row']}"}


def compare_public_cases(data: dict, findings: list) -> dict:
    eng = Engine(data)
    cases = eng.rows("public_test_cases")
    if not cases:
        return {"available": False, "reason": "aba casos_teste_publicos ausente ou vazia", "summary": {}, "cases": []}
    out = []
    for c in cases:
        tid, domain = get(c.d, "test_case_id"), normalize(get(c.d, "domain", default=""))
        subject, related = get(c.d, "subject_id"), get(c.d, "related_id")
        exp_cat, exp_dec = normalize(get(c.d, "expected_category", default="")), normalize(get(c.d, "expected_decision", default=""))
        exp_pri_raw = normalize(get(c.d, "expected_priority", default=""))
        exp_pri = PRIORITY.get(exp_pri_raw)
        scope = SCOPES.get(domain)
        res = {"test_case_id": tid, "domain": get(c.d, "domain"), "subject_id": subject, "related_id": related,
               "scenario": get(c.d, "scenario"),
               "expected": {"priority": get(c.d, "expected_priority"), "decision": get(c.d, "expected_decision"),
                            "category": get(c.d, "expected_category")}}
        if scope is None or subject is None:
            out.append({**res, "verdict": "unmatched", "actual": None, "explanation": f"domínio {get(c.d, 'domain')!r} sem escopo de comparação definido"})
            continue
        mine = [f for f in findings if str(f["subject_id"]).lower() == str(subject).lower() and _related_ok(f, related)]
        in_scope = [f for f in mine if scope(f)]
        extra = [f for f in findings if str(f["subject_id"]).lower() == str(subject).lower() and not scope(f)]
        sevs = [f["severity"] for f in in_scope]
        open_ = [f for f in in_scope if f["status"] != "valid_exception"]
        covered_crit = any(f["status"] == "valid_exception" and f["severity"] == "critical" for f in in_scope)
        actual = {"findings": len(in_scope), "types": sorted({f["finding_type"] for f in in_scope}),
                  "max_severity": max(sevs, key=SEV_ORDER.index) if sevs else None,
                  "decision": "Conforme" if not in_scope else ("Revisao" if open_ or covered_crit else "Atencao")}
        res["actual"], res["matched_findings"] = actual, [_brief(f) for f in in_scope]
        res["extra_findings"] = [{"rule_id": k[0], "finding_type": k[1], "severity": k[2], "count": n}
                                 for k, n in sorted(Counter((f["rule_id"], f["finding_type"], f["severity"]) for f in extra).items())]
        verdict, why = "unmatched", ""
        if exp_dec == "calcular":
            verdict = "computed"
            why = ("resultado calculado pelo motor: " + (f"{len(in_scope)} achado(s) ({', '.join(actual['types'])})" if in_scope else
                   "nenhum achado — destino aprovado, com minimização e proteção; compartilhamento conforme"))
        elif exp_cat == "sem_achado":
            verdict = "match" if not in_scope else "unmatched"
            why = "nenhum achado no escopo do caso" if not in_scope else f"o motor gerou {len(in_scope)} achado(s) no escopo onde se esperava nenhum: {', '.join(actual['types'])}"
        elif exp_cat == "excecao_valida":
            valid = [f for f in in_scope if f["status"] == "valid_exception"]
            if in_scope and not open_:
                verdict, why = "match", "todos os achados do escopo estão cobertos por exceção válida"
            else:
                ex_state = [e for e in eng._exceptions if e["subject"] == str(subject).lower()]
                why = ("existe exceção " + ", ".join(f"{e['row'].number and get(e['row'].d, 'exception_id')} ({e['state']})" for e in ex_state) +
                       " para o sujeito, mas o motor não produz nenhum achado ao qual ela se aplique com as regras atuais; "
                       "a definição do achado esperado depende da equipe") if ex_state else "nenhuma exceção encontrada e nenhum achado coberto"
                if valid:
                    why = "parte dos achados está coberta por exceção"
        else:
            same = [f for f in in_scope if normalize(f["finding_type"]) == exp_cat]
            if not same:
                why = f"o motor não produziu achado da categoria {get(c.d, 'expected_category')} para este sujeito/relacionado"
            else:
                top = max((f["severity"] for f in same), key=SEV_ORDER.index)
                covered = all(f["status"] == "valid_exception" for f in same)
                problems = []
                if exp_pri and top != exp_pri:
                    problems.append(f"prioridade do motor = {top}, esperada = {exp_pri}")
                if exp_dec == "revisao" and covered and top != "critical":
                    problems.append("o achado está coberto por exceção válida (decisão do motor: Atencao), mas o caso espera Revisao — "
                                    "o caso público não considera a exceção; decisão de negócio pendente")
                verdict = "match" if not problems else "divergent"
                why = "; ".join(problems) or "categoria, prioridade e decisão coincidem"
        res.update(verdict=verdict, explanation=why)
        out.append(res)
    count = Counter(r["verdict"] for r in out)
    return {"available": True, "reference_date": eng.today.isoformat(),
            "summary": {"total": len(out), **{k: count.get(k, 0) for k in ("match", "divergent", "unmatched", "computed")}},
            "cases": out}
