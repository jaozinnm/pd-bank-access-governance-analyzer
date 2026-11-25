Para: Sena, Matheus, Letícia
Assunto: Decisões dos casos públicos e premissas — v0.4.0

Pessoal, decisões fechadas (detalhe em docs/entregas/abraao/decisoes_casos_publicos.md):

1. TC01 (U003 × EX001): fica REVISÃO. Exceção válida não rebaixa crítico. Regra: aberto → Revisão; coberto por exceção e crítico → Revisão; coberto e alto/médio/baixo → Atenção. O achado continua valid_exception.
2. TC09 (SH005): "Calcular" = aplicar a R04 na linha. Aprovado + mínimo + protegido = Conforme. SH005 = Conforme → confere.
3. TC15 (AI03 × EX004): não aplicável. Sem regra nova; AI03 não tem violação. EX003/EX004 seguem na cobertura como exceções sem achado.
4. Premissas: A1, A2, A3 aprovadas. A4 aprovada com ressalva: evidência sempre diz "papel inferido por permissão".

Resultado: 14 conferem + 1 não aplicável.

O que cada um faz:
- Sena: atualizar o catálogo com D1–D3 e A1–A4 como aprovadas.
- Matheus: ajustar o teste test_public_cases_comparison_is_honest e os relatórios (tirar os [PENDENTE: decisão do Abraão]).
- Letícia: copiar a seção 1 e 2 do arquivo de decisões para o Playbook.
