from connectsql import obter_conexao, fechar_execusao
import mysql.connector
import os
from time import sleep
from colorama import Fore, Style

def menu_adm(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Administrador
    """
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔════════════════════════════════════════════════════════════════════════╗
║                            DISTRIBUIDORA G2                            ║
╠════════════════════════════════════════════════════════════════════════╣
║                      Caixa Acumulado: {Fore.GREEN}R$ {caixa_atual:>8.2f}{Fore.CYAN}                      ║
╚════════════════════════════════════════════════════════════════════════╝{Fore.RESET}""")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute(
            """SELECT p.id_produto, p.nome, c.nome, f.nome, p.preco_venda, p.quantidade_estoque, p.nota, p.desconto
               FROM produtos AS p
               INNER JOIN fornecedores AS f
                   ON p.id_fornecedor = f.id_fornecedor
               INNER JOIN categorias AS c
                   ON p.id_categoria = c.id_categoria 
               WHERE p.ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print(Fore.YELLOW + Style.BRIGHT + "\n" + "─"*25 + " ESTOQUE ATUAL " + "─"*25 + Fore.RESET)
        for bebida in resultados:
            id_produto, nome_produto, nome_categoria, nome_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            tag_formatada = f"{tag_promo:<8}" 

            print(
                Fore.WHITE + f"[{id_produto:^3}] | " +
                f"{nome_produto:<20} {tag_formatada} | " +
                f"{nome_categoria:<15} | {nome_fornecedor:<15} | " +
                f"Estoque: {quantidade_estoque:^5} | Nota: {nota:^3} | " + 
                Fore.GREEN + f"R$ {preco_final:>6.2f}"
            )
            
    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] Erro ao listar produtos no menu: {e}" + Fore.RESET)
    finally:
        fechar_execusao(conexao, cursor)

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 ════════════════════════════════════════════════════════════════════════
                        ══ MENU DO ADMINISTRADOR ══
 ════════════════════════════════════════════════════════════════════════

 ┌── VENDAS E CAIXA ────────────────────────────────────────────────────┐
 │ {Fore.WHITE}[1]{Fore.CYAN} Registrar Venda               {Fore.WHITE}[2]{Fore.CYAN} Nota Fiscal (Sessão)           │
 │ {Fore.WHITE}[3]{Fore.CYAN} Exportar Notinha                          │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── PRODUTOS E ESTOQUE ────────────────────────────────────────────────┐
 │ {Fore.WHITE}[4]{Fore.CYAN} Cadastrar Nova Bebida         {Fore.WHITE}[5]{Fore.CYAN} Repor Estoque                  │
 │ {Fore.WHITE}[6]{Fore.CYAN} Alterar Preço                 {Fore.WHITE}[7]{Fore.CYAN} Alterar Nome                   │
 │ {Fore.WHITE}[8]{Fore.CYAN} Desativar Bebida              {Fore.WHITE}[9]{Fore.CYAN} Reativar Bebida                │
 │ {Fore.WHITE}[10]{Fore.CYAN} Adicionar Cliente            {Fore.WHITE}[11]{Fore.CYAN} Adicionar Categoria           │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── CONSULTAS E RELATÓRIOS ────────────────────────────────────────────┐
 │ {Fore.WHITE}[12]{Fore.CYAN} Busca                        {Fore.WHITE}[13]{Fore.CYAN} Relatórios Expresso           │
 │ {Fore.WHITE}[14]{Fore.CYAN} Histórico de Vendas          {Fore.WHITE}[15]{Fore.CYAN} Catálogo Ordenado             │
 │ {Fore.WHITE}[16]{Fore.CYAN} Filtro                       {Fore.WHITE}[17]{Fore.CYAN} Estatísticas e Balanço        │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── MARKETING E FORNECEDORES ──────────────────────────────────────────┐
 │ {Fore.WHITE}[18]{Fore.CYAN} Promoções                    {Fore.WHITE}[19]{Fore.CYAN} Novo Fornecedor               │
 │ {Fore.WHITE}[20]{Fore.CYAN} Adicionar Cupom              {Fore.WHITE}[21]{Fore.CYAN} Cupons Mais Utilizados        │
 │ {Fore.WHITE}[22]{Fore.CYAN} Ver Dashboard Analytics      {Fore.WHITE}[23]{Fore.CYAN} Reclame aqui                  │
 └──────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────────┐
 │ {Fore.WHITE}[0]{Fore.CYAN} Sair do Sistema                           │
 └──────────────────────────────────────────────────────────────────────┘
 ════════════════════════════════════════════════════════════════════════{Fore.RESET}
    """)


