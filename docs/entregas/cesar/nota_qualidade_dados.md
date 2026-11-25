# Nota de qualidade de dados — PD Bank Analyzer v0.4.0

**Responsável:** Caio César Leandro Amorim (qualidade do dataset e interpretação dos resultados)
**Destinatários:** Abraão (decisões), Sena (regras), Letícia (documentação); Matheus (testes) para conhecimento.
**Versão:** 2 (2026-11-25), consolidada após as entregas de Abraão (PR #7), Sena (PR #5) e Matheus (PRs #3 e #6).
**Status:** todas as pendências estão **encerradas**, com decisão ou limitação registrada (ver §Encerramento).
**Base:** `tests/data/PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx`, versão 2.0, `data_referencia` 2026-11-05,
SHA-256 `70e7e7598125fa5026fbc36adba65322247c3adac62d699020fc0157c2299e76`. O arquivo **não** foi alterado; o hash é
conferido de novo depois de gerar a cópia de teste.

## Como reproduzir

```powershell
python scripts/check_data_quality.py tests/data/PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx --corrected-copy docs/entregas/cesar/PD_Bank_Dataset_AI07_Corrigido_TESTE.xlsx --out docs/entregas/cesar/evidencias_qualidade_dados.json
python -m pytest -q tests/test_data_quality.py
```

O script usa o mesmo importador (`pdbank.importer`) e o mesmo motor (`pdbank.rules.analyze_full`) do sistema.
Cada número desta nota está em `evidencias_qualidade_dados.json` e travado em `tests/test_data_quality.py`.
A tabela resumida das pendências está em `pendencias_dados.csv`.

## Resumo executivo

* O dataset é **estruturalmente íntegro**: 20/20 abas, 1.890 registros e 0 cabeçalhos sem tratamento no schema.
  As relações entre entidades têm apenas 2 tipos de órfão, ambos explicados (P2).
* Há **um defeito de dado comprovado**: a linha AI07 de `casos_uso_ia` está deslocada uma coluna para a esquerda.
  O motor já trata isso corretamente como `Dado_Inconsistente`. Na cópia de teste corrigida o total continua em 431:
  sai 1 `R06:Dado_Inconsistente` e entra 1 `R05:Guardrail_Ausente`.
* **Nenhuma pendência de dados exige mudar o número oficial de achados (431)**. As propostas que mudariam contagens
  (P3, P8) são recomendações para Sena e Abraão, com o impacto já medido.
* A R09 domina o volume: 287 de 431 achados (66,6%). Desses, 124 são `Recertificacao_Vencida` de severidade baixa.
  A recomendação é manter, mas separar na apresentação (P6).
* **Após as decisões da equipe (v2):** A1–A3 aprovadas e A4 aprovada com ressalva (Abraão); TC15 passou a
  *não aplicável* (D3); Sena e Matheus confirmaram o tratamento de P3, P4, P5, P6 e P8. Nenhuma pendência ficou sem dono.

## Decisões por pendência

Legenda: **Decisão** = adotada nesta entrega. **Recomendação** = depende do dono indicado. **Limitação** = o dataset
não permite concluir e isso fica registrado.

### P1 — Nomes das 20 abas e cabeçalhos
* **Evidência:** as 20 abas de `OFFICIAL_SHEETS` estão presentes, sem abas extras. São 1.890 registros. Todo
  cabeçalho do arquivo está em `FIELD_ALIASES` ou em `INFORMATIONAL_FIELDS` de `pdbank/schema.py` (0 sem tratamento).
  Os acentos (`Privilégio_Minimo` em `controles_ia` e cenários de `casos_teste_publicos`) são UTF-8 válido e passam por
  `normalize()`.
* **Decisão:** conforme. Nenhuma alteração de schema.
* **Impacto:** nenhum.

### P2 — Relações usuário, papel, baseline, permissão, ativo, compartilhamento, IA e exceção
* **Evidência:** foram checadas 26 relações de chave estrangeira. Só 2 têm órfãos:
  * `usuarios.manager_id`: 10 usuários apontam para `M001`, que não existe em `usuarios`. É um gestor externo à base.
  * `casos_uso_ia.owner_id`: 1 órfão (`"Proposta"`), causado pelo deslocamento da AI07 (P5).
  * Também há 14 usuários com `manager_id` igual ao próprio `user_id` (U011, U021 … U141, um a cada 10 IDs). O padrão
    sugere líderes de área.
  * Os compartilhamentos SH002 e SH022 foram pedidos por usuários desligados (U037 e U111).
  * Todos os casos de IA têm controles e todos os ativos têm política de retenção.
* **Decisão:** limitação. Os casos ficam registrados, mas não viram achado: o enunciado não tem regra de cadeia de
  gestão nem de solicitante desligado.
* **Recomendação (Sena):** se quiserem, criar uma verificação informativa para "gestor inexistente/autogestão" e para
  "compartilhamento pedido por desligado" (no máximo 2 itens).
* **Impacto:** nenhum nos 431.

### P3 — 29 permissões de principals `Aplicacao`
* **Evidência:** 29 permissões em 18 aplicações. Por nível: 16 Admin, 9 Read, 3 Write e 1 Execute. Por criticidade do
  recurso: 11 Crítica, 17 Alta e 1 Média. Todas são `Permanente`, com a mesma justificativa genérica ("Acesso tecnico
  da aplicacao"). Todas as aplicações têm dono ativo em `aplicacoes.owner_id`.
  7 são **Admin em recurso Crítico**: P0510 APP02→RES02, P0512 APP03→RES03, P0515 APP05→RES06, P0516 APP06→RES06,
  P0524 APP12→RES12, P0526 APP15→RES15 e P0535 APP20→RES06.
* **Decisão:** continuam **fora da R01**. O `rbac_baseline` é definido por papel de usuário, e comparar uma conta
  técnica com ele produziria falsos positivos sem base.
* **Recomendação (Sena / Abraão):** tratar como conta técnica, com o dono da aplicação como responsável. Proposta de
  verificação: Admin permanente de aplicação em recurso Crítico com justificativa genérica vira revisão de severidade
  alta, endereçada ao dono da aplicação.
* **Impacto se adotado:** +7 achados (ou itens de revisão). Hoje: 0.
* **Fechamento (v2):** a revisão da Sena confirmou "manter a regra humana como está até que exista baseline técnico
  explícito" e propôs um inventário de contas técnicas priorizando os 7 Admin. Abraão não abriu decisão contrária.
  **Encerrada:** fora da R01 na v0.4.0. O inventário de contas técnicas foi para o backlog da Semana 2. Isso é dedução
  da equipe de dados a partir das duas entregas, não uma decisão formal escrita pelo Abraão.

### P4 — Usuários em `Licenca` e a R07
* **Evidência:**
  * U052 (Aprovador_Pagamento) tem 4 permissões permanentes, incluindo **Approve em RES02**. O último uso foi em
    2026-10-31, 5 dias antes da data de referência.
  * U105 (Auditor) tem 6 permissões Read. O último uso foi em 2026-10-20.
  * O dataset **não tem data de início da licença**.
* **Decisão:** **não entram na R07**. Licença não é desligamento, e o acesso volta no retorno. A R07 continua restrita a
  `Desligado` (19 achados).
* **Limitação:** sem a data de início, não dá para saber se o uso de 2026-10-31 aconteceu durante a licença.
* **Recomendação (Abraão):** revisar manualmente o caso U052/RES02 Approve, que é poder de aprovação de pagamento. Se o
  dataset final trouxer a data da licença, avaliar um achado de *atenção* para uso durante a licença.
* **Impacto:** nenhum nos 431.
* **Fechamento (v2):** confirmado por Sena ("não usar licença como sinônimo de desligamento") e por Matheus (teste T1:
  `test_r07_only_dismissed_users_not_those_on_leave`). **Encerrada.** A revisão de U052/RES02 fica como ação operacional
  do dono do recurso, fora do motor.

### P5 — Linha AI07 deslocada
* **Evidência:** linha 8 de `casos_uso_ia`.

  | coluna | valor no arquivo | valor reconstruído |
  |---|---|---|
  | business_area | Resumir avaliacoes de colaboradores | *(perdido — vazio)* |
  | purpose | Recomendar | Resumir avaliacoes de colaboradores |
  | action_level | Alto | Recomendar |
  | impact_level | U016 | Alto |
  | owner_id | Proposta | U016 |
  | status | *(vazio)* | Proposta |

  O deslocamento é inequívoco: cada valor cai exatamente no domínio da coluna seguinte. O valor original de
  `business_area` se perdeu. O nome `Analise_RH` sugere RH, mas o dono U016 é de Atendimento, então a área **não foi
  inferida**.
* **Decisão:** o arquivo oficial **fica como está**, e o `R06:Dado_Inconsistente` do motor é o tratamento correto. Foi
  gerada uma **cópia de teste** com a linha reconstruída: `PD_Bank_Dataset_AI07_Corrigido_TESTE.xlsx`, criada por
  `write_corrected_copy`, que se recusa a sobrescrever a origem.
* **Impacto medido na cópia:** total 431 → 431. Sai `R06:Dado_Inconsistente` (−1). Entra `R05:Guardrail_Ausente` (+1):
  com impacto Alto, a premissa A2 exige revisão humana obrigatória, e a AI07 tem `Amostral`. A AI07 já tinha
  `Fonte_Nao_Aprovada` (DA09), que não muda.
* **Recomendação (dono do dataset / Abraão):** corrigir na fonte e informar `business_area`.
* **Fechamento (v2):** com a **A2 aprovada** pelo Abraão, o `Guardrail_Ausente` da cópia corrigida deixa de depender de
  premissa e passa a ser o resultado esperado. Matheus reproduziu o delta (T7 e relatório de validação), e Sena manteve
  `insufficient_information` para a linha original. **Encerrada.** A correção na fonte fica com o dono do dataset. Como
  o dataset final "poderá conter dados diferentes", o motor continua sem adivinhar.

### P6 — 124 `Recertificacao_Vencida` da R09
* **Evidência:** `revisoes_acesso` tem 257 Manter, 155 Pendente e 8 Remover. Dos Manter, 124 têm a próxima revisão
  vencida. Atraso: 12 até 30 dias, 32 entre 31 e 90, 39 entre 91 e 180, e 41 acima de 180 dias. Nenhuma revisão
  "Pendente" ainda não vencida (0), então a dúvida sobre exibi-las não se aplica a este dataset.
* **Decisão:** **manter no escopo com severidade low**. São tecnicamente corretas, e 80 delas (65%) estão vencidas há
  mais de 90 dias, o que é risco real de recertificação.
* **Recomendação (Letícia / frontend):** apresentar separado de `Revisao_Vencida` (155) e `Remocao_Nao_Executada` (8),
  porque a R09 sozinha soma 66,6% do total. Opcional para Abraão: elevar para medium as que passam de 180 dias (41).
* **Impacto:** nenhum na contagem. A opção de elevar muda só a severidade de 41 achados.
* **Fechamento (v2):** Sena manteve a decisão e recomendou segmentar por `finding_type`. Elevar acima de 180 dias só
  com política de SLA aprovada. **Encerrada:** low, separado por tipo, sem elevação na v0.4.0.

### P7 — EX003, EX004 e TC15
* **Evidência:**
  * EX003 (DA11, "Retencao estendida por auditoria", válida até 2027-06-30): DA11 tem a política RP011 (1.095 dias,
    `Hipotese_Educacional`) e não gera nenhum achado. A exceção **não cobre achado algum**.
  * EX004 (AI03, "Piloto com revisao humana integral", válida até 2026-12-31): AI03 é Recomendar/Alto, tem os 5
    controles com revisão humana Obrigatória e 4 fontes aprovadas e minimizadas (DA02, DA12, DA21, DA26). Também
    **não há achado** a cobrir.
  * TC15 (AI03/DA12) espera `Excecao_Valida` / Médio / Atenção.
  * Para comparação, EX001 e EX002 cobrem 1 achado de R01 cada.
* **Decisão:** limitação. O motor não inventa achado para "consumir" uma exceção. EX003 e EX004 continuam como
  "exceção sem objeto" em `coverage.EXCEPTIONS`, e o TC15 continua "não casa", com esta justificativa.
* **Fechamento (v2): decidido pelo Abraão (D3).** TC15 = **não aplicável**, sem regra nova. EX003/EX004 continuam em
  `coverage.EXCEPTIONS`. No código o veredito segue `unmatched`, lido como não aplicável. **Encerrada.**
* **Recomendação original (Abraão):** registrar o TC15 como divergência explicada. O caso de teste supõe um risco que os dados
  de AI03 não mostram, porque os controles estão completos. Se a banca exigir, a alternativa é uma política
  explícita ("caso de IA de impacto Alto em Desenvolvimento só é aceito com exceção vigente"). Isso seria regra nova
  (Sena), não correção de dado.
* **Impacto:** nenhum nos 431.

### P8 — `campos_dados` em R03/R04
* **Evidência:** 135 campos em 30 ativos (todos os ativos têm campos). 46 são sensíveis, dos quais 11 são
  identificadores diretos. Categorias: 89 Operacional, 20 Financeiro, 19 Pessoal e 7 Credencial. Cruzamento com
  `ativos_dados`:
  * Campo Pessoal em ativo com `contains_personal_data=Nao`: **0**.
  * Identificador direto em ativo abaixo de Confidencial: **0**.
  * Campo Financeiro em ativo com `contains_financial_data=Nao`: **4** (DA01, DA09, DA10, DA16). Em DA01, DA10 e DA16
    a causa é `customer_id` categorizado como Financeiro, um identificador e não dado financeiro. **DA09
    (Dados_Colaboradores) tem `salario`**, que é dado financeiro de fato.
  * 14 compartilhamentos com `minimum_data_only=Sim` saem de ativos que têm identificador direto. O evento não diz
    quais campos foram enviados, então não dá para verificar.
* **Decisão:** **R04 só preserva** `campos_dados`, porque não há granularidade de campo por compartilhamento. A **R03
  não muda nesta entrega**.
* **Recomendação (Sena):** opcionalmente, usar `campos_dados` na R03 como checagem de consistência de flags, o que
  geraria 1 achado real (DA09: `salario` × `contains_financial_data=Nao`). Os outros 3 dependem de decidir se
  `customer_id` é Financeiro; a sugestão é recategorizar como identificador e não gerar achado.
* **Impacto se adotado:** +1 achado na R03 (ou +4, se `customer_id` continuar como Financeiro).
* **Fechamento (v2):** Sena decidiu que a "R03 não incorpora a aba nesta versão", e o relatório de Matheus registra a
  aba como importada e preservada. **Encerrada:** preservada. O caso DA09 (`salario` × `contains_financial_data=Nao`) e
  a recategorização de `customer_id` foram para o backlog como melhoria de regra.

## Decisões de política que afetam esta nota (Abraão, 2026-11-25)
* **D1 — TC01 × EX001:** continua *Revisão*; exceção válida não rebaixa achado crítico. Não muda nenhuma contagem
  desta nota (o achado segue `valid_exception`).
* **D2 — TC09:** "Calcular" = aplicar a R04 à linha; SH005 confere.
* **D3 — TC15:** não aplicável (ver P7).
* **A1–A3 aprovadas; A4 aprovada com ressalva.** A A2 consolida o impacto medido na P5.
* Os casos públicos ficam em 14 conferem, 1 não aplicável e 0 divergentes.

> Observação para a Sena: `revisao_regras_governanca.md` ainda trata A1–A4 e TC01 como pendentes, porque foi escrito
> antes do PR #7. Vale atualizar para "aprovadas".

## Encerramento — checklist do kit

| Critério do kit | Situação |
|---|---|
| Cada pendência do relatório tem decisão ou limitação explícita | ✅ P1–P8 encerradas (tabela `pendencias_dados.csv`) |
| Nenhuma decisão baseada em suposição não registrada | ✅ Toda evidência é reproduzida pelo script e travada em teste. Os fechamentos deduzidos (P3, P8) estão marcados como tal |
| Original oficial intacto | ✅ SHA-256 `70e7e759…c2299e76` conferido após gerar a cópia |
| Conclusões disponíveis para Abraão, Sena, Matheus e Letícia | ✅ Usadas no PR #5 (Sena), nos PRs #3/#6 (Matheus), no README (seção de qualidade) e no relatório do Boniek |
| Backlog gerado para a Semana 2 | Inventário de contas técnicas (P3); correção da AI07 na fonte (P5); SLA de R09 (P6); checagem de flags via `campos_dados` em R03 (P8) |

## Observações de ambiente (para Matheus e Boniek)
* No Windows, `pytest -q` na `main` tem 7 falhas em `tests/test_sql_repository.py` por
  `PermissionError [WinError 32]`: o arquivo SQLite temporário continua aberto na limpeza. Isso existe antes desta
  entrega e não tem relação com ela.
* Caminhos com mais de 260 caracteres (limite MAX_PATH do Windows) fazem os scripts falharem quando usam o caminho
  padrão. Nesse caso, passe o XLSX por caminho relativo.
