from forces import force_int, force_float, force_str, bsc_id
from connectsql import obter_conexao, fechar_execusao
from marketing_fornecedores.marketing import cadastrar_fornecedor
import mysql.connector
from colorama import Fore, Style
def adicionar_item() -> None:
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO PRODUTO{Fore.CYAN}                                            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

    while True:
        nome_produto = force_str("Digite o nome do produto ou [0] para sair: ").title()
        if nome_produto == '0':
            print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
            break
        try:
            preco_custo = force_float("Digite o preço de CUSTO ou [0] para sair: R$ ")
            if preco_custo == 0:
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                break
            preco_venda = force_float("Digite o preço de VENDA ou [0] para sair: R$ ")
            if preco_venda == 0:
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                break
            quantidade = force_int("Quantidade inicial em estoque ou [0] para sair: ")
            if quantidade == 0:
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                break
            nota = force_float("Nota do produto (ex: 4.5) ou 0 para não avaliado: ")
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: Digite apenas números." + Fore.RESET)
            continue
        if nota > 5 or nota < 0:
            print(Fore.RED + "\n[✖] ERRO: Valor de nota inválido (deve ser entre 0 e 5)." + Fore.RESET)
            continue
        
        tem_validade = force_str("O produto tem data de validade?, Caso queira retornar digite [0] (S/N): ").upper()
        if tem_validade == "0":
            print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
            break
        validade = force_str("Digite a validade ou [0] para sair 0(AAAA-MM-DD): ") if tem_validade == "S" else None
        if validade == 0:
            print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
            break
        if validade and len(validade) != 10:
            print(Fore.RED + "\n[✖] ERRO: Quantidade de caracteres da validade inválida!" + Fore.RESET)
            return
        conexao = obter_conexao()
        cursor = conexao.cursor()

        try:
            print(Fore.CYAN + "\n--- SELECIONE A CATEGORIA ---" + Fore.RESET)
            cursor.execute("SELECT id_categoria, nome FROM categorias WHERE ativo = 1")
            categorias = cursor.fetchall()
            
            if categorias:
                for i in categorias:
                    print(f"[{i[0]}] - {i[1]}")
                id_categoria = force_int("Digite o ID da categoria correspondente ou [0]: ")
                if id_categoria == 0:
                    print("Voltando ao menu")
                    break
            else:
                print(Fore.YELLOW + "Nenhuma categoria cadastrada. Usando ID 1 por padrão.")
                id_categoria = 1

            print(Fore.CYAN + "\n--- SELECIONE O FORNECEDOR ---" + Fore.RESET)
            cursor.execute("SELECT id_fornecedor, nome FROM fornecedores WHERE ativo = 1")
            fornecedores = cursor.fetchall()

            id_fornecedor_escolhido = None

            if fornecedores:
                for forn in fornecedores:
                    print(f"[{forn[0]}] - {forn[1]}")
                
                fornece = force_int("\nO fornecedor está na lista acima? (1-Sim | 2-Não): ")
                
                if fornece == 1:
                    id_fornecedor_escolhido = force_int("Digite o [ID] do fornecedor ou [0] para sair: ")
                    if id_fornecedor_escolhido == 0:
                        print("Voltando ao menu")
                        break
                elif fornece == 2:
                    id_fornecedor_escolhido = cadastrar_fornecedor() 
                else:
                    print(Fore.RED + "Opção inválida. Operação cancelada.")
                    return
            else:
                print(Fore.YELLOW + "Nenhum fornecedor cadastrado ainda!")
                opcao = force_int("Deseja cadastrar um novo fornecedor agora? (1-Sim | 2-Não): ")
                if opcao == 1:
                    id_fornecedor_escolhido = cadastrar_fornecedor()
                else:
                    print(Fore.RED + "Operação cancelada. É obrigatório ter um fornecedor.")
                    return

            cursor.execute(
                """
                INSERT INTO produtos (nome, id_categoria, id_fornecedor, preco_venda, preco_custo, quantidade_estoque, nota, validade, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
                """,
                (
                    nome_produto,
                    id_categoria,
                    id_fornecedor_escolhido,
                    preco_venda,
                    preco_custo,
                    quantidade,
                    nota,
                    validade
                )
            )
            conexao.commit()
            print(Fore.GREEN + f"\nProduto '{nome_produto}' cadastrado com sucesso no sistema!" + Fore.RESET)

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )

