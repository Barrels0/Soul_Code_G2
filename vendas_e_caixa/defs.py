from connectsql import obter_conexao, fechar_execusao, enviar_email_relatorio
import mysql.connector, datetime,time
from forces import force_int, force_str
from marketing_fornecedores.marketing import teste_qualidade
from produtos_estoque1.def1 import add_cliente
from colorama import Fore, Style
from interface import barra_carregamento

def exp_nota(id_operador):
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}EXPORTAR NOTA FISCAL{Fore.CYAN}                                              █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    barra_carregamento("Gerando relatório de fechamento")    
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT 
                vendas.id_venda, 
                vendas.data_hora, 
                vendas.id_cliente, 
                vendas.valor_total, 
                vendas.forma_pagamento,
                COALESCE(SUM(produtos.preco_custo * itens_venda.quantidade), 0) AS custo_total,
                GROUP_CONCAT(CONCAT(itens_venda.quantidade, 'x ', produtos.nome) SEPARATOR ', ') AS produtos_vendidos
            FROM vendas
            LEFT JOIN itens_venda ON vendas.id_venda = itens_venda.id_venda
            LEFT JOIN produtos ON itens_venda.id_produto = produtos.id_produto
            GROUP BY vendas.id_venda, vendas.data_hora, vendas.id_cliente, vendas.valor_total, vendas.forma_pagamento
            ORDER BY vendas.id_venda ASC
        """)
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda registrada hoje.")
            return None

        conteudo_relatorio = "=================================\n"
        conteudo_relatorio += "        RELATÓRIO DE VENDAS      \n"
        conteudo_relatorio += "=================================\n\n"

        faturamento_total = 0.0
        custo_total_dia = 0.0
        lucro_total_dia = 0.0

        for venda in vendas:
            id_venda = venda[0]
            data_hora = venda[1]
            id_cliente = venda[2]
            valor_total = float(venda[3])
            pagamento = venda[4]
            custo_da_venda = float(venda[5])
            produtos_vendidos = venda[6]

            lucro_venda = valor_total - custo_da_venda

            faturamento_total += valor_total
            custo_total_dia += custo_da_venda
            lucro_total_dia += lucro_venda

            linha = f"Venda ID: {id_venda} | Data: {data_hora} | Cliente ID: {id_cliente} | Produtos: [{produtos_vendidos}] | Faturado: R${valor_total:.2f} | Custo: R${custo_da_venda:.2f} | Lucro: R${lucro_venda:.2f} | Pagamento: {pagamento}\n"
            
            conteudo_relatorio += linha 

        conteudo_relatorio += "\n=================================\n"
        conteudo_relatorio += f"FATURAMENTO BRUTO: R${faturamento_total:.2f}\n"
        conteudo_relatorio += f"CUSTO DOS PRODUTOS: R${custo_total_dia:.2f}\n"
        conteudo_relatorio += f"LUCRO LÍQUIDO: R${lucro_total_dia:.2f}\n"
        conteudo_relatorio += "=================================\n"

        nome_arquivo = f"fechamento_caixa_{datetime.datetime.now().strftime('%y_%m_%d_%Hh%Mm%Ss')}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_relatorio)

        print(Fore.GREEN + f"\n[✔] SUCESSO! Arquivo '{nome_arquivo}' foi criado na sua pasta!")
        
        email = force_str(Fore.YELLOW + "➤ Você deseja enviar este relatório para o seu e-mail? (Sim/Não): " + Fore.RESET).upper()    
        if email in ["S", "SIM"]:
            assunto = "FECHAMENTO DE CAIXA E LUCRO"
            resposta = conteudo_relatorio
            enviar_email = enviar_email_relatorio(id_operador, resposta, assunto)
            
            if not enviar_email:
                print(Fore.RED + "\n[✖] ERRO: E-mail não enviado. Voltando para o menu!" + Fore.RESET)
                return
            else:
                print(Fore.GREEN + "\n[✔] E-mail enviado com sucesso!" + Fore.RESET)
                return
        else:
            print(Fore.YELLOW + "\n[!] Operação ignorada. Voltando para o menu..." + Fore.RESET)

    except mysql.connector.Error as erro:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {erro}" + Fore.RESET)
        return None
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )


def nota_fiscal():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}NOTA FISCAL{Fore.CYAN}                                                       █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT vendas.data_hora, vendas.id_cliente, vendas.id_usuario, vendas.id_cupom, vendas.valor_total, vendas.forma_pagamento, itens_venda.quantidade, itens_venda.preco_unitario, produtos.nome 
            FROM vendas
            INNER JOIN itens_venda ON vendas.id_venda = itens_venda.id_venda
            INNER JOIN produtos ON itens_venda.id_produto = produtos.id_produto
            ORDER BY data_hora DESC
            LIMIT 10
        """)
        vendas = cursor.fetchall()
        total = 0

        for venda in vendas:
            print(
                Fore.WHITE + f"{venda[0]} | Cliente:{venda[1]} | Usuario:{venda[2]} | Produto:{venda[8]} | Cupom:{venda[3]} | Valor: " + Fore.GREEN + f"R${venda[4]:.2f}" + Fore.WHITE + f" | Pagamento:{venda[5]} | Quantidade:{venda[6]} | Preço Unitário:{venda[7]} |"
            )
            total += venda[4]

        print(Fore.CYAN + "-" * 30)
        print(Fore.GREEN + Style.BRIGHT + f"TOTAL EXIBIDO: R$ {total:.2f}")

    except mysql.connector.Error as erro:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {erro}" + Fore.RESET)
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None,
            cursor if "cursor" in locals() else None,
        )


