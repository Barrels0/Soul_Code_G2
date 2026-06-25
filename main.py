import mysql.connector
from connectsql import obter_conexao,fechar_execusao
from login import login, new_user, recuperar_senha
from consulta_relatorio.consulta_relatorio import (
    relatorio_expresso,
    busca,
    filtros,
    painel_estatisticas,
    catalogo_ordenado,
    historico_vendas,
)
from marketing_fornecedores.marketing import (
    cadastrar_fornecedor,
    cadastrar_cupom,
    promocoes,
    relatorio_cupons_mais_utilizados,
    abrir_dashboard,
    reclame_aqui,
)
from produtos_estoque1.def1 import (
    adicionar_item,
    alterar_preco,
    repor_estoque,
    alterar_nome,
    off_prod,
    atv_prod,
    add_cliente,
    add_categoria,
)
from vendas_e_caixa.defs import exp_nota, nota_fiscal, registar_venda
from continuar import continuar_sistema_f, continuar_sistema_a
from bnc_dados import inicializar_banco
from interface import menu_adm, menu_funca, pausar, limpar_tela
from forces import force_int,force_str

inicializar_banco()
conexao = obter_conexao()
cursor = conexao.cursor()

try:
    cursor.execute("SELECT SUM(valor_total) FROM vendas")
    resultado_caixa = cursor.fetchone()[0]
    caixa = resultado_caixa if resultado_caixa is not None else 0.0
except mysql.connector.Error as e:
    conexao.rollback()
    print(f"Ocorreu um erro: {e}")
finally:
    fechar_execusao(
            conexao if "conexao" in locals() else None, 
            cursor if "cursor" in locals() else None
            )

print("Seja bem-vindo a distribuidora G2...")
print("""Seja bem-vindo a distribuidora G2!
          1-Criar usuario
          2-Fazer Login
          3-Recuperar Senha
      """)

try:
    escolha = force_int("Selecione um dos dois itens mostrados acima: ")

    if escolha == 1:
        new_user()
        resultado_login = login()
        if resultado_login is None:
            print("Falha no login. Encerrando o sistema...")
            exit()
        else:
            user_ativ, id_operador = resultado_login
    elif escolha == 2:
        resultado_login = login()
        if resultado_login is None:
            print("Falha no login. Encerrando o sistema...")
            exit()
        else:
            user_ativ, id_operador = resultado_login
    elif escolha == 3:
        busca = force_str("Digite o nome do seu usuário ou o seu e-mail: ")

        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute(
            "SELECT id_usuario, usuario, gmail FROM usuarios WHERE gmail = %s OR usuario = %s", 
            (busca, busca)
        )
        result = cursor.fetchone()
        
        fechar_execusao(conexao, cursor)

        if not result:
            print("Nenhum usuário encontrado com esse nome/e-mail!")
        else:
            print(f"Usuário encontrado: {result[1]} | E-mail: {result[2]}")
            recuperar_senha(result[0])
            if not recuperar_senha:
                print("Não foi possivel recuperar a senha!")
            else:
                resultado_login = login()
                if resultado_login is None:
                    print("Falha no login. Encerrando o sistema...")
                    exit()
                else:
                    user_ativ, id_operador = resultado_login        
except mysql.connector.Error as e:
        conexao.rollback()
        print(f"\nOcorreu um erro no banco de dados: {e}")
finally:
    fechar_execusao(
        conexao if "conexao" in locals() else None, 
        cursor if "cursor" in locals() else None
        )
if id_operador and user_ativ:
    try:
        while True:
            if user_ativ == "Admin":
                menu_adm(caixa)
                comando = force_int("Digite o numero da função que você deseja acessar: ")

                if comando == 0:
                    print(
                        f"Obrigado por visitar nossa loja o caixa total ficou em R${caixa:.2f}"
                    )
                    caixa = 0
                    exit()
                elif comando == 1:
                    registar_venda(id_operador)
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 2:
                    nota_fiscal()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 3:
                    exp_nota(id_operador)
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 4:
                    adicionar_item()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 5:
                    repor_estoque()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 6:
                    alterar_preco()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 7:
                    alterar_nome()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 8:
                    off_prod()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 9:
                    atv_prod()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 10:
                    add_cliente()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 11:
                    add_categoria()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 12:
                    busca()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 13:
                    relatorio_expresso()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 14:
                    historico_vendas()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 15:
                    catalogo_ordenado()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 16:
                    filtros()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 17:
                    painel_estatisticas()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 18:
                    promocoes()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 19:
                    cadastrar_fornecedor()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 20:
                    cadastrar_cupom()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 21:
                    relatorio_cupons_mais_utilizados()
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                elif comando == 22:
                    abrir_dashboard()
                    continuar_sistema_a()
                elif comando == 23:
                    reclame_aqui(id_operador)
                    pausar()
                    limpar_tela()
                    continuar_sistema_a()
                else:
                    print("ERRO: Opção invalida.")
                    limpar_tela()
                    continuar_sistema_a()

            elif user_ativ == "Funcionario":
                menu_funca(caixa)
                comando = force_int("Digite o numero da função que você deseja acessar: ")

                if comando == 0:
                    print(
                        f"Obrigado por visitar nossa loja o caixa total ficou em R${caixa:.2f}"
                    )
                    exit()
                elif comando == 1:
                    registar_venda()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 2:
                    nota_fiscal()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 3:
                    exp_nota()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 4:
                    adicionar_item()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 5:
                    repor_estoque()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 6:
                    alterar_nome()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 7:
                    add_cliente()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 8:
                    add_categoria()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 9:
                    busca()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 10:
                    catalogo_ordenado()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 11:
                    filtros()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 12:
                    cadastrar_fornecedor()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 13:
                    relatorio_cupons_mais_utilizados()
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                elif comando == 14:
                    reclame_aqui(id_operador)
                    pausar()
                    limpar_tela()
                    continuar_sistema_f()
                else:
                    print("ERRO: Opção invalida.")
                    limpar_tela()
                    continuar_sistema_f()

    except Exception as i:
        print(f"Erro inesperado... {i}")
else:
    print("Ocorreu um problema com o seu login!")