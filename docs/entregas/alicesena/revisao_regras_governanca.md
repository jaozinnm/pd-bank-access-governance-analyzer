# Revisão das regras de governança R01–R09

## Resumo executivo

Esta revisão compara o comportamento implementado no motor v0.4.0 com o briefing da Semana 1, os resultados do dataset oficial v2.0 e as entregas técnicas de validação e qualidade de dados. O motor produziu 431 achados na referência de 05/11/2026. As nove regras foram avaliadas; os achados incluem evidência com aba/linha e cobertura por regra.

**Conclusão:** a estrutura de rastreabilidade e os guardrails para dados desconhecidos devem ser preservados. As regras não devem ser tratadas como política aprovada apenas por estarem implementadas. A1–A4 continuam premissas sujeitas a decisão de política. Decisões mais recentes de qualidade já registradas pelas entregas de César e Matheus são preservadas neste relatório, em especial a exclusão de usuários em licença da R07 e a manutenção das recertificações vencidas da R09 como baixa severidade.

Esta entrega documenta revisão; não altera a lógica de detecção de R01–R09.

## Base e método

1. Ler as regras e critérios implementados em `pdbank/rules.py` e o contrato em `docs/API.md`.
2. Comparar resultados por regra e limitações com `docs/v0.4.0-relatorio.md` e `docs/resultado_dataset_oficial.json`.
3. Incorporar decisões/limitações já registradas em `docs/entregas/cesar/nota_qualidade_dados.md` e `docs/entregas/matheus/relatorio_validacao.md`.
4. Separar: (a) comportamento de código, (b) decisão de qualidade de dados já adotada, (c) premissa de política aguardando o responsável.

O dataset é educacional e fictício; os resultados são uma referência de execução, não uma declaração de conformidade real. Contagens abaixo são o snapshot oficial, não uma expectativa invariável para todo dataset.

## Resultados observados

| Regra | Achados | Registros / entradas avaliadas | Composição resumida no snapshot |
|---|---:|---:|---|
| R01 — Acesso fora do baseline | 16 | 507 | 11 excessos de privilégio e 5 divergências de modo; 29 permissões de principals Aplicação ficaram fora da comparação de baseline humano. |
| R02 — Conflito SoD | 5 | 8 regras | Conflitos em U043, U099, U021, U035 e U141 conforme as regras SoD do dataset e a premissa A4. |
| R03 — Ativo sem classificação/proprietário | 7 | 30 | DA18 sem proprietário, DA20 sem classificação e 5 divergências de classificação. |
| R04 — Compartilhamento/retenção | 65 | 130 | 46 destinos não aprovados, 16 proteções insuficientes e 3 políticas de retenção ausentes. |
| R05 — Controles/fontes de IA | 25 | 64 | Guardrails ausentes, fontes não aprovadas, falta de minimização, acesso excessivo e risco integrado. |
| R06 — Autonomia de IA | 3 | 15 | 2 casos de agência excessiva e AI07 com dado inconsistente. |
| R07 — Usuário inativo/desligado | 19 | 670 | Contas desligadas com permissão ou papel remanescente. Usuários em licença não são tratados como desligados. |
| R08 — Acesso temporário vencido | 4 | 536 | Quatro concessões temporárias vencidas no snapshot. |
| R09 — Revisão de acesso | 287 | 420 | 155 revisões pendentes vencidas, 8 remoções não executadas e 124 recertificações vencidas classificadas como baixa severidade. |

Total: 431 achados; 44 críticos, 119 altos, 142 médios e 126 baixos. O resultado mantém 428 `non_compliant`, 2 `valid_exception` e 1 `insufficient_information` conforme o relatório v0.4.0.

## Revisão por regra

### R01 — Acesso fora do baseline RBAC

**Implementação:** compara principal, papel ativo, recurso, permissão e modo ao baseline. A data de referência é explícita, herdada de `dataset_info.data_referencia` ou, na ausência, a data atual. Sem baseline, concessões ou atribuições suficientes, a cobertura explica por que a regra foi pulada.

