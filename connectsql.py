import os,string,random
import mysql.connector
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
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
        print(f"Erro ao conectar ao banco de dados: {erro}")
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
    email_origem = "viniciusgsales789@gmail.com" 
    senha_app = os.getenv("GMAIL")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT gmail FROM usuarios WHERE id_usuario = %s", (id_operador,))
        result = cursor.fetchone()
        
        if not result:
            print("ERRO: E-mail do usuário não localizado no sistema.")
            return False
            
        destinatario = result[0]
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
        )
    
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg.set_content(resposta)

    try:
        print("Processando o envio da mensagem...")
        
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(email_origem, senha_app)
            servidor.send_message(msg)
            
        print(f"SUCESSO: E-mail enviado para {destinatario}.")
        return True

    except smtplib.SMTPException as erro_smtp:
        print(f"ERRO: Falha na conexão de rede/e-mail: {erro_smtp}")
        return False
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao enviar o e-mail: {e}")
        return False
