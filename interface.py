from connectsql import obter_conexao, fechar_execusao
import mysql.connector
import os
from time import sleep
from colorama import Fore, Style

def menu_adm(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Administrador
    """
    texto_caixa = f"R$ {caixa_atual:.2f}"
    espacos = " " * (47 - len(texto_caixa))

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}🏪 DISTRIBUIDORA G2{Fore.CYAN}                                                █
 █  {Fore.WHITE}💵 Caixa Acumulado: {Fore.GREEN}{texto_caixa}{espacos}{Fore.CYAN}█
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
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
        
        for bebida in resultados:
            id_produto, nome_produto, nome_categoria, nome_fornecedor, preco_venda, quantidade_estoque, nota, desconto = bebida
            
            preco_final = float(preco_venda)
            tag_promo = ""
            
            if desconto and desconto > 0:
                preco_final = float(preco_venda) - (float(preco_venda) * (float(desconto) / 100))
                tag_promo = f"(-{float(desconto):.0f}%)"
                
            tag_formatada = f"{tag_promo:<10}" 

            nome_str = str(nome_produto)[:19]
            cat_str = str(nome_categoria)[:14]
            forn_str = str(nome_fornecedor)[:14]

            print(
                Fore.WHITE + f"[{id_produto:^3}] | " +
                f"{nome_str:<19} {tag_formatada} | " +
                f"{cat_str:<14} | {forn_str:<14} | " +
                f"Estoque: {quantidade_estoque:<5} | Nota: {nota:<3} | " + 
                Fore.GREEN + f"R$ {preco_final:>7.2f}"
            )
            
    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] Erro ao listar produtos no menu: {e}" + Fore.RESET)
    finally:
        fechar_execusao(conexao, cursor)

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}               ✦ PAINEL DE CONTROLE ADMINISTRATIVO ✦{Fore.CYAN}              █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.MAGENTA}❖ VENDAS E CAIXA {Fore.CYAN}───────────────────────────────────────────────────
   {Fore.WHITE}[1]{Fore.CYAN} 🛒 Registrar Venda             {Fore.WHITE}[2]{Fore.CYAN} 🧾 Nota Fiscal (Sessão)
   {Fore.WHITE}[3]{Fore.CYAN} 📤 Exportar Notinha

 {Fore.MAGENTA}❖ PRODUTOS E ESTOQUE {Fore.CYAN}───────────────────────────────────────────────
   {Fore.WHITE}[4]{Fore.CYAN} 📦 Cadastrar Nova Bebida        {Fore.WHITE}[5]{Fore.CYAN} 🔄 Repor Estoque
   {Fore.WHITE}[6]{Fore.CYAN} 💲 Alterar Preço                {Fore.WHITE}[7]{Fore.CYAN} ✏️ Alterar Nome
   {Fore.WHITE}[8]{Fore.CYAN} 🔴 Desativar Bebida             {Fore.WHITE}[9]{Fore.CYAN} 🟢 Reativar Bebida
   {Fore.WHITE}[10]{Fore.CYAN} 👥 Adicionar Cliente           {Fore.WHITE}[11]{Fore.CYAN} 🏷️ Adicionar Categoria

 {Fore.MAGENTA}❖ CONSULTAS E RELATÓRIOS {Fore.CYAN}───────────────────────────────────────────
   {Fore.WHITE}[12]{Fore.CYAN} 🔍 Busca Avançada              {Fore.WHITE}[13]{Fore.CYAN} ⚡ Relatórios Expresso
   {Fore.WHITE}[14]{Fore.CYAN} 📜 Histórico de Vendas         {Fore.WHITE}[15]{Fore.CYAN} 🗂️ Catálogo Ordenado
   {Fore.WHITE}[16]{Fore.CYAN} 🎛️ Filtro                       {Fore.WHITE}[17]{Fore.CYAN} 📊 Estatísticas e Balanço

 {Fore.MAGENTA}❖ MARKETING E FORNECEDORES {Fore.CYAN}─────────────────────────────────────────
   {Fore.WHITE}[18]{Fore.CYAN} 🎁 Promoções                   {Fore.WHITE}[19]{Fore.CYAN} 🤝 Novo Fornecedor
   {Fore.WHITE}[20]{Fore.CYAN} 🎟️ Adicionar Cupom              {Fore.WHITE}[21]{Fore.CYAN} 🏆 Cupons Mais Utilizados
   {Fore.WHITE}[22]{Fore.CYAN} 📈 Ver Dashboard Analytics     {Fore.WHITE}[23]{Fore.CYAN} 🗣️ Reclame Aqui

 ──────────────────────────────────────────────────────────────────────
   {Fore.RED}[0]{Fore.WHITE} ❌ Sair do Sistema
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}
    """)