**Avaliação:** a comparação por papel e recurso é apropriada para as concessões humanas representadas no baseline. O dataset tem 29 permissões de `Aplicacao` em 18 aplicações, inclusive 7 concessões Admin em recursos críticos; a entrega de César documenta que essas contas técnicas continuam fora da R01 para evitar comparação indevida com baseline de pessoas.

**Recomendação:** manter a regra humana como está até que exista baseline técnico explícito. Criar inventário complementar para contas técnicas com dono da aplicação, finalidade, recurso, permissões, justificativa específica, modo e revisão. Priorizar as 7 concessões Admin permanentes em recurso crítico e substituir a justificativa genérica por justificativa operacional verificável. Tratar severidade como premissa A1 até aprovação.

### R02 — Conflito de segregação de funções

**Implementação:** usa pares incompatíveis de `regras_sod` aplicados a papéis ativos e a permissões efetivas. A inferência de que permissão de escrita do baseline representa exercício funcional do papel é a premissa A4.

**Avaliação:** cruzar atribuições e permissões efetivas ajuda a detectar conflito indireto, mas a inferência pode produzir conclusões erradas quando uma permissão não equivale ao conjunto de responsabilidades de um papel. Conflitos de solicitação/aprovação/execução financeira devem ser explícitos na matriz SoD e ligados aos papéis R10/R11 do catálogo.

**Recomendação:** manter a evidência diferenciando papel atribuído de papel inferido por permissão. Ratificar A4 e definir a condição para conflitos de papel, recurso, ação e vigência. Não apresentar a inferência como fato de RH. Adotar SOD-PAY-01 do catálogo como requisito proposto para Semana 2.

### R03 — Ativo sem classificação ou proprietário

**Implementação:** verifica dados do ativo e divergências de classificação com base na taxonomia reconhecida. A ausência de sinal suficiente não deve ser convertida em conformidade.

**Avaliação:** a cobertura atual identifica lacunas de classificação e ownership sem depender de atribuição humana presumida. A aba `campos_dados` contém dados úteis, mas a entrega de César conclui que R03 não deve mudar nesta entrega; uma checagem de consistência por campo é apenas recomendação futura e pode gerar falso positivo se `customer_id` continuar classificado como dado financeiro.

**Recomendação:** manter escopo atual nesta versão. Antes de usar `campos_dados`, aprovar taxonomia de campos e flags do ativo, incluindo se identificadores diretos são categoria própria. Se avançar, limitar primeira checagem a inconsistências semânticas comprovadas, como salário em ativo marcado sem dado financeiro, e mostrar origem da evidência.

### R04 — Compartilhamento e retenção

**Implementação:** avalia destino/aprovação, minimização/proteção e política de retenção por fontes disponíveis.

**Avaliação:** separar os três tipos de achado melhora a remediação. A decisão de qualidade de dados já registrada é que R04 preserve `campos_dados`, pois o registro de compartilhamento não identifica quais campos foram efetivamente enviados; sem essa relação, a regra não pode afirmar minimização por campo.

**Recomendação:** manter detecção atual, definir o que constitui destino aprovado para cada classe de dado e quais salvaguardas são obrigatórias. Não inferir campos compartilhados a partir da lista de campos do ativo. Registrar aprovação, finalidade, retenção, minimização e evidência no evento de compartilhamento futuro.

### R05 — Controles e fontes de IA

**Implementação:** avalia controles do caso, aprovação e minimização de fontes, controles exigidos e sinal integrado. A matriz de controle por impacto inclui entrada/saída e proteção contra prompt injection em todos os casos, logging a partir de impacto médio e revisão humana obrigatória conforme A2.

**Avaliação:** a trilha de evidência deve distinguir controle ausente, fonte não aprovada e falta de minimização. A matriz A2 não é fornecida pelo dataset e precisa de decisão. EX004 (AI03) e EX003 (DA11) permanecem exceções válidas sem achado correspondente; o motor não deve fabricar um risco só para associar a exceção. TC15 é uma divergência explicada pela entrega de Matheus, pois AI03 tem controles completos no snapshot.

