import mysql.connector
from connectsql import obter_conexao,enviar_email_relatorio
from forces import force_float, force_int, force_str, bsc_id
import subprocess
import sys
import os


def abrir_dashboard():

    
    print("\n" + "═" * 50)
    print("       DASHBOARD ANALYTICS ATIVO      ")
    print("═" * 50)
    print("  O painel está rodando no seu navegador.")
    print("  Pressione [CTRL + C] para encerrar e voltar ao menu.")
    print("═" * 50 + "\n")
    
    caminho_script = os.path.join("marketing_fornecedores", "analytics.py")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", caminho_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except KeyboardInterrupt:
        
        print("\n" + "─" * 40)
        print("  Dashboard finalizado com sucesso.")
        print("  Retornando ao menu principal...")
        print("─" * 40 + "\n")
    except Exception as e:
        print(f"\n Erro crítico ao iniciar o dashboard: {e}")
        
        
def cadastrar_fornecedor():
    print("\n════════ CADASTRAR NOVO FORNECEDOR ════════")
    nome = force_str("Nome da empresa/fornecedor: ")
    pais = force_str("País de origem: ")
    estado = force_str("Estado (UF): ")
    cidade = force_str("Cidade: ")

    if not nome or not pais or not estado or not cidade:
        print("\nERRO: Todos os campos são obrigatórios para o cadastro.")
        return None

    try:
        conexao = obter_conexao()
        if not conexao:
            return None

        cursor = conexao.cursor()

        query = """
            INSERT INTO fornecedores (nome, pais, estado, cidade)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (nome, pais, estado, cidade))
        conexao.commit()

        print(
            f"\nSucesso! O fornecedor '{nome}' foi registrado com o ID {cursor.lastrowid}."
        )

        return cursor.lastrowid  

    except Exception as erro:
        print(f"\nERRO DE BANCO DE DADOS: {erro}")
        if "conexao" in locals() and conexao is not None:
            conexao.rollback()

        return None

    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conexao" in locals() and conexao is not None:
            conexao.close()

def cadastrar_cupom():
    print("\n════════ CADASTRAR NOVO CUPOM ════════")
    nome_cupom = force_str("Digite o código do cupom (Ex: PROMO10): ").upper()

    if not nome_cupom:
        print("\nERRO: O nome do cupom não pode ficar em branco.")
        return

    try:
        desconto = force_float("Digite o valor/porcentagem de desconto (Ex: 15.50): ")
        quantidade = force_int("Qual a quantidade de usos permitidos para este cupom? ")

        if desconto <= 0 or desconto > 99 or quantidade <= 0:
            print("\nERRO: O desconto e a quantidade devem ser maiores que zero.")
            return

    except ValueError:
        print("\nERRO: Utilize apenas números para o desconto e para a quantidade.")
        return

    try:
        conexao = obter_conexao()
        if not conexao:
            return

        cursor = conexao.cursor()

        query = """
            INSERT INTO cupons (nome, desconto, quantidade)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (nome_cupom, desconto, quantidade))
        conexao.commit()

        print(
            f"\nSucesso! O cupom '{nome_cupom}' foi criado e está liberado para {quantidade} usos."
        )

    except mysql.connector.IntegrityError:
        print(
            f"\nERRO: O cupom '{nome_cupom}' já existe no banco de dados. Escolha outro código."
        )

    except mysql.connector.Error as erro:
        print(f"\nERRO DE BANCO DE DADOS: {erro}")
        if "conexao" in locals() and conexao is not None:
            conexao.rollback()

    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conexao" in locals() and conexao is not None:
            conexao.close()

