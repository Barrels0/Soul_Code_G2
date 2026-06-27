from forces import force_int, force_float, force_str, bsc_id
from connectsql import obter_conexao, fechar_execusao
from marketing_fornecedores.marketing import cadastrar_fornecedor
import mysql.connector
from colorama import Fore, Style
def adicionar_item():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO PRODUTO{Fore.CYAN}                                            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    while True:
        nome_produto = force_str("\n➤ Digite o nome do produto ou [0] para sair: ").title()
        if nome_produto == '0':
            print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
            break
            
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
            
        while True:
            nota = force_float("Nota do produto (ex: 4.5) ou 0 para não avaliado: ")
            if 0 <= nota <= 5:
                break
            print(Fore.RED + "\n[✖] ERRO: Valor de nota inválido (deve ser entre 0 e 5)." + Fore.RESET)
        
        tem_validade = force_str("O produto tem data de validade? (S/N) ou [0] para sair: ").upper()
        if tem_validade == "0":
            print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
            break
            
        validade = force_str("Digite a validade (AAAA-MM-DD) ou [0] para sair: ") if tem_validade == "S" else None
        
        if validade == '0':
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
                id_categoria = force_int("➤ Digite o ID da categoria correspondente ou [0] para cancelar: ")
                if id_categoria == 0:
                    print(Fore.YELLOW + "\n[!] Voltando ao menu." + Fore.RESET)
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
                
                fornece = force_int("\n➤ O fornecedor está na lista acima? (1-Sim | 2-Não): ")
                
                if fornece == 1:
                    id_fornecedor_escolhido = force_int("Digite o [ID] do fornecedor ou [0] para sair: ")
                    if id_fornecedor_escolhido == 0:
                        print(Fore.YELLOW + "\n[!] Voltando ao menu." + Fore.RESET)
                        break
                elif fornece == 2:
                    id_fornecedor_escolhido = cadastrar_fornecedor() 
                    if not id_fornecedor_escolhido: return
                else:
                    print(Fore.RED + "\n[✖] Opção inválida. Operação cancelada." + Fore.RESET)
                    return
            else:
                print(Fore.YELLOW + "Nenhum fornecedor cadastrado ainda!")
                opcao = force_int("Deseja cadastrar um novo fornecedor agora? (1-Sim | 2-Não): ")
                if opcao == 1:
                    id_fornecedor_escolhido = cadastrar_fornecedor()
                    if not id_fornecedor_escolhido: return
                else:
                    print(Fore.RED + "\n[✖] Operação cancelada. É obrigatório ter um fornecedor." + Fore.RESET)
                    return

            cursor.execute(
                """
                INSERT INTO produtos (nome, id_categoria, id_fornecedor, preco_venda, preco_custo, quantidade_estoque, nota, validade)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nome_produto, id_categoria, id_fornecedor_escolhido, preco_venda, preco_custo, quantidade, nota, validade)
            )
            conexao.commit()
            print(Fore.GREEN + f"\n[✔] Produto '{nome_produto}' cadastrado com sucesso no sistema!" + Fore.RESET)
            break

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            break
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

def repor_em_lote(*args):
    # Se a função for chamada sem nenhum argumento, ela não faz nada
    if not args:
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        for id_produto in args:
            cursor.execute(
                "SELECT nome, quantidade_estoque FROM produtos WHERE id_produto = %s AND ativo = 1",
                (id_produto,),
            )
            found = cursor.fetchall()

            if len(found) == 0:
                print(Fore.RED + f"\n[✖] ERRO: Produto ID [{id_produto}] não encontrado ou desativado!" + Fore.RESET)
                continue
                
            bebida = found[0]

            quantidade_adicional = force_int(Fore.YELLOW + 
                f"\n➤ Quantidade para adicionar de '{bebida[0].title()}' (Estoque atual: {bebida[1]}): " + Fore.RESET
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
            print(Fore.GREEN + f"[✔] SUCESSO: '{bebida[0]}' agora tem {nova_quantidade} unidades em estoque." + Fore.RESET)

        conexao.commit()

    except mysql.connector.Error as e:
        conexao.rollback() 
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO CRÍTICO no banco de dados: {e}" + Fore.RESET)
        
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
    
    opcao = input(Fore.YELLOW + "\n➤ Deseja repor (1) Único produto ou (2) Múltiplos produtos em lote? " + Fore.RESET).strip()

    if opcao == '1':
        try:
            id_produto = bsc_id()
            # Chama a função em lote passando apenas 1 argumento
            repor_em_lote(id_produto)
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: Digite um ID válido!" + Fore.RESET)
            
    elif opcao == '2':
        entrada = input(Fore.YELLOW + "➤ Digite os [IDs] separados por vírgula (ex: 2, 5, 8): " + Fore.RESET)
        try:
            ids_para_repor = [int(x.strip()) for x in entrada.split(',')]
            
            repor_em_lote(*ids_para_repor)
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: Formato inválido! Use apenas números separados por vírgula." + Fore.RESET)
            
    else:
        print(Fore.RED + "\n[✖] Opção inválida! Operação cancelada." + Fore.RESET)

def alterar_nome():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}ALTERAR NOME DO PRODUTO{Fore.CYAN}                                           █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

        try:
            id_produto = force_int(Fore.YELLOW + "➤ Digite o ID da bebida que deseja alterar o nome ou [0] para sair: " + Fore.RESET)

            if id_produto == 0:
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                break
            
            if id_produto < 0:
                print(Fore.RED + "\n[✖] ERRO: O ID deve ser maior que zero." + Fore.RESET)
                continue

        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: O ID precisa ser um número válido." + Fore.RESET)
            continue

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM produtos WHERE id_produto = %s AND ativo = 1", (id_produto,))
            found = cursor.fetchall()

            if len(found) == 0:
                print(Fore.RED + "\n[✖] ERRO: Produto não encontrado ou desativado!" + Fore.RESET)
                continue

            produto = found[0]

            print(Fore.WHITE + f"\nProduto encontrado: {produto[0]}")
            print("(Se não quiser seguir com a alteração, deixe em branco e aperte Enter)")

            novo_nome = force_str(Fore.YELLOW + f"➤ Alterar nome da bebida [{produto[0]}] para: " + Fore.RESET)

            if not novo_nome:
                print(Fore.YELLOW + "\n[!] Alteração cancelada pelo operador." + Fore.RESET)
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
            print(Fore.GREEN + f"\n[✔] SUCESSO: Nome do produto alterado para '{novo_nome}'!" + Fore.RESET)
            break

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO CRÍTICO no banco de dados: {e}" + Fore.RESET)

        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )


def ativ_off(tabela, coluna_id, nome_exibicao, ativar=True):
    """
    Função universal para ativar ou desativar registros em qualquer tabela.
    """
    acao_titulo = "ATIVAR" if ativar else "DESATIVAR"
    acao_verbo = "ativar" if ativar else "desativar"
    status_buscado = 0 if ativar else 1 
    status_novo = 1 if ativar else 0 
    
    espaco = " " * (45 - len(f"{acao_titulo} {nome_exibicao.upper()}"))
    
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}{acao_titulo} {nome_exibicao.upper()}{espaco}{Fore.CYAN}                     █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

    while True:
        try:
            id_alvo = force_int(Fore.YELLOW + f"➤ Digite o [ID] do {nome_exibicao} ou [0] para sair: " + Fore.RESET)
            if id_alvo == 0:
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                return
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: Digite somente números." + Fore.RESET)
            continue

        conexao = obter_conexao()
        cursor = conexao.cursor()

        try:
            query_busca = f"SELECT nome FROM {tabela} WHERE {coluna_id} = %s AND ativo = %s"
            cursor.execute(query_busca, (id_alvo, status_buscado))
            
            found = cursor.fetchall()

            if len(found) == 0:
                print(Fore.RED + f"\n[✖] ERRO: {nome_exibicao} não encontrado ou já está {acao_verbo}." + Fore.RESET)
                continue    

            nome_registro = found[0][0]
            confirm = force_str(Fore.YELLOW + f"➤ Tem certeza que deseja {acao_verbo} '{nome_registro}'? [S/N]: " + Fore.RESET).lower()

            if confirm in ["s", "sim"]:
                query_update = f"UPDATE {tabela} SET ativo = %s WHERE {coluna_id} = %s"
                cursor.execute(query_update, (status_novo, id_alvo))
                conexao.commit()
                print(Fore.GREEN + f"\n[✔] SUCESSO: {nome_exibicao} '{nome_registro}' foi {acao_verbo}(a) no sistema!" + Fore.RESET)
                break
            else:
                print(Fore.YELLOW + "\n[!] Operação cancelada pelo operador." + Fore.RESET)

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO CRÍTICO no banco de dados: {e}" + Fore.RESET)
            break
            
        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )        
def off_prod():
    ativ_off("produtos", "id_produto", "produto", ativar=False)

def atv_prod():
    ativ_off("produtos", "id_produto", "produto", ativar=True)

def off_cli():
    ativ_off("clientes", "id_cliente", "cliente", ativar=False)

def atv_cli():
    ativ_off("clientes", "id_cliente", "cliente", ativar=True)

def off_forn():
    ativ_off("fornecedores", "id_fornecedor", "fornecedor", ativar=False)

def atv_forn():
    ativ_off("fornecedores", "id_fornecedor", "fornecedor", ativar=True)

def add_cliente():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO CLIENTE{Fore.CYAN}                                            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
        nome_cliente = force_str("Digite o nome do novo cliente ou [0] para sair: ").lower()
        if nome_cliente == '0':
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
            
        cnpj = force_str("Digite o CPF/CNPJ do cliente ou [0] para sair (apenas números): ")
        if cnpj == '0':
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
            
        if len(cnpj) != 14 and len(cnpj) != 11 or not cnpj.isdigit():
            print(Fore.RED + "\n[✖] ERRO: Documento inválido! Digite 11 (CPF) ou 14 (CNPJ) números." + Fore.RESET)
            continue
            
        if len(cnpj) == 14:
            doc_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        else:
            doc_formatado = f"{cnpj[:3]}.{cnpj[3:6]}.{cnpj[6:9]}-{cnpj[9:]}"
            
        endereco = force_str("Digite o endereço do cliente ou [0] para sair: ").lower()
        if endereco == '0':
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
            
        telefone = force_str("Digite o telefone do cliente ou [0] para sair (apenas números): ")
        
        if telefone == '0':
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
            
        if len(telefone) != 11 or not telefone.isdigit():
            print(Fore.RED + "\n[✖] ERRO: Quantidade de caracteres do telefone inválida (deve ter 11)." + Fore.RESET)
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
                (nome_cliente, doc_formatado, endereco, telefone_ajustado),
            )
            conexao.commit()
            
            id_gerado = cursor.lastrowid
            print(Fore.GREEN + f"\n[✔] O cliente '{nome_cliente.title()}' foi salvo com sucesso (ID: {id_gerado})! " + Fore.RESET)
            return id_gerado

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            return None
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
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
            
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                    INSERT INTO categorias(nome)
                    VALUES (%s)
                """,(nome_categoria,))
            conexao.commit()
            
            id_gerado = cursor.lastrowid
            print(Fore.GREEN + f"\n[✔] A categoria '{nome_categoria.title()}' foi salva com sucesso! " + Fore.RESET)
            return id_gerado # Retorna o número caso outra função precise dele futuramente

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            return None
        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )