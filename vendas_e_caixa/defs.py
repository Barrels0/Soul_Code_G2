from connectsql import obter_conexao, fechar_execusao,enviar_email_relatorio
import mysql.connector, datetime
from forces import force_int, force_str
from marketing_fornecedores.marketing import teste_qualidade
from produtos_estoque1.def1 import add_cliente

def exp_nota(id_operador):
    print("\nGerando relatório de fechamento...")
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT id_venda, data_hora, id_cliente, valor_total, forma_pagamento
            FROM vendas
            ORDER BY id_venda ASC
        """)
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda registrada hoje.")
            return None

        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento_total = cursor.fetchone()[0]
        conteudo_relatorio = "=================================\n"
        conteudo_relatorio += "        RELATÓRIO DE VENDAS      \n"
        conteudo_relatorio += "=================================\n\n"

        for venda in vendas:
            id_venda = venda[0]
            data_hora = venda[1]
            id_cliente = venda[2]
            valor_total = venda[3]
            pagamento = venda[4]

            linha = f"Venda ID: {id_venda} | Data: {data_hora} | Cliente ID: {id_cliente} | Valor: R${valor_total:.2f} | Pagamento: {pagamento}\n"
            
            conteudo_relatorio += linha 

        conteudo_relatorio += "\n=================================\n"
        conteudo_relatorio += f"FATURAMENTO TOTAL: R${faturamento_total:.2f}\n"
        conteudo_relatorio += "=================================\n"

        nome_arquivo = f"fechamento_caixa_{datetime.datetime.now().strftime('%y_%m_%d_%Hh%Mm%Ss')}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_relatorio)

        print(f"SUCESSO! Arquivo '{nome_arquivo}' foi criado na sua pasta!")
        email = force_str("Você deseja enviar isso para o seu email? (Sim/Não)").upper()    
        if email in ["S", "SIM"]:
            assunto = "NOTA FISCAL"
            resposta = conteudo_relatorio
            enviar_email = enviar_email_relatorio(id_operador,resposta,assunto)
            if not enviar_email:
                print("Erro: email não enviado. Voltando para o menu!")
                return
            else:
                print("Email enviado com sucesso!")
                return
        else:
            print("Voltando para o menu!")

    except mysql.connector.Error as e:
        print(f"Ocorreu um erro no banco de dados: {e}")
        return None
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )        

def nota_fiscal():
    print("\n----- NOTA FISCAL -----")
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT vendas.data_hora, vendas.id_cliente, vendas.id_usuario, vendas.id_cupom, vendas.valor_total, vendas.forma_pagamento, itens_venda.quantidade, itens_venda.preco_unitario 
            FROM vendas
            INNER JOIN itens_venda ON vendas.id_venda = itens_venda.id_venda
            ORDER BY data_hora DESC
            LIMIT 10
        """)
        vendas = cursor.fetchall()
        total = 0

        for venda in vendas:
            print(f"{venda[0]} | Cliente:{venda[1]} | Usuario:{venda[2]} | Cupom:{venda[3]} | Valor: R${venda[4]:.2f} | Pagamento:{venda[5]} | Quantidade:{venda[6]} | Preço Unitário:{venda[7]} |")
            total += venda[4]

        print("-" * 30)
        print(f"TOTAL EXIBIDO: R$ {total:.2f}")

    except mysql.connector.Error as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )        