def promocoes():
    while True:
        print("\n" + "=" * 40)
        print("          MENU DE PROMOÇÕES          ")
        print("=" * 40)
        print("""
        [1] Aplicar/Alterar desconto em um único item
        [2] Aplicar desconto para TODOS os itens
        [3] Aplicar desconto por Categoria
        [4] REMOVER desconto de TODOS os itens
        [0] Voltar
        """)

        escolha_promo = force_int("\nEscolha uma opção: ")

        if escolha_promo == 0:
            break

        elif escolha_promo == 1:
            desconto = force_float("Porcentagem de desconto (Ex: 10 para 10%): ")
            if not (0 <= desconto < 100):
                print("ERRO: Desconto inválido! Deve ser entre 0 e 99.")
                continue

            try:
                id_produto = bsc_id()
            except ValueError:
                print("ERRO: ID inválido!")
                continue
                
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                conexao.start_transaction()
                
                cursor.execute(
                    "UPDATE produtos SET desconto = %s WHERE id_produto = %s AND ativo = 1",
                    (desconto, id_produto)
                )
                conexao.commit()
                print("Desconto salvo com sucesso no produto!")
            except mysql.connector.Error as e:
                conexao.rollback()
                print(f"Erro ao acessar o banco de dados: {e}")
            finally:
                if "cursor" in locals() and cursor is not None:
                    cursor.close()
                if "conexao" in locals() and conexao is not None:
                    conexao.close()

        elif escolha_promo == 2:
            desconto = force_float("Porcentagem de desconto GERAL (Ex: 10 para 10%): ")
            if not (0 <= desconto < 100):
                print("ERRO: Desconto inválido! Deve ser entre 0 e 99.")
                continue

            confirmar = force_str("TEM CERTEZA que deseja aplicar esse desconto em TODOS os produtos? (S/N): ").upper()
            if confirmar not in ["S", "SIM"]:
                print("Operação cancelada.")
                continue

            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                conexao.start_transaction()
                cursor.execute("UPDATE produtos SET desconto = %s AND ativo = 1", (desconto,))
                conexao.commit()
                print("Desconto aplicado com sucesso a TODOS os produtos!")
            except mysql.connector.Error as e:
                conexao.rollback()
                print(f"Erro ao acessar o banco de dados: {e}")
            finally:
                if "cursor" in locals() and cursor is not None:
                    cursor.close()
                if "conexao" in locals() and conexao is not None:
                    conexao.close()

        elif escolha_promo == 3:
            conexao = obter_conexao()
            cursor = conexao.cursor()

            try:
                print("\n--- CATEGORIAS DISPONÍVEIS ---")
                cursor.execute("SELECT id_categoria, nome_categoria FROM categorias")
                categorias = cursor.fetchall()

                if not categorias:
                    print("Nenhuma categoria cadastrada no sistema.")
                    continue

                for i in categorias:
                    print(f"[{i[0]}] - {i[1]}")

                id_categoria = force_int("\nDigite o [ID] da categoria que receberá o desconto: ")

                desconto = force_float("Porcentagem de desconto (Ex: 10 para 10%): ")
                if not (0 <= desconto < 100):
                    print("ERRO: Desconto inválido! Deve ser entre 0 e 99.")
                    continue
                conexao.start_transaction()
                cursor.execute(
                    "UPDATE produtos SET desconto = %s WHERE id_categoria = %s AND ativo = 1",
                    (desconto, id_categoria)
                )
                conexao.commit()
                print(f"Desconto de {desconto}% aplicado a todos os produtos da categoria {id_categoria}!")

            except mysql.connector.Error as e:
                conexao.rollback()
                print(f"Erro: ocorreu um erro: {e}")
            finally:
                if "cursor" in locals() and cursor is not None:
                    cursor.close()
                if "conexao" in locals() and conexao is not None:
                    conexao.close()
                
        elif escolha_promo == 4:
            confirmar = force_str("TEM CERTEZA que deseja ZERAR os descontos de TODOS os produtos? (S/N): ").upper()
            if confirmar in ["S", "SIM"]:
                conexao = obter_conexao()
                cursor = conexao.cursor()
                try:
                    conexao.start_transaction()
                    cursor.execute("UPDATE produtos SET desconto = 0")
                    conexao.commit()
                    print("Todos os descontos foram removidos. Preços originais restaurados!")
                except mysql.connector.Error as e:
                    conexao.rollback()
                finally:
                    if "cursor" in locals() and cursor is not None:
                        cursor.close()
                    if "conexao" in locals() and conexao is not None:
                        conexao.close()

        else:
            print("Opção inválida!")
            continue

