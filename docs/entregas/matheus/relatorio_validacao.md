# Relatório de Validação — PD Bank Access & Governance Analyzer (v0.4.0)

* **Responsáveis:** Matheus do Nascimento Gomes Vaz e Mateus Valerino Barros de Santana
* **Base Avaliada:** Motor v0.4.0 + Dataset Oficial v2.0 (`2026-11-05`)
* **Decisões de Referência:** `docs/entregas/abraao/decisoes_casos_publicos.md` (`D1`–`D3` e premissas `A1`–`A4` aprovadas em `2026-11-25`)

---

## 1. Resumo Executivo da Validação

A bateria completa de testes e a execução sobre o dataset oficial confirmam que o motor v0.4.0 opera de forma determinística, rastreável e defensiva:
* **Suíte automatizada:** 132 testes aprovados (`PASSED`) e 6 testes de integração PostgreSQL ignorados (`SKIPPED`) no ambiente padrão SQLite.
* **Cobertura funcional:** Todas as 9 regras (`R01`–`R09`) e a validação de exceções (`EXCEPTIONS`) foram avaliadas sem falhas de importação ou exceções não tratadas, totalizando **431 achados** (`44 critical`, `119 high`, `142 medium`, `126 low`).
* **Casos públicos (`casos_teste_publicos` — 15 cenários):** Após as decisões formais `D1`–`D3` (`docs/entregas/abraao/decisoes_casos_publicos.md`), **14 casos conferem integralmente** (`13 match` diretos e `1 computed` conferente em `TC09`), **1 caso é classificado como não aplicável** (`TC15` / `unmatched` por ausência de violação no dado oficial) e **0 casos permanecem divergentes**.

---

## 2. Tabela Comparativa dos 15 Casos Públicos (`casos_teste_publicos`)

| Caso | Domínio | Sujeito / Recurso | Esperado (Categoria / Prioridade / Decisão) | Obtido pelo Motor (Achado / Severidade / Decisão) | Classificação | Veredito Oficial |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC01** | Acesso | `U003` / `RES03` | `Excesso_de_Privilegio` / `Critico` / `Revisao` | `Excesso_de_Privilegio` (`R01`) / `critical` / `Revisao` *(coberto por `EX001` válida)* | **VP** | **Confere (`match`)** — Conforme **D1**, exceção válida não rebaixa achado de severidade crítica para *Atenção*; o status permanece `valid_exception` e a decisão exige *Revisao*. |
| **TC02** | Acesso | `U037` / `RES04` | `Conta_Desligada` / `Critico` / `Revisao` | `Conta_Desligada` (`R07`) + `Excesso_de_Privilegio` (`R01`) / `critical` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC03** | Acesso | `U099` / `RES02` | `Conflito_SoD` / `Critico` / `Revisao` | `Conflito_SoD` (`R02`) + `Excesso_de_Privilegio` (`R01`) / `critical` / `Revisao` | **VP** | **Confere (`match`)** *(sustentado por **A4** aprovada com ressalva de evidência)* |
| **TC04** | Acesso | `U010` / `RES01` | `Acesso_Expirado` / `Alto` / `Revisao` | `Acesso_Expirado` (`R08`) + `Excesso_de_Privilegio` (`R01`) / `high` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC05** | Acesso | `U001` / `RES01` | `Sem_Achado` / `Baixo` / `Conforme` | 0 achados no escopo / `Conforme` | **VN** | **Confere (`match`)** |
| **TC06** | Dados | `DA18` | `Proprietario_Ausente` / `Alto` / `Revisao` | `Proprietario_Ausente` (`R03`) + `Retencao_Ausente` (`R04`) / `high` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC07** | Dados | `DA20` | `Classificacao_Ausente` / `Alto` / `Revisao` | `Classificacao_Ausente` (`R03`) + `Retencao_Ausente` (`R04`) / `high` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC08** | Dados | `DA02` | `Sem_Achado` / `Baixo` / `Conforme` | 0 achados / `Conforme` | **VN** | **Confere (`match`)** |
| **TC09** | Compartilhamento | `SH005` | `Destino_Aprovado_ou_Nao` / `Variavel` / `Calcular` | 0 achados (`R04`) / `Conforme` | **VN** | **Confere (`computed`)** — Conforme **D2**, "Calcular" deriva o esperado aplicando `R04` à linha `SH005` (`destination_approved=Sim`, `minimum_data_only=Sim`, `protected=Sim` → *Conforme*). |
| **TC10** | Retenção | `DA23` | `Retencao_Ausente` / `Alto` / `Revisao` | `Retencao_Ausente` (`R04`) / `high` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC11** | IA | `AI06` | `Agencia_Excessiva` / `Critico` / `Revisao` | `Agencia_Excessiva` (`R06`) + `Acesso_Excessivo`, `Fonte_Nao_Aprovada`, `Fonte_Sem_Minimizacao` (`R05`) / `critical` / `Revisao` | **VP** | **Confere (`match`)** *(sustentado por **A3** aprovada)* |
| **TC12** | IA | `AI12` | `Sem_Achado` / `Baixo` / `Conforme` | 0 achados / `Conforme` | **VN** | **Confere (`match`)** *(sustentado por **A2** aprovada)* |
| **TC13** | IA | `AI02` | `Guardrail_Ausente` / `Alto` / `Revisao` | `Guardrail_Ausente` (`R05`) / `high` / `Revisao` | **VP** | **Confere (`match`)** *(sustentado por **A2** aprovada)* |
| **TC14** | Integrado | `AI14` / `DA03` | `Risco_Integrado` / `Critico` / `Revisao` | `Risco_Integrado` (`R05`) + achados correlatos (`R05`, `R06`) / `critical` / `Revisao` | **VP** | **Confere (`match`)** |
| **TC15** | Integrado | `AI03` / `DA12` | `Excecao_Valida` / `Medio` / `Atencao` | 0 achados / `Conforme` *(exceção `EX004` vigente sem violação associada)* | **VN / NA** | **Não aplicável (`unmatched`)** — Conforme **D3**, `AI03` possui todos os controles obrigatórios e fontes minimizadas; não se cria regra artificial para consumir `EX004`. |

