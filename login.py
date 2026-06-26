import mysql.connector,random,string
from connectsql import obter_conexao, fechar_execusao,enviar_email_relatorio
from forces import force_str,force_int
from interface import limpar_tela
from colorama import Fore, Style
import pywhatkit as kit
import pyautogui
import time

def email_valido(email):
    email = email.strip()
    if email.count('@') != 1:
        return False
    usuario, dominio = email.split('@')
    if not usuario or not dominio:
        return False
    if usuario.startswith('.') or usuario.endswith('.') or dominio.startswith('.') or dominio.endswith('.'):
        return False
    if '.' not in dominio:
        return False
    partes_dominio = dominio.split('.')
    if len(partes_dominio[-1]) < 2:
        return False
    return True 

def new_user():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔═════════════════════════════════════════════════╗
║                CADASTRAR NOVO USUÁRIO           ║
╚═════════════════════════════════════════════════╝{Fore.RESET}""")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        while True:#colocar opção de sair da função e voltar ao menu
            new_user = force_str(Fore.YELLOW + "➤ Digite o nome do usuário a ser cadastrado (ou [0] para sair): " + Fore.RESET)
            if new_user == '0':
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                return None
            try:  # pergunta login e senha desejada e valida se é possivel
                senha = force_int(Fore.YELLOW + "➤ Digite a senha desejada (SOMENTE NÚMEROS): " + Fore.RESET)
            except ValueError:
                print(Fore.RED + "\n[✖] ERRO: Digite somente números para a senha." + Fore.RESET)
                continue
            while True:
                email = force_str(Fore.YELLOW + "➤ Digite o e-mail que será vinculado (ou [0] para sair): " + Fore.RESET)
                if email == '0':
                    break
                if email_valido(email):
                    break
                
                print(Fore.RED + "\n[✖] E-mail inválido! Digite um formato correto (ex: nome@exemplo.com)" + Fore.RESET)
                
            if email == '0':
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                return False
                
            try:
                chose = force_int(f"""{Fore.CYAN}{Style.BRIGHT}
