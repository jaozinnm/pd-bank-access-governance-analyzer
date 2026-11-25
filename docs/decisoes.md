# Decisões de projeto

1. **Desconhecido ≠ violação ≠ conforme.** Valores irreconhecíveis geram `insufficient_information` (revisão humana), nunca aprovação nem alerta presumido.
2. **Rastreabilidade.** Cada achado cita aba/linha de origem; cada análise guarda `reference_date` e `coverage` por regra.
3. **Aliases de campo centralizados** em `pdbank/schema.py` e não confirmados com o dataset oficial; `get()` só expande o grupo pedido.
4. **Regras puras** (`rules.py` não conhece banco/HTTP); persistência atrás de `Repository`, com o mesmo teste de contrato para memória e SQL.
5. **Exceções:** aprovação explícita + vigência válida + objeto/regra idênticos; sem curingas; o achado é mantido como risco aceito (`valid_exception`).
6. **Importação defensiva:** nada é extraído em disco; limites de tamanho real, entradas, linhas, colunas; rejeição de caminhos inseguros, criptografia, symlink e zip bomb.
7. **Datasets/análises imutáveis**; reanálise cria novo registro (histórico).
8. **Sem IA paga**, sem autenticação padrão (acadêmico); `API_KEY` e `CORS_ORIGINS` opcionais para integração.
9. Migração de banco aditiva (colunas novas anuláveis), sem Alembic nesta versão.

## Decisões de negócio da validação oficial (v0.4.0) — Abraão, 2026-11-25

Detalhamento completo (justificativa, impacto, ação, tabela dos 15 casos): `docs/entregas/abraao/decisoes_casos_publicos.md`.

10. **D1 — TC01 × EX001: mantém *Revisão*.** Exceção válida mantém o achado como `valid_exception` (severidade e evidência preservadas). A decisão passa a ser: achado aberto → *Revisão*; achado coberto por exceção com severidade **crítica** → *Revisão*; achado coberto por exceção com severidade alta ou menor → *Atenção*. Exceção não rebaixa crítico.
11. **D2 — TC09: "Calcular" = resultado derivado da linha de origem.** O esperado não é fixo: aplica-se a R04 à linha do compartilhamento. Se `destination_approved`, `minimum_data_only` e `protected` = Sim → *Sem_Achado / Baixo / Conforme*; caso contrário, o achado R04 correspondente com decisão *Revisão*. Para SH005 o esperado é *Conforme*; o resultado do motor confere.
12. **D3 — TC15 × EX004: não aplicável, sem regra nova.** AI03 tem todos os controles e revisão humana obrigatória; não há violação. Não se cria regra só para "consumir" a exceção. EX004 (e EX003) seguem visíveis em `coverage.EXCEPTIONS` como exceções sem achado. Caso registrado como limitação do caso público.
13. **Premissas:** A1 aprovada; A2 aprovada; A3 aprovada; A4 aprovada com ressalva (achado por papel inferido deve dizer isso na evidência — já diz: "Base: permissões efetivas").
