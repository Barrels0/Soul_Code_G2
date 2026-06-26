import mysql.connector
from connectsql import obter_conexao, fechar_execusao
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
from forces import force_int, force_str

from colorama import init, Fore, Style

init(autoreset=True)

inicializar_banco()


while True:
    try:
        # Menu principal redesenhado para ficar mais bonito e profissional
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}BEM-VINDO À DISTRIBUIDORA G2{Fore.CYAN}                                      █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Criar novo usuário
 {Fore.WHITE}[2]{Fore.CYAN} Fazer Login
 {Fore.WHITE}[3]{Fore.CYAN} Recuperar Senha
 {Fore.WHITE}[0]{Fore.CYAN} Sair do sistema
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")
        
        escolha = force_int(
            Fore.YELLOW + "➤ Selecione uma das opções acima: " + Fore.RESET
        )

        if escolha == 0:
            print(Fore.YELLOW + "\n[!] Saindo do sistema. Até logo!" + Fore.RESET)
            break

        elif escolha == 1:
            cadastro = new_user()
            if not cadastro:
                continue
            user_ativ, id_operador = login()
            if user_ativ is None:
                continue
            break
        elif escolha == 2:
            user_ativ, id_operador = login()
            if user_ativ is None:
                continue
            break
        elif escolha == 3:
            busca = force_str(
                Fore.YELLOW
                + "\n➤ Digite o nome do seu usuário ou o seu e-mail: "
                + Fore.RESET
            )

            conexao = obter_conexao()
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id_usuario, usuario, gmail FROM usuarios WHERE gmail = %s OR usuario = %s",
                (busca, busca),
            )
            result = cursor.fetchone()

            fechar_execusao(conexao, cursor)

            if not result:
                print(Fore.RED + "\n[✖] Nenhum usuário encontrado com esse nome/e-mail!" + Fore.RESET)
            else:
                print(
                    Fore.GREEN
                    + f"\n[✔] Usuário encontrado: {result[1]} | E-mail: {result[2]}"
                    + Fore.RESET
                )
                recuperar_senha(result[0])
                user_ativ, id_operador = login()
                if user_ativ is None:
                    continue

                break
    except mysql.connector.Error as e:
        conexao.rollback()
        print(Fore.RED + Style.BRIGHT + f"\n[✖] Ocorreu um erro no banco de dados: {e}" + Fore.RESET)
    finally:
        fechar_execusao(
            conexao if "conexao" in locals() else None,
            cursor if "cursor" in locals() else None,
        )
        
conexao = obter_conexao()
cursor = conexao.cursor()

try:
    cursor.execute(
        "SELECT SUM(valor_total) FROM vendas WHERE id_usuario = %s", (id_operador,)
    )
    resultado_caixa = cursor.fetchone()[0]
    caixa = resultado_caixa if resultado_caixa is not None else 0.0
except mysql.connector.Error as e:
    conexao.rollback()
    print(Fore.RED + f"\n[✖] Ocorreu um erro: {e}" + Fore.RESET)
finally:
    fechar_execusao(
        conexao if "conexao" in locals() else None,
        cursor if "cursor" in locals() else None,
    )
    
try:
    while True:
        if user_ativ == "Admin":
            menu_adm(caixa)
            comando = force_int(
                Fore.YELLOW
                + "➤ Digite o número da função que você deseja acessar: "
                + Fore.RESET
            )

            if comando == 0:
                print(f"""{Fore.GREEN}{Style.BRIGHT}
══════════════════════════════════════════════════
  Obrigado por visitar nossa loja!
  O caixa total do turno fechou em: R$ {caixa:.2f}
══════════════════════════════════════════════════{Fore.RESET}""")
                caixa = 0.00
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
                print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)
                limpar_tela()
                continuar_sistema_a()

        elif user_ativ == "Funcionario":
            menu_funca(caixa)
            comando = force_int(
                Fore.YELLOW
                + "➤ Digite o número da função que você deseja acessar: "
                + Fore.RESET
            )

            if comando == 0:
                print(f"""{Fore.GREEN}{Style.BRIGHT}
══════════════════════════════════════════════════
  Obrigado por visitar nossa loja!
  O caixa total do turno fechou em: R$ {caixa:.2f}
══════════════════════════════════════════════════{Fore.RESET}""")
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
                print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)
                limpar_tela()
                continuar_sistema_f()

except Exception as i:
    print(Fore.RED + Style.BRIGHT + f"\n[✖] Erro inesperado: {i}" + Fore.RESET)