**Recomendação:** aprovar formalmente os controles e limiares de A2 e documentar versão/autoridade da política. Manter exceções órfãs visíveis na cobertura, com processo de limpeza/renovação, sem criar achado artificial. Para risco integrado, preservar a ligação aos sinais que o compõem para não contar correlação como evidência independente.

### R06 — Autonomia de IA acima do limite

**Implementação:** considera `Executar` excessivo em impacto crítico e em impacto alto sem revisão humana obrigatória; também verifica divergência entre a autonomia declarada e as fontes com escrita. Estes limites correspondem a A3 e parte de A2.

**Avaliação:** limite de autonomia e revisão humana dependem da taxonomia de impacto e do significado verificável de revisão “Obrigatória”. AI07 possui valores deslocados; a decisão das entregas técnicas é preservar o arquivo oficial e classificar como `Dado_Inconsistente`, sem adivinhar os campos.

**Recomendação:** aprovar A3, definir evidência da revisão humana (revisor, momento, decisão e capacidade de bloquear) e manter a proteção contra dado inconsistente. Corrigir AI07 somente na fonte oficial/dataset corrigido controlado, sem substituir silenciosamente a cópia de referência.

### R07 — Acesso remanescente de usuário inativo ou desligado

**Implementação:** sinaliza concessões e atribuições de papéis de usuários com estado de desligamento/inatividade reconhecido. Licença/afastamento tem tratamento separado.

**Avaliação:** decisão documentada por César: U052 e U105 em `Licenca` não entram na R07, pois licença não é desligamento e o dataset não fornece data de início que permita avaliar uso durante a licença. O caso U052/RES02 `Approve` deve ser revisado manualmente por sua criticidade funcional, sem reclassificá-lo como desligamento automaticamente.

**Recomendação:** manter a R07 restrita a desligamento/inatividade conforme vocabulário aprovado. Para licença, definir política própria com início/fim, suspensão conforme risco, exceção e revisão; não mudar a regra com dados insuficientes. Definir também o ciclo de vida de contas técnicas separadamente.

### R08 — Acesso temporário vencido

**Implementação:** detecta concessões `JIT`/temporárias com data de expiração vencida e emite informação insuficiente quando o término não é legível. A associação de papéis temporários também é verificada.

**Avaliação:** a regra é coerente com a recomendação JIT do catálogo. Uma data vencida no cadastro, porém, não comprova por si só que o acesso foi tecnicamente removido; a evidência precisa permitir confirmar a ação efetiva.

**Recomendação:** manter o achado de prazo vencido e, em fase futura, integrar evidência de desprovisionamento. Exigir justificativa, aprovador, escopo, início/fim e responsável por cada elevação. A severidade e o prazo máximo devem considerar criticidade do recurso e ser aprovados na política de acesso.

### R09 — Revisão de acesso pendente, vencida ou reprovada

**Implementação:** detecta remoção decidida e não executada; revisão pendente já vencida; e decisão “Manter” cuja próxima recertificação venceu.

**Avaliação:** é a regra de maior volume no snapshot: 287/431 achados (66,6%). César registra decisão de manter as 124 `Recertificacao_Vencida` no escopo com severidade `low`; 80 estavam vencidas há mais de 90 dias e 41 há mais de 180. No dataset oficial não houve pendência ainda dentro do prazo. A entrega de César recomenda exibir recertificações separadas das revisões pendentes e remoções não executadas, para preservar interpretação operacional.

**Recomendação:** manter a decisão atual e segmentar por `finding_type` na leitura dos relatórios. Definir SLA de revisão por criticidade e considerar elevar a severidade após 180 dias somente após aprovação de política e análise de impacto nas contagens. Pendência dentro do prazo pode ser lembrete de workflow, não achado de risco, a menos que haja requisito explícito.

## Premissas de política que continuam pendentes

O relatório de qualidade de dados deixa explicitamente TC01 × EX001 e A1–A4 para decisão do responsável por política (Abraão). Esta entrega não os apresenta como aprovados.

