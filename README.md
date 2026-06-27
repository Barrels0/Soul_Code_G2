# 🍷 G2 Distribuidora System

Um sistema robusto de gestão de vendas, estoque e CRM desenvolvido em Python, focado na automação de processos para distribuidoras de bebidas. O sistema oferece controle total sobre o ciclo de vendas, desde o cadastro de produtos até a análise de dados financeiros.

## 🚀 Funcionalidades Principais

* **Ponto de Venda (PDV) Inteligente:**
    * Registro de vendas com verificação dinâmica de estoque.
    * Aplicação automática de descontos por atacado baseada em regras de negócio.
    * Gestão de cupons de desconto com limite de uso.
* **Gestão de Estoque:**
    * Controle de produtos com validade e notas de qualidade.
    * Relatórios de estoque crítico automatizados (suporte para exportação via Pandas).
    * Funcionalidade de reposição em lote para agilizar o dia a dia.
* **Analytics & BI:**
    * Dashboard interativo (via Streamlit) para visualização de faturamento e ticket médio.
    * Ranking de produtos mais vendidos e análise de métodos de pagamento preferidos.
* **Segurança:**
    * Controle de acesso por níveis de usuário (Administrador/Vendedor).
    * Validação de dados rigorosa com tratamento de erros integrado ao MySQL.

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Banco de Dados:** MySQL (mysql-connector)
* **Análise de Dados:** Pandas
* **Interface:** CLI estilizada (Colorama) e Dashboard (Streamlit)

## 📂 Estrutura do Projeto

```text
├── marketing_fornecedores/   # Módulos de marketing e analytics
├── consulta_relatorio/       # Lógica de exportação e relatórios
├── connectsql.py             # Gerenciamento de conexões (Singleton/Pool)
├── forces.py                 # Validações de input (Input Sanitization)
├── main.py                   # Ponto de entrada do sistema
└── README.md