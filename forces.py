# USAR O BSC_ID EM TUDO!!!!!!!!!
import mysql.connector
from connectsql import obter_conexao
from colorama import Fore, Style


def force_int(message: str) -> int:
    while True:
        try:
            return int(input(Fore.YELLOW + message + Fore.RESET))
        except:
            print(Fore.RED + "\n[✖] ERRO: Digite um número inteiro válido." + Fore.RESET)
            continue


def force_float(message: str) -> float:
    while True:
        try:
            entrada = input(Fore.YELLOW + message + Fore.RESET).strip()
            entrada_corrigida = entrada.replace(",", ".")
            return float(entrada_corrigida)
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: Digite um número decimal válido (Ex: 15.50 ou 15,50)." + Fore.RESET)


def force_str(message: str) -> str:
    while True:
        try:
            return str(input(Fore.YELLOW + message + Fore.RESET)).strip()
        except:
            print(Fore.RED + "\n[✖] ERRO: Digite um texto válido." + Fore.RESET)
            continue


def bsc_id(mensagem="➤ Digite o [ID] do produto (ou [0] para sair): ") -> int:    
    while True:
        try:
            id_venda = force_int(mensagem)
        except ValueError:
            print(Fore.RED + "\n[✖] ERRO: O ID deve ser um número inteiro!" + Fore.RESET)
            continue
        if id_venda == 0:
            break    
        conexao = obter_conexao()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT id_produto FROM produtos WHERE id_produto = %s AND ativo = 1",
                (id_venda,),
            )
            bebida_encontrada = cursor.fetchone()

            if not bebida_encontrada:
                print(Fore.RED + Style.BRIGHT + "\n[✖] ERRO: ID INVÁLIDO. Essa bebida não existe no sistema." + Fore.RESET)
                continue

            return id_venda

        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO no banco de dados: {e}" + Fore.RESET)
            break
        finally:
            cursor.close()
            conexao.close()