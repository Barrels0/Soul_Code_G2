import os
import mysql.connector
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from colorama import Fore, Style

load_dotenv()

def obter_conexao():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        return conexao
    except mysql.connector.Error as erro:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha ao conectar ao banco de dados: {erro}" + Fore.RESET)
        return None
    
def executar_query(conexao, cursor, query, parametros=None):
    if not conexao or not cursor:
        raise Exception("Conexão com o banco não está estabelecida.")

    if parametros:
        cursor.execute(query, parametros)
    else:
        cursor.execute(query)

def fechar_execusao(conexao, cursor):
    if cursor is not None:
        try:
            cursor.close()
        except Exception:
            pass

    if conexao is not None and conexao.is_connected():
        try:
            conexao.close()
        except Exception:
            pass

def enviar_email_relatorio(id_operador, resposta, assunto):
    
    # Uso do getenv para puxar a variavel do arquivo env onde existe uma senha para essa função funcionar!
    email_origem = "viniciusgsales789@gmail.com" 
    senha_app = os.getenv("GMAIL")
    
    # Trava de segurança para o conexão funcionar corretamente
    conexao = obter_conexao()
    if not conexao:
        print(Fore.RED + Style.BRIGHT + "\n[✖] ERRO: Sistema offline. Não foi possível acessar os dados para enviar o e-mail." + Fore.RESET)
        return False
        
    cursor = conexao.cursor()
    
    try:
        # Para buscar o e-mail do usuário logado, utilizo o %s
        # isso impede tentativas de injeção de SQL no banco de dados.
        cursor.execute("SELECT gmail FROM usuarios WHERE id_usuario = %s AND ativo = 1", (id_operador,))
        result = cursor.fetchone()
        
        if not result:
            print(Fore.RED + Style.BRIGHT + "\n[✖] ERRO: E-mail do usuário não localizado no sistema." + Fore.RESET)
            return False
            
        destinatario = result[0]
        
    # Ofinally garante o fechamente do banco de dados caso QUALQUER coisa der errado porque é tratado como uma função de prioridade 
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )
    
    # Para montar a estrutura do e-mail, usei a classe EmailMessage para o codigo ficar mais seguro e limpo
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg.set_content(resposta)

    try:
        print(Fore.YELLOW + "\n[!] Processando o envio da mensagem, aguarde..." + Fore.RESET)
        
        # O bloco 'with' abre a conexão SMTP(serve para que o codigo consiga conversar com o servidor a partir de uma porta) e já fecha sozinho quando termina. 
        # O comando starttls cria um túnel criptografado para o envio seguro(ferramenta obrigatoria quando falamos de GMAIL)
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(email_origem, senha_app)
            servidor.send_message(msg)
            
        print(Fore.GREEN + f"\n[✔] SUCESSO: E-mail enviado para {destinatario}." + Fore.RESET)
        return True
    
    #separei os erros, caso for na rede ou SMPT ele avisa, mas caso não funcione acionei o protocolo padrão de erro que usamos em todo o codigo
    except smtplib.SMTPException as erro_smtp:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Falha na conexão de rede/e-mail: {erro_smtp}" + Fore.RESET)
        return False
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] ERRO: Ocorreu um erro inesperado ao enviar o e-mail: {e}" + Fore.RESET)
        return False