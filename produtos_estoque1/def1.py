from forces import force_int, force_float, force_str, bsc_id
from connectsql import obter_conexao,fechar_execusao
from marketing_fornecedores.marketing import cadastrar_fornecedor
import mysql.connector

def adicionar_item() -> None:
    print("\n" + "="*40)
    print("        CADASTRAR NOVO PRODUTO        ")
    print("="*40)

    # 1. Coleta os dados básicos do produto
    nome_produto = force_str("Digite o nome do produto: ").title()
    preco_custo = force_float("Digite o preço de CUSTO: R$ ")
    preco_venda = force_float("Digite o preço de VENDA: R$ ")
    quantidade = force_int("Quantidade inicial em estoque: ")
    nota = force_float("Nota do produto (ex: 4.5) ou 0 para não avaliado: ")
    if nota > 5 or nota < 0:
        print("Valor inválido!")
        return
    
    # Validade opcional
    tem_validade = force_str("O produto tem data de validade? (S/N): ").upper()
    validade = force_str("Digite a validade (AAAA-MM-DD): ") if tem_validade == "S" else None

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        print("\n--- SELECIONE A CATEGORIA ---")
        cursor.execute("SELECT id_categoria, nome FROM categorias")
        categorias = cursor.fetchall()
        
        if categorias:
            for i in categorias:
                print(f"[{i[0]}] - {i[1]}")
            id_categoria = force_int("Digite o ID da categoria correspondente: ")
        else:
            print("Nenhuma categoria cadastrada. Usando ID 1 por padrão.")
            id_categoria = 1

        print("\n--- SELECIONE O FORNECEDOR ---")
        cursor.execute("SELECT id_fornecedor, nome FROM fornecedores")
        fornecedores = cursor.fetchall()

        id_fornecedor_escolhido = None

        if fornecedores:
            for forn in fornecedores:
                print(f"[{forn[0]}] - {forn[1]}")
            
            fornece = force_int("\nO fornecedor está na lista acima? (1-Sim | 2-Não): ")
            
            if fornece == 1:
                id_fornecedor_escolhido = force_int("Digite o [ID] do fornecedor: ")
            elif fornece == 2:
                id_fornecedor_escolhido = cadastrar_fornecedor() 
            else:
                print("Opção inválida. Operação cancelada.")
                return
        else:
            print("Nenhum fornecedor cadastrado ainda!")
            opcao = force_int("Deseja cadastrar um novo fornecedor agora? (1-Sim | 2-Não): ")
            if opcao == 1:
                id_fornecedor_escolhido = cadastrar_fornecedor()
            else:
                print("Operação cancelada. É obrigatório ter um fornecedor.")
                return

        cursor.execute(
            """
            INSERT INTO produtos (nome, id_categoria, id_fornecedor, preco_venda, preco_custo, quantidade_estoque, nota, validade, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
            """,
            (
                nome_produto,
                id_categoria,
                id_fornecedor_escolhido, # Agora enviamos o ID numérico, não o texto
                preco_venda,
                preco_custo,
                quantidade,
                nota,
                validade
            )
        )
        conexao.commit()
        print(f"\nProduto '{nome_produto}' cadastrado com sucesso no sistema!")

    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"\nOcorreu um erro no banco de dados: {e}")
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def alterar_preco():
    print("\n" + "="*40)
    print("            ALTERAR PREÇO            ")
    print("="*40)
    
    try:
        id_produto = bsc_id()
    except ValueError:
        print("ERRO: Digite um ID válido!")
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # Busca o nome e o preço de venda atual na tabela produtos
        cursor.execute(
            "SELECT nome, preco_venda FROM produtos WHERE id_produto = %s", 
            (id_produto,)
        )
        bebida = cursor.fetchone()

        if not bebida:
            print("ERRO: Produto não encontrado no banco de dados!")
            return
        
        novo_preco = force_float(
            f"Atualizar o preço de '{bebida[0]}' (PREÇO ATUAL: R$ {bebida[1]:.2f}): "
        )

        cursor.execute(
            """
            UPDATE produtos 
            SET preco_venda = %s 
            WHERE id_produto = %s
            """,
            (novo_preco, id_produto),
        )
        conexao.commit()
        print(f"\nAlteração feita com sucesso! '{bebida[0]}' agora custa R$ {novo_preco:.2f}.")

    except mysql.connector.Error as e:
        conexao.rollback()
        print("\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
        print(f"Motivo técnico: {e}")
        
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def repor_estoque():
    print("\n" + "="*40)
    print("            REPOR ESTOQUE            ")
    print("="*40)
    
    try:
        id_produto = bsc_id()
    except ValueError:
        print("ERRO: Digite um ID válido!")
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # Busca o nome e o estoque atual na tabela produtos
        cursor.execute(
            "SELECT nome, quantidade_estoque FROM produtos WHERE id_produto = %s",
            (id_produto,),
        )
        bebida = cursor.fetchone()

        if not bebida:
            print("ERRO: Produto não encontrado no banco de dados!")
            return

        quantidade_adicional = force_int(
            f"Quantidade para adicionar de '{bebida[0].title()}' (Estoque atual: {bebida[1]}): "
        )

        nova_quantidade = bebida[1] + quantidade_adicional

        cursor.execute(
            """
            UPDATE produtos 
            SET quantidade_estoque = %s 
            WHERE id_produto = %s
            """,
            (nova_quantidade, id_produto),
        )
        conexao.commit()
        print(f"\nReposição feita com sucesso! '{bebida[0]}' agora tem {nova_quantidade} unidades em estoque.")

    except mysql.connector.Error as e:
        conexao.rollback() 
        print(f"\nErro no banco de dados: {e}")
        
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def alterar_nome():

    while True:
        print("ALTERAR NOME")

        try:
            id_produto = force_int("Digite o ID da bebida que deseja alterar o nome: ")
            

            if id_produto <= 0:
                print("O ID deve ser maior que zero.")
                continue

        except ValueError:
            print("O ID precisa ser um número válido.")

            escolha = force_str("Deseja tentar novamente? Digite SIM ou NÃO: ").lower()

            if escolha in ("sim", "s"):
                continue
            elif escolha in ("nao", "não", "n"):
                break
            else:
                print("Informação inválida.")
                break

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s", (id_produto,))

            produto = cursor.fetchone()

            if not produto:
                print("Produto não encontrado!")
                continue

            print(f"Produto encontrado: {produto[0]}")
            print(
                "(Se não quiser seguir com a alteração, deixe em branco e aperte Enter)"
            )

            novo_nome = force_str(f"Alterar nome da bebida [{produto[0]}] para: ")

            if not novo_nome:
                print("Alteração cancelada.")
                continue

            cursor.execute(
                """
                UPDATE produtos
                SET nome = %s
                WHERE id_produto = %s
                """,
                (novo_nome, id_produto),
            )

            conexao.commit()
            print("Nome do produto alterado com sucesso!!")

            break

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Erro no banco de dados: {erro}")

        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def off_prod():
    print("\n Ocultar item do catálogo(Soft Delete)")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    while True:
        try:
            id_prod = force_int("Digite o [ID] do produto desejado ou [0] para sair: ")
        except ValueError:
            print("Digite somente números")
            continue


        if id_prod == 0:
            break
        try:
            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 1",(id_prod,))

            found = cursor.fetchone()

            if not found:
                print("Bebida não encontrada ou já foi desativada")
                continue    

            confirm = force_str(f"Tem certeza que deseja desativar {found[0]}? Para confirmar digite [s] e para cancelar [n]: ").lower()

            if confirm == "s" or "sim":
                cursor.execute("UPDATE produtos SET ativo = 0 WHERE id_produto = %s ",(id_prod,))
                conexao.commit()
                print("Bebida desativada do catálogo")

            else:
                print("Cancelando operação, retornando ao menu")
                continue

        except mysql.connector.Error as e:
            print(f"Erro no banco de dados: {e}")
            conexao.rollback()
            break
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )         

        
def atv_prod():
    print("\n Ativar bebida no catálogo")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    while True:
        try:
            id_prod = force_int("Digite o [ID] do produto desejado ou [0] para sair: ")
        except ValueError:
            print("Digite somente números")
            continue


        if id_prod == 0:
            break
        try:
            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 0",(id_prod,))

            found = cursor.fetchone()

            if not found:
                print("Bebida não encontrada ou já está ativada")
                continue    

            confirm = force_str(f"Tem certeza que deseja ativar{found[0]}? Para confirmar digite [s] e para cancelar [n]: ").lower()

            if confirm in ("sim", "s"):
                cursor.execute("UPDATE produtos SET ativo = 1 WHERE id_produto = %s ",(id_prod,))
                conexao.commit()
                print("Bebida ativada no catálogo")

            else:
                print("Cancelando operação, retornando ao menu")
                continue

        except mysql.connector.Error as erro:
            print(f"Erro no banco de dados: {erro}")
            conexao.rollback()
            break
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )         


def add_cliente():
    while True:
        print("\n----- NOVO CLIENTE --------")
        nome_cliente = force_str("Digite o nome do novo cliente: ").lower()
        cnpj = force_str("Digite o cnpj do cliente (Digite apenas os numeros): ")
        if len (cnpj) != 14 or not cnpj.isdigit():#função que garante que o usuario so vai colocar numeros pois se colocar alguma letra ou algo do tipo pois ele retorna como false!!!
            print("Quantidade de caracteres inválida!")
            continue
        cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        endereco = force_str("Digite o endereço do cliente: ").lower()
        telefone = force_str("Digite o telefone do cliente (Digite apenas os numeros): ")
        if len (telefone) != 11 or not telefone.isdigit():
            print("Quantidade de caracteres inválida!")
            continue
        telefone_ajustado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                    INSERT INTO clientes(nome,cnpj_cpf,endereco,telefone)
                    VALUES (%s,%s,%s,%s)
                """,
                (
                    nome_cliente,
                    cnpj_formatado,
                    endereco,
                    telefone_ajustado
                ),
            )
            conexao.commit()
            print(f"O cliente '{nome_cliente}' foi salvo com sucesso! ")
            return nome_cliente

        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return "Sem cliente"
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )         