def alterar_preco():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}ALTERAR PREÇO{Fore.CYAN}                                                     █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
    try:
        id_produto = bsc_id()
    except ValueError:
        print(Fore.RED + "\n[✖] ERRO: Digite um ID válido!" + Fore.RESET)
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT nome, preco_venda FROM produtos WHERE id_produto = %s AND ativo = 1", 
            (id_produto,)
        )
        bebida = cursor.fetchone()

        if not bebida:
            print(Fore.RED + "\n[✖] ERRO: Produto não encontrado no banco de dados!" + Fore.RESET)
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
        print(Fore.GREEN + f"\nAlteração feita com sucesso! '{bebida[0]}' agora custa R$ {novo_preco:.2f}." + Fore.RESET)

    except mysql.connector.Error as e:
        conexao.rollback()
        print(Fore.RED + Style.BRIGHT + "\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
        
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )

def repor_estoque():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}REPOR ESTOQUE{Fore.CYAN}                                                     █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
    try:
        id_produto = bsc_id()
    except ValueError:
        print(Fore.RED + "ERRO: Digite um ID válido!")
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT nome, quantidade_estoque FROM produtos WHERE id_produto = %s AND ativo = 1",
            (id_produto,),
        )
        bebida = cursor.fetchone()

        if not bebida:
            print(Fore.RED + "\n[✖] ERRO: Produto não encontrado no banco de dados!" + Fore.RESET)
            return

        quantidade_adicional = force_int(
            f"Quantidade para adicionar de '{bebida[0].title()}' (Estoque atual: {bebida[1]}): "
        )

        nova_quantidade = bebida[1] + quantidade_adicional
        conexao.start_transaction()
        cursor.execute(
            """
            UPDATE produtos 
            SET quantidade_estoque = %s 
            WHERE id_produto = %s
            """,
            (nova_quantidade, id_produto),
        )
        conexao.commit()
        print(Fore.GREEN + f"\nReposição feita com sucesso! '{bebida[0]}' agora tem {nova_quantidade} unidades em estoque." + Fore.RESET)

    except mysql.connector.Error as e:
        conexao.rollback() 
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
        
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )

def alterar_nome():

    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}ALTERAR NOME DO PRODUTO{Fore.CYAN}                                           █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

        try:
            id_produto = force_int("Digite o ID da bebida que deseja alterar o nome ou [0] para sair: ")

            if id_produto == 0:
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                break
            
            if id_produto < 0:
                print(Fore.RED + "\n[✖] ERRO: O ID deve ser maior que zero." + Fore.RESET)
                continue

        except ValueError:
            print(Fore.RED + "O ID precisa ser um número válido.")
            escolha = force_str("Deseja tentar novamente? Digite SIM ou NÃO: ").lower()
            if escolha in ("sim", "s"):
                continue
            elif escolha in ("nao", "não", "n"):
                break
            else:
                print(Fore.RED + "Informação inválida.")
                break

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 1", (id_produto,))

            produto = cursor.fetchone()

            if not produto:
                print(Fore.RED + "Produto não encontrado!")
                continue

            print(Fore.WHITE + f"Produto encontrado: {produto[0]}")
            print("(Se não quiser seguir com a alteração, deixe em branco e aperte Enter)")

            novo_nome = force_str(f"Alterar nome da bebida [{produto[0]}] para: ")

            if not novo_nome:
                print(Fore.YELLOW + "Alteração cancelada.")
                continue
            conexao.start_transaction()
            cursor.execute(
                """
                UPDATE produtos
                SET nome = %s
                WHERE id_produto = %s
                """,
                (novo_nome, id_produto),
            )

            conexao.commit()
            print(Fore.GREEN + "Nome do produto alterado com sucesso!!" + Fore.RESET)

            break

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)

        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def off_prod():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}OCULTAR ITEM DO CATÁLOGO{Fore.CYAN}                                          █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    while True:
        try:
            id_prod = force_int("Digite o [ID] do produto desejado ou [0] para sair: ")
        except ValueError:
            print(Fore.RED + "Digite somente números")
            continue

        if id_prod == 0:
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            break
        try:
            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 1",(id_prod,))

            found = cursor.fetchone()

            if not found:
                print(Fore.RED + "Bebida não encontrada ou já foi desativada")
                continue    

            confirm = force_str(f"Tem certeza que deseja desativar {found[0]}? Para confirmar digite [s] e para cancelar [n]: ").lower()

            if confirm in ["s", "sim"]:
                conexao.start_transaction()
                cursor.execute("UPDATE produtos SET ativo = 0 WHERE id_produto = %s ",(id_prod,))
                conexao.commit()
                print(Fore.GREEN + "Bebida desativada do catálogo" + Fore.RESET)

            else:
                print(Fore.YELLOW + "\n[!] Operação cancelada, retornando ao menu..." + Fore.RESET)
                continue

        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            conexao.rollback()
            break
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )        

