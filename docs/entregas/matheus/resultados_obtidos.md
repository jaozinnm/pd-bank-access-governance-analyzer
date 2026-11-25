# Resultados Obtidos — Execução da Suíte de Testes (v0.4.0)

* **Responsáveis:** Matheus do Nascimento Gomes Vaz e Mateus Valerino Barros de Santana
* **Data de Referência:** `2026-11-05` (`dataset_info.data_referencia`)
* **Comando Base:** `.venv\Scripts\python.exe -m pytest`

---

## 1. Resumo Quantitativo do Motor (`PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx`)

* **Importação:** 20 abas lidas e reconhecidas (`valido: true`, 1.890 registros, 0 avisos).
* **Total de Achados:** **431**
  * **Por Severidade:** `critical`: 44 | `high`: 119 | `medium`: 142 | `low`: 126
  * **Por Status:** `non_compliant`: 428 | `valid_exception`: 2 | `insufficient_information`: 1 | `compliant`: 0
  * **Por Regra:** `R01`: 16 | `R02`: 5 | `R03`: 7 | `R04`: 65 | `R05`: 25 | `R06`: 3 | `R07`: 19 | `R08`: 4 | `R09`: 287
* **Casos Públicos (`casos_teste_publicos` — 15 casos após decisões `D1`–`D3`):**
  * `match`: **13** (`TC01`–`TC08`, `TC10`–`TC14`)
  * `computed`: **1** (`TC09` — `SH005`, conferente conforme `D2`)
  * `unmatched`: **1** (`TC15` — `AI03/DA12`, não aplicável conforme `D3`)
  * `divergent`: **0**

---

## 2. Resultados Obtidos por Caso de Teste (`T1`–`T8`)

| ID | Teste Automatizado Executado | Status | Resultado Obtido e Evidência |
| :--- | :--- | :--- | :--- |
| **T1** | `tests/test_official_dataset.py::OfficialDatasetTests::test_r07_only_dismissed_users_not_those_on_leave` | **PASSED** (`1.67s`) | 19 achados `Conta_Desligada` em `R07` para os 5 usuários desligados (`U037`, `U074`, `U111`, `U148`, `U150`); `U052` e `U105` (`Licenca`) corretamente ignorados por `R07`. Log: `evidencias/T1_conta_desligada.txt`. |
| **T2** | `tests/test_official_dataset.py::OfficialDatasetTests::test_r03_r04_r08_planted_cases` | **PASSED** (`1.40s`) | 7 achados em `R03` (`DA18` sem proprietário, `DA20` sem classificação e 5 divergências de classificação), além de `DA23` em `R04`. Log: `evidencias/T2_ativos_dados_incompletos.txt`. |
| **T3** | `tests/test_official_dataset.py::OfficialDatasetTests::test_ai_findings_use_controles_ia_values` | **PASSED** (`1.38s`) | `AI02` detectado com `Guardrail_Ausente` (`high`) em `R05`; total de 6 achados `Guardrail_Ausente` coerentes com `controles_ia`. Log: `evidencias/T3_ia_guardrail_ausente.txt`. |
| **T4** | `tests/test_official_dataset.py::OfficialDatasetTests::test_r01_outside_baseline_exactly_the_eleven_anomalies` | **PASSED** (`1.33s`) | 0 achados em `R01` para `U001/RES01` (`TC05`); exatamente 11 `Excesso_de_Privilegio` e 5 `Modo_de_Acesso_Divergente` detectados nas 507 permissões humanas avaliadas. Log: `evidencias/T4_acesso_conforme_baseline.txt`. |
| **T5** | `tests/test_official_dataset.py::OfficialDatasetTests::test_public_cases_comparison_is_honest` | **PASSED** | `AI12` (`TC12`) e `DA02` (`TC08`) retornaram `0` achados (`Conforme`); `TC01` atualizado para `match` após decisão `D1` (`13 match, 0 divergent, 1 computed, 1 unmatched`). Log: `evidencias/T5_ia_baixo_impacto_e_retencao_ok.txt`. |
| **T6** | `tests/test_official_dataset.py::OfficialDatasetTests::test_exception_association_and_validity` | **PASSED** (`1.51s`) | 4 achados `Acesso_Expirado` (`R08`, incluindo `U010/RES01`); 4 exceções válidas (`expired: 0`), com `EX001` e `EX002` associadas aos respectivos achados de `R01` como `valid_exception`. Log: `evidencias/T6_fronteira_datas_e_excecoes.txt`. |
| **T7** | `tests/test_frontend_integration.py::test_frontend_multipart_validation_does_not_persist` *(e `test_ai_findings_use_controles_ia_values`)* | **PASSED** (`0.47s`) | `AI07` gerou `Dado_Inconsistente` (`insufficient_information`) em `R06` sem interromper `Fonte_Nao_Aprovada` (`DA09`) em `R05`; endpoint `/api/datasets/validate` retornou `200` com CORS ativo e `0` registros persistidos no banco. Log: `evidencias/T7_adversarial_ai07_e_multipart.txt`. |
| **T8** | `tests/test_frontend_integration.py::test_frontend_cors_exposes_total_count` *(e `test_public_cases_comparison_is_honest`)* | **PASSED** (`0.55s`) | `AI14/DA03` (`TC14`) gerou `Risco_Integrado` (`critical`) e achados correlatos em `R05`/`R06`; `/api/findings` retornou cabeçalho `X-Total-Count` exposto via CORS. Log: `evidencias/T8_integrado_ai14_da03_e_cors.txt`. |
