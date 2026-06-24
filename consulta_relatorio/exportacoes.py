import pandas as pd
from forces import force_int

def perguntar_exportacao(df, nome_padrao="relatorio"):
    """
    Recebe um DataFrame do Pandas e pergunta ao usuário se ele quer salvar.
    """
    if df.empty:
        return 

    print("\n" + "-"*40)
    print(" Deseja exportar esses resultados?")
    print(" [1] Sim, em CSV (Abre no Excel)")
    print(" [2] Sim, em TXT (Bloco de Notas)")
    print(" [0] Não, voltar ao menu")
    print("-"*40)
    
    escolha = force_int("Sua escolha: ")
    
    try:
        if escolha == 1:
            nome_arquivo = f"{nome_padrao}.csv"
            
            df.to_csv(nome_arquivo, sep=';', index=False, encoding='utf-8-sig')
            print(f"\n Sucesso! Arquivo '{nome_arquivo}' salvo na pasta do projeto.")
            
        elif escolha == 2:
            nome_arquivo = f"{nome_padrao}.txt"
        
            df.to_csv(nome_arquivo, sep='\t', index=False, encoding='utf-8')
            print(f"\n Sucesso! Arquivo '{nome_arquivo}' salvo na pasta do projeto.")
            
        else:
            print("\nExportação ignorada.")
            
    except Exception as e:
        print(f"\n Erro ao tentar salvar o arquivo: {e}")