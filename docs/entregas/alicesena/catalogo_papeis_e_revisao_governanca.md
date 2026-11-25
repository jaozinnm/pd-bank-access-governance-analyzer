# Entrega de Alice Maria Sena Pereira — catálogo de papéis e revisão de governança

**Projeto:** PD Bank Access & Governance Analyzer  
**Escopo:** Catálogo e revisão das regras de governança  
**Base técnica:** backend v0.4.0 e dataset oficial v2.0  
**Data de referência dos resultados citados:** 05/11/2026  
**Status desta entrega:** documentação e catálogo funcional proposto; decisões de política indicadas como pendentes permanecem sob validação da equipe.

## Resumo

Esta entrega organiza o catálogo de papéis e a revisão das regras em documentação e código. A estrutura preserva os IDs, nomes e áreas dos 14 papéis observados na aba `catalogo_papeis` do dataset oficial, explicita que esses papéis não cobrem perfeitamente os quatro perfis do briefing e acrescenta duas personas externas de cliente sem tratá-las como papéis de funcionários. Responsabilidades, incompatibilidades, separação de funções e modo de elevação são propostas para preparar a Matriz RBAC da Semana 2; não são permissões concedidas.

A revisão das regras R01–R09 mantém a distinção entre comportamento implementado, decisão de dado já registrada por outras entregas e premissa de política ainda pendente. Não foram alteradas as regras de detecção nesta entrega.

## Arquivos e uso

| Arquivo | Conteúdo |
|---|---|
| [`catalogo_papeis.md`](catalogo_papeis.md) | Catálogo humano, mapeamento dos perfis macro, responsabilidades e controles SoD/JIT propostos. |
| [`revisao_regras_governanca.md`](revisao_regras_governanca.md) | Revisão R01–R09, resultados por regra, premissas, decisões existentes, limitações e encaminhamentos. |
| [`pdbank/role_catalog.py`](../../../pdbank/role_catalog.py) | Fonte estruturada do catálogo consumida pela API. |
| `GET /api/roles` | Endpoint que publica o catálogo funcional para clientes da API. |

## Decisões de escopo

- **IDs oficiais preservados:** R01–R14 seguem exatamente os identificadores do catálogo de papéis do dataset.
- **Papéis extras do cenário:** Cliente titular e representante autorizado usam IDs `EXT-*`; são personas externas e não entram no baseline interno.
- **Áreas fora dos quatro perfis:** Financeiro, Dados, RH e Produtos são preservadas e marcadas como fora do mapeamento macro inicial, em vez de forçadas para uma área inadequada.
- **Privilegiados:** DBA (R05), Cloud Admin (R06) e Analista SecOps (R09) são marcados para elevação JIT; o campo `permanent` permanece `false` para todos os papéis propostos.
- **Separação de funções:** as restrições são propostas e não configuram automaticamente conflito em uma análise. A Matriz RBAC e os controles compensatórios ainda precisam de aprovação.
- **Política das regras:** o relatório registra A1–A4 como premissas ainda sujeitas à validação do responsável por política. A classificação técnica das pendências de qualidade de dados segue as notas de César e Matheus.

## Interface técnica adicionada

`GET /api/roles` retorna `version`, `status`, notas de origem, `roles` e `separation_constraints`. O endpoint é informativo: não atribui, revoga ou autoriza acesso. Seu schema foi incluído no OpenAPI e o contrato está descrito em `docs/API.md`.

## Limites e validação

Responsabilidades, incompatibilidades e justificativas de elevação são uma proposta acadêmica derivada do briefing e dos nomes/áreas do dataset; a planilha não contém essas descrições. A lista não substitui aprovação dos donos dos processos, definição de alçadas nem a Matriz RBAC. As regras R01–R09 não foram alteradas. Esta entrega não registra execução de testes ou evidências de chamada HTTP.
