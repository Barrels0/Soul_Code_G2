from forces import force_int
from interface import menu_adm,menu_funca
#importar o menu
def continuar_sistema_a():
    while True:
        print("-"*10)
        print("[1] Voltar ao Menu")
        print("[2] Sair")
        print("-"*10)
        try:
            acao_pos_comando = force_int("Escolha uma ação: ")
            if acao_pos_comando == 1:
                return
            elif acao_pos_comando == 2:
                exit()
            else:
                print("Opção inválida!")
        except ValueError:
            return menu_adm
def continuar_sistema_f():
    while True:
        print("-"*10)
        print("[1] Voltar ao Menu")
        print("[2] Sair")
        print("-"*10)
        try:
            acao_pos_comando = force_int("Escolha uma ação: ")
            if acao_pos_comando == 1:
                return
            elif acao_pos_comando == 2:
                exit()
            else:
                print("Opção inválida!")
        except ValueError:
            return menu_funca