def registar_venda(id_operador):
    print("\n====== CARRINHO DE COMPRAS ======")
    carrinho = []

    while True:
        try:
            id_produto = force_int("Digite o [ID] do produto (-1 concluir | -2 cancelar): ")
        except ValueError:
            print("ERRO: O ID DEVE SER UM NÚMERO INTEIRO.")
            continue

        if id_produto == -1:
            break
        elif id_produto == -2:
            print("Compra cancelada pelo operador!")
            carrinho.clear()
            return

        conexao = obter_conexao()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """SELECT nome, id_categoria, id_fornecedor, preco_venda, preco_custo, 
                          quantidade_estoque, nota, validade, ativo, desconto
                   FROM produtos WHERE id_produto = %s""",
                (id_produto,),
            )
            bebida = cursor.fetchone()

            if not bebida:
                print("ERRO: ID INVÁLIDO. Esse produto não existe no sistema.")
                continue

            if bebida[8] == 0:
                print("Produto está atualmente desativado, tente outra opção!")
                continue

            nome_bebida = bebida[0]
            preco_venda = float(bebida[3])
            quantidade_estoque = bebida[5]

            desconto_banco = float(bebida[9]) if bebida[9] else 0.0

            preco_promocional = preco_venda
            if desconto_banco > 0:
                preco_promocional = preco_venda - (preco_venda * (desconto_banco / 100))

        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )  

        venda_autorizada = teste_qualidade(id_produto)
        if not venda_autorizada:
            print("-> Produto rejeitado. Escolha outro item.")
            continue

        try:
            quantidade = force_int(f"Quantas unidades de '{nome_bebida}' você deseja? ")
        except ValueError:
            print("ERRO: Quantidade inválida.")
            continue

        qtd_carrinho = sum(item["quantidade"] for item in carrinho if item["id_produto"] == id_produto)
        estoque_disponivel = quantidade_estoque - qtd_carrinho

        if quantidade <= 0:
            print("ERRO: Quantidade inválida.")
            continue
        elif quantidade > estoque_disponivel:
            print(f"Estoque insuficiente. Você já tem {qtd_carrinho} no carrinho, estoque disponível é {quantidade_estoque}.")
            continue
        else:
            carrinho.append({
                "id_produto": id_produto,
                "nome": nome_bebida,
                "quantidade": quantidade,
                "preco": preco_promocional,
                "subtotal_original": quantidade * float(preco_venda),
                "subtotal_promocional": quantidade * preco_promocional,
            })
            print(f"-> {quantidade}x '{nome_bebida}' adicionado ao carrinho!")

    if not carrinho:
        return

    id_cliente_final = None
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_cliente, nome, cnpj_cpf FROM clientes")
        clientes = cursor.fetchall()

        if not clientes:
            add_cl = force_str("Não temos clientes cadastrados. Cadastrar agora? (S/N): ").upper()
            if add_cl in ["S", "SIM"]:
                id_cliente_final = add_cliente()
            else:
                print("Compra não pode continuar sem cliente!")
                return
        else:
            print("\nEsses são os nossos clientes:")
            for linha in clientes:
                print(f"-> ID: {linha[0]} | Nome: {linha[1]} | Doc: {linha[2]}")

            cliente_v = force_int("\nO cliente dessa venda é algum desses? (1-Sim | 2-Não): ")
            if cliente_v == 1:
                escolha = force_int("Digite o [ID] do cliente: ")
                cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = %s", (escolha,))
                result = cursor.fetchone()
                if result:
                    id_cliente_final = result[0]
                else:
                    print("ID de cliente inválido!")
                    return
            elif cliente_v == 2:
                add_cl = force_str("Você vai precisar adicionara o seu cliente!. Cadastrar agora? (S/N): ").upper()
                if add_cl in ["S", "SIM"]:
                    id_cliente_final = add_cliente()
                else:
                    print("Compra não pode continuar sem cliente!")
                    return

    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        ) 
    total_original_compra = sum(item["subtotal_original"] for item in carrinho)
    total_compra = sum(item["subtotal_promocional"] for item in carrinho)
    
    print(f"\n============= FECHAMENTO DE CAIXA ==============")
    print(f"Total a pagar: R$ {total_compra:.2f}")
    confirmar = force_str("Confirmar pagamento e registrar venda? (S/N): ").upper()
    if confirmar not in ["S", "SIM"]:
        print("Venda cancelada pelo operador.")
        return

    print("\n1-PIX | 2-Boleto | 3-Transferência | 4-Cartão de Crédito")
    pagamento_opcao = force_str("Qual o método de pagamento? ")
    mapa_pagamentos = {"1": "PIX", "2": "Boleto", "3": "Transferência", "4": "Cartão de Crédito"}
    forma_pagamento = mapa_pagamentos.get(pagamento_opcao)

    if not forma_pagamento:
        print("ERRO: Método de pagamento inválido.")
        return 

    id_cupom_bd = None
    cupom = force_str("Você possui algum cupom de desconto? (S/N): ").upper()

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        if cupom in ["S", "SIM"]:
            nm_cup = force_str("Digite o nome do seu cupom: ").upper()
            cursor.execute("SELECT id_cupom, desconto, quantidade FROM cupons WHERE nome = %s", (nm_cup,))
            result = cursor.fetchone()

            if not result or result[2] == 0:
                print("Cupom inválido ou esgotado!")
            else:
                id_cupom_bd = result[0]
                
                total_compra *= 1 - (float(result[1]) / 100)
                print(f"Cupom aplicado com sucesso! Novo total: R$ {total_compra:.2f}")

                cursor.execute(
                    "UPDATE cupons SET quantidade = quantidade - 1, qtd_used = qtd_used + 1 WHERE id_cupom = %s",
                    (id_cupom_bd,)
                )
                
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        cursor.execute(
            """
            INSERT INTO vendas (data_hora, id_cliente, id_usuario, id_cupom, valor_total, forma_pagamento)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data_hora, id_cliente_final, id_operador, id_cupom_bd, total_compra, forma_pagamento)
        )
        
        id_venda_gerada = cursor.lastrowid 

        for item in carrinho:
            cursor.execute(
                """
                UPDATE produtos 
                SET quantidade_estoque = quantidade_estoque - %s
                WHERE id_produto = %s
                """,
                (item["quantidade"], item["id_produto"])
            )
            
            cursor.execute(
                """
                INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (id_venda_gerada, item["id_produto"], item["quantidade"], item["preco"])
            )

        conexao.commit()
        print("\nVenda registrada, nota fiscal gerada e estoque atualizado com sucesso!")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print("\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
        print(f"Motivo técnico: {erro}")
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )