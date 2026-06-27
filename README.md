🍷 G2 Distribuidora System
Um sistema de gestão de vendas, estoque e CRM desenvolvido em Python com integração MySQL, focado na automação de processos para distribuidoras de bebidas. O sistema permite um controle rigoroso de estoque, aplicação de políticas de preços (atacado/varejo), gestão de cupons e análise de dados.

🚀 Funcionalidades Principais
Ponto de Venda (PDV) Inteligente:

Registro de vendas com verificação de estoque em tempo real.

Aplicação automática de descontos por atacado baseada em regras de negócio.

Vínculo obrigatório com clientes e controle de pagamentos.

Gestão de Estoque:

Cadastro de produtos com controle de validade e notas de avaliação.

Relatórios de estoque crítico automatizados com exportação (via Pandas).

Funcionalidade de reposição em lote.

Marketing e CRM:

Gestão de cupons de desconto com limite de uso.

Dashboard Analytics interativo para visualização de tendências.

Ranking dos produtos mais vendidos e análise de ticket médio.

Segurança e Manutenção:

Controle de acesso por níveis de usuário (Administrador/Vendedor).

Validação de dados robusta para evitar corrupção no banco de dados.

🛠 Tecnologias Utilizadas
Linguagem: Python 3.x

Banco de Dados: MySQL (utilizando mysql-connector)

Análise de Dados: Pandas

Interface: CLI (Interface de Linha de Comando) estilizada com Colorama

Analytics: Streamlit

📂 Estrutura do Projeto
Plaintext
├── marketing_fornecedores/   # Módulos de marketing e analytics
├── consulta_relatorio/       # Lógica de exportação e relatórios
├── connectsql.py             # Gerenciamento de conexões com banco
├── forces.py                 # Funções de validação de input (CLI)
├── main.py                   # Ponto de entrada do sistema
└── README.md