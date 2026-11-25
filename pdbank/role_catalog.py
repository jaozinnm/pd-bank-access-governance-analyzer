"""Catálogo funcional proposto para os papéis do PD Bank.

Os IDs R01–R14 reproduzem os nomes e áreas observados na aba
``catalogo_papeis`` do dataset oficial. Responsabilidades, incompatibilidades e
modos de elevação são propostas de governança derivadas do briefing da Semana 1;
não são permissões efetivas nem uma Matriz RBAC aprovada. Personas de cliente
são externas e não pertencem ao catálogo de papéis internos do dataset.
"""
from __future__ import annotations

from copy import deepcopy


ROLE_CATALOG_VERSION = "1.0.0-proposal"

ROLES = (
    {
        "role_id": "R01", "name": "Analista_Atendimento", "area": "Atendimento",
        "macro_profile": "atendimento_suporte", "catalog_status": "observed_dataset_enriched",
        "purpose": "Atender solicitações de clientes e executar atividades de onboarding dentro do procedimento aprovado.",
        "responsibilities": ["Conferir completude do cadastro e orientar o cliente.", "Acompanhar pendências de onboarding e encaminhar evidências para validação.", "Registrar interações e decisões no histórico do caso.", "Escalonar suspeitas de fraude, identidade inconsistente ou exceção de processo."],
        "incompatibilities": ["Não aprovar a própria validação de identidade nem a própria exceção.", "Não acumular a solicitação, aprovação e execução de uma operação financeira crítica."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "Atendimento de rotina não exige administração de sistemas nem acesso irrestrito a dados."},
    },
    {
        "role_id": "R02", "name": "Supervisor_Atendimento", "area": "Atendimento",
        "macro_profile": "atendimento_suporte", "catalog_status": "observed_dataset_enriched",
        "purpose": "Coordenar a operação de atendimento e revisar decisões dentro da alçada definida.",
        "responsibilities": ["Distribuir casos e acompanhar prazos e escalonamentos.", "Revisar qualidade de evidências e aderência aos procedimentos.", "Aprovar exceções de atendimento dentro da alçada delegada.", "Monitorar indicadores operacionais e encaminhar riscos recorrentes."],
        "incompatibilities": ["Não aprovar a própria solicitação ou exceção.", "A aprovação não deve ser executada pela mesma pessoa quando a operação alterar ou movimentar fundos."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "A alçada de supervisão é funcional; não concede administração técnica."},
    },
    {
        "role_id": "R03", "name": "Dev_Backend", "area": "Engenharia",
        "macro_profile": "engenharia_operacoes", "catalog_status": "observed_dataset_enriched",
        "purpose": "Desenvolver e manter serviços backend e APIs do banco.",
        "responsibilities": ["Implementar APIs e regras de negócio aprovadas.", "Corrigir defeitos e manter testes automatizados da aplicação.", "Revisar código de colegas e registrar decisões técnicas.", "Documentar impactos de mudanças sobre dados, identidade e controles."],
        "incompatibilities": ["Autor de mudança crítica não aprova sozinho a própria implantação em produção.", "Não acumular desenvolvimento e administração irrestrita de produção."],
        "elevated_access": {"required": False, "mode": "jit_if_approved", "permanent": False, "rationale": "Diagnóstico excepcional em produção deve ter finalidade, aprovador, escopo e janela definidos."},
    },
    {
        "role_id": "R04", "name": "Dev_Frontend", "area": "Engenharia",
        "macro_profile": "engenharia_operacoes", "catalog_status": "observed_dataset_enriched",
        "purpose": "Desenvolver e manter interfaces usadas por clientes e equipes internas.",
        "responsibilities": ["Implementar interfaces e fluxos de interação.", "Integrar a interface aos contratos de API documentados.", "Corrigir defeitos e validar acessibilidade e estados de erro.", "Revisar mudanças que afetem exposição de dados no cliente."],
        "incompatibilities": ["Não aprovar nem publicar sozinho a própria mudança crítica.", "Não alterar controles de autorização do backend sem revisão da equipe responsável."],
        "elevated_access": {"required": False, "mode": "jit_if_approved", "permanent": False, "rationale": "Acesso a produção só para diagnóstico específico aprovado; desenvolvimento cotidiano usa ambientes não produtivos."},
    },
    {
        "role_id": "R05", "name": "DBA", "area": "Infraestrutura",
        "macro_profile": "engenharia_operacoes", "catalog_status": "observed_dataset_enriched",
        "purpose": "Administrar disponibilidade, integridade e recuperação dos bancos de dados.",
        "responsibilities": ["Monitorar saúde, capacidade e desempenho dos bancos.", "Preparar e executar migrações aprovadas.", "Administrar backup, restauração e continuidade.", "Apoiar incidentes com evidências e trilha de mudanças."],
        "incompatibilities": ["Não aprovar sozinho a mudança que preparou ou executou.", "Separar administração técnica da leitura rotineira do conteúdo financeiro de produção.", "Não alterar ou apagar os logs usados para auditar sua atividade."],
        "elevated_access": {"required": True, "mode": "jit", "permanent": False, "rationale": "Administração de produção deve ser ativada por tarefa e janela; eventual conta de emergência exige monitoramento e revisão posterior."},
    },
    {
        "role_id": "R06", "name": "Cloud_Admin", "area": "Infraestrutura",
        "macro_profile": "engenharia_operacoes", "catalog_status": "observed_dataset_enriched",
        "purpose": "Manter infraestrutura em nuvem e responder a incidentes operacionais.",
        "responsibilities": ["Manter disponibilidade e configuração dos serviços em nuvem.", "Responder a alertas e incidentes técnicos.", "Executar mudanças aprovadas e manter evidências de implantação.", "Revisar capacidade, resiliência e recuperação dos serviços."],
        "incompatibilities": ["Solicitante, aprovador e executor de mudança crítica devem ser pessoas distintas, salvo contingência documentada.", "Não administrar sozinho o cofre de segredos e os logs que registram a própria atividade."],
        "elevated_access": {"required": True, "mode": "jit", "permanent": False, "rationale": "Privilégio de nuvem é amplo; ativação temporária e monitorada reduz exposição contínua."},
    },
    {
        "role_id": "R07", "name": "Auditor", "area": "Risco_Auditoria",
        "macro_profile": "auditoria_conformidade", "catalog_status": "observed_dataset_enriched",
        "purpose": "Verificar, com independência, a existência e a efetividade dos controles.",
        "responsibilities": ["Consultar políticas, trilhas e evidências autorizadas.", "Testar desenho e execução dos controles.", "Registrar achados, limitações e recomendações.", "Acompanhar respostas às recomendações sem executar a remediação auditada."],
        "incompatibilities": ["Não alterar o controle ou evidência que está auditando.", "Não aprovar e executar a própria remediação."],
        "elevated_access": {"required": False, "mode": "read_only", "permanent": False, "rationale": "A independência é preservada com leitura; acesso a dados sensíveis deve ser limitado ao escopo de auditoria."},
    },
    {
        "role_id": "R08", "name": "Cientista_Dados", "area": "Dados",
        "macro_profile": "fora_dos_quatro_perfis", "catalog_status": "observed_dataset_enriched",
        "purpose": "Preparar análises e modelos usando dados autorizados para finalidades definidas.",
        "responsibilities": ["Preparar conjuntos de dados minimizados para análise.", "Desenvolver e avaliar modelos analíticos em ambiente controlado.", "Documentar origem, finalidade, limitações e resultados dos modelos.", "Submeter casos de IA e fontes de dados à aprovação de governança."],
        "incompatibilities": ["Não aprovar a própria fonte ou finalidade de dados.", "Não promover modelo para produção sem revisão e aprovação independentes."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "O trabalho deve usar conjuntos minimizados e ambientes controlados, sem acesso administrativo por padrão."},
    },
    {
        "role_id": "R09", "name": "Analista_SecOps", "area": "Seguranca",
        "macro_profile": "engenharia_operacoes", "catalog_status": "observed_dataset_enriched",
        "purpose": "Monitorar eventos de segurança e coordenar resposta técnica a incidentes.",
        "responsibilities": ["Analisar alertas de autenticação e atividade privilegiada.", "Investigar incidentes e preservar evidências.", "Recomendar contenção e encaminhar mudanças para aprovação.", "Acompanhar vulnerabilidades e controles de segurança."],
        "incompatibilities": ["Não apagar ou alterar evidências de auditoria da própria atividade.", "Não aprovar sozinho uma elevação que solicitou nem encerrar sem revisão um incidente sob sua própria administração."],
        "elevated_access": {"required": True, "mode": "jit", "permanent": False, "rationale": "Ações de contenção podem exigir elevação temporária; manter conta cotidiana separada e registrar o uso."},
    },
    {
        "role_id": "R10", "name": "Aprovador_Pagamento", "area": "Financeiro",
        "macro_profile": "fora_dos_quatro_perfis", "catalog_status": "observed_dataset_enriched",
        "purpose": "Revisar e aprovar solicitações de pagamento dentro da alçada financeira.",
        "responsibilities": ["Revisar dados e justificativa da solicitação.", "Confirmar alçada e controles aplicáveis.", "Registrar decisão e evidência de aprovação.", "Encaminhar inconsistências para investigação."],
        "incompatibilities": ["Não solicitar e aprovar a mesma operação.", "A aprovação deve ser separada da execução quando a operação e a alçada permitirem."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "A aprovação financeira é uma capacidade funcional segregada, não uma administração técnica."},
    },
    {
        "role_id": "R11", "name": "Solicitante_Pagamento", "area": "Financeiro",
        "macro_profile": "fora_dos_quatro_perfis", "catalog_status": "observed_dataset_enriched",
        "purpose": "Preparar solicitações de pagamento para revisão e aprovação independente.",
        "responsibilities": ["Registrar beneficiário, valor e finalidade da solicitação.", "Anexar documentos e evidências de suporte.", "Corrigir dados devolvidos para ajuste.", "Acompanhar o status até a decisão."],
        "incompatibilities": ["Não aprovar a própria solicitação.", "Não executar alteração de beneficiário e aprovar o pagamento correspondente sem controle independente."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "A função de solicitação não requer privilégio administrativo nem aprovação."},
    },
    {
        "role_id": "R12", "name": "Compliance_Officer", "area": "Compliance",
        "macro_profile": "auditoria_conformidade", "catalog_status": "observed_dataset_enriched",
        "purpose": "Acompanhar aderência a políticas internas e obrigações de conformidade do cenário.",
        "responsibilities": ["Manter inventário de obrigações e controles aplicáveis.", "Revisar evidências de conformidade e exceções.", "Encaminhar lacunas e incidentes aos responsáveis.", "Acompanhar planos de ação e prazos."],
        "incompatibilities": ["Não aprovar sozinho o controle cuja execução também realizou.", "Não editar evidência original sob revisão."],
        "elevated_access": {"required": False, "mode": "read_only", "permanent": False, "rationale": "Consulta e acompanhamento bastam para a finalidade; elevação de investigação deve ser pontual."},
    },
    {
        "role_id": "R13", "name": "Analista_RH", "area": "RH",
        "macro_profile": "fora_dos_quatro_perfis", "catalog_status": "observed_dataset_enriched",
        "purpose": "Executar processos de RH e tratar dados de colaboradores para finalidades autorizadas.",
        "responsibilities": ["Manter registros funcionais necessários aos processos de RH.", "Tratar dados de colaboradores com finalidade e acesso restritos.", "Encaminhar alterações de vínculo aos responsáveis por identidade e acesso.", "Preservar evidências de alterações e solicitações."],
        "incompatibilities": ["Não aprovar sozinho a própria alteração funcional nem a concessão de acesso decorrente.", "Não usar dados de RH para finalidades alheias ao processo autorizado."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "Acesso é restrito por finalidade; administração de identidade deve permanecer em função separada."},
    },
    {
        "role_id": "R14", "name": "Product_Owner", "area": "Produtos",
        "macro_profile": "fora_dos_quatro_perfis", "catalog_status": "observed_dataset_enriched",
        "purpose": "Definir prioridades e critérios funcionais dos produtos digitais.",
        "responsibilities": ["Priorizar necessidades e requisitos do produto.", "Definir critérios de aceitação e comunicar impactos aos stakeholders.", "Avaliar resultados de produto sem acessar dados além da necessidade.", "Submeter mudanças de finalidade ou uso de dados à governança apropriada."],
        "incompatibilities": ["Não aprovar sozinho a própria mudança em produção.", "Não autorizar finalidade de uso de dados que também implementa sem revisão independente."],
        "elevated_access": {"required": False, "mode": "none", "permanent": False, "rationale": "Responsabilidade de produto não exige privilégio técnico ou acesso a dados de produção."},
    },
    {
        "role_id": "EXT-CLIENT-HOLDER", "name": "Titular de conta", "area": "Cliente final",
        "macro_profile": "cliente_final", "catalog_status": "proposal_from_week1_briefing",
        "purpose": "Usar os serviços digitais em nome próprio e sobre a própria conta.",
        "responsibilities": ["Consultar saldo e extrato próprios.", "Iniciar Pix e pagamentos sujeitos aos controles da operação.", "Administrar cartões próprios.", "Acompanhar solicitações de crédito e interagir com o assistente de IA autorizado."],
        "incompatibilities": ["Não consultar ou alterar conta de terceiro sem vínculo autorizado.", "Iniciação e aprovação de operação crítica devem ser controladas pelo fluxo transacional, sem autoaprovação de exceções."],
        "elevated_access": {"required": False, "mode": "not_applicable", "permanent": False, "rationale": "Persona externa; não recebe papel administrativo interno nem entra no baseline de funcionários."},
    },
    {
        "role_id": "EXT-CLIENT-REPRESENTATIVE", "name": "Representante autorizado de conta", "area": "Cliente final",
        "macro_profile": "cliente_final", "catalog_status": "proposal_from_week1_briefing",
        "purpose": "Realizar atividades permitidas em uma conta conforme mandato registrado.",
        "responsibilities": ["Consultar apenas as informações cobertas pelo mandato.", "Acompanhar solicitações da conta representada.", "Iniciar operações dentro dos limites do mandato.", "Solicitar atualização cadastral sujeita a validação."],
        "incompatibilities": ["Não ampliar o próprio mandato nem cadastrar a própria autorização.", "Não aprovar sozinho alteração de identidade ou de poderes que lhe beneficie."],
        "elevated_access": {"required": False, "mode": "not_applicable", "permanent": False, "rationale": "Persona externa; escopo depende de mandato vigente, não de privilégio administrativo interno."},
    },
)

