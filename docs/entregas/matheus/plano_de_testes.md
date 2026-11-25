# Plano de Testes Formais — PD Bank Access & Governance Analyzer (v0.4.0)

* **Responsáveis:** Matheus do Nascimento Gomes Vaz e Mateus Valerino Barros de Santana
* **Versão do Sistema:** v0.4.0
* **Dataset de Referência:** `PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx` (v2.0, data de referência `2026-11-05`, 20 abas, 1.890 registros)
* **Ambiente Oficial de Execução:** Backend Python/Flask + SQLite (`caminho oficial`), Frontend React 18 / TypeScript / Vite

---

## 1. Escopo e Critérios de Classificação

Este plano formaliza os **8 casos de teste exigidos pela Semana 9** (3 positivos, 2 negativos, 1 de limite/fronteira, 1 adversarial/inconsistência e 1 integrado envolvendo acesso, dados e IA), alinhados à revisão oficial das regras `R01`–`R09` (`docs/entregas/alicesena/revisao_regras_governanca.md`), além da validação dos contratos de integração HTTP/Frontend (`multipart`, `CORS`, header `X-Total-Count` e build de produção).

Cada execução é classificada segundo a matriz padrão de validação:
* **Verdadeiro Positivo (VP):** Condição de violação ou inconsistência presente na entrada e corretamente detectada pelo motor com categoria, severidade e evidência rastreável.
* **Verdadeiro Negativo (VN):** Cenário conforme ou dentro dos limites permitidos em que o motor corretamente não dispara falso alerta.
* **Falso Positivo (FP):** Alerta gerado indevidamente para cenário conforme.
* **Falso Negativo (FN):** Violação prevista nas regras que deixou de ser detectada pelo motor.
* **Não Executado (NE):** Caso dependente de recurso ou decisão ainda não implementada.

---

## 2. Especificação dos 8 Casos de Teste

| ID | Categoria / Tipo | Cenário e Dados de Entrada | Regra Oficial (`R01`–`R09`) | Condição Avaliada | Evidência Vinculada |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | Positivo 1 — Identidade e Acesso | Usuário com status `Desligado` (`U037`) mantendo permissão ativa de escrita/acesso em `RES04` (`permissoes_atuais`) e demais contas desligadas (`U074`, `U111`, `U148`, `U150`). | `R07 — Usuário inativo/desligado` *(e `R01`)* | `status` em `INACTIVE_STATES` com concessão ativa em `permissoes_atuais` ou `atribuicoes_papeis` (excluindo usuários em `Licenca`). | `evidencias/T1_conta_desligada.txt` (`tests/test_official_dataset.py`) |
| **T2** | Positivo 2 — Governança de Dados | Ativo `DA18` sem `owner_id` preenchido e ativo `DA20` sem `classification` preenchida na aba `ativos_dados`. | `R03 — Ativo sem classificação/proprietário` | Ausência de proprietário (`Proprietario_Ausente`) ou de classificação (`Classificacao_Ausente`). | `evidencias/T2_ativos_dados_incompletos.txt` (`tests/test_official_dataset.py`) |
| **T3** | Positivo 3 — IA Segura | Caso de uso de IA `AI02` (`impact_level = Alto`) com `prompt_injection_protection = Nao` na aba `controles_ia`. | `R05 — Controles/fontes de IA` | Falta de controle obrigatório previsto na matriz `AI_REQUIRED_ALWAYS` (premissa `A2`). | `evidencias/T3_ia_guardrail_ausente.txt` (`tests/test_official_dataset.py`) |
| **T4** | Negativo 1 — Identidade e Acesso | Usuário ativo `U001` com permissão em `RES01` compatível com seu papel atribuído e modo de acesso previsto no `rbac_baseline` (`TC05`). | `R01 — Acesso fora do baseline RBAC` | Concessão em `permissoes_atuais` totalmente aderente à tupla `(role_id, resource_id, permission, expected_access_mode)`. | `evidencias/T4_acesso_conforme_baseline.txt` (`tests/test_official_dataset.py`) |
| **T5** | Negativo 2 — IA Segura e Retenção | Caso de IA `AI12` (`impact_level = Baixo`, `action_level = Recomendar`, controles básicos presentes, sem `logging`) e ativo `DA02` com política de retenção completa (`TC08`, `TC12`). | `R05 — Controles/fontes de IA` e `R04 — Compartilhamento/retenção` | Premissa `A2` (`logging` exigido apenas a partir de impacto `Medio`) e preenchimento completo de `politicas_retencao`. | `evidencias/T5_ia_baixo_impacto_e_retencao_ok.txt` (`tests/test_official_dataset.py`) |
| **T6** | Limite / Fronteira | Comparação temporal na data de corte `2026-11-05`:<br>1) Acesso temporário `U010/RES01` expirado (`valid_until < 2026-11-05`);<br>2) Exceções na fronteira de vencimento: `EX002` (`U057/RES06`, válida até `2026-11-30`) e `EX001` (`U003/RES03`, válida até `2026-12-01`). | `R08 — Acesso temporário vencido` e motor de exceções | Fronteira estrita `end < self.today` para expiração e `end >= self.today` para vigência de exceção. | `evidencias/T6_fronteira_datas_e_excecoes.txt` (`tests/test_official_dataset.py`) |
| **T7** | Adversarial / Dado Inconsistente e Contrato API | 1) Linha `AI07` em `casos_uso_ia` com colunas deslocadas na origem (`action_level` e `impact_level` fora do domínio esperado);<br>2) Requisição HTTP `multipart/form-data` para `/api/datasets/validate` com cabeçalho `Origin: http://localhost:5173`. | `R06 — Autonomia de IA`, `R05 — Controles/fontes de IA` e `pdbank/api.py` | Princípio defensivo: valor desconhecido/deslocado nunca é adivinhado (gera `insufficient_information`), sem interromper a avaliação da fonte `DA09`; endpoint de validação não persiste dados. | `evidencias/T7_adversarial_ai07_e_multipart.txt` (`tests/test_official_dataset.py` e `tests/test_frontend_integration.py`) |
| **T8** | Integrado (Acesso + Dado + IA + Frontend) | Caso `AI14` (`impact_level = Critico`, `action_level = Executar`) consumindo ativo `DA03` (`has_credentials = Sim`) com `privilege_model` acima do mínimo (`TC14`), somado à consulta paginada `/api/findings` via CORS com `X-Total-Count`. | `R05 — Controles/fontes de IA` e `R06 — Autonomia de IA` (correlacionando `R01` e `ativos_dados`) | Correlação transversal entre impacto crítico de IA, exposição de credenciais em ativo de dados e excesso de privilégio, com exposição de metadados HTTP ao frontend. | `evidencias/T8_integrado_ai14_da03_e_cors.txt` (`tests/test_official_dataset.py` e `tests/test_frontend_integration.py`) |
