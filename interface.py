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
        cursor.execute(
            """SELECT p.id_produto, p.nome, c.nome, f.nome, p.preco_venda, p.quantidade_estoque, p.nota, p.desconto
               FROM produtos AS p
               INNER JOIN fornecedores AS f
                   ON p.id_fornecedor = f.id_fornecedor
               INNER JOIN categorias AS c
                   ON p.id_categoria = c.id_categoria 
               WHERE p.ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print("--- ESTOQUE ATUAL ---")
        for bebida in resultados:
            id_produto, nome_produto, nome_categoria, nome_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            print(
                f"[{id_produto:^3}] | {nome_produto:<28}(-{tag_promo}) | {nome_categoria:<15} | {nome_fornecedor:<15} | "
                f"{quantidade_estoque:^7} | {nota:^4} | R$ {preco_final:>6.2f}"
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
        │ [10] Adicionar Cliente            [11] Adicionar categoria     │
        └────────────────────────────────────────────────────────────────┘

        ┌── CONSULTAS E RELATÓRIOS ──────────────────────────────────────┐
        │ [12] Busca                        [13] Relatórios Expresso     │
        │ [14] Histórico de Vendas          [15] Catálogo Ordenado       │
        │ [16] Filtro por Preço             [17] Estatísticas e Balanço  │
        └────────────────────────────────────────────────────────────────┘

        ┌── MARKETING E FORNECEDORES ────────────────────────────────────┐
        │ [18] Promoções                    [19] Novo Fornecedor         │
        │ [20] Adicionar Cupom              [21] Cupons Mais Utilizados  │
        │ [22] Ver Dashboard Analytics      [23] Reclame aqui            │
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
        cursor.execute(
            """SELECT p.id_produto, p.nome, c.nome, f.nome, p.preco_venda, p.quantidade_estoque, p.nota, p.desconto
               FROM produtos AS p
               INNER JOIN fornecedores AS f
                   ON p.id_fornecedor = f.id_fornecedor
               INNER JOIN categorias AS c
                   ON p.id_categoria = c.id_categoria 
               WHERE p.ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print("--- ESTOQUE ATUAL ---")
        for bebida in resultados:
            id_produto, nome_produto, nome_categoria, nome_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            print(
                f"[{id_produto}] {nome_produto}{tag_promo} | Categoria: {nome_categoria} | Fornecedor: {nome_fornecedor} | Nota: {nota} | R$ {preco_final:.2f} | Estoque: {quantidade_estoque}"
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
        │ [6] Alterar Nome                  [7] Adicionar Cliente        |
        │ [8] Adicionar categoria                                        |
        └────────────────────────────────────────────────────────────────┘

        ┌── CONSULTAS E RELATÓRIOS ──────────────────────────────────────┐
        │ [9] Busca                        [10] Catálogo Ordenado        │
        │ [11] Filtro por Preço                                          │
        └────────────────────────────────────────────────────────────────┘

        ┌── MARKETING E FORNECEDORES ────────────────────────────────────┐
        │ [12] Novo Fornecedor              [13] Cupons Mais Utilizados  |
        │ [14] Reclame aqui                                              |
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
