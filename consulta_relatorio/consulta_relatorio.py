import mysql.connector
import datetime
import pandas as pd
from connectsql import obter_conexao
from forces import force_int, force_float, force_str, bsc_id
from consulta_relatorio.exportacoes import perguntar_exportacao
from colorama import Fore, Style

def relatorio_expresso():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}RELATÓRIO EXPRESSO: ESTOQUE CRÍTICO{Fore.CYAN}                                          █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

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
            print(Fore.GREEN + "Estoque seguro! Nenhuma bebida com menos de 5 unidades." + Fore.RESET)
        else:
            print(Fore.YELLOW + "\nATENÇÃO! Produtos precisando de reposição urgente:\n" + Fore.RESET)
            print(df_critico.to_string(index=False))
            perguntar_exportacao(df_critico, nome_padrao="relatorio_estoque_critico")

    except Exception as erro:
        print(Fore.RED + f"Erro inesperado ao gerar o relatório expresso: {erro}" + Fore.RESET)

    finally:
        if "conexao" in locals() and conexao.is_connected():
            conexao.close()




def busca():
    while True: 
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}BUSCA AVANÇADA{Fore.CYAN}                                                      █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Buscar por nome
 {Fore.WHITE}[2]{Fore.CYAN} Buscar por categoria
 {Fore.WHITE}[3]{Fore.CYAN} Buscar por fornecedor
 {Fore.WHITE}[0]{Fore.CYAN} Sair
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")

        try:
            opcao = force_int(Fore.YELLOW + "➤ Digite o número da busca: " + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Digite apenas números" + Fore.RESET)
            continue

        if opcao == 0:
            print("Voltando ao menu...")
            break
            
        if opcao not in [1, 2, 3]:
            print(Fore.RED + "Opção inválida. Tente novamente." + Fore.RESET)
            continue

        conexao = obter_conexao()
        if conexao is None:
            print(Fore.RED + "Erro ao conectar ao banco." + Fore.RESET)
            return
            
        cursor = conexao.cursor()
        resultados = []

        try:
            if opcao == 1:
                nome = force_str(Fore.YELLOW + "➤ Digite o nome da bebida: " + Fore.RESET).lower()
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
                """, (f"%{nome}%",))
                resultados = cursor.fetchall()

            elif opcao == 2:
                cursor.execute("SELECT id_categoria, nome FROM categorias WHERE ativo = 1")
                categorias = cursor.fetchall()
                    
                for i in categorias:
                    print(Fore.WHITE + f"[{i[0]}] - {i[1]}" + Fore.RESET)
                try:
                    categoria = force_int(Fore.YELLOW + "➤ Digite o número da categoria correspondente (ou [0] para sair): " + Fore.RESET)
                except ValueError:
                    print("Digite apenas números")
                    continue
                if categoria == 0:
                    print("Voltando ao menu")
                    break
                        
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
                    WHERE categorias.id_categoria = %s
                    AND produtos.ativo = 1
                """, (categoria,))
                resultados = cursor.fetchall()

            elif opcao == 3:
                cursor.execute("SELECT id_fornecedor, nome FROM fornecedores WHERE ativo = 1")
                fornecedores = cursor.fetchall()
                    
                for i in fornecedores:
                    print(Fore.WHITE + f"[{i[0]}] - {i[1]}" + Fore.RESET)
                try:
                    fornecedor = force_int(Fore.YELLOW + "➤ Digite o número do fornecedor correspondente (ou [0] para sair): " + Fore.RESET)
                except ValueError:
                    print("Digite apenas números")
                    continue
                if categoria == 0:
                    print("Voltando ao menu")
                    break
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
                    WHERE fornecedores.id_fornecedor = %s
                    AND produtos.ativo = 1
                """, (fornecedor,))
                resultados = cursor.fetchall()

            if len(resultados) == 0:
                print(Fore.YELLOW + "\nNenhuma bebida encontrada." + Fore.RESET)
            else:
                print(Fore.GREEN + "\n--- RESULTADOS ---\n" + Fore.RESET)
                for bebida in resultados:
                    print(
                        f"{bebida[0]} | {bebida[1]} | {bebida[2]} | {Fore.GREEN}R$ {bebida[3]:.2f}{Fore.RESET} | Estoque: {bebida[4]}"
                    )

        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            
        except Exception as i:
            print(Fore.RED + f"Erro inesperado: {i}" + Fore.RESET)

        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def filtros():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}FILTROS DE CONSULTA{Fore.CYAN}                                                █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Filtrar por Faixa de Preço
 {Fore.WHITE}[2]{Fore.CYAN} Filtrar por Categoria
 {Fore.WHITE}[3]{Fore.CYAN} Filtrar por Categoria + Faixa de Preço
 {Fore.WHITE}[0]{Fore.CYAN} Sair
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")

        try:
            opcao = force_int(Fore.YELLOW + "➤ Escolha uma opção: " + Fore.RESET)
            conexao = obter_conexao()

            if conexao is None:
                print(Fore.RED + "Erro ao conectar ao banco." + Fore.RESET)
                return

            cursor = conexao.cursor()

            try:
                if opcao == 0:
                    print("Saindo dos filtros e voltando ao menu principal...")
                    break # Encerra o laço While True

                elif opcao == 1:
                    try:
                        preco_minimo = force_float("➤ Preço mínimo: R$ ")
                        preco_maximo = force_float("➤ Preço máximo: R$ ")
                        confirm = force_int(Fore.YELLOW + "➤ Para buscar digite [1] ou [0] para cancelar: " + Fore.RESET)
                    except ValueError:
                        print(Fore.RED + "Digite apenas números!" + Fore.RESET)
                        continue # Volta pro topo do laço
                        
                    if confirm == 0:
                        print("Filtro cancelado. Voltando ao menu...")
                        continue

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
                    cursor.execute("SELECT id_categoria, nome FROM categorias WHERE ativo = 1")
                    categorias = cursor.fetchall()
                    
                    for i in categorias:
                        print(Fore.WHITE + f"[{i[0]}] - {i[1]}" + Fore.RESET)
                        
                    try:   
                        categoria_id = force_int(Fore.YELLOW + "➤ Digite o [ID] da categoria (ou [0] para cancelar): " + Fore.RESET)
                    except ValueError:
                        print(Fore.RED + "Digite apenas números!" + Fore.RESET)
                        continue

                    if categoria_id == 0:
                        print("Filtro cancelado. Voltando ao menu...")
                        continue
                    else:
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
                            WHERE categorias.id_categoria = %s
                            AND produtos.ativo = 1
                        """, (categoria_id,))

                elif opcao == 3:
                    cursor.execute("SELECT id_categoria, nome FROM categorias WHERE ativo = 1")
                    categorias = cursor.fetchall()
                    
                    for i in categorias:
                        print(Fore.WHITE + f"[{i[0]}] - {i[1]}" + Fore.RESET)
                        
                    try:
                        categoria_id = force_int(Fore.YELLOW + "➤ Digite o [ID] da categoria (ou [0] para cancelar): " + Fore.RESET)
                        if categoria_id == 0:
                            print(Fore.YELLOW + "\n[!] Filtro cancelado. Voltando..." + Fore.RESET)
                            continue
                            
                        preco_minimo = force_float("➤ Preço mínimo: R$ ")
                        preco_maximo = force_float("➤ Preço máximo: R$ ")
                    except ValueError:
                        print(Fore.RED + "Digite apenas números!" + Fore.RESET)
                        continue

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
                        WHERE categorias.id_categoria = %s
                        AND produtos.preco_venda >= %s
                        AND produtos.preco_venda <= %s
                        AND produtos.ativo = 1
                    """, (categoria_id, preco_minimo, preco_maximo))

                else:
                    print(Fore.RED + "Opção inválida. Tente novamente." + Fore.RESET)
                    continue

                bebidas = cursor.fetchall()

                if len(bebidas) == 0:
                    print(Fore.YELLOW + "\nNenhuma bebida encontrada com esses filtros." + Fore.RESET)
                else:
                    print(Fore.GREEN + "\n--- RESULTADOS ---\n" + Fore.RESET)
                    for bebida in bebidas:
                        preco_venda = bebida[2]
                        desconto = bebida[4]
                        
                        preco_final = float(preco_venda)
                        tag_promo = ""
                        
                        if desconto and float(desconto) > 0:
                            preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                            tag_promo = f" (-{desconto}%) | PROMO: {Fore.GREEN}R$ {preco_final:.2f}{Fore.RESET}"
                        
                        print(
                            f"{bebida[0]} | {bebida[1]} | {Fore.GREEN}R$ {bebida[2]:.2f}{Fore.RESET}{tag_promo} | Estoque: {bebida[3]}"
                        )

            except mysql.connector.Error as e:
                print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)

            finally:
                if 'conexao' in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
                
        except Exception as i:
            print(Fore.RED + f"Erro inesperado: {i}" + Fore.RESET)

def painel_estatisticas():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}PAINEL DE ESTATÍSTICAS E PRODUTOS MAIS VENDIDOS{Fore.CYAN}                                          █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM vendas")
        if cursor.fetchone()[0] == 0:
            print(Fore.YELLOW + "-> Sem dados disponíveis para gerar o balanço hoje!" + Fore.RESET)
            return

        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f"Histórico de Faturação Bruta : {Fore.GREEN}R$ {faturamento:.2f}{Fore.RESET}")

        cursor.execute("SELECT AVG(valor_total) FROM vendas")
        ticket_medio = cursor.fetchone()[0]
        print(f"Ticket Médio por venda       : {Fore.GREEN}R$ {ticket_medio:.2f}{Fore.RESET}")

        print(Fore.CYAN + "\nTOP 3 BEBIDAS MAIS VENDIDAS:" + Fore.RESET)
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

        print(Fore.CYAN + "="*55 + Fore.RESET)

    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def catalogo_ordenado():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}ORDENAÇÃO DO CATÁLOGO{Fore.CYAN}                                              █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Ordenar por Nome
 {Fore.WHITE}[2]{Fore.CYAN} Ordenar por Maior Preço
 {Fore.WHITE}[3]{Fore.CYAN} Ordenar por Menor Preço
 {Fore.WHITE}[4]{Fore.CYAN} Ordenar por Maior Estoque
 {Fore.WHITE}[5]{Fore.CYAN} Ordenar por Menor Estoque
 {Fore.WHITE}[0]{Fore.CYAN} Sair
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")
        
        query_base = """
                SELECT nome, preco_venda, nota, quantidade_estoque, desconto
                FROM produtos
                WHERE ativo = 1
            """
        
        try:
            escolha = force_int(Fore.YELLOW + "➤ Escolha o tipo de ordenação: " + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Digite apenas números na sua escolha" + Fore.RESET)
            continue
            
        if escolha == 0:
            print(Fore.YELLOW + "Voltando ao menu" + Fore.RESET)
            break

        if escolha == 1:
            query = f"{query_base} ORDER BY LOWER(nome) ASC"
        elif escolha == 2:
            query = f"{query_base} ORDER BY preco_venda DESC"
        elif escolha == 3:  
            query = f"{query_base} ORDER BY preco_venda ASC"
        elif escolha == 4:
            query = f"{query_base} ORDER BY quantidade_estoque DESC"
        elif escolha == 5:
            query = f"{query_base} ORDER BY quantidade_estoque ASC"        
        else:
            print(Fore.RED + "Opção inválida" + Fore.RESET)
            continue
        
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query)
            bebidas = cursor.fetchall()

            if not bebidas:
                print(Fore.YELLOW + "\n Nenhum produto encontrado" + Fore.RESET)
            else:
                print(Fore.CYAN + "\n" + "="*60 + Fore.RESET)
                
                for bebida in bebidas:
                    nome, preco_venda, nota, quantidade_estoque, desconto = bebida
                    
                    preco_final = float(preco_venda)
                    tag_promo = ""
                    
                    if desconto and float(desconto) > 0:
                        preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                        tag_promo = f" (-{desconto}%) | PREÇO PROMO: {Fore.GREEN}R${preco_final:.2f}{Fore.RESET}"
                    
                    print(f"= {nome} | Base: {Fore.GREEN}R${float(preco_venda):.2f}{Fore.RESET}{tag_promo} | Nota:{nota} | Quantidade:{quantidade_estoque}")
                
                print(Fore.CYAN + "="*60 + Fore.RESET)
                
        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
    
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def historico_vendas():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}HISTÓRICO DE VENDAS{Fore.CYAN}                                          █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            SELECT id_venda, data_hora, id_cliente, valor_total, forma_pagamento
            FROM vendas
            ORDER BY data_hora DESC
        """)
        vendas = cursor.fetchall()
        
        if not vendas:
            print(Fore.YELLOW + "Nenhuma venda registrada no sistema." + Fore.RESET)
            print("="*60)
            return

        for venda in vendas:
            id_venda, data_hora, id_cliente, valor_total, forma_pagamento = venda
            
            print(Fore.CYAN + f"\nVENDA #{id_venda}")
            print("="*60)
            print(f"ID Cliente: {id_cliente}")
            print(f"Data      : {data_hora}")
            print(f"Pagamento : {forma_pagamento}")
            print("-" * 60)
            print("ITENS")
            print("-" * 60 + Fore.RESET)
            
            cursor.execute("""
                SELECT produtos.nome, itens_venda.quantidade, itens_venda.preco_unitario
                FROM itens_venda
                INNER JOIN produtos ON itens_venda.id_produto = produtos.id_produto
                WHERE itens_venda.id_venda = %s
            """, (id_venda,))
            
            itens = cursor.fetchall()
            
            for item in itens:
                nome_produto, quantidade, preco_unitario = item
                subtotal_item = quantidade * preco_unitario
                
                print(f"{quantidade:>2}X  {nome_produto:<35} {Fore.GREEN}R$ {subtotal_item:>16.2f}{Fore.RESET}")
                print("-" * 60)
            
            print(f"{'TOTAL DA VENDA':<40} {Fore.GREEN}R$ {valor_total:>16.2f}{Fore.RESET}")            
            print(Fore.CYAN + "=" * 60 + Fore.RESET)

    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()