SEPARATION_CONSTRAINTS = (
    {"constraint_id": "SOD-PAY-01", "roles": ["R11", "R10"], "activities": ["solicitar pagamento", "aprovar pagamento"], "rationale": "Quem solicita não aprova a mesma operação.", "status": "proposed"},
    {"constraint_id": "SOD-SUPPORT-01", "roles": ["R01", "R02"], "activities": ["preparar evidência/caso", "revisar ou aprovar exceção"], "rationale": "A revisão do caso deve ser independente de quem o preparou; supervisor não aprova a própria solicitação.", "status": "proposed"},
    {"constraint_id": "SOD-CHANGE-01", "roles": ["R03", "R04", "R05", "R06", "R09"], "activities": ["autorizar mudança", "executar implantação"], "rationale": "Mudanças críticas em produção exigem autoria, aprovação e execução separadas sempre que possível.", "status": "proposed"},
    {"constraint_id": "SOD-DB-01", "roles": ["R05", "R07"], "activities": ["administrar banco", "auditar evidência de banco"], "rationale": "O administrador não altera a evidência que o auditor usa para verificar sua atividade.", "status": "proposed"},
    {"constraint_id": "SOD-SEC-01", "roles": ["R09", "R07"], "activities": ["operar controles de segurança", "auditar controles e trilhas"], "rationale": "A auditoria de atividade privilegiada requer independência da operação de segurança.", "status": "proposed"},
    {"constraint_id": "SOD-IDENTITY-01", "roles": ["R13", "R09"], "activities": ["informar mudança de vínculo", "aprovar e provisionar acesso"], "rationale": "RH informa o evento funcional; provisionamento e validação de acesso ficam sob controle separado.", "status": "proposed"},
)


def get_role_catalog() -> dict:
    """Retorna uma cópia independente do catálogo para serialização pela API."""
    return {
        "version": ROLE_CATALOG_VERSION,
        "status": "proposed",
        "source_notes": [
            "R01–R14 preservam os IDs, nomes e áreas da aba catalogo_papeis do dataset oficial.",
            "Responsabilidades, incompatibilidades e elevação são propostas derivadas do briefing da Semana 1.",
            "Papéis EXT-* são personas externas de cliente e não pertencem ao baseline interno do dataset.",
            "Este catálogo não concede permissões nem substitui a Matriz RBAC da Semana 2.",
        ],
        "roles": deepcopy(list(ROLES)),
        "separation_constraints": deepcopy(list(SEPARATION_CONSTRAINTS)),
    }
