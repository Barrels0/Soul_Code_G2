from connectsql import obter_conexao, fechar_execusao
import mysql.connector
import os
from time import sleep

def menu_adm(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Administrador
    """
    print(f"""
    ========================================================
                        DISTRIBUIDORA G2
               Caixa Acumulado: R${caixa_atual:.2f}
    ========================================================
    """)
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # Buscamos a coluna desconto junto com os dados do produto
        cursor.execute(
            """SELECT id_produto, nome, id_categoria, id_fornecedor, preco_venda, quantidade_estoque, nota, desconto 
               FROM produtos 
               WHERE ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print("--- ESTOQUE ATUAL (PRODUTOS ATIVOS) ---")
        for bebida in resultados:
            id_produto, nome, id_categoria, id_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            print(
                f"[{id_produto}] {nome}{tag_promo} | Tipo: {id_categoria} | Fornecedor: {id_fornecedor} | Nota: {nota} | R$ {preco_final:.2f} | Estoque: {quantidade_estoque}"
            )
            
    except mysql.connector.Error as e:
        print(f"Erro ao listar produtos no menu: {e}")
    finally:
        fechar_execusao(conexao, cursor)

    print("""
        ===================================================================
                            ══ MENU DO ADMINISTRADOR ══
        ===================================================================

        ┌── VENDAS E CAIXA ──────────────────────────────────────────────┐
        │ [1] Registrar Venda               [2] Nota Fiscal (Sessão)     │
        │ [3] Exportar Notinha                                           │
        └────────────────────────────────────────────────────────────────┘

        ┌── PRODUTOS E ESTOQUE ──────────────────────────────────────────┐
        │ [4] Cadastrar Nova Bebida         [5] Repor Estoque            │
        │ [6] Alterar Preço                 [7] Alterar Nome             │
        │ [8] Desativar Bebida              [9] Reativar Bebida          │
        │ [10] Adicionar Cliente                                         │
        └────────────────────────────────────────────────────────────────┘

        ┌── CONSULTAS E RELATÓRIOS ──────────────────────────────────────┐
        │ [11] Buscar por Nome              [12] Relatórios Expresso     │
        │ [13] Histórico de Vendas          [14] Catálogo Ordenado       │
        │ [15] Filtro por Preço             [16] Estatísticas e Balanço  │
        └────────────────────────────────────────────────────────────────┘

        ┌── MARKETING E FORNECEDORES ────────────────────────────────────┐
        │ [17] Promoções                    [18] Novo Fornecedor         │
        │ [19] Adicionar Cupom              [20] Cupons Mais Utilizados  │
        │ [21] Ver Dashboard Analytics      [22] Reclame aqui            │
        └────────────────────────────────────────────────────────────────┘

        ┌────────────────────────────────────────────────────────────────┐
        │ [0] Sair do Sistema                                            │
        └────────────────────────────────────────────────────────────────┘
        ===================================================================
    """)


def menu_funca(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Funcionário
    """
    print(f"""
    ========================================================
                        DISTRIBUIDORA G2
               Caixa Acumulado: R${caixa_atual:.2f}
    ========================================================
    """)
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # Funcionário também visualiza o preço calculado com o desconto
        cursor.execute(
            """SELECT id_produto, nome, id_categoria, id_fornecedor, preco_venda, quantidade_estoque, nota, desconto 
               FROM produtos 
               WHERE ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print("--- ESTOQUE ATUAL ---")
        for bebida in resultados:
            id_produto, nome, id_categoria, id_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            print(
                f"[{id_produto}] {nome}{tag_promo} | Tipo: {id_categoria} | Fornecedor: {id_fornecedor} | Nota: {nota} | R$ {preco_final:.2f} | Estoque: {quantidade_estoque}"
            )
            
    except mysql.connector.Error as e:
        print(f"Erro ao listar produtos no menu: {e}")
    finally:
        fechar_execusao(conexao, cursor)

    print("""
        ===================================================================
                             ══ MENU DO FUNCIONÁRIO ══
        ===================================================================

        ┌── VENDAS E CAIXA ──────────────────────────────────────────────┐
        │ [1] Registrar Venda               [2] Nota Fiscal (Sessão)     │
        │ [3] Exportar Notinha                                           │
        └────────────────────────────────────────────────────────────────┘

        ┌── PRODUTOS E ESTOQUE ──────────────────────────────────────────┐
        │ [4] Cadastrar Nova Bebida         [5] Repor Estoque            │
        │ [6] Alterar Nome                  [7] Adicionar Cliente        │
        └────────────────────────────────────────────────────────────────┘

        ┌── CONSULTAS E RELATÓRIOS ──────────────────────────────────────┐
        │ [8] Buscar por Nome              [9] Catálogo Ordenado         │
        │ [10] Filtro por Preço                                          │
        └────────────────────────────────────────────────────────────────┘

        ┌── MARKETING E FORNECEDORES ────────────────────────────────────┐
        │ [11] Novo Fornecedor              [12] Cupons Mais Utilizados  |
        │ [13] Reclame aqui                                              |
        └────────────────────────────────────────────────────────────────┘

        ┌────────────────────────────────────────────────────────────────┐
        │ [0] Sair do Sistema                                            │
        └────────────────────────────────────────────────────────────────┘
        ===================================================================
    """)

def delay(s=0.5):
  sleep(s)

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
    delay()

def pausar():
    print("Pressione [ENTER] para continuar")
    input()
    delay()