┌── SELECIONE O NÍVEL DE ACESSO ──────────────────┐
│ {Fore.WHITE}[1]{Fore.CYAN} O usuário será um FUNCIONÁRIO             │
│ {Fore.WHITE}[2]{Fore.CYAN} O usuário será um ADMINISTRADOR           │
└─────────────────────────────────────────────────┘
{Fore.YELLOW}➤ Escolha uma opção: {Fore.RESET}""")
                if chose == 1:
                    cargo = "Funcionario"
                elif chose == 2:
                    cargo = "Admin"
                else:
                    print(Fore.RED + "\n[✖] ERRO: Selecione uma das duas opções apresentadas." + Fore.RESET)
                    continue
            except ValueError:
                print(Fore.RED + "\n[✖] ERRO: Selecione apenas números." + Fore.RESET)
                continue
            confirm = force_int(Fore.YELLOW + "\n➤ Para confirmar, digite a senha master de ADM (ou [0] para sair): " + Fore.RESET)
            
            if confirm == 0:
                print(Fore.YELLOW + "\n[!] Operação cancelada. Voltando ao menu..." + Fore.RESET)
                break

            elif confirm != 1234:
                print(Fore.RED + "\n[✖] ERRO: Senha de administrador inválida. Acesso negado." + Fore.RESET)
                continue

            try:
                cursor.execute(
                    """SELECT usuario,gmail FROM usuarios WHERE usuario = %s OR gmail = %s AND ativo = 1 """, (new_user,email)
                )  # carrega do banco de dados se tem algum usuario com o mesmo nome do que vai ser cadastrado
                found = cursor.fetchone()
                

                if found:  # caso já exista esse nome ele manda mostra essa mensagem e volta para o incio
                    print(Fore.RED + f"\n[✖] O nome de usuário '{new_user}' ou o e-mail já existem! Tente novamente." + Fore.RESET)
                    continue  # aqui ele volta para o começo do loop

                cursor.execute(
                    "INSERT INTO usuarios(usuario, senha, cargo, gmail) VALUES(%s,%s,%s,%s)",
                    (new_user, senha, cargo, email),
                )  # abre o banco de dados e insere na tabela usuarios as variaveis, e tudo isso ocorre
                # depois das validações
                conexao.commit()  # salva no db

                print(Fore.GREEN + Style.BRIGHT + f"\n[✔] Sucesso! Usuário '{new_user}' cadastrado como {cargo}." + Fore.RESET)
                break
            except mysql.connector.Error as erro:
                conexao.rollback()  # se der algum erro no banco de dados devolve os valores iniciais para não dar erro ou corromper arquivos e manter a integridade dos dados
                print(Fore.RED + Style.BRIGHT + f"\n[✖] Ocorrreu um erro crítico no banco de dados: {erro}" + Fore.RESET)

    finally:  # independente do que aconteça fecha o banco
        fechar_execusao(
        conexao if "conexao" in locals() else None, 
        cursor if "cursor" in locals() else None
            )

def login():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔═════════════════════════════════════════════════╗
║                   FAZER LOGIN                   ║
╚═════════════════════════════════════════════════╝{Fore.RESET}""")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        while True:
            user = force_str(Fore.YELLOW + "➤ Digite o seu usuário (ou [0] para sair): " + Fore.RESET)
            if user == "0":
                print(Fore.YELLOW + "\n[!] Voltando ao menu principal..." + Fore.RESET)
                limpar_tela()

                return None, 'voltar'

            try:
                senha = force_int(Fore.YELLOW + "➤ Digite a sua senha: " + Fore.RESET)
            except ValueError:
                print(Fore.RED + "\n[✖] Senha inválida. Use apenas números." + Fore.RESET)
                continue
            try:
                cursor.execute(
                    "SELECT id_usuario, usuario,senha,cargo FROM usuarios WHERE usuario = %s AND senha = %s AND ativo = 1",
                    (user, senha),
                )
                found = (
                    cursor.fetchone()
                )  # confere se o usuario existe e senha está correta

                if not found:
                    print(Fore.RED + "\n[✖] Login ou senha incorretos. Tente novamente." + Fore.RESET)
                    continue

                id_user, usuario, senha, cargo = found

                if cargo == "Admin": # atribui o cargo a variavel e devolve pra main para poder fazer o menu expecifico para cada um
                    print(Fore.GREEN + Style.BRIGHT + f"\n[✔] Login aprovado! Bem-vindo(a) ao painel de ADMINISTRADOR." + Fore.RESET)
                    return "Admin",id_user

                elif cargo == "Funcionario":
                    print(Fore.GREEN + Style.BRIGHT + f"\n[✔] Login aprovado! Bem-vindo(a) ao painel de FUNCIONÁRIO." + Fore.RESET)
                    return "Funcionario",id_user

            except mysql.connector.Error as erro:
                conexao.rollback()
                print(Fore.RED + Style.BRIGHT + f"\n[✖] Ocorreu um erro crítico no banco de dados: {erro}" + Fore.RESET)
    finally: 
        fechar_execusao(
        conexao if "conexao" in locals() else None, 
        cursor if "cursor" in locals() else None)