def registar_venda(id_operador):
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CARRINHO DE COMPRAS{Fore.CYAN}                                               █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    carrinho = []

    conexao = obter_conexao()
    if conexao is None:
        print(Fore.RED + "\n[✖] Sistema offline. Não é possível registrar vendas no momento." + Fore.RESET)
        return
        
    cursor = conexao.cursor()

    try:
        while True:
            try:
                id_produto = force_int(
                    Fore.YELLOW + "\n➤ Digite o [ID] do produto (-1 concluir | -2 cancelar): " + Fore.RESET
                )
            except ValueError:
                print(Fore.RED + "ERRO: O ID deve ser um número inteiro.")
                continue

            if id_produto == -1:
                break
            elif id_produto == -2:
                print(Fore.YELLOW + "\n[!] Compra cancelada pelo operador!" + Fore.RESET)
                return

            cursor.execute(
                """SELECT nome, id_categoria, id_fornecedor, preco_venda, preco_custo, 
                          quantidade_estoque, nota, validade, ativo, desconto, min_atac, desc_atac
                   FROM produtos WHERE id_produto = %s AND ativo = 1""",
                (id_produto,),
            )
            bebida = cursor.fetchone()

            if not bebida:
                print(Fore.RED + "[✖] ERRO: ID INVÁLIDO. Esse produto não existe ou foi desativado.")
                continue

            if bebida[8] == 0:
                print(Fore.RED + "[✖] Produto está atualmente desativado, tente outra opção!")
                continue

            venda_autorizada = teste_qualidade(id_produto)
            if not venda_autorizada:
                print(Fore.RED + "-> Produto rejeitado pelo controle de qualidade. Escolha outro item.")
                continue

            nome_bebida = bebida[0]
            preco_venda = float(bebida[3])
            quantidade_estoque = bebida[5]
            desconto_banco = float(bebida[9]) if bebida[9] else 0.0

            preco_promocional = preco_venda
            if desconto_banco > 0:
                preco_promocional = preco_venda - (preco_venda * (desconto_banco / 100))

            try:
                quantidade = force_int(Fore.YELLOW + f"➤ Quantas unidades de '{nome_bebida}' você deseja? " + Fore.RESET)
            except ValueError:
                print(Fore.RED + "ERRO: Quantidade inválida.")
                continue
                
            if quantidade <= 0:
                print(Fore.RED + "ERRO: A quantidade deve ser maior que zero.")
                continue

            qtd_carrinho = sum(item["quantidade"] for item in carrinho if item["id_produto"] == id_produto)
            estoque_disponivel = quantidade_estoque - qtd_carrinho

            if quantidade > estoque_disponivel:
                print(Fore.RED + f"Estoque insuficiente. Você já tem {qtd_carrinho} no carrinho, o estoque restante é {estoque_disponivel}.")
                continue

            min_atacado = int(bebida[10]) if bebida[10] else 999999
            desconto_atacado = float(bebida[11]) if bebida[11] else 0.0

            if quantidade >= min_atacado:
                print(Fore.GREEN + "Quantidade de atacado atingida!")
                desconto = (preco_venda * (desconto_atacado/100))
                preco_promocional = preco_promocional - desconto 
                print(Fore.GREEN + f"Desconto de atacado aplicado! Novo preço un: R$ {preco_promocional:.2f}")

            carrinho.append({
                "id_produto": id_produto,
                "nome": nome_bebida,
                "quantidade": quantidade,
                "preco": preco_promocional,
                "subtotal_promocional": quantidade * preco_promocional,
            })
            print(Fore.GREEN + f"✔ {quantidade}x '{nome_bebida}' adicionado ao carrinho!")

        if not carrinho:
            return

        id_cliente_final = None
        cursor.execute("SELECT id_cliente, nome, cnpj_cpf FROM clientes WHERE ativo = 1")
        clientes = cursor.fetchall()

        while True:
            if not clientes:
                add_cl = force_str(Fore.YELLOW + "\nNão temos clientes cadastrados. Cadastrar agora? (S/N): " + Fore.RESET).upper()
                if add_cl in ["S", "SIM"]:
                    id_cliente_final = add_cliente()
                    if id_cliente_final: break
                print(Fore.RED + "A compra não pode continuar sem um cliente!")
                return

            else:
                print(Fore.CYAN + Style.BRIGHT + "\n--- CLIENTES CADASTRADOS ---")
                for linha in clientes:
                    print(Fore.WHITE + f"-> ID: {linha[0]} | Nome: {linha[1][:20]} | Doc: {linha[2]}")

                cliente_v = force_int(Fore.YELLOW + "\n➤ O cliente dessa venda é algum destes? [1] Sim | [2] Não: " + Fore.RESET)
                
                if cliente_v == 1:
                    escolha = force_int(Fore.YELLOW + "Digite o [ID] do cliente: " + Fore.RESET)
                    cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = %s AND ativo = 1", (escolha,))
                    result = cursor.fetchone()
                    if result:
                        id_cliente_final = result[0]
                        break
                    else:
                        print(Fore.RED + "[✖] ID inválido! Tente novamente.")
                
                elif cliente_v == 2:
                    add_cl = force_str(Fore.YELLOW + "Você precisa adicionar o cliente. Cadastrar agora? (S/N): " + Fore.RESET).upper()
                    if add_cl in ["S", "SIM"]:
                        id_cliente_final = add_cliente()
                        if id_cliente_final: 
                            break
                    print(Fore.RED + "A compra não pode continuar sem um cliente!")
                    return
                else:
                    print(Fore.RED + "[✖] Opção inválida.")


        total_compra = sum(item["subtotal_promocional"] for item in carrinho)

        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}FECHAMENTO DE CAIXA{Fore.CYAN}                                               █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
        print(Fore.WHITE + f"Total a pagar: " + Fore.GREEN + f"R$ {total_compra:.2f}")
        
        confirmar = force_str(Fore.YELLOW + "Confirmar pagamento e registrar venda? (S/N): " + Fore.RESET).upper()
        if confirmar not in ["S", "SIM"]:
            print(Fore.YELLOW + "\n[!] Venda cancelada pelo operador. Carrinho esvaziado.")
            return

        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}SELECIONE O MÉTODO DE PAGAMENTO{Fore.CYAN}                                   █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 {Fore.WHITE}[1]{Fore.CYAN} PIX            {Fore.WHITE}[2]{Fore.CYAN} Boleto
 {Fore.WHITE}[3]{Fore.CYAN} Transferência  {Fore.WHITE}[4]{Fore.CYAN} Cartão de Crédito
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")
        
        while True:
            pagamento_opcao = force_str(Fore.YELLOW + "➤ Escolha o método (1-4): " + Fore.RESET)
            mapa_pagamentos = {"1": "PIX", "2": "Boleto", "3": "Transferência", "4": "Cartão de Crédito"}
            forma_pagamento = mapa_pagamentos.get(pagamento_opcao)

            if forma_pagamento:
                break
            print(Fore.RED + "[✖] ERRO: Método inválido. Digite um número de 1 a 4.")

        id_cupom_bd = None
        cupom = force_str(Fore.YELLOW + "\n➤ Você possui algum cupom de desconto? (S/N): " + Fore.RESET).upper()

        if cupom in ["S", "SIM"]:
            nm_cup = force_str(Fore.YELLOW + "Digite o nome do seu cupom: " + Fore.RESET).upper()
            cursor.execute("SELECT id_cupom, desconto, quantidade FROM cupons WHERE nome = %s AND ativo = 1", (nm_cup,))
            result = cursor.fetchone()

            if not result or result[2] == 0:
                print(Fore.RED + "\n[✖] Cupom inválido ou esgotado! A compra seguirá com o preço normal." + Fore.RESET)
            else:
                id_cupom_bd = result[0]
                total_compra *= 1 - (float(result[1]) / 100)
                print(Fore.GREEN + f"\n[✔] Cupom aplicado com sucesso! Novo total: R$ {total_compra:.2f}" + Fore.RESET)
                
                cursor.execute(
                    "UPDATE cupons SET quantidade = quantidade - 1, qtd_used = qtd_used + 1 WHERE id_cupom = %s AND ativo = 1",
                    (id_cupom_bd,),
                )

        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """INSERT INTO vendas (data_hora, id_cliente, id_usuario, id_cupom, valor_total, forma_pagamento)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (data_hora, id_cliente_final, id_operador, id_cupom_bd, total_compra, forma_pagamento),
        )
        id_venda_gerada = cursor.lastrowid

        for item in carrinho:
            cursor.execute(
                "UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s WHERE id_produto = %s",
                (item["quantidade"], item["id_produto"]),
            )
            cursor.execute(
                """INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                   VALUES (%s, %s, %s, %s)""",
                (id_venda_gerada, item["id_produto"], item["quantidade"], item["preco"]),
            )

        conexao.commit()
        print(Fore.GREEN + Style.BRIGHT + f"\n[✔] SUCESSO! Venda #{id_venda_gerada} registrada e estoque atualizado." + Fore.RESET)

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO CRÍTICO: Falha na transação do banco de dados: {erro}" + Fore.RESET)
        
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None,
            cursor if "cursor" in locals() else None,
        )