---

## 3. Análise de Falsos Positivos (FP), Falsos Negativos (FN) e Tratamento Defensivo

* **Prevenção de Falsos Positivos (`VN` protegidos):**
  * **Usuários em Licença (`U052`, `U105`):** A regra `R07` filtra exclusivamente estados de desligamento/inatividade (`INACTIVE_STATES`), evitando classificar colaboradores afastados temporariamente como contas desligadas.
  * **Principals do tipo `Aplicacao` (29 registros):** Excluídos da comparação com o `rbac_baseline` humano em `R01`, evitando falsos alertas de excesso de privilégio por incompatibilidade de modelo.
  * **Exceções sem achado (`EX003` em `DA11` e `EX004` em `AI03`):** Mantidas visíveis na seção `coverage.EXCEPTIONS` sem gerar achados artificiais (`D3`).
* **Tratamento de Dados Inconsistentes (`AI07`):**
  * Na linha `AI07` (`casos_uso_ia`), os campos `action_level` e `impact_level` apresentam deslocamento de colunas na planilha original. O motor aplica o princípio defensivo de não inferir valores desconhecidos, registrando `Dado_Inconsistente` (`R06`, `insufficient_information`) e prosseguindo normalmente com a avaliação de `Fonte_Nao_Aprovada` (`DA09`) em `R05`.
* **Contratos de API e Integração Frontend:**
  * Validado que `/api/datasets/validate` aceita requisições `multipart/form-data` sem persistir registros no SQLite (`0` datasets gravados após validação).
  * Validado que `/api/findings` expõe o cabeçalho `X-Total-Count` via `Access-Control-Expose-Headers` para origens autorizadas em `CORS_ORIGINS`.

---

## 4. Evidências Anexadas

Todos os logs brutos de execução do `pytest` (utilizando `.venv`) e o snapshot completo dos 15 casos públicos estão versionados em `docs/entregas/matheus/evidencias/`:
* `T1_conta_desligada.txt` a `T8_integrado_ai14_da03_e_cors.txt`
* `snapshot_15_casos_publicos.json`