def recuperar_senha(id_operador):
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔═════════════════════════════════════════════════╗
║               RECUPERAÇÃO DE SENHA              ║
╠═════════════════════════════════════════════════╣
║ {Fore.WHITE}Esqueceu sua senha? Não se preocupe!            {Fore.CYAN}║
║ {Fore.WHITE}Vamos enviar um código de segurança de 8 dígitos{Fore.CYAN}║
║ {Fore.WHITE}para o seu e-mail ou WhatsApp cadastrado.       {Fore.CYAN}║
╚═════════════════════════════════════════════════╝{Fore.RESET}""")

    escolha = force_int(Fore.YELLOW + "➤ Como deseja receber o código? [1] E-mail | [2] WhatsApp: " + Fore.RESET)
    if escolha == 1:
        assunto = "Recuperação de Senha - Distribuidora G2"
        caracteres = string.ascii_uppercase + string.digits
        codigo_gerado = "".join(random.choices(caracteres, k=8))
        
        resposta = f"Olá!\n\nSeu código de verificação para acesso ao sistema é: {codigo_gerado}\n\nSe você não solicitou esta recuperação, por favor ignore este aviso."
        
        enviado = enviar_email_relatorio(id_operador, resposta, assunto)
            
        if not enviado:
            print(Fore.RED + "\n[✖] AVISO: Falha de comunicação. Não foi possível enviar o código via e-mail. Tente novamente." + Fore.RESET)
            return

        print(Fore.GREEN + "\n[✔] E-mail enviado com sucesso! Verifique sua caixa de entrada ou spam." + Fore.RESET)
        
        codigo_digitado = input(Fore.YELLOW + "\n➤ Digite o código de 8 dígitos que chegou no e-mail: " + Fore.RESET).strip().upper()
        
        if codigo_digitado != codigo_gerado:
            print(Fore.RED + Style.BRIGHT + "\n[✖] ERRO: Código incorreto ou expirado. Operação cancelada." + Fore.RESET)
            return
            
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE id_usuario = %s", (id_operador,))
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"""{Fore.GREEN}{Style.BRIGHT}
┌─────────────────────────────────────────────────┐
│ [✔] Identidade verificada com sucesso!          │
│ Sua senha atual é: {Fore.YELLOW}{resultado[0]:<29}{Fore.GREEN}│
└─────────────────────────────────────────────────┘{Fore.RESET}""")
            else:
                print(Fore.RED + "\n[✖] ERRO: Usuário não localizado no banco de dados." + Fore.RESET)
                
        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO FATAL: Falha ao consultar o banco de dados: {e}" + Fore.RESET)
        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )
    elif escolha == 2:
        telefone = input(Fore.YELLOW + "➤ Digite seu telefone com DDI e DDD (EX: +5511999998888): " + Fore.RESET).strip()
        if not telefone.startswith("+") or not telefone[1:].isdigit() or len(telefone) < 12:
            print(Fore.RED + "\n[✖] ERRO: Número de telefone inválido! O formato exigido é +5511999998888." + Fore.RESET)
            return
        caracteres = string.ascii_uppercase + string.digits
        codigo_gerado = "".join(random.choices(caracteres, k=8))
        
        print(Fore.CYAN + "\nPreparando envio pelo WhatsApp. Não feche o navegador que será aberto..." + Fore.RESET)
        kit.sendwhatmsg_instantly(f"{telefone}",f"Olá!\n\nSeu código de verificação para acesso ao sistema é: {codigo_gerado}\n\nSe você não solicitou esta recuperação, por favor ignore este aviso.", wait_time=10)
        time.sleep(5)
        pyautogui.press('enter')
        print(Fore.GREEN + "\n[✔] Mensagem de verificação disparada pelo WhatsApp com sucesso!" + Fore.RESET)
        
        codigo_digitado = input(Fore.YELLOW + "\n➤ Digite o código de 8 dígitos que chegou no seu WhatsApp: " + Fore.RESET).strip().upper()
        
        if codigo_digitado != codigo_gerado:
            print(Fore.RED + Style.BRIGHT + "\n[✖] ERRO: Código incorreto ou expirado. Operação cancelada." + Fore.RESET)
            return
            
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute("SELECT senha,cargo FROM usuarios WHERE id_usuario = %s", (id_operador,))
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"""{Fore.GREEN}{Style.BRIGHT}
┌─────────────────────────────────────────────────┐
│ [✔] Identidade verificada com sucesso!          │
│ Sua senha atual é: {Fore.YELLOW}{resultado[0]:<29}{Fore.GREEN}│
└─────────────────────────────────────────────────┘{Fore.RESET}""")
                if resultado[1] == "Admin":
                    return "Admin"
                else:
                    return "Funcionario"
            else:
                print(Fore.RED + "\n[✖] ERRO: Usuário não localizado no banco de dados." + Fore.RESET)
                
        except mysql.connector.Error as e:
            print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO FATAL: Falha ao consultar o banco de dados: {e}" + Fore.RESET)
        finally:
            fechar_execusao(
                conexao if "conexao" in locals() else None, 
                cursor if "cursor" in locals() else None
            )
    else:
        print(Fore.RED + "\n[✖] ERRO: Escolha uma opção válida!" + Fore.RESET)
        return