def relatorio_cupons_mais_utilizados():
    print("\nRANKING: CUPONS MAIS UTILIZADOS")
    print("-" * 40)

    try:
        conexao = obter_conexao()
        if not conexao:
            return

        cursor = conexao.cursor()

        query = """
            SELECT 
                c.nome, 
                COUNT(v.id_venda) AS total_usos,
                SUM(v.valor_total) AS receita_gerada
            FROM 
                vendas v
            INNER JOIN 
                cupons c ON v.id_cupom = c.id_cupom
            GROUP BY 
                c.id_cupom, c.nome
            ORDER BY 
                total_usos DESC
            LIMIT 5
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhum cupom foi utilizado em vendas até o momento.")
            return

        print(f"{'CÓDIGO DO CUPOM':<20} | {'USOS':<5} | {'RECEITA ATRELADA'}")
        print("-" * 40)

        for linha in resultados:
            nome_cupom = linha[0]
            usos = linha[1]
            receita = linha[2]
            print(f"{nome_cupom:<20} | {usos:<5} | R$ {receita:.2f}")

        print("-" * 40)

    except mysql.connector.Error as erro:
        print(f"\nERRO AO GERAR RELATÓRIO: {erro}")

    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conexao" in locals() and conexao is not None:
            conexao.close()


def reclame_aqui(id_operador):
    while True:
        print("\n" + "=" * 50)
        print("                 RECLAME AQUI                 ")
        print("=" * 50)
        print("Utilize este canal para nos enviar criticas,")
        print("dicas ou sugestoes de melhoria para o sistema.")
        print("-" * 50)
        assunto = input("Digite o assunto da mensagem: ").strip()
        resposta = input("Digite sua mensagem (ou '0' para sair): \n> ").strip()
        
        if resposta == "0":
            print("\nSaindo do canal de atendimento...")
            break
            
        if not resposta:
            print("\nAVISO: A mensagem nao pode estar vazia.")
            print("Por favor, digite um texto valido.")
            continue 
            
        enviado = enviar_email_relatorio(id_operador, resposta, assunto)
        
        if enviado:
            print("-" * 50)
            print("Agradecemos o seu feedback! Ele é muito importante.")
            break 
        else:
            print("\nAVISO: O envio falhou. Tente novamente mais tarde.")
            break

def teste_qualidade(id_produto):
    print("\n" + "=" * 40)
    print("      TESTE DE QUALIDADE (AVALIAÇÃO)      ")
    print("=" * 40)

    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute(
            "SELECT nome, nota FROM produtos WHERE id_produto = %s", 
            (id_produto,)
        )
        resultado = cursor.fetchone()

        if not resultado:
            print("ERRO: Produto não encontrado no sistema.")
            return False

    except mysql.connector.Error as e:
        print(f"Ocorreu um erro no banco de dados: {e}")
        return False
    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conexao" in locals() and conexao is not None:
            conexao.close()

    print(f"Analisando o item: {resultado[0]}")
    
    if resultado[1] == 5:
        print(f"Produto excelente (Nota {resultado[1]})! Qualidade máxima garantida.")
    elif resultado[1] > 3 and resultado[1] < 5:
        print(f"Produto muito bom (Nota {resultado[1]}). Ótima aceitação pelos clientes.")
    elif resultado[1] > 2 and resultado[1] < 4:
        print(f"Produto com avaliação regular (Nota {resultado[1]}). Pode conter pequenas variações.")
    elif resultado[1] > 1 and resultado[1] < 3:
        print(f"ATENÇÃO: Produto mal avaliado (Nota {resultado[1]}). Considere alertar o cliente.")
    elif resultado[1] >= 1 and resultado[1] <= 0:
        print(f"PERIGO: Produto péssimo (Nota {resultado[1]}). A adega não se responsabiliza por defeitos!")
    else:
        print("Produto ainda não avaliado (Nota 0). Sem histórico de reclamações.")

    confirmacao = force_str(
        "\nDeseja prosseguir com a compra deste item? (S/N): "
    ).upper()

    if confirmacao in ("SIM", "S"):
        print("-> Qualidade aceita pelo operador. Prosseguindo...")
        return True
    else:
        print("-> Operação cancelada pelo operador por critérios de qualidade.")
        return False