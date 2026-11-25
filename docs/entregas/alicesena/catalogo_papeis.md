# Catálogo funcional de papéis do PD Bank

## Finalidade

Este catálogo transforma nomes de papéis em responsabilidades verificáveis para apoiar a futura Matriz RBAC. Ele não define permissões específicas e não altera atribuições do dataset. Os identificadores R01–R14, nomes e áreas são os da aba `catalogo_papeis` do arquivo oficial; descrições, incompatibilidades e recomendações de elevação são propostas desta entrega, derivadas do cenário e do briefing da Semana 1.

## Leitura do catálogo existente

O briefing apresenta quatro perfis macro: Cliente final, Atendimento e suporte, Engenharia e operações, e Auditoria e conformidade. O dataset oficial contém 14 papéis internos em várias áreas, mas não inclui um papel de Cliente final. Também contém Financeiro, Dados, RH e Produtos, que não correspondem diretamente aos quatro perfis macro. Este catálogo não renomeia nem apaga essa diferença: marca o mapeamento proposto e deixa as áreas não cobertas explicitamente fora dos quatro perfis.

Os dois papéis de cliente abaixo são personas do serviço digital, identificadas por `EXT-*`. Eles não são papéis da tabela oficial, não são empregados e não devem ser adicionados ao baseline de funcionários. Seu vínculo é limitado à própria conta ou a mandato autorizado.

## Papéis internos observados no dataset

| ID | Nome oficial | Área do dataset | Perfil macro proposto | Finalidade resumida | Acesso elevado |
|---|---|---|---|---|---|
| R01 | Analista_Atendimento | Atendimento | Atendimento e suporte | Onboarding, orientação, registro e encaminhamento de casos. | Não; sem administração. |
| R02 | Supervisor_Atendimento | Atendimento | Atendimento e suporte | Coordenação, revisão de evidências e aprovações dentro de alçada. | Não; alçada funcional limitada. |
| R03 | Dev_Backend | Engenharia | Engenharia e operações | Desenvolvimento e manutenção de APIs/serviços. | Somente JIT aprovado para diagnóstico excepcional. |
| R04 | Dev_Frontend | Engenharia | Engenharia e operações | Interfaces, integração com API, acessibilidade e exposição de dados no cliente. | Somente JIT aprovado para diagnóstico excepcional. |
| R05 | DBA | Infraestrutura | Engenharia e operações | Disponibilidade, integridade, migração, backup e recuperação de bancos. | Sim; JIT, sem privilégio permanente. |
| R06 | Cloud_Admin | Infraestrutura | Engenharia e operações | Infraestrutura em nuvem, mudanças e resposta operacional. | Sim; JIT, sem privilégio permanente. |
| R07 | Auditor | Risco_Auditoria | Auditoria e conformidade | Verificação independente de políticas, evidências e controles. | Não; leitura no escopo autorizado. |
| R08 | Cientista_Dados | Dados | Fora dos quatro perfis | Preparação minimizada de dados e avaliação de modelos/casos analíticos. | Não; ambiente controlado, sem administração. |
| R09 | Analista_SecOps | Seguranca | Engenharia e operações | Monitoramento, investigação e resposta de segurança. | Sim; JIT em ações que exijam contenção privilegiada. |
| R10 | Aprovador_Pagamento | Financeiro | Fora dos quatro perfis | Revisão e aprovação de solicitações dentro da alçada financeira. | Não; privilégio funcional de aprovação não é administração técnica. |
| R11 | Solicitante_Pagamento | Financeiro | Fora dos quatro perfis | Preparação de pagamentos e respectivos documentos de suporte. | Não; solicita, mas não aprova a própria operação. |
| R12 | Compliance_Officer | Compliance | Auditoria e conformidade | Acompanhamento de políticas, exceções, evidências e planos de ação. | Não; leitura e acompanhamento. |
| R13 | Analista_RH | RH | Fora dos quatro perfis | Processos de RH com acesso limitado a dados de colaboradores. | Não; administração de identidade permanece separada. |
| R14 | Product_Owner | Produtos | Fora dos quatro perfis | Requisitos, critérios funcionais e priorização de produto. | Não; sem privilégio técnico por padrão. |

## Responsabilidades por papel

As responsabilidades abaixo são propostas funcionais. A coluna de área preserva o valor original do dataset; o mapeamento para o perfil macro é uma interpretação para esta entrega.

### R01 — Analista_Atendimento

- Conferir a completude do cadastro e orientar clientes.
- Acompanhar pendências de onboarding e encaminhar evidências para validação.
- Registrar interações e decisões no histórico do caso.
- Escalonar suspeita de fraude, inconsistência de identidade ou exceção de processo.
- **Separação:** não aprova a própria validação ou exceção; não solicita, aprova e executa sozinho uma operação crítica.

### R02 — Supervisor_Atendimento

- Distribuir casos e acompanhar prazos e escalonamentos.
- Revisar a qualidade das evidências e a aderência ao procedimento.
- Aprovar exceções de atendimento somente dentro da alçada delegada.
- Acompanhar padrões recorrentes e encaminhar riscos.
- **Separação:** não aprova sua própria solicitação; autorização e execução de operação financeira crítica devem ter pessoas distintas.

### R03 — Dev_Backend

- Implementar APIs e regras de negócio aprovadas.
- Corrigir defeitos e manter testes da aplicação.
- Revisar código de colegas e registrar decisões técnicas.
- Documentar impactos sobre dados, identidade e controles.
- **Separação:** autoria de mudança não equivale à aprovação de implantação; sem administração contínua de produção.

### R04 — Dev_Frontend

- Implementar interfaces e fluxos de interação.
- Integrar a interface aos contratos de API documentados.
- Corrigir defeitos e validar acessibilidade e estados de erro.
- Revisar exposição de dados nos componentes cliente.
- **Separação:** não publica sozinho a própria mudança crítica nem altera controles backend sem revisão responsável.

### R05 — DBA

- Monitorar saúde, capacidade e desempenho de bancos.
- Preparar e executar migrações aprovadas.
- Administrar backup, restauração e continuidade.
- Apoiar incidentes com trilha de mudanças e evidências.
- **Separação:** não aprova sozinho a mudança executada; não altera logs usados para auditar a própria atividade.
- **Elevação:** JIT por tarefa e janela definidas. Conta de emergência exige monitoramento e revisão pós-uso.

### R06 — Cloud_Admin

- Manter disponibilidade e configuração dos serviços em nuvem.
- Responder a alertas e incidentes técnicos.
- Executar mudanças aprovadas e documentar implantação.
- Revisar capacidade, resiliência e recuperação.
- **Separação:** solicitante, aprovador e executor de mudança crítica devem ser distintos, salvo contingência documentada.
- **Elevação:** JIT com escopo mínimo e registro; não administrar sozinho os logs ou segredos que comprovam a própria atividade.

### R07 — Auditor

- Consultar políticas, trilhas e evidências autorizadas.
- Testar desenho e execução dos controles.
- Registrar achados, limitações e recomendações.
- Acompanhar respostas sem executar a remediação auditada.
- **Separação:** não altera o controle ou evidência sob auditoria.
- **Elevação:** sem privilégio administrativo; acesso de leitura limitado ao escopo da auditoria.

### R08 — Cientista_Dados

- Preparar conjuntos de dados minimizados para análise.
- Desenvolver e avaliar modelos em ambiente controlado.
- Documentar origem, finalidade, limitações e resultados.
- Submeter fontes e casos de IA ao processo de governança.
- **Separação:** não aprova a própria fonte/finalidade nem promove sozinho modelo para produção.

### R09 — Analista_SecOps

- Analisar alertas de autenticação e atividade privilegiada.
- Investigar incidentes e preservar evidências.
- Recomendar contenção e encaminhar mudanças para aprovação.
- Acompanhar vulnerabilidades e controles de segurança.
- **Separação:** não altera evidência de auditoria da própria atividade nem aprova a elevação que solicitou.
- **Elevação:** JIT para contenção privilegiada; conta cotidiana separada e trilha revisada.

### R10 — Aprovador_Pagamento

- Revisar dados, valor, beneficiário e justificativa da solicitação.
- Confirmar alçada e controles aplicáveis.
- Registrar decisão e evidência de aprovação.
- Encaminhar inconsistências para investigação.
- **Separação:** não solicita nem executa sozinho a mesma operação que aprovou.

### R11 — Solicitante_Pagamento

- Registrar beneficiário, valor e finalidade do pagamento.
- Anexar documentos de suporte.
- Corrigir dados devolvidos para ajuste.
- Acompanhar a solicitação até a decisão.
- **Separação:** não aprova a própria solicitação nem combina alteração de beneficiário com aprovação do pagamento.

