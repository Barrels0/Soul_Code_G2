import mysql.connector
from connectsql import obter_conexao, enviar_email_relatorio, fechar_execusao
from forces import force_float, force_int, force_str, bsc_id
import subprocess
import sys
import os
from colorama import Fore, Style

def abrir_dashboard():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
{"═" * 50}
       DASHBOARD ANALYTICS ATIVO      
{"═" * 50}
  O painel está rodando no seu navegador.
  Pressione [CTRL + C] para encerrar e voltar ao menu.
{"═" * 50}
{Fore.RESET}""")
    
    caminho_script = os.path.join("marketing_fornecedores", "analytics.py")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", caminho_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except KeyboardInterrupt:
        print(f"""{Fore.YELLOW}
{"─" * 40}
  Dashboard finalizado com sucesso.
  Retornando ao menu principal...
{"─" * 40}
{Fore.RESET}""")
    except Exception as e:
        print(Fore.RED + f"\n Erro crítico ao iniciar o dashboard: {e}" + Fore.RESET)
        
        
def cadastrar_fornecedor():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO FORNECEDOR{Fore.CYAN}                                         █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    while True:
        nome = force_str("➤ Nome da empresa/fornecedor (0 para sair): ").title()
        if nome == "0":
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
        pais = force_str("➤ País de origem (0 para sair): ").title()
        if pais == "0":
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
        estado = force_str("➤ Estado (UF) (0 para sair): ").upper()
        if estado == "0":
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None
        cidade = force_str("➤ Cidade (0 para sair): ").title()
        if cidade == "0":
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return None

        if not nome or not pais or not estado or not cidade:
            print(Fore.RED + "\nERRO: Todos os campos são obrigatórios para o cadastro." + Fore.RESET)
            return None

        conexao = obter_conexao()
        if not conexao:
            print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
            return None
            
        cursor = conexao.cursor()

        try:
            query = """
                INSERT INTO fornecedores (nome, pais, estado, cidade)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (nome, pais, estado, cidade))
            conexao.commit()

            id_gerado = cursor.lastrowid
            print(Fore.GREEN + f"\n[✔] Sucesso! O fornecedor '{nome}' foi registrado com o ID {id_gerado}." + Fore.RESET)
            return id_gerado  

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO DE BANCO DE DADOS: {erro}" + Fore.RESET)
            return None

        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )

def cadastrar_cupom():
    print(f"""{Fore.CYAN}{Style.BRIGHT}     
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}CADASTRAR NOVO CUPOM{Fore.CYAN}                                              █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    while True:
        nome_cupom = force_str("➤ Digite o código do cupom (Ex: PROMO10) ou 0 para sair: ").upper()
        if nome_cupom == "0":
            print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
            return
            
        if not nome_cupom:
            print(Fore.RED + "\nERRO: O nome do cupom não pode ficar em branco." + Fore.RESET)
            continue

        try:
            desconto = force_float("➤ Digite a porcentagem de desconto (Ex: 15.50) ou 0 para sair: ")
            if desconto == 0:
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                return
                
            quantidade = force_int("➤ Qual a quantidade de usos permitidos para este cupom? (0 para sair) ")
            if quantidade == 0:
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                return

            if desconto < 0 or desconto > 99 or quantidade < 0:
                print(Fore.RED + "\nERRO: Valores inválidos. O desconto deve ser entre 1 e 99." + Fore.RESET)
                continue

        except ValueError:
            print(Fore.RED + "\nERRO: Utilize apenas números para o desconto e para a quantidade." + Fore.RESET)
            continue

        conexao = obter_conexao()
        if not conexao:
            print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
            return
            
        cursor = conexao.cursor()

        try:
            query = """
                INSERT INTO cupons (nome, desconto, quantidade)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (nome_cupom, desconto, quantidade))
            conexao.commit()

            print(Fore.GREEN + f"\n[✔] Sucesso! O cupom '{nome_cupom}' foi criado e liberado para {quantidade} usos." + Fore.RESET)

        except mysql.connector.IntegrityError:
            print(Fore.RED + f"\n[✖] ERRO: O cupom '{nome_cupom}' já existe no banco de dados. Escolha outro código." + Fore.RESET)

        except mysql.connector.Error as e:
            conexao.rollback()
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)

        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )

def promocoes():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}MENU DE PROMOÇÕES{Fore.CYAN}                                                 █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Aplicar/Alterar desconto em um único item
 {Fore.WHITE}[2]{Fore.CYAN} Aplicar desconto para TODOS os itens
 {Fore.WHITE}[3]{Fore.CYAN} Aplicar desconto por Categoria
 {Fore.WHITE}[4]{Fore.CYAN} REMOVER desconto de TODOS os itens
 {Fore.RED}[0]{Fore.CYAN} Voltar ao menu principal
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")

        escolha_promo = force_int(Fore.YELLOW + "\n➤ Escolha uma opção: " + Fore.RESET)

        if escolha_promo == 0:
            print(Fore.YELLOW + "\n[!] Voltando..." + Fore.RESET)
            break

        elif escolha_promo == 1:
            desconto = force_float("➤ Porcentagem de desconto (Ex: 10 para 10%): ")
            if not (0 <= desconto < 100):
                print(Fore.RED + "[✖] ERRO: Desconto inválido! Deve ser entre 0 e 99." + Fore.RESET)
                continue

            try:
                id_produto = bsc_id()
            except ValueError:
                print(Fore.RED + "[✖] ERRO: ID inválido!" + Fore.RESET)
                continue
                
            conexao = obter_conexao()
            if not conexao:
                print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
                continue
                
            cursor = conexao.cursor()
            
            try:
                cursor.execute(
                    "UPDATE produtos SET desconto = %s WHERE id_produto = %s AND ativo = 1",
                    (desconto, id_produto)
                )
                conexao.commit()
                print(Fore.GREEN + f"\n[✔] Desconto de {desconto}% salvo com sucesso no produto de ID {id_produto}!" + Fore.RESET)
            except mysql.connector.Error as e:
                conexao.rollback()
                print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            finally:
                fechar_execusao(
                    conexao if "conexao" in locals() else None, 
                    cursor if "cursor" in locals() else None
                )

        elif escolha_promo == 2:
            desconto = force_float("➤ Porcentagem de desconto GERAL (Ex: 10 para 10%): ")
            if not (0 <= desconto < 100):
                print(Fore.RED + "[✖] ERRO: Desconto inválido! Deve ser entre 0 e 99." + Fore.RESET)
                continue

            confirmar = force_str(Fore.YELLOW + "➤ TEM CERTEZA que deseja aplicar esse desconto em TODOS os produtos? (S/N): " + Fore.RESET).upper()
            if confirmar not in ["S", "SIM"]:
                print(Fore.YELLOW + "Operação cancelada." + Fore.RESET)
                continue

            conexao = obter_conexao()
            if not conexao:
                print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
                continue
                
            cursor = conexao.cursor()
            
            try:
                cursor.execute("UPDATE produtos SET desconto = %s WHERE ativo = 1", (desconto,))
                conexao.commit()
                print(Fore.GREEN + f"\n[✔] MEGA DESCONTO! Todos os produtos agora estão com {desconto}% OFF!" + Fore.RESET)
            except mysql.connector.Error as e:
                conexao.rollback()
                print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            finally:
                fechar_execusao(
                    conexao if "conexao" in locals() else None, 
                    cursor if "cursor" in locals() else None
                )

        elif escolha_promo == 3:
            conexao = obter_conexao()
            if not conexao:
                print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
                continue
                
            cursor = conexao.cursor()

            try:
                print(Fore.CYAN + "\n--- CATEGORIAS DISPONÍVEIS ---" + Fore.RESET)
                cursor.execute("SELECT id_categoria, nome FROM categorias")
                categorias = cursor.fetchall()

                if not categorias:
                    print(Fore.RED + "Nenhuma categoria cadastrada no sistema." + Fore.RESET)
                    continue

                for i in categorias:
                    print(f"[{i[0]}] - {i[1]}")

                id_categoria = force_int("\n➤ Digite o [ID] da categoria que receberá o desconto: ")

                desconto = force_float("➤ Porcentagem de desconto (Ex: 10 para 10%): ")
                
                if not (0 <= desconto < 100):
                    print(Fore.RED + "[✖] ERRO: Desconto inválido! Deve ser entre 0 e 99." + Fore.RESET)
                    continue
                    
                cursor.execute(
                    "UPDATE produtos SET desconto = %s WHERE id_categoria = %s AND ativo = 1",
                    (desconto, id_categoria)
                )
                conexao.commit()
                print(Fore.GREEN + f"\n[✔] Desconto de {desconto}% aplicado a todos os produtos da categoria {id_categoria}!" + Fore.RESET)

            except mysql.connector.Error as e:
                conexao.rollback()
                print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
            finally:
                fechar_execusao(
                    conexao if "conexao" in locals() else None, 
                    cursor if "cursor" in locals() else None
                )

        elif escolha_promo == 4:
            confirmar = force_str(Fore.YELLOW + "➤ TEM CERTEZA que deseja ZERAR os descontos de TODOS os produtos? (S/N): " + Fore.RESET).upper()
            
            if confirmar in ["S", "SIM"]:
                conexao = obter_conexao()
                if not conexao:
                    print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
                    continue
                    
                cursor = conexao.cursor()
                try:
                    cursor.execute("UPDATE produtos SET desconto = 0")
                    conexao.commit()
                    print(Fore.GREEN + "\n[✔] Todos os descontos foram removidos. Preços originais restaurados!" + Fore.RESET)
                except mysql.connector.Error as e:
                    conexao.rollback()
                    print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)
                finally:
                    fechar_execusao(
                        conexao if "conexao" in locals() else None, 
                        cursor if "cursor" in locals() else None
                    )

        else:
            print(Fore.RED + "\n[✖] Opção inválida!" + Fore.RESET)

