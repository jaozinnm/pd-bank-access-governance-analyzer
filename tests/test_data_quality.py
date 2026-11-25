"""Trava as evidências da nota de qualidade de dados (docs/entregas/cesar/nota_qualidade_dados.md).

Snapshot do dataset OFICIAL v2.0. Se o dataset ou uma regra mudar de propósito, atualize os números
junto com a nota e com docs/entregas/cesar/pendencias_dados.csv.
"""
import os
import tempfile
import unittest

from scripts.check_data_quality import (build_report, reconstruct_shifted_ai_row, sha256,
                                        summarize_findings, write_corrected_copy, load)
from pdbank.rules import analyze_full

PATH = os.path.join(os.path.dirname(__file__), "data", "PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx")
OFFICIAL_SHA256 = "70e7e7598125fa5026fbc36adba65322247c3adac62d699020fc0157c2299e76"


@unittest.skipUnless(os.path.exists(PATH), "dataset oficial ausente em tests/data")
class DataQualityEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = build_report(PATH)

    def test_official_file_is_the_expected_one(self):
        self.assertEqual(self.rep["sha256"], OFFICIAL_SHA256)
        self.assertEqual(self.rep["data_referencia"], "2026-11-05")

    def test_p1_all_sheets_and_headers_are_handled(self):
        p = self.rep["P1_schema"]
        self.assertEqual((p["abas_presentes"], p["abas_extras"], p["registros"], p["cabecalhos_sem_tratamento"]),
                         (20, [], 1890, 0))

    def test_p2_only_known_orphans(self):
        orphans = {r["relacao"]: r["orfaos"] for r in self.rep["P2_relacoes"]["relacoes"] if r["orfaos"]}
        self.assertEqual(orphans, {"usuarios.manager_id": 10, "casos_uso_ia.owner_id": 1})
        self.assertEqual(len(self.rep["P2_relacoes"]["usuarios_gestor_de_si_mesmo"]), 14)
        self.assertEqual(self.rep["P2_relacoes"]["compartilhamentos_pedidos_por_desligado"], ["SH002(U037)", "SH022(U111)"])

    def test_p3_application_principals(self):
        p = self.rep["P3_principals_aplicacao"]
        self.assertEqual((p["total"], p["aplicacoes"]), (29, 18))
        self.assertEqual(p["por_permissao"], {"Admin": 16, "Read": 9, "Write": 3, "Execute": 1})
        self.assertEqual(len(p["admin_em_recurso_critico"]), 7)
        self.assertEqual(p["aplicacoes_com_dono_nao_ativo"], [])

    def test_p4_leave_users_have_no_leave_start_date(self):
        p = self.rep["P4_usuarios_licenca"]
        self.assertEqual([u["user_id"] for u in p["usuarios"]], ["U052", "U105"])
        self.assertFalse(p["data_inicio_licenca_disponivel"])

    def test_p5_only_ai07_is_shifted_and_reconstruction_is_unambiguous(self):
        rows = self.rep["P5_linhas_ia_deslocadas"]["linhas_inconsistentes"]
        self.assertEqual([r["ai_use_case_id"] for r in rows], ["AI07"])
        fixed = rows[0]["reconstruida"]
        self.assertEqual((fixed["action_level"], fixed["impact_level"], fixed["owner_id"], fixed["status"]),
                         ("Recomendar", "Alto", "U016", "Proposta"))
        self.assertIsNone(fixed["business_area"])  # valor perdido: não é inventado

    def test_p6_recertification_distribution(self):
        p = self.rep["P6_revisoes"]
        self.assertEqual(p["recertificacao_vencida_total"], 124)
        self.assertEqual(sum(p["recertificacao_vencida_por_atraso_dias"].values()), 124)
        self.assertEqual(p["pendentes_ainda_nao_vencidas"], 0)

    def test_p7_ex003_ex004_cover_no_finding(self):
        cover = {e["exception_id"]: e["achados_cobertos"] for e in self.rep["P7_excecoes"]["excecoes"]}
        self.assertEqual(cover["EX003"], [])
        self.assertEqual(cover["EX004"], [])
        self.assertTrue(cover["EX001"] and cover["EX002"])

    def test_p8_data_fields(self):
        p = self.rep["P8_campos_dados"]
        self.assertEqual((p["campos"], p["ativos_com_campos"]), (135, 30))
        self.assertEqual(p["campo_financeiro_mas_ativo_sem_dado_financeiro"], ["DA01", "DA09", "DA10", "DA16"])
        self.assertEqual(p["campo_pessoal_mas_ativo_sem_dado_pessoal"], [])
        self.assertEqual(p["identificador_direto_em_ativo_abaixo_de_confidencial"], [])

    def test_total_findings_unchanged(self):
        self.assertEqual(self.rep["achados"]["total"], 431)


@unittest.skipUnless(os.path.exists(PATH), "dataset oficial ausente em tests/data")
class CorrectedCopyTests(unittest.TestCase):
    def test_corrected_copy_changes_only_ai07_and_keeps_original_intact(self):
        before = summarize_findings(analyze_full(load(PATH)).findings)["por_tipo"]
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            dst = os.path.join(tmp, "copia_teste.xlsx")
            self.assertEqual(write_corrected_copy(PATH, dst), ["AI07"])
            after = summarize_findings(analyze_full(load(dst)).findings)["por_tipo"]
        delta = {k: after.get(k, 0) - before.get(k, 0) for k in set(before) | set(after) if after.get(k, 0) != before.get(k, 0)}
        self.assertEqual(delta, {"R05:Guardrail_Ausente": 1, "R06:Dado_Inconsistente": -1})
        self.assertEqual(sha256(PATH), OFFICIAL_SHA256)

    def test_refuses_to_overwrite_official(self):
        with self.assertRaises(ValueError):
            write_corrected_copy(PATH, PATH)


class ReconstructionUnitTests(unittest.TestCase):
    def test_valid_row_is_not_touched(self):
        self.assertIsNone(reconstruct_shifted_ai_row({"action_level": "Executar", "impact_level": "Critico"}))

    def test_ambiguous_row_is_not_guessed(self):
        self.assertIsNone(reconstruct_shifted_ai_row({"purpose": "x", "action_level": "Alto", "impact_level": "U1"}))


class DeliveryClosureTests(unittest.TestCase):
    """A tabela de pendências da entrega do César precisa estar 100% encerrada e coerente com a nota."""
    CSV = os.path.join(os.path.dirname(__file__), "..", "docs", "entregas", "cesar", "pendencias_dados.csv")

    def test_every_pending_item_is_closed_with_a_recorded_outcome(self):
        import csv
        with open(self.CSV, encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh, delimiter=";"))
        self.assertEqual([r["id"] for r in rows], [f"P{i}" for i in range(1, 9)])
        for r in rows:
            self.assertEqual(r["status"], "Concluída", r["id"])
            self.assertTrue(r["decisao"].strip() and r["fechamento_v2"].strip(), r["id"])


if __name__ == "__main__":
    unittest.main()
