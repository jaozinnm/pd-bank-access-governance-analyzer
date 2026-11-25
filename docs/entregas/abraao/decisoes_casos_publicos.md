# Decisões dos casos públicos e premissas — v0.4.0

**Responsável pela decisão:** Abraão Filipi dos Santos · **Data:** 2026-11-25
**Base:** `docs/v0.4.0-relatorio.md`, `docs/resultado_dataset_oficial.json`, aba `casos_teste_publicos` (dataset oficial v2.0, referência 2026-11-05).

## 1. Decisões

### D1 — TC01 (U003/RES03 × EX001)
| Campo | Conteúdo |
|---|---|
| Decisão | **Manter *Revisão*.** Exceção válida não rebaixa achado crítico. |
| Regra formal | Achado aberto → *Revisão*. Achado coberto por exceção válida: severidade crítica → *Revisão*; severidade alta, média ou baixa → *Atenção*. O status continua `valid_exception` (o achado não some). |
| Justificativa | (1) É Admin permanente, por acesso direto, em recurso fora do baseline — o pior caso de R01. (2) A própria EX001 diz "Acesso legado **em revisão**": a exceção documenta que a revisão está em andamento, não que o risco foi aceito. (3) EX001 vence em 2026-12-01; tratar como *Atenção* tiraria o caso da fila justamente antes do vencimento. (4) Mantém coerência com TC15, onde *Atenção* aparece para prioridade Média. |
| Impacto | TC01 passa a conferir. No dataset oficial só U003/RES03 muda; U057/RES06 (EX002, severidade alta) continua *Atenção*. |
| Ação | **Feito:** `pdbank/public_cases.py` (cálculo de `decision` + mensagem de divergência) e `tests/test_official_dataset.py::test_public_cases_comparison_is_honest` ajustados; `docs/resultado_dataset_oficial.json` regenerado (13 match, 0 divergent). |
| Responsável pela ação | Abraão (código e teste) · Sena (catálogo) · Letícia (Playbook) |

### D2 — TC09 (SH005) — significado de "resultado calculado"
| Campo | Conteúdo |
|---|---|
| Decisão | **"Calcular" significa: o esperado é derivado aplicando a R04 à própria linha de `eventos_compartilhamento`.** |
| Regra formal | `destination_approved` = Sim **e** `minimum_data_only` = Sim **e** `protected` = Sim → *Sem_Achado / Baixo / Conforme*. Qualquer um = Não → achado R04 correspondente (`Destino_Nao_Aprovado` ou `Protecao_Insuficiente`) com decisão *Revisão*. Valor ilegível → `insufficient_information`. |
| Justificativa | O caso público diz "Destino deve ser comparado com aprovação" e prioridade "Variável": não há resposta fixa, há um critério. SH005: Terceiro, Email_Corporativo, aprovado = Sim, mínimo = Sim, protegido = Sim. |
| Impacto | Esperado do TC09 = *Conforme*. O motor deu *Conforme* (nenhum achado R04) → **confere**. O achado R03 `Classificacao_Divergente` de DA06 está fora do escopo de compartilhamento. |
| Ação | Nenhuma mudança de regra. Registrar no catálogo/Playbook que `computed` conta como conferente quando o resultado do motor bate com a regra acima. |
| Responsável pela ação | Sena (catálogo) · Letícia (Playbook) · Matheus (relatório de validação) |

### D3 — TC15 (AI03/DA12 × EX004)
| Campo | Conteúdo |
|---|---|
| Decisão | **Não criar regra. Registrar o caso como não aplicável (limitação do caso público).** |
| Justificativa | AI03 é `Recomendar`, impacto Alto, em Desenvolvimento, com validação de entrada/saída, proteção contra prompt injection, logging, privilégio mínimo e revisão humana **Obrigatória**; fontes aprovadas e minimizadas. Não existe violação para a exceção cobrir. Criar uma regra só para gerar o achado esperado seria fabricar risco (contraria a decisão de projeto nº 1). |
| Impacto | TC15 sai de "não casa" para "não aplicável". EX004 e EX003 continuam listadas em `coverage.EXCEPTIONS` como exceções vigentes sem achado. |
| Ação | No código o veredito continua `unmatched`; ele é lido como **não aplicável** por esta decisão. Se a política quiser exigir exceção formal para piloto de IA de impacto Alto, abrir requisito novo para a Semana 2 (não entra na v0.4.0). |
| Responsável pela ação | Sena (catálogo) · Matheus (relatório de validação) |