### R12 — Compliance_Officer

- Manter inventário de obrigações e controles aplicáveis ao cenário.
- Revisar evidências de conformidade e exceções.
- Encaminhar lacunas e incidentes aos responsáveis.
- Acompanhar planos de ação e prazos.
- **Separação:** não aprova sozinho o controle que também executou nem altera evidência original sob revisão.

### R13 — Analista_RH

- Manter registros funcionais necessários aos processos de RH.
- Tratar dados de colaboradores com finalidade e acesso restritos.
- Comunicar alterações de vínculo ao processo de identidade e acesso.
- Preservar evidências de alterações e solicitações.
- **Separação:** não aprova a própria alteração funcional nem provisiona sozinho o acesso decorrente.

### R14 — Product_Owner

- Priorizar requisitos do produto.
- Definir critérios de aceitação e comunicar impactos.
- Avaliar resultados sem acesso a dados além da necessidade.
- Submeter mudança de finalidade ou uso de dados à governança.
- **Separação:** não aprova sozinho sua própria publicação em produção nem autoriza sozinho a finalidade de dados que implementa.

## Personas externas do briefing

### EXT-CLIENT-HOLDER — Titular de conta

Consulta saldo e extrato próprios, inicia pagamentos/Pix conforme controles da operação, administra cartões próprios e acompanha solicitações. Não consulta nem altera dados de terceiros sem vínculo autorizado. Não é administrador de sistema.

### EXT-CLIENT-REPRESENTATIVE — Representante autorizado de conta

Consulta informações permitidas pelo mandato, acompanha solicitações, inicia operações dentro dos limites autorizados e solicita atualização sujeita a validação. Não amplia o próprio mandato nem aprova alteração de identidade ou poderes que lhe beneficie.

## Restrições SoD propostas

Estas restrições são propostas para que a Semana 2 associe as atividades a recursos e permissões concretas. A lista não afirma que o dataset ou o motor já implementa todos estes controles.

| ID | Papéis / atividades | Regra de separação | Razão |
|---|---|---|---|
| SOD-PAY-01 | R11 solicitar pagamento / R10 aprovar pagamento | Pessoas distintas na mesma operação. | Impede autoaprovação de solicitação financeira. |
| SOD-SUPPORT-01 | R01 preparar evidência/caso / R02 revisar ou aprovar exceção | Revisão independente; supervisor também não aprova sua própria solicitação. | Reduz erro ou abuso em onboarding e atendimento. |
| SOD-CHANGE-01 | R03/R04 autorar / R05/R06/R09 executar ou administrar / aprovação independente | Separar autoria, aprovação e implantação de mudança crítica sempre que possível. | Evita que uma única identidade introduza e publique mudança crítica sem controle. |
| SOD-DB-01 | R05 administrar banco / R07 auditar evidência | DBA não altera a evidência que auditor usa para verificar a atividade. | Preserva integridade da trilha e independência. |
| SOD-SEC-01 | R09 operar segurança / R07 auditar segurança e trilhas | Atividade privilegiada deve ter revisão independente. | Reduz conflito de autoauditoria. |
| SOD-IDENTITY-01 | R13 comunicar vínculo / responsável distinto provisionar e aprovar acesso | RH informa evento; identidade/acesso valida e executa provisionamento. | Evita concessões baseadas em alteração funcional não revisada. |

## Critérios de elevação JIT

Para DBA, Cloud Admin e SecOps, toda ativação elevada deve especificar identidade, justificativa, aprovador independente, recursos e ações autorizados, horário de início/fim, evidências de uso e revisão após a tarefa. Acesso permanente só deve ser aprovado mediante necessidade operacional comprovada, alternativas temporárias insuficientes, escopo reduzido, dono, controles compensatórios e prazo de reavaliação. Nenhum acesso permanente é proposto nesta versão.

## Preparação da Matriz RBAC

Para cada papel, a equipe deve decidir por recurso e ação: leitura, criação, alteração, aprovação, execução ou administração. Permissões de aprovação e execução devem ser diferenciadas; os pares SoD devem ser cruzados com `regras_sod`; os acessos JIT devem ter duração, justificativa, aprovador e revisão; dados e fontes de IA devem seguir finalidade e minimização. Papéis `EXT-*` devem receber um modelo de autorização separado de contas de empregados e de contas técnicas.
