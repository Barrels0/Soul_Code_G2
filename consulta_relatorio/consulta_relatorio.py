from connectsql import obter_conexao
import datetime
import mysql.connector
from forces import force_int,force_float,force_str
from consulta_relatorio.exportacoes import perguntar_exportacao
import pandas as pd

def relatorio_expresso():
    print("\n" + "="*40)
    print(" RELATÓRIO EXPRESSO: ESTOQUE CRÍTICO ")
    print("="*40)

    try:
        conexao = obter_conexao()
        
        if not conexao:
            return

        
        query = """
            SELECT id_produto AS 'ID', 
                   nome AS 'Produto', 
                   quantidade_estoque AS 'Estoque Atual'
            FROM produtos
            WHERE quantidade_estoque < 5 AND ativo = 1
            ORDER BY quantidade_estoque ASC
        """

        
        df_critico = pd.read_sql(query, conexao)

        if df_critico.empty:
            print("Estoque seguro! Nenhuma bebida com menos de 5 unidades.")
        else:
            print("\nATENÇÃO! Produtos precisando de reposição urgente:\n")
            
            
            print(df_critico.to_string(index=False))
            
            
            perguntar_exportacao(df_critico, nome_padrao="relatorio_estoque_critico")

    except Exception as erro:
        print(f"Erro inesperado ao gerar o relatório expresso: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            conexao.close()




def busca():

    print("\n--- BUSCA AVANÇADA ---")

    print("""
    [1] Buscar por nome
    [2] Buscar por categoria
    [3] Buscar por fornecedor
    """)

    try:
        opcao = force_int(
            "Digite o número da busca: "
        )

        conexao = obter_conexao()
        cursor = conexao.cursor()

        try:

            if opcao == 1:

                nome = force_str(
                    "Digite o nome da bebida: "
                ).lower()

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        fornecedores.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque
                    FROM produtos
                    INNER JOIN fornecedores
                        ON produtos.id_fornecedor = fornecedores.id_fornecedor
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE LOWER(produtos.nome) LIKE %s
                    AND produtos.ativo = 1
                """, (

                    f"%{nome}%",

                ))

            elif opcao == 2:

                categoria = force_str(
                    "Digite a categoria (exemplo: Cervejas, Refrigerantes, etc...): "
                ).lower()

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        fornecedores.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque
                    FROM produtos
                    INNER JOIN fornecedores
                        ON produtos.id_fornecedor = fornecedores.id_fornecedor
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE LOWER(categorias.nome) LIKE %s
                    AND produtos.ativo = 1
                """, (

                    f"%{categoria}%",

                ))

            elif opcao == 3:

                fornecedor = force_str(
                    "Digite o fornecedor: "
                ).lower()

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        fornecedores.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque
                    FROM produtos
                    INNER JOIN fornecedores
                        ON produtos.id_fornecedor = fornecedores.id_fornecedor
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE LOWER(fornecedores.nome) LIKE %s
                    AND produtos.ativo = 1
                """, (

                    f"%{fornecedor}%",

                ))

            else:

                print("Opção inválida.")
                return

            resultados = cursor.fetchall()

            if len(resultados) == 0:

                print("\nNenhuma bebida encontrada.")

            else:

                print("\nRESULTADOS:\n")

                for bebida in resultados:

                    print(
                        f"{bebida[0]} | "
                        f"{bebida[1]} | "
                        f"{bebida[2]} | "
                        f"R$ {bebida[3]:.2f} | "
                        f"Estoque: {bebida[4]}"
                    )

        except mysql.connector.Error as e:

            print(
                f"Erro ao realizar a busca: {e}"
            )

        finally:

            if "conexao" in locals() and conexao.is_connected():

                cursor.close()
                conexao.close()

    except Exception as i :
        print(f"Erro inesperado... {i}")



def filtros():
    print("\n--- FILTROS ---")
    print("""
    [1] Faixa de preço
    [2] Categoria
    [3] Categoria + faixa de preço
    """)

    try:
        opcao = force_int("Escolha: ")
        conexao = obter_conexao()

        if conexao is None:
            print("Erro ao conectar ao banco.")
            return

        cursor = conexao.cursor()

        try:
            if opcao == 1:
                preco_minimo = force_float("Preço mínimo: R$ ")
                preco_maximo = force_float("Preço máximo: R$ ")

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque,
                        produtos.desconto
                    FROM produtos
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE produtos.preco_venda >= %s
                    AND produtos.preco_venda <= %s
                    AND produtos.ativo = 1
                """, (preco_minimo, preco_maximo))

            elif opcao == 2:
                categoria = force_str("Digite a categoria: ").lower()

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque,
                        produtos.desconto
                    FROM produtos
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE LOWER(categorias.nome) LIKE %s
                    AND produtos.ativo = 1
                """, (f"%{categoria}%",))

            elif opcao == 3:
                categoria = force_str("Digite a categoria: ").lower()
                preco_minimo = force_float("Preço mínimo: R$ ")
                preco_maximo = force_float("Preço máximo: R$ ")

                cursor.execute("""
                    SELECT
                        produtos.nome,
                        categorias.nome,
                        produtos.preco_venda,
                        produtos.quantidade_estoque,
                        produtos.desconto
                    FROM produtos
                    INNER JOIN categorias
                        ON produtos.id_categoria = categorias.id_categoria
                    WHERE LOWER(categorias.nome) LIKE %s
                    AND produtos.preco_venda >= %s
                    AND produtos.preco_venda <= %s
                    AND produtos.ativo = 1
                """, (f"%{categoria}%", preco_minimo, preco_maximo))

            else:
                print("Opção inválida.")
                return

            bebidas = cursor.fetchall()

            if len(bebidas) == 0:
                print("\nNenhuma bebida encontrada.")
            else:
                print("\nRESULTADOS:\n")

                for bebida in bebidas:
                    preco_venda = bebida[2]
                    desconto = bebida[4]
                    
                    preco_final = float(preco_venda)
                    tag_promo = ""
                    
                    if desconto and float(desconto) > 0:
                        preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                        tag_promo = f" (-{desconto}%) | PROMO: R$ {preco_final:.2f}"

                    print(
                        f"{bebida[0]} | "
                        f"{bebida[1]} | "
                        f"R$ {bebida[2]:.2f}{tag_promo} | "
                        f"Estoque: {bebida[3]}"
                    )

        except mysql.connector.Error as e:
            print(f"Erro no banco: {e}")

        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
                
    except Exception as i:
        print(f"Erro inesperado... {i}")

def painel_estatisticas():
    print("\n" + "="*55)
    print("    PAINEL DE ESTATÍSTICAS E PRODUTOS MAIS VENDIDOS    ")
    print("="*55)
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM vendas")
        if cursor.fetchone()[0] == 0:
            print("-> Sem dados disponíveis para gerar o balanço hoje!")
            return

        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f"Histórico de Faturação Bruta : R$ {faturamento:.2f}")

        cursor.execute("SELECT AVG(valor_total) FROM vendas")
        ticket_medio = cursor.fetchone()[0]
        print(f"Ticket Médio por venda       : R$ {ticket_medio:.2f}")

        print("\nTOP 3 BEBIDAS MAIS VENDIDAS:")
        cursor.execute("""
            SELECT produtos.nome, SUM(itens_venda.quantidade) AS total_vendido
            FROM itens_venda
            INNER JOIN produtos ON itens_venda.id_produto = produtos.id_produto
            GROUP BY produtos.id_produto, produtos.nome
            ORDER BY total_vendido DESC
            LIMIT 3
        """)
        
        produtos_campeoes = cursor.fetchall()
        
        for i, (nome_produto, quantidade) in enumerate(produtos_campeoes, 1):
            print(f"   {i}º Lugar: {nome_produto} — {quantidade} unidades vendidas")

        cursor.execute("""
            SELECT forma_pagamento, COUNT(*) as quantidade_usos
            FROM vendas
            GROUP BY forma_pagamento
            ORDER BY quantidade_usos DESC
            LIMIT 1
        """)
        pagamento_fav = cursor.fetchone()
        if pagamento_fav:
            print(f"\nMétodo de Pagamento Favorito : {pagamento_fav[0]} ({pagamento_fav[1]} operações)")

        print("="*55)

    except mysql.connector.Error as e:
        print(f"\nOcorreu um erro ao gerar as estatísticas: {e}")
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()




def catalogo_ordenado():
    print("\n--- CATÁLOGO ORDENADO ---")
    while True:
        print("""
    [1] Nome
            
    [2] Maior preço          
            
    [3] Menor preço         
            
    [4] Maior estoque          
            
    [5] Menor estoque

    [0] Sair          
            """)
        
        # Puxa os dados base do banco (incluindo a coluna de desconto)
        query = """
                SELECT nome, preco_venda, nota, quantidade_estoque, desconto
                FROM produtos
                WHERE ativo = 1
            """
        
        try:
            escolha = force_int("\nEscolha: ")
        except ValueError:
            print("Digite apenas números na sua escolha")
            continue
            
        if escolha == 0:
            print("Voltando ao menu")
            break

        # Monta o resto da query de acordo com o filtro escolhido
        elif escolha == 1:
            query = f"{query} ORDER BY LOWER(nome) ASC"
        elif escolha == 2:
            query = f"{query} ORDER BY preco_venda DESC"
        elif escolha == 3:  
            query = f"{query} ORDER BY preco_venda ASC"
        elif escolha == 4:
            query = f"{query} ORDER BY quantidade_estoque DESC"
        elif escolha == 5:
            query = f"{query} ORDER BY quantidade_estoque ASC"         
        else:
            print("Opção inválida")
            continue
        
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query)
            bebidas = cursor.fetchall()

            # Checa se a busca retornou vazia
            if not bebidas:
                print("\n Nenhum produto encontrado")
            else:
                print("\n" + "="*60)
                
                # Roda a lista de produtos formatando os valores
                for bebida in bebidas:
                    # Desempacota os dados na mesma ordem do SELECT lá de cima
                    nome = bebida[0]
                    preco_venda = bebida[1]
                    nota = bebida[2]
                    quantidade_estoque = bebida[3]
                    desconto = bebida[4]
                    
                    # Aplica a lógica de desconto se o produto tiver um cadastrado
                    preco_final = float(preco_venda)
                    tag_promo = ""
                    
                    if desconto and float(desconto) > 0:
                        preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                        tag_promo = f" (-{desconto}%) | PREÇO PROMO: R${preco_final:.2f}"
                    
                    # Printa o item formatado
                    print(f"= {nome} | Base: R${float(preco_venda):.2f}{tag_promo} | Nota:{nota} | Quantidade:{quantidade_estoque}")
                
                print("="*60)
                
        except mysql.connector.Error as erro:
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
        
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()




def historico_vendas():
    print("\n" + "="*60)
    print("HISTÓRICO DE VENDAS".center(60))
    print("="*60)
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # 1. Busca todas as vendas organizadas da mais recente para a mais antiga
        cursor.execute("""
            SELECT id_venda, data_hora, id_cliente, valor_total, forma_pagamento
            FROM vendas
            ORDER BY data_hora DESC
        """)
        vendas = cursor.fetchall()
        
        if not vendas:
            print("Nenhuma venda registrada no sistema.")
            print("="*60)
            return

        # 2. Percorre cada venda para exibir o cabeçalho e buscar os itens
        for venda in vendas:
            id_venda = venda[0]
            data_hora = venda[1]
            id_cliente = venda[2]
            valor_total = venda[3]
            forma_pagamento = venda[4]
            
            # Formata a exibição principal da venda
            print(f"\nVENDA #{id_venda}")
            print("="*60)
            print(f"ID Cliente: {id_cliente}")
            print(f"Data      : {data_hora}")
            print(f"Pagamento : {forma_pagamento}")
            print("-"*60)
            print("ITENS")
            print("-"*60)
            
            # 3. Busca os detalhes dessa venda específica na tabela itens_venda
            cursor.execute("""
                SELECT produtos.nome, itens_venda.quantidade, itens_venda.preco_unitario
                FROM itens_venda
                INNER JOIN produtos ON itens_venda.id_produto = produtos.id_produto
                WHERE itens_venda.id_venda = %s
            """, (id_venda,))
            
            itens = cursor.fetchall()
            
            # 4. Imprime cada produto atrelado àquela venda
            for item in itens:
                nome_produto = item[0]
                quantidade = item[1]
                preco_unitario = item[2]
                subtotal_item = quantidade * preco_unitario
                
                print(f"{quantidade:>2}X  {nome_produto:<35} R$ {subtotal_item:>16.2f}")
                print("-"*60)
                print(f"{'TOTAL DA VENDA':<40} R$ {valor_total:>16.2f}")            
            print("=" * 60) # Linha separadora entre uma venda e outra

    except mysql.connector.Error as e:
        print(f"\nOcorreu um erro ao buscar o histórico: {e}")
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()