## 2. Premissas

| Premissa | Resultado | Observação |
|---|---|---|
| **A1** Severidade fora do baseline: Admin = crítico; escrita/aprovação = alto (crítico em recurso Crítica); leitura = médio (recurso Crítica/Alta ou Restrito) ou baixo | **Aprovada** | Sustenta TC01 (crítico). |
| **A2** Controles de IA: entrada/saída e prompt injection sempre; logging a partir de impacto Médio; revisão humana obrigatória para `Executar` ou impacto ≥ Alto; severidade = impacto do caso | **Aprovada** | Sustenta TC12 (AI12, Baixo, sem logging → conforme) e TC13. |
| **A3** Autonomia: `Executar` é excessivo em impacto Crítico; em Alto só com revisão humana obrigatória | **Aprovada** | Sustenta TC11 (AI06). |
| **A4** SoD por permissão: quem tem permissão de escrita do baseline de um papel exerce esse papel | **Aprovada com ressalva** | A evidência deve sempre indicar "papel inferido por permissão" (o motor já escreve "Base: permissões efetivas"). Não apresentar como fato de RH. Sustenta TC03 (U099), U043 e U141. Rejeitar A4 quebraria TC03. |

## 3. Vereditos dos 15 casos (após as decisões)

| Caso | Sujeito | Esperado (categoria / prioridade / decisão) | Motor | Veredito final |
|---|---|---|---|---|
| TC01 | U003/RES03 | Excesso_de_Privilegio / Crítico / Revisão | crítico, coberto por EX001 | **Confere** (após ajuste da D1) |
| TC02 | U037/RES04 | Conta_Desligada / Crítico / Revisão | idem | Confere |
| TC03 | U099/RES02 | Conflito_SoD / Crítico / Revisão | idem (A4) | Confere |
| TC04 | U010/RES01 | Acesso_Expirado / Alto / Revisão | idem | Confere |
| TC05 | U001/RES01 | Sem_Achado / Baixo / Conforme | idem (R09 extra, fora do escopo) | Confere |
| TC06 | DA18 | Proprietario_Ausente / Alto / Revisão | idem | Confere |
| TC07 | DA20 | Classificacao_Ausente / Alto / Revisão | idem | Confere |
| TC08 | DA02 | Sem_Achado / Baixo / Conforme | idem | Confere |
| TC09 | SH005 | Calcular → Sem_Achado / Baixo / Conforme (D2) | Conforme | **Confere** (calculado) |
| TC10 | DA23 | Retencao_Ausente / Alto / Revisão | idem | Confere |
| TC11 | AI06 | Agencia_Excessiva / Crítico / Revisão | idem (A3) | Confere |
| TC12 | AI12 | Sem_Achado / Baixo / Conforme | idem (A2) | Confere |
| TC13 | AI02 | Guardrail_Ausente / Alto / Revisão | idem (A2) | Confere |
| TC14 | AI14/DA03 | Risco_Integrado / Crítico / Revisão | idem | Confere |
| TC15 | AI03/DA12 | Excecao_Valida / Médio / Atenção | sem achado | **Não aplicável** (D3) |

**Total:** 14 conferem, 1 não aplicável, 0 divergentes.
**Evidência:** `python scripts/analyze_official_dataset.py --out docs/resultado_dataset_oficial.json` → `match 13, divergent 0, unmatched 1 (TC15), computed 1 (TC09)`; `pytest -q` → 132 passam, 6 pulados (PostgreSQL).

## 4. Pendências que continuam abertas (fora desta entrega)
AI07 com colunas deslocadas (corrigir na fonte), principals *Aplicacao*, usuários em *Licenca*, `manager_id` = próprio usuário, ruído de `Recertificacao_Vencida` — itens 4–8 do relatório v0.4.0.