| Premissa | Regra(s) afetadas | Questão a decidir | Recomendação de validação |
|---|---|---|---|
| A1 — Severidade RBAC | R01 | Como Admin, escrita/aprovação e leitura variam com criticidade/classificação? | Aprovar matriz publicada e testar recursos críticos, altos e comuns. |
| A2 — Controles de IA | R05/R06 | Quais guardrails/logging/revisão humana são obrigatórios por impacto? | Aprovar controles por impacto e aplicar aos casos de uso, documentando exceções. |
| A3 — Limite de autonomia | R06 | Quando `Executar` é proibido ou condicionado a supervisão? | Definir impacto máximo, revisão humana efetiva e possibilidade de bloqueio. |
| A4 — Inferência SoD | R02 | Permissão de escrita do baseline basta para inferir exercício de papel? | Validar cada tipo de permissão contra responsabilidades e declarar inferência na evidência. |
| TC01 × EX001 | R01 / exceções | Exceção válida transforma caso crítico em “Atenção” ou severidade crítica continua exigindo “Revisão”? | Decidir hierarquia entre exceção, severidade e recomendação de ação; alinhar TC01. |

## Pendências de qualidade de dados e escopo

- **Principals Aplicação:** 29 permissões não comparadas por R01. Criar baseline/ciclo de revisão de contas técnicas antes de incluir na regra humana.
- **Exceções sem achado:** EX003 (DA11) e EX004 (AI03) seguem registradas na cobertura; não criar achados para consumi-las.
- **TC15:** resultado não casado é explicado por ausência de violação detectável em AI03/DA12 no snapshot. Se a política deseja exigir exceção para piloto de IA, isso será regra nova e precisa de requisito explícito.
- **AI07:** manter `insufficient_information` para a linha deslocada; corrigir em fonte controlada e preservar a versão original como referência.
- **`campos_dados`:** manter apenas preservação em R04 por falta de campos efetivamente compartilhados; R03 não incorpora a aba nesta versão.
- **Licença:** não usar estado de licença como sinônimo de desligamento; avaliar política própria quando houver datas de vigência.
- **Retenção estendida:** EX003 não cobre achado no snapshot porque a política RP011 é aceita pelo motor atual; eventual restrição é regra de política a especificar.

## Plano de encaminhamento

| Ordem | Ação | Dependência | Saída esperada |
|---:|---|---|---|
| 1 | Aprovar A1–A4 e a interação entre severidade e exceções em TC01. | Responsável pela política de governança. | Registro de decisão com versão e data; atualizações no contrato e nos casos esperados. |
| 2 | Definir modelo de identidade técnica e revisão de principals Aplicação. | Donos de aplicações e segurança. | Inventário, dono, baseline por recurso e critérios de JIT/revisão. |
| 3 | Confirmar SoD financeira e de mudança privilegiada usando o catálogo de papéis. | Responsáveis de Financeiro, Engenharia e Auditoria. | Pares incompatíveis e atividades explícitas na futura Matriz RBAC. |
| 4 | Publicar uma visão operacional distinta para os três tipos de R09. | Frontend/relatórios e política de SLA. | Contagens separadas e leitura que não confunde recertificação com remoção não executada. |
| 5 | Preservar o tratamento de AI07, EX003/EX004 e `campos_dados` até haver decisão/fonte corrigida. | Dono do dataset e política de dados/IA. | Nenhum falso positivo ou dado presumido; limitações visíveis na cobertura. |

## Referências

- `pdbank/rules.py` — regras, severidades, cobertura e exceções implementadas.
- `docs/v0.4.0-relatorio.md` — snapshot, A1–A4 e pendências de política.
- `docs/resultado_dataset_oficial.json` — resultado bruto do dataset oficial.
- `docs/entregas/cesar/nota_qualidade_dados.md` — decisões e limitações de qualidade por pendência.
- `docs/entregas/matheus/relatorio_validacao.md` — comparação dos casos públicos e resultados formais.
- `docs/entregas/alicesena/catalogo_papeis.md` — papéis e separações funcionais propostas.