def menu_funca(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Funcionário
    """
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔════════════════════════════════════════════════════════════════════════╗
║                            DISTRIBUIDORA G2                            ║
╠════════════════════════════════════════════════════════════════════════╣
║                      Caixa Acumulado: {Fore.GREEN}R$ {caixa_atual:>8.2f}{Fore.CYAN}                      ║
╚════════════════════════════════════════════════════════════════════════╝{Fore.RESET}""")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute(
            """SELECT p.id_produto, p.nome, c.nome, f.nome, p.preco_venda, p.quantidade_estoque, p.nota, p.desconto
               FROM produtos AS p
               INNER JOIN fornecedores AS f
                   ON p.id_fornecedor = f.id_fornecedor
               INNER JOIN categorias AS c
                   ON p.id_categoria = c.id_categoria 
               WHERE p.ativo = 1"""
        )
        resultados = cursor.fetchall()
        
        print(Fore.YELLOW + Style.BRIGHT + "\n" + "─"*25 + " ESTOQUE ATUAL " + "─"*25 + Fore.RESET)
        for bebida in resultados:
            id_produto, nome_produto, nome_categoria, nome_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f" (-{desconto}%)"
                
            tag_formatada = f"{tag_promo:<8}" 

            print(
                Fore.WHITE + f"[{id_produto:^3}] | " +
                f"{nome_produto:<20} {tag_formatada} | " +
                f"{nome_categoria:<15} | {nome_fornecedor:<15} | " +
                f"Estoque: {quantidade_estoque:^5} | Nota: {nota:^3} | " + 
                Fore.GREEN + f"R$ {preco_final:>6.2f}"
            )
            
    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] Erro ao listar produtos no menu: {e}" + Fore.RESET)
    finally:
        fechar_execusao(conexao, cursor)

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 ════════════════════════════════════════════════════════════════════════
                         ══ MENU DO FUNCIONÁRIO ══
 ════════════════════════════════════════════════════════════════════════

 ┌── VENDAS E CAIXA ────────────────────────────────────────────────────┐
 │ {Fore.WHITE}[1]{Fore.CYAN} Registrar Venda               {Fore.WHITE}[2]{Fore.CYAN} Nota Fiscal (Sessão)         │
 │ {Fore.WHITE}[3]{Fore.CYAN} Exportar Notinha                          │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── PRODUTOS E ESTOQUE ────────────────────────────────────────────────┐
 │ {Fore.WHITE}[4]{Fore.CYAN} Cadastrar Nova Bebida         {Fore.WHITE}[5]{Fore.CYAN} Repor Estoque                │
 │ {Fore.WHITE}[6]{Fore.CYAN} Alterar Nome                  {Fore.WHITE}[7]{Fore.CYAN} Adicionar Cliente            │
 │ {Fore.WHITE}[8]{Fore.CYAN} Adicionar Categoria                       │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── CONSULTAS E RELATÓRIOS ────────────────────────────────────────────┐
 │ {Fore.WHITE}[9]{Fore.CYAN} Busca                         {Fore.WHITE}[10]{Fore.CYAN} Catálogo Ordenado            │
 │ {Fore.WHITE}[11]{Fore.CYAN} Filtro                                   │
 └──────────────────────────────────────────────────────────────────────┘

 ┌── MARKETING E FORNECEDORES ──────────────────────────────────────────┐
 │ {Fore.WHITE}[12]{Fore.CYAN} Novo Fornecedor               {Fore.WHITE}[13]{Fore.CYAN} Cupons Mais Utilizados        │
 │ {Fore.WHITE}[14]{Fore.CYAN} Reclame aqui                             │
 └──────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────────┐
 │ {Fore.WHITE}[0]{Fore.CYAN} Sair do Sistema                           │
 └──────────────────────────────────────────────────────────────────────┘
 ════════════════════════════════════════════════════════════════════════{Fore.RESET}
    """)

def delay(s=0.5):
  sleep(s)

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
    delay()

def pausar():
    print(Fore.YELLOW + "\n➤ Pressione [ENTER] para continuar..." + Fore.RESET)
    input()
    delay()