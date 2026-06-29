from forces import force_int
from colorama import Fore, Style
import sys

def continuar_sistema_a(caixa):
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}O QUE DESEJA FAZER AGORA?{Fore.CYAN}                                         █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 
   {Fore.WHITE}[1]{Fore.CYAN} Voltar ao Menu Principal
   {Fore.WHITE}[0]{Fore.CYAN} Sair do Sistema{Fore.RESET}
""")
        
        acao_pos_comando = force_int(Fore.YELLOW + "➤ Escolha uma ação: " + Fore.RESET)
        
        if acao_pos_comando == 1:
            return
            
        elif acao_pos_comando == 0:
            print(f"""{Fore.GREEN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  OBRIGADO POR VISITAR NOSSA LOJA!                 █
 █  CAIXA DO TURNO: R$ {caixa:>10.2f}                    █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
            sys.exit()
            
        else:
            print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)


def continuar_sistema_f(caixa):
    while True:
        print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}O QUE DESEJA FAZER AGORA?{Fore.CYAN}                                         █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
 
   {Fore.WHITE}[1]{Fore.CYAN} Voltar ao Menu Principal
   {Fore.WHITE}[0]{Fore.CYAN} Sair do Sistema{Fore.RESET}
""")
        
        acao_pos_comando = force_int(Fore.YELLOW + "➤ Escolha uma ação: " + Fore.RESET)
        
        if acao_pos_comando == 1:
            return
            
        elif acao_pos_comando == 0:
            print(f"""{Fore.GREEN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  OBRIGADO POR VISITAR NOSSA LOJA!                 █
 █  CAIXA DO TURNO: R$ {caixa:>10.2f}                    █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
            sys.exit()
            
        else:
            print(Fore.RED + "\n[✖] ERRO: Opção inválida. Tente novamente." + Fore.RESET)