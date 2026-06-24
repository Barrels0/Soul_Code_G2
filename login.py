import mysql.connector,random,string
from connectsql import obter_conexao, fechar_execusao,enviar_email_relatorio
from forces import force_str,force_int


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
    print("\nCadastrar usuário")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        while True:#colocar opção de sair da função e voltar ao menu
            new_user = force_str("Digite o nome do usuário que vai ser cadastrado ou [0] para sair: ")
            if new_user == '0':
                print("Voltando")
                break
            try:  # pergunta login e senha desejada e valida se é possivel
                senha = force_int("Digite a senha que deseja SOMENTE números: ")
            except ValueError:
                print("Digite somente números para a senha")
                continue
            email = force_str("Digite o email que vai ser cadastrado ou [0] para sair: ")
            if email == '0':
                break

            if not email_valido(email):
                print("E-mail inválido! Digite um formato correto (ex: nome@exemplo.com)")
            
            try:
                chose = force_int("""
        SELECIONE UMA DAS SEGUINTES OPÇÕES
                                
        [1] ESSE USUARIO SERÁ UM FUNCIONARIO
                                
        [2] ESSE USUARIO É ADMIN\n->""")
                if chose == 1:
                    cargo = "Funcionario"
                elif chose == 2:
                    cargo = "Admin"
                else:
                    print("ERRO selecione uma das duas opções apresentadas")
                    continue
            except ValueError:
                print("Selecione apenas números")
                continue
            confirm = force_int("Para continuar digite a senha de confirmação ou para sair digite [0]: ")
            
            if confirm == 0:
                print("Voltando ao menu")
                break

            elif confirm != 1234:
                print("Senha de adm invalida")
                continue

            try:
                cursor.execute(
                    """SELECT usuario,gmail FROM usuarios WHERE usuario = %s OR gmail = %s """, (new_user,email)
                )  # carrega do banco de dados se tem algum usuario com o mesmo nome do que vai ser cadastrado
                found = cursor.fetchone()
                

                if found:  # caso já exista esse nome ele manda mostra essa mensagem e volta para o incio
                    print(f"Esse nome de usuário {new_user} ou email já existe, tente um novo nome")
                    continue  # aqui ele volta para o começo do loop

                cursor.execute(
                    "INSERT INTO usuarios(usuario, senha, cargo, gmail) VALUES(%s,%s,%s,%s)",
                    (new_user, senha, cargo, email),
                )  # abre o banco de dados e insere na tabela usuarios as variaveis, e tudo isso ocorre
                # depois das validações
                conexao.commit()  # salva no db

                print("Usuário cadastrado com sucesso")
                break
            except mysql.connector.Error as erro:
                conexao.rollback()  # se der algum erro no banco de dados devolve os valores iniciais para não dar erro ou corromper arquivos e manter a integridade dos dados
                print(f"Ocorrreu um erro no banco de dados erro:{erro}")

    finally:  # independente do que aconteça fecha o banco
        fechar_execusao(
        conexao if "conexao" in locals() else None, 
        cursor if "cursor" in locals() else None
            )


def login():
    print("\n INSIRA OS DADOS SOLICITADOS ABAIXO PARA FAZER O LOGIN")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    while True:
        user = force_str("Digite o nome do usuário ou [0] para sair: ")
        if user == "0":
            print("Voltando ao menu")
            break

        try:
            senha = force_int("Digite a senha: ")
        except ValueError:
            print("Senha invalida tente novamente")
            continue
        try:
            cursor.execute(
                "SELECT id_usuario, usuario,senha,cargo FROM usuarios WHERE usuario = %s AND senha = %s",
                (user, senha),
            )
            found = (
                cursor.fetchone()
            )  # confere se o usuario existe e senha está correta

            if not found:
                print("Login ou senha invalida, tente novamente")
                continue

            id_user, usuario, senha, cargo = found

            if cargo == "Admin": # atribui o cargo a variavel e devolve pra main para poder fazer o menu expecifico para cada um
                print("Usuário logado é um ADMIN")
                return "Admin",id_user

            elif cargo == "Funcionario":
                print("Usuário logado é um FUNCIONARIO")
                return "Funcionario",id_user

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Ocorrreu um erro no banco de dados erro:{erro}")
        finally: 
            fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

def recuperar_senha(id_operador):
    print("\n" + "=" * 50)
    print("               RECUPERAÇÃO DE SENHA               ")
    print("=" * 50)
    print("Esqueceu sua senha? Não se preocupe!")
    print("Vamos enviar um código de segurança de 8 caracteres")
    print("para o e-mail cadastrado na sua conta.")
    print("-" * 50)

    assunto = "Recuperação de Senha - Distribuidora G2"
    caracteres = string.ascii_uppercase + string.digits
    codigo_gerado = "".join(random.choices(caracteres, k=8))
    
    resposta = f"Olá!\n\nSeu código de verificação para acesso ao sistema é: {codigo_gerado}\n\nSe você não solicitou esta recuperação, por favor ignore este aviso."
    
    enviado = enviar_email_relatorio(id_operador, resposta, assunto)
        
    if not enviado:
        print("\nAVISO: Falha de comunicação. Não foi possível enviar o código. Tente novamente mais tarde.")
        return

    print("\nE-mail enviado com sucesso!")
    
    codigo_digitado = input("Digite o código que chegou no seu e-mail: ").strip().upper()
    
    if codigo_digitado != codigo_gerado:
        print("\nERRO: Código incorreto ou expirado. Operação cancelada.")
        return
        
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT senha FROM usuarios WHERE id_usuario = %s", (id_operador,))
        resultado = cursor.fetchone()
        
        if resultado:
            print("\n" + "-" * 50)
            print(f"Verificação realizada com sucesso!")
            print(f"Sua senha atual é: {resultado[0]}")
            print("-" * 50)
        else:
            print("\nERRO: Usuário não localizado no sistema.")
            
    except mysql.connector.Error as e:
        print(f"\nERRO FATAL: Falha ao consultar o banco de dados: {e}")
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )
