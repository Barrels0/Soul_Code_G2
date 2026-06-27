import pandas as pd
from forces import force_int
from colorama import Fore, Style

def perguntar_exportacao(df, nome_padrao="relatorio"):
    """
    Recebe um DataFrame do Pandas e pergunta ao usuário se ele quer salvar.
    """
    if df.empty:
        return 

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}EXPORTAR RESULTADOS{Fore.CYAN}                                               █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.WHITE}[1]{Fore.CYAN} Sim, em CSV (Abre no Excel)
 {Fore.WHITE}[2]{Fore.CYAN} Sim, em TXT (Bloco de Notas)
 {Fore.WHITE}[0]{Fore.CYAN} Não, voltar ao menu
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}""")
    
    escolha = force_int(Fore.YELLOW + "➤ Sua escolha: " + Fore.RESET)
    
    try:
        if escolha == 1:
            nome_arquivo = f"{nome_padrao}.csv"
            
            df.to_csv(nome_arquivo, sep=';', index=False, encoding='utf-8-sig')
            print(Fore.GREEN + f"\n[✔] SUCESSO: Arquivo '{nome_arquivo}' salvo na pasta do projeto!" + Fore.RESET)
            
        elif escolha == 2:
            nome_arquivo = f"{nome_padrao}.txt"
        
            df.to_csv(nome_arquivo, sep='\t', index=False, encoding='utf-8')
            print(Fore.GREEN + f"\n[✔] SUCESSO: Arquivo '{nome_arquivo}' salvo na pasta do projeto!" + Fore.RESET)
            
        else:
            print(Fore.YELLOW + "\n[!] Exportação ignorada pelo operador." + Fore.RESET)
            
    except Exception as e:
        print(Fore.RED + f"\n[✖] ERRO ao tentar salvar o arquivo: {e}" + Fore.RESET)