# PD Bank Access & Governance Analyzer (v0.4.0): roteiro e demonstração

**Apresentação:** qualquer integrante do grupo, ou mais de um · **Duração:** 5 min (≈ 4:45 falado) · **Itens `[PREENCHER]`:** completar antes de entregar

**Integrantes (11):** Abrão Filipi dos Santos, Alice Maria Sena Pereira, Boniek Araújo dos Santos Júnior, Caio César Leandro Amorim, Danilo Gabriel Diniz e Silva, João Rafael Morato Uchoa Cavalcanti, Letícia Gomes da Silva, Marcio Aureliano Pedro da Silva, Maria Larysse Yasmin Lira Pereira, Mateus Valerino Barros de Santana, Matheus do Nascimento Gomes Vaz.

> Regra de ouro: o Analyzer **apoia** a decisão humana. Nunca dizer que ele "decide", "aprova" ou "corrige" acessos sozinho.

## 1. Roteiro falado (por slide)

| Slide | Tempo | O que falar |
|---|---|---|
| 1. Capa | 0:20 | Boa noite. Somos o grupo do PD Bank Access & Governance Analyzer, versão 0.4.0; os integrantes estão neste slide. Em cinco minutos mostramos o que ele faz, uma execução real e seus limites. Ele apoia a decisão humana, não decide sozinho. |
| 2. Problema, objetivo e usuários | 0:35 | O problema: permissões, papéis, exceções e casos de uso de IA ficam em planilhas. Cruzar tudo à mão é lento, inconsistente e difícil de provar em auditoria. O objetivo do Analyzer é transformar esses dados em achados rastreáveis: cada um traz regra, evidência e linha de origem. Os usuários são o analista de governança, que roda a análise, o gestor responsável, que decide, e a auditoria, que confere as evidências. |
| 3. Como funciona | 0:25 | Na entrada, um dataset estruturado. A análise aplica regras determinísticas, de R01 a R09, e registra a cobertura de cada uma. A saída são achados classificados, com severidade, status, impacto e recomendação, exportáveis em JSON e CSV. A arquitetura usa React e TypeScript no frontend, Flask na API e SQLite ou PostgreSQL. |
| 4. Execução real | 0:20 | Esta é a tela de Visão Geral com a execução real, feita em 25 de novembro, com data de referência de 5 de novembro: 1.890 registros importados e 431 achados, sendo 44 críticos e 119 altos. |
| 5. Frontend (**demo ao vivo**) | 0:45 | Vamos começar pelo upload, na tela de Datasets. *[Ação: importar o dataset e executar a análise.]* Em Achados, filtramos por regra, severidade, domínio, status e exceção e abrimos o detalhe de um achado. Em Relatórios, exportamos JSON e CSV da análise. O PDF ainda não faz parte do contrato da API. |
| 6. Caso principal | 0:50 | O caso principal é o achado 17, crítico e não conforme: a regra R02 detectou o conflito SOD01 para o usuário U043. A regra vem da linha 2 de regras_sod; a evidência é a permissão Approve em RES02, linha 493, e o papel R11, linha 154. O impacto é que uma mesma identidade pode iniciar e aprovar operações conflitantes. Recomendamos remover um dos acessos ou registrar exceção aprovada, com prazo e controles compensatórios. A prioridade é crítica, e a decisão é humana, do Compliance Officer; o Analyzer não atribui revisores. Esse conflito foi validado no caso público TC03, U099 e RES02: o esperado era crítico, revisão e Conflito_SoD, e o sistema retornou o mesmo. |
| 7. Situações | 0:45 | O sistema diferencia situações. Dos 431 achados, 428 são não conformes, como o 17. O achado 1 é exceção válida: U003 em RES03 está coberto pela exceção EX001, e a decisão é Atenção. O caso público TC01 esperava Revisão; essa é a divergência que assumimos. O achado 120 mostra prudência: impact_level veio com U016, valor inesperado, então o sistema não conclui e recomenda corrigir a origem, com revisão humana. O caso negativo é o TC05: U001 em RES01 é compatível com o papel e não gera achado de acesso. |
| 8. Limitações e próximos passos | 0:30 | Limitações da v0.4.0: a API não retorna resumo executivo, não exporta PDF e não permite alterar status nem atribuir revisores. Também o TC15 não casa: a exceção de AI03 é válida, mas nenhuma regra gera achado, e o sistema não inventa um. Os próximos passos vão nessa direção, com correção dos dados de origem. |
| 9. Conclusão | 0:15 | Em resumo: dados, regras e evidências geram achados rastreáveis, e a decisão final continua humana. Obrigado. Ficamos à disposição para perguntas. |

**Total: ≈ 4:45**, com ~15 s de folga para a demonstração ao vivo. As falas estão na primeira pessoa do plural, para qualquer integrante apresentar. Divisão opcional para duas pessoas: uma fala os slides 1 a 4, a outra conduz a demonstração (5 a 7) e fecha (8 e 9). Se estourar o tempo, corte primeiro a arquitetura (slide 3) e a explicação dos usuários (slide 2). Nunca corte o slide 6, o TC01 do slide 7 nem a frase de decisão humana.

> **Ensaio com cronômetro:** o texto acima tem cerca de 530 palavras. Ensaie em voz alta e ajuste. Marque aqui o tempo real: `____ min ____ s`.

## 2. Arquivos necessários para a demonstração