def menu_funca(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque para o Funcionário
    """
    texto_caixa = f"R$ {caixa_atual:.2f}"
    espacos = " " * (47 - len(texto_caixa))

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}🏪 DISTRIBUIDORA G2{Fore.CYAN}                                                █
 █  {Fore.WHITE}💵 Caixa Acumulado: {Fore.GREEN}{texto_caixa}{espacos}{Fore.CYAN}█
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{Fore.RESET}""")
    
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

            nome_str = str(nome_produto)[:19]
            cat_str = str(nome_categoria)[:14]
            forn_str = str(nome_fornecedor)[:14]

            print(
                Fore.WHITE + f"[{id_produto:^3}] | " +
                f"{nome_str:<19} {tag_formatada} | " +
                f"{cat_str:<14} | {forn_str:<14} | " +
                f"Estoque: {quantidade_estoque:<5} | Nota: {nota:<3} | " + 
                Fore.GREEN + f"R$ {preco_final:>7.2f}"
                )
            
    except mysql.connector.Error as e:
        print(Fore.RED + Style.BRIGHT + f"\n[✖] Erro ao listar produtos no menu: {e}" + Fore.RESET)
    finally:
        fechar_execusao(conexao, cursor)

    print(f"""{Fore.CYAN}{Style.BRIGHT}
 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █  {Fore.YELLOW}               ✦ PAINEL DE CONTROLE FUNCIONARIO ✦{Fore.CYAN}                 █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

 {Fore.MAGENTA}❖ VENDAS E CAIXA {Fore.CYAN}───────────────────────────────────────────────────
   {Fore.WHITE}[1]{Fore.CYAN} 🛒 Registrar Venda             {Fore.WHITE}[2]{Fore.CYAN} 🧾 Nota Fiscal (Sessão)
   {Fore.WHITE}[3]{Fore.CYAN} 📤 Exportar Notinha

 {Fore.MAGENTA}❖ PRODUTOS E ESTOQUE {Fore.CYAN}───────────────────────────────────────────────
   {Fore.WHITE}[4]{Fore.CYAN} 📦 Cadastrar Nova Bebida       {Fore.WHITE}[5]{Fore.CYAN} 🔄 Repor Estoque
   {Fore.WHITE}[6]{Fore.CYAN} ✏️ Alterar Nome                 {Fore.WHITE}[7]{Fore.CYAN} 👥 Adicionar Cliente
   {Fore.WHITE}[8]{Fore.CYAN} 🏷️ Adicionar Categoria

 {Fore.MAGENTA}❖ CONSULTAS E RELATÓRIOS {Fore.CYAN}───────────────────────────────────────────
   {Fore.WHITE}[9]{Fore.CYAN} 🔍 Busca Avançada              {Fore.WHITE}[10]{Fore.CYAN} 🗂️ Catálogo Ordenado
   {Fore.WHITE}[11]{Fore.CYAN} 🎛️ Filtro

 {Fore.MAGENTA}❖ MARKETING E FORNECEDORES {Fore.CYAN}─────────────────────────────────────────
   {Fore.WHITE}[12]{Fore.CYAN} 🤝 Novo Fornecedor             {Fore.WHITE}[13]{Fore.CYAN} 🏆 Cupons Mais Utilizados
   {Fore.WHITE}[14]{Fore.CYAN} 🗣️ Reclame Aqui

 ──────────────────────────────────────────────────────────────────────
   {Fore.RED}[0]{Fore.WHITE} ❌ Sair do Sistema
 ══════════════════════════════════════════════════════════════════════{Fore.RESET}
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