def relatorio_cupons_mais_utilizados():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}RANKING: CUPONS MAIS UTILIZADOS{Fore.CYAN}                                   █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

    conexao = obter_conexao()
    if not conexao:
        print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
        return

    cursor = conexao.cursor()

    try:
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
            print(Fore.YELLOW + "\nNenhum cupom foi utilizado em vendas até o momento." + Fore.RESET)
            return

        print(Fore.CYAN + f"\n{'CÓDIGO DO CUPOM':<20} | {'USOS':<5} | {'RECEITA ATRELADA'}")
        print("-" * 48 + Fore.RESET)

        for linha in resultados:
            nome_cupom = linha[0]
            usos = linha[1]
            receita = linha[2]
            print(f"{nome_cupom:<20} | {usos:<5} | R$ {receita:.2f}")

        print(Fore.CYAN + "-" * 48 + Fore.RESET)

    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {e}" + Fore.RESET)

    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )

def reclame_aqui(id_operador):
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}RECLAME AQUI{Fore.CYAN}                                                      █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 
 {Fore.WHITE}Utilize este canal para nos enviar críticas,
 dicas ou sugestões de melhoria para o sistema.
 ──────────────────────────────────────────────────────────────────────{Fore.RESET}""")
        
        assunto = force_str(Fore.YELLOW + "➤ Digite o assunto da mensagem ou [0] para sair: " + Fore.RESET)
        if assunto == "0":
            print(Fore.YELLOW + "\nSaindo do canal de atendimento..." + Fore.RESET)
            break
            
        resposta = force_str(Fore.YELLOW + "➤ Digite sua mensagem detalhada: \n> " + Fore.RESET)
        if resposta == "0":
            print(Fore.YELLOW + "\nSaindo do canal de atendimento..." + Fore.RESET)
            break
            
        if not resposta or not assunto:
            print(Fore.RED + "\n[✖] AVISO: A mensagem e o assunto não podem estar vazios." + Fore.RESET)
            continue 
            
        enviado = enviar_email_relatorio(id_operador, resposta, assunto)
        
        if enviado:
            print(Fore.CYAN + "\n" + "-" * 50)
            print(Fore.GREEN + "[✔] Mensagem enviada! Agradecemos o seu feedback." + Fore.RESET)
            break 
        else:
            print(Fore.RED + "\n[✖] AVISO: O envio falhou. Tente novamente mais tarde." + Fore.RESET)
            break

def teste_qualidade(id_produto):
    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}TESTE DE QUALIDADE (AVALIAÇÃO){Fore.CYAN}                                    █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")

    conexao = obter_conexao()
    if not conexao:
        print(Fore.RED + "\n[✖] Erro de conexão com o banco de dados." + Fore.RESET)
        return False
        
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT nome, nota FROM produtos WHERE id_produto = %s", (id_produto,))
        resultado = cursor.fetchone()

        if not resultado:
            print(Fore.RED + "\n[✖] ERRO: Produto não encontrado no sistema." + Fore.RESET)
            return False

    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao banco de dados: {e}" + Fore.RESET)
        return False
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )

    nome_produto = resultado[0]
    nota = float(resultado[1]) if resultado[1] is not None else 0.0

    print(Fore.WHITE + f"\n➤ Analisando o item: {nome_produto}" + Fore.RESET)
    
    if nota >= 4.5:
        print(Fore.GREEN + f"Produto excelente (Nota {nota:.1f})! Qualidade máxima garantida." + Fore.RESET)
    elif 3.5 <= nota < 4.5:
        print(Fore.CYAN + f"Produto muito bom (Nota {nota:.1f}). Ótima aceitação pelos clientes." + Fore.RESET)
    elif 2.5 <= nota < 3.5:
        print(Fore.WHITE + f"Produto regular (Nota {nota:.1f}). Pode conter pequenas variações." + Fore.RESET)
    elif 1.0 <= nota < 2.5:
        print(Fore.YELLOW + f"ATENÇÃO: Produto mal avaliado (Nota {nota:.1f}). Considere alertar o cliente." + Fore.RESET)
    elif 0 < nota < 1.0:
        print(Fore.RED + Style.BRIGHT + f"PERIGO: Produto péssimo (Nota {nota:.1f}). A loja não se responsabiliza por defeitos!" + Fore.RESET)
    else:
        print(Fore.WHITE + "Produto ainda não avaliado. Sem histórico de reclamações." + Fore.RESET)

    confirmacao = force_str(Fore.YELLOW + "\n➤ Deseja prosseguir com a compra deste item? (S/N): " + Fore.RESET).upper()

    if confirmacao in ("SIM", "S"):
        print(Fore.GREEN + "[✔] Qualidade aceita pelo operador. Prosseguindo..." + Fore.RESET)
        return True
    else:
        print(Fore.RED + "[✖] Operação cancelada pelo operador por critérios de qualidade." + Fore.RESET)
        return False