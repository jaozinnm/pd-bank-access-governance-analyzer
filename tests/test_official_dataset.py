"""Integração com o dataset OFICIAL (tests/data/*.xlsx, cópia idêntica do arquivo recebido; não alterada).

Os totais abaixo são um SNAPSHOT de regressão do comportamento da v0.4.0 contra esse arquivo. Se uma
regra/política mudar de propósito, atualize os números junto com docs/v0.4.0-relatorio.md.
"""
import io
import os
import unittest

from pdbank.api import create_app
from pdbank.config import Settings
from pdbank.repository import MemoryRepository
from pdbank.rules import RULE_IDS
from pdbank.schema import OFFICIAL_SHEETS

PATH = os.path.join(os.path.dirname(__file__), "data", "PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx")


@unittest.skipUnless(os.path.exists(PATH), "dataset oficial ausente em tests/data")
class OfficialDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = MemoryRepository()
        cls.c = create_app(cls.repo, Settings(database_url="memory")).test_client()
        with open(PATH, "rb") as fh:
            up = cls.c.post("/api/datasets/import", data={"file": (io.BytesIO(fh.read()), os.path.basename(PATH))},
                            content_type="multipart/form-data")
        cls.upload = up
        cls.analysis = cls.c.post("/api/analyses", json={"dataset_id": up.json["dataset"]["id"]}).json
        cls.findings = cls.analysis["findings"]
        cls.cases = cls.c.get(f"/api/analyses/{cls.analysis['id']}/public-cases").json

    # --- importação
    def test_import_recognizes_all_20_sheets_without_warnings(self):
        self.assertEqual(self.upload.status_code, 201)
        v = self.upload.json["validation"]
        self.assertEqual((v["valid"], len(v["recognized_sheets"]), v["unknown_sheets"], v["warnings"]), (True, 20, [], []))
        self.assertEqual({s["canonical_name"] for s in v["recognized_sheets"]} and len(v["recognized_sheets"]), len(OFFICIAL_SHEETS))
        t = v["tables"]
        self.assertEqual((t["usuarios"], t["permissoes_atuais"], t["revisoes_acesso"], t["casos_uso_ia"], t["excecoes"]), (150, 536, 420, 15, 4))
        self.assertEqual(v["records_total"], 1890)

    # --- cobertura
    def test_all_nine_rules_were_effectively_evaluated(self):
        cov = self.analysis["coverage"]
        for r in RULE_IDS:
            self.assertTrue(cov[r]["evaluated"], f"{r}: {cov[r]['reason']}")
            self.assertGreater(cov[r]["records_checked"], 0, r)
        self.assertEqual((self.analysis["reference_date"]), "2026-11-05")

    def test_findings_per_rule_snapshot(self):
        self.assertEqual(self.analysis["summary"]["by_rule"],
                         {"R01": 16, "R02": 5, "R03": 7, "R04": 65, "R05": 25, "R06": 3, "R07": 19, "R08": 4, "R09": 287})
        self.assertEqual(self.analysis["summary"]["total"], 431)

    # --- anomalias plantadas no dataset
    def pairs(self, rule, ftype):
        return {(f["subject_id"], f["related_id"]) for f in self.findings if f["rule_id"] == rule and f["finding_type"] == ftype}

    def test_r01_outside_baseline_exactly_the_eleven_anomalies(self):
        got = self.pairs("R01", "Excesso_de_Privilegio")
        self.assertEqual(len(got), 11)
        self.assertIn(("U003", "RES03"), got)       # admin legado fora do baseline
        self.assertIn(("U037", "RES04"), got)       # conta desligada
        self.assertIn(("U099", "RES02"), got)       # solicita e aprova
        self.assertNotIn(("U001", "RES01"), got)    # acesso compatível com o papel

    def test_r02_sod_flags_the_five_conflicting_users_via_roles_and_effective_permissions(self):
        self.assertEqual({s for s, _ in self.pairs("R02", "Conflito_SoD")}, {"U021", "U035", "U043", "U099", "U141"})

    def test_r03_r04_r08_planted_cases(self):
        self.assertEqual({s for s, _ in self.pairs("R03", "Proprietario_Ausente")}, {"DA18"})
        self.assertEqual({s for s, _ in self.pairs("R03", "Classificacao_Ausente")}, {"DA20"})
        self.assertEqual({s for s, _ in self.pairs("R04", "Retencao_Ausente")}, {"DA18", "DA20", "DA23"})
        self.assertIn(("U010", "RES01"), self.pairs("R08", "Acesso_Expirado"))
        self.assertEqual(len(self.pairs("R08", "Acesso_Expirado")), 4)

    def test_r07_only_dismissed_users_not_those_on_leave(self):
        self.assertEqual({s for s, _ in self.pairs("R07", "Conta_Desligada")}, {"U037", "U074", "U111", "U148", "U150"})

    def test_ai_findings_use_controles_ia_values(self):
        by_case = {}
        for f in self.findings:
            if f["rule_id"] in ("R05", "R06"):
                by_case.setdefault(f["subject_id"], set()).add(f["finding_type"])
        self.assertIn("Guardrail_Ausente", by_case["AI02"])          # prompt_injection_protection = Nao
        self.assertIn("Agencia_Excessiva", by_case["AI06"])           # Executar + Critico
        self.assertTrue({"Risco_Integrado", "Acesso_Excessivo", "Agencia_Excessiva"} <= by_case["AI14"])
        self.assertNotIn("AI12", by_case)                              # baixo impacto, controles exigidos presentes
        # AI07: linha de casos_uso_ia com colunas deslocadas no Excel -> não se adivinha autonomia/impacto;
        # a fonte DA09 não aprovada (outra aba, chave ai_use_case_id) continua sendo avaliada normalmente.
        self.assertEqual(by_case["AI07"], {"Dado_Inconsistente", "Fonte_Nao_Aprovada"})

    # --- exceções
    def test_exception_association_and_validity(self):
        cov = self.analysis["coverage"]["EXCEPTIONS"]["notes"]
        self.assertIn("valid: 4", cov)
        ex = [f for f in self.findings if f["status"] == "valid_exception"]
        self.assertEqual({(f["subject_id"], f["related_id"], f["rule_id"]) for f in ex},
                         {("U003", "RES03", "R01"), ("U057", "RES06", "R01")})
        self.assertTrue(any("DA11" in n and "AI03" in n for n in cov), "exceções sem achado associado devem ser reportadas")

    # --- casos públicos
    def test_public_cases_comparison_is_honest(self):
        c = self.cases
        self.assertEqual(c["summary"], {"total": 15, "match": 13, "divergent": 0, "unmatched": 1, "computed": 1})
        v = {x["test_case_id"]: x["verdict"] for x in c["cases"]}
        self.assertEqual((v["TC01"], v["TC09"], v["TC15"]), ("match", "computed", "unmatched"))
        for tc in ("TC01", "TC02", "TC03", "TC04", "TC05", "TC06", "TC07", "TC08", "TC10", "TC11", "TC12", "TC13", "TC14"):
            self.assertEqual(v[tc], "match", tc)

    def test_export_csv_has_traceability_columns(self):
        r = self.c.get(f"/api/analyses/{self.analysis['id']}/export?format=csv")
        head = r.data.decode("utf-8-sig").splitlines()[0]
        for col in ("finding_type", "subject_id", "related_id", "source_sheet", "source_row"):
            self.assertIn(col, head)


if __name__ == "__main__":
    unittest.main()