1. `PD_Bank_Apresentacao_5min.pptx` (9 slides, e a versão `.pdf`) e `PD_Bank_Plano_B.pptx` (5 slides com capturas, e a versão `.pdf`).
2. Dataset de entrada usado na execução (1.890 registros): `PD_Bank_Analyzer_Dataset_Completo_Alunos_1.xlsx` (no repositório: `tests/data/`). O upload aceita XLSX, CSV e ZIP, até 50 MB.
3. Código na versão **v0.4.0** (frontend React/TypeScript + backend Flask): `[PREENCHER: pasta/branch/tag]`.
4. Exportações já geradas (plano B): CSV com os 431 achados e JSON da execução: `[PREENCHER: caminhos]`.
5. Capturas de tela: Visão Geral (slide 4) e as telas de Datasets, Achados, Relatórios e detalhe do Achado 17 (slide 5 e arquivo `PD_Bank_Plano_B.pptx`).

## 3. Passos da demonstração (repetível)

1. Subir o backend Flask: `[PREENCHER: comando]`.
2. Subir o frontend: `[PREENCHER: comando]` e abrir `http://localhost:5173`. A tela de relatórios fica em `/reports`.
3. Em **Datasets**, fazer o **upload** e, em **Nova Análise**, executar a análise. Conferir: **1.890 registros**, **431 achados**, **44 críticos**.
4. Em **Achados**, aplicar um filtro (ex.: regra **R02** ou severidade **Crítica**) e abrir o **Achado 17** (R02 · U043). Mostrar a origem (planilha `regras_sod`, linha 2), a evidência (linhas 493 e 154) e a ação recomendada.
5. Mostrar os estados: Achado 1 (exceção válida) e Achado 120 (informação insuficiente).
6. Em **Relatórios**, escolher a análise #1, **exportar** JSON e CSV e abrir um deles para mostrar as colunas de rastreabilidade (`finding_type`, `subject_id`, `related_id`, `source_sheet`, `source_row`; os testes automatizados garantem essas cinco). Conferir o cabeçalho real antes de falar de outras colunas.

## 4. Plano B (se algo falhar ao vivo)

- Backend ou frontend não sobe: ficar no slide 5 (capturas pequenas) ou abrir o arquivo **`PD_Bank_Plano_B.pptx`** (5 slides, capturas grandes, na ordem da demonstração) e falar o mesmo texto. Deixe os dois arquivos abertos antes de começar.
- Sem tempo ou sem rede: abrir os **arquivos exportados** (CSV/JSON) direto no computador.
- Se a tela travar: voltar ao slide 6 e seguir só pelo slide.

## 5. Checklist do kit

- [ ] Cabe em 5 min (ensaiado com cronômetro)
- [ ] Nomes dos integrantes nos slides 1 e 9
- [ ] Demonstração repetível (passos acima testados)
- [ ] Nenhuma fala diz que o Analyzer decide sozinho
- [ ] Plano B com capturas ou exportados
- [ ] Slides e roteiro enviados a **Larysse** (pacote final) e **Letícia** (anexo do Playbook)

## 6. Verificações antes de apresentar (vindas dos testes do repositório)

- **Data de referência:** o teste do dataset oficial fixa `reference_date = 2026-11-05`. A tela de Relatórios mostra "4 de nov. de 2026, 21:00", provavelmente por conversão de fuso (UTC−3). O deck usa **05/11/2026**. Se alguém perguntar, explique a diferença. Confirmar com o Matheus.
- **Casos de teste públicos (TC):** o dataset tem 15 (`casos_teste_publicos`). O teste fixa: 12 conferem (inclui **TC03** e **TC14**), **TC01 divergente**, TC09 calculado, TC15 sem correspondência. **TC03** (confirmado em `docs/resultado_dataset_oficial.json`): U099 × RES02, cenário "Papéis de solicitante e aprovador"; esperado Conflito_SoD, prioridade Crítico, decisão Revisão; o sistema retornou 2 achados (R02 Conflito_SoD, origem `regras_sod#2`, e R01 Excesso_de_Privilegio, origem `permissoes_atuais#498`), ambos críticos, decisão Revisão: veredito **match**. A divergência assumida é o TC01 (abaixo).
- **Divergência assumida (TC01, U003/RES03):** o motor acha o achado crítico, mas a exceção EX001 (válida até 2026-12-01) o cobre, e a decisão fica **Atenção**; o caso esperava **Revisão**. Veredito: divergente. É o Achado 1 do deck.
- **Caso negativo (TC05, U001/RES01):** esperado Sem_Achado; confere. Existe uma revisão R09 vencida (AR0001) para o par, reportada como extra e fora do escopo do caso; por isso a fala diz "sem achado de acesso". Outros casos Sem_Achado que conferem: TC08 (DA02) e TC12 (AI12).
- **Calculado (TC09, SH005):** destino aprovado, mínimo e protegido, logo conforme; o sistema não aprova nem reprova o caso.
- **Não casa (TC15, AI03/DA12):** EX004 é válida, mas nenhuma regra gera achado para AI03; o sistema não inventou um. Está na lista de limitações (slide 8).
- **Exceções:** o dataset tem 4 exceções válidas, mas só 2 aparecem em achados (U003/RES03 e U057/RES06, ambos R01). As outras (ex.: DA11, AI03) ficam sem achado associado.
- **Reprodutibilidade:** os totais (431 achados, por regra R01=16, R02=5, R03=7, R04=65, R05=25, R06=3, R07=19, R08=4, R09=287) são um snapshot de regressão. Se mudar regra, atualizar teste e `docs/v0.4.0-relatorio.md`.
