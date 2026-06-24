import streamlit as st
import pandas as pd
import plotly.express as px
from connectsql import obter_conexao

# Configuração inicial da página
st.set_page_config(page_title="Distribuidora G2", layout="wide")

# Função que serve para não termos que buscar os dados no banco toda vez que a página é atualizada
@st.cache_data(ttl=60)
def buscar_dados(query):
    conexao = obter_conexao()
    if conexao:
        df = pd.read_sql(query, conexao)
        conexao.close()
        return df
    return pd.DataFrame()

# ==========================================
# 1. HEADER DO DASHBOARD
# ==========================================
st.title(" Dashboard - Distribuidora G2")
st.markdown("Visão geral de faturamento, rentabilidade por fornecedor e fluxo de saída do estoque.")
st.markdown("---")

# ==========================================
# 2. BUSCANDO DADOS
# ==========================================
# KPIs Gerais
df_vendas = buscar_dados("SELECT id_venda, valor_total, forma_pagamento, data_hora FROM vendas")

# Evolução do Faturamento por Data (Série Temporal)
query_tempo = """
    SELECT DATE(data_hora) as data, SUM(valor_total) as faturamento 
    FROM vendas 
    GROUP BY DATE(data_hora) 
    ORDER BY data
"""
df_tempo = buscar_dados(query_tempo)

# Receita gerada por Fornecedor
query_fornecedores = """
    SELECT f.nome as Fornecedor, SUM(iv.quantidade * iv.preco_unitario) as Receita 
    FROM itens_venda iv 
    JOIN produtos p ON iv.id_produto = p.id_produto 
    JOIN fornecedores f ON p.id_fornecedor = f.id_fornecedor 
    GROUP BY f.nome 
    ORDER BY Receita DESC
"""
df_fornecedores = buscar_dados(query_fornecedores)

# Volume de Vendas por Categoria
query_categorias = """
    SELECT c.nome as Categoria, SUM(iv.quantidade) as Unidades_Vendidas 
    FROM itens_venda iv 
    JOIN produtos p ON iv.id_produto = p.id_produto 
    JOIN categorias c ON p.id_categoria = c.id_categoria 
    GROUP BY c.nome
    ORDER BY Unidades_Vendidas DESC
"""
df_categorias = buscar_dados(query_categorias)

# Top Produtos mais vendidos vs Estoque
query_produtos_saida = """
    SELECT p.nome as Produto, SUM(iv.quantidade) as Vendidos, p.quantidade_estoque as Estoque_Atual
    FROM itens_venda iv
    JOIN produtos p ON iv.id_produto = p.id_produto
    GROUP BY p.id_produto, p.nome, p.quantidade_estoque
    ORDER BY Vendidos DESC
    LIMIT 5
"""
df_produtos_saida = buscar_dados(query_produtos_saida)


# ==========================================
# 3. MÉTRICAS PRINCIPAIS (Cards)
# ==========================================
if not df_vendas.empty:
    faturamento_total = df_vendas['valor_total'].sum()
    total_pedidos = df_vendas['id_venda'].count()
    ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0
    total_unidades = df_categorias['Unidades_Vendidas'].sum() if not df_categorias.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Faturamento Bruto", f"R$ {faturamento_total:,.2f}")
    col2.metric(" Pedidos Realizados", f"{total_pedidos}")
    col3.metric(" Ticket Médio", f"R$ {ticket_medio:,.2f}")
    col4.metric(" Garrafas/Itens Vendidos", f"{total_unidades}")
else:
    st.info(" Nenhuma venda registrada até o momento. Realize vendas no sistema para popular o Dashboard.")

st.markdown("---")

# ==========================================
# 4. GRÁFICOS INTERATIVOS COM PLOTLY
# ==========================================
if not df_vendas.empty:
    
    
    colA, colB = st.columns([2, 1]) 
    
    with colA:
        st.subheader(" Faturamento por Dia")
        if not df_tempo.empty:
            fig_tempo = px.line(
                df_tempo, x='data', y='faturamento', 
                markers=True, 
                line_shape='spline', 
                labels={'data': 'Data da Venda', 'faturamento': 'Valor Arrecadado (R$)'}
            )
            fig_tempo.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig_tempo, use_container_width=True)

    with colB:
        st.subheader(" Categorias Mais Vendidas")
        if not df_categorias.empty:
            fig_cat = px.pie(
                df_categorias, names='Categoria', values='Unidades_Vendidas', hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # LINHA 2 DE GRÁFICOS: Fornecedores e Formas de Pagamento
    colC, colD = st.columns(2)

    with colC:
        st.subheader(" Receita por Fornecedor")
        if not df_fornecedores.empty:
            fig_forn = px.bar(
                df_fornecedores, x='Receita', y='Fornecedor', orientation='h',
                labels={'Receita': 'Receita Gerada (R$)'},
                color='Receita', color_continuous_scale='Blues'
            )
            fig_forn.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_forn, use_container_width=True)

    with colD:
        st.subheader(" Formas de Pagamento")
        vendas_pagamento = df_vendas.groupby('forma_pagamento')['valor_total'].sum().reset_index()
        fig_pag = px.bar(
            vendas_pagamento, x='forma_pagamento', y='valor_total',
            labels={'forma_pagamento': 'Método', 'valor_total': 'Total (R$)'},
            color='forma_pagamento', color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pag, use_container_width=True)

    st.markdown("---")

    # LINHA 3: TABELA DE ESTOQUE VS SAÍDA
    st.subheader(" Top 5 Produtos: Giro de Estoque")
    if not df_produtos_saida.empty:
        st.dataframe(
            df_produtos_saida,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Produto": st.column_config.TextColumn("Nome do Produto"),
                "Vendidos": st.column_config.ProgressColumn("Qtd Vendida", min_value=0, max_value=int(df_produtos_saida['Vendidos'].max()), format="%f"),
                "Estoque_Atual": st.column_config.NumberColumn("Estoque Disponível")
            }
        )