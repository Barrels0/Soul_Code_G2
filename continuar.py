from forces import force_int
from interface import menu_adm, menu_funca
from colorama import Fore, Style

# Importar o menu
def continuar_sistema_a():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}O QUE DESEJA FAZER AGORA?{Fore.CYAN}                                         █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 
   {Fore.WHITE}[1]{Fore.CYAN} Voltar ao Menu Principal
   {Fore.WHITE}[2]{Fore.CYAN} Sair do Sistema{Fore.RESET}
""")
        try:
            acao_pos_comando = force_int(Fore.YELLOW + "➤ Escolha uma ação: " + Fore.RESET)
            if acao_pos_comando == 1:
                return
            elif acao_pos_comando == 2:
                exit()
            else:
                print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)
        except ValueError:
            return menu_adm

def continuar_sistema_f():
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}O QUE DESEJA FAZER AGORA?{Fore.CYAN}                                         █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 
   {Fore.WHITE}[1]{Fore.CYAN} Voltar ao Menu Principal
   {Fore.WHITE}[2]{Fore.CYAN} Sair do Sistema{Fore.RESET}
""")
        try:
            acao_pos_comando = force_int(Fore.YELLOW + "➤ Escolha uma ação: " + Fore.RESET)
            if acao_pos_comando == 1:
                return
            elif acao_pos_comando == 2:
                exit()
            else:
                print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)
        except ValueError:
            return menu_funca