def atv_prod():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}ATIVAR ITEM NO CATÁLOGO{Fore.CYAN}                                           █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    while True:
        try:
            id_prod = force_int("Digite o [ID] do produto desejado ou [0] para sair: ")
        except ValueError:
            print(Fore.RED + "Digite somente números")
            continue

        if id_prod == 0:
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            break
        try:
            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 0",(id_prod,))

            found = cursor.fetchone()

            if not found:
                print(Fore.RED + "Bebida não encontrada ou já está ativada")
                continue    

            confirm = force_str(f"Tem certeza que deseja ativar {found[0]}? Para confirmar digite [s] e para cancelar [n]: ").lower()

            if confirm in ("sim", "s"):
                conexao.start_transaction()
                cursor.execute("UPDATE produtos SET ativo = 1 WHERE id_produto = %s ",(id_prod,))
                conexao.commit()
                print(Fore.GREEN + "Bebida ativada no catálogo" + Fore.RESET)

            else:
                print(Fore.YELLOW + "\n[!] Operação cancelada, retornando ao menu..." + Fore.RESET)
                continue

        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            conexao.rollback()
            break
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )        

def add_cliente():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO CLIENTE{Fore.CYAN}                                            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
        nome_cliente = force_str("Digite o nome do novo cliente ou [0] para sair: ").lower()
        if nome_cliente == '0':
            print("Voltando ao menu")
            break
        cnpj = force_str("Digite o cnpj do cliente ou [0] para sair (Digite apenas os numeros): ")
        if cnpj == '0':
            print("Voltando ao menu")
            break
        if len(cnpj) != 14 or not cnpj.isdigit():
            print(Fore.RED + "\n[✖] ERRO: Quantidade de caracteres do CNPJ inválida!" + Fore.RESET)
            continue
        cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        endereco = force_str("Digite o endereço do cliente ou [0] para sair: ").lower()
        if endereco == '0':
            print("Voltando ao menu")
            break
        telefone = force_str("Digite o telefone do cliente ou [0] para sair(Digite apenas os numeros): ")
        if telefone == 0:
            print("Voltando ao menu")
            break
        if len(telefone) != 11 or not telefone.isdigit():
            print(Fore.RED + "\n[✖] ERRO: Quantidade de caracteres do telefone inválida!" + Fore.RESET)
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
            print(Fore.GREEN + f"O cliente '{nome_cliente}' foi salvo com sucesso! " + Fore.RESET)
            return nome_cliente

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            return "Sem cliente"
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )   
def add_categoria():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVA CATEGORIA{Fore.CYAN}                                          █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
        nome_categoria = force_str("Digite o nome da nova categoria ou [0] para sair: ").lower()
        if nome_categoria == '0':
            print("Voltando ao menu")
            break
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                    INSERT INTO categorias(nome)
                    VALUES (%s)
                """,(nome_categoria,))
            conexao.commit()
            print(Fore.GREEN + f"A categoria '{nome_categoria}' foi salva com sucesso! " + Fore.RESET)
            return nome_categoria

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            return "Sem categoria"
        finally:
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )