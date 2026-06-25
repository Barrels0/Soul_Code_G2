import mysql.connector
from connectsql import obter_conexao


""" 
função responsável por incializar o banco e caso necesssário
já colocar alguns dados iniciais
"""
def inicializar_banco():
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        #tabela de FORNECEDORES da distribuidora
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fornecedores (
                id_fornecedor INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                pais VARCHAR(100) NOT NULL,
                estado VARCHAR(100) NOT NULL,
                cidade VARCHAR(100) NOT NULL,
                ativo INT NOT NULL DEFAULT 1
            )
            """)
        
        #Tabela de CLIENTES da distribuidora
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(150) NOT NULL,
                cnpj_cpf VARCHAR(18) UNIQUE NOT NULL,
                endereco VARCHAR(255) NOT NULL,
                telefone VARCHAR(20),
                ativo INT NOT NULL DEFAULT 1
            )
            """)

        #tabela de USUÁRIOS do nosso sistema
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTO_INCREMENT,
                usuario VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(100) NOT NULL
                ativo INT NOT NULL DEFAULT 1,
                cargo VARCHAR(100) NOT NULL,
                gmail VARCHAR(100) NOT NULL
            )
            """)
            
        #tabela de CUPONS
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cupons (
                id_cupom INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) UNIQUE NOT NULL,
                desconto DECIMAL NOT NULL,
                quantidade INTEGER NOT NULL,
                ativo INT NOT NULL DEFAULT 1,
                qtd_used INT NOT NULL
            )
            """)
            
            
        #tabela de CATEGORIAS
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) UNIQUE NOT NULL,
                ativo INT NOT NULL DEFAULT 1
            )
            """)


        #Abaixo são as tabelas intermediárias, no sentido de que possuem FK
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id_produto INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                id_categoria INTEGER NOT NULL,
                id_fornecedor INTEGER NOT NULL,
                preco_venda DECIMAL(10,2) NOT NULL,
                preco_custo DECIMAL(10,2) NOT NULL,
                quantidade_estoque INTEGER NOT NULL DEFAULT 0,
                nota INTEGER NOT NULL DEFAULT 0,
                validade DATE NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                desconto INT NOT NULL,
                min_atac INT NOT NULL,
                desc_atac INT NOT NULL DEFAULT 5,
                FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria),
                FOREIGN KEY (id_fornecedor) REFERENCES fornecedores (id_fornecedor)
            )
            """)

            

            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id_venda INTEGER PRIMARY KEY AUTO_INCREMENT,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_cliente INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                id_cupom INTEGER,
                valor_total DECIMAL(10,2) NOT NULL,
                forma_pagamento VARCHAR(50) NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
                FOREIGN KEY (id_cupom) REFERENCES cupons (id_cupom)
            )
            """)

            # Tabela detalhe de ITENS_VENDA
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda (
                id_item INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_venda INTEGER NOT NULL,
                id_produto INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (id_venda) REFERENCES vendas (id_venda) ON DELETE CASCADE,
                FOREIGN KEY (id_produto) REFERENCES produtos (id_produto)
            )
            """) 
            

            cursor.execute("SELECT COUNT(*) FROM estoque")
            

            if cursor.fetchone()[0] == 0:
                
                cursor.execute("""
                    INSERT INTO categorias (nome) VALUES 
                    ('Vinho Tinto'), 
                    ('Vinho Branco'),
                    ('Destilados'),
                    ('Cervejas'),
                    ('Espumantes'),
                    ('Sem Álcool')
                """)
                
                cursor.execute("""
                    INSERT INTO fornecedores (nome, pais, estado, cidade) VALUES 
                    ('Concha y Toro', 'Chile', 'Região Central', 'Santiago'),
                    ('Catena Zapata', 'Argentina', 'Mendoza', 'Mendoza'),
                    ('Ambev Brasil', 'Brasil', 'SP', 'São Paulo'),
                    ('Diageo', 'Reino Unido', 'Londres', 'Londres'),
                    ('Vinícola Salton', 'Brasil', 'RS', 'Bento Gonçalves')
                """)


                bebidas_iniciais = [
                    ("Casillero del Diablo Reserva", 1, 1, 89.90, 45.00, 50, 4, "2030-12-31", 1),
                    ("Angelica Zapata Malbec", 1, 2, 280.00, 150.00, 20, 5, "2030-12-31", 1),
                    ("Marques de Casa Concha Chardonnay", 2, 1, 120.00, 70.00, 30, 4, "2030-12-31", 1),
                    
                    ("Whisky Johnnie Walker Black Label", 3, 4, 189.90, 110.00, 40, 5, "2035-12-31", 1),
                    ("Gin Tanqueray London Dry", 3, 4, 135.00, 80.00, 60, 5, "2035-12-31", 1),
                    ("Vodka Smirnoff", 3, 4, 45.90, 25.00, 100, 3, "2035-12-31", 1),
                    
                    ("Cerveja Stella Artois Long Neck", 4, 3, 6.50, 3.50, 300, 4, "2027-06-30", 1),
                    ("Cerveja Budweiser Lata 350ml", 4, 3, 4.50, 2.20, 500, 4, "2027-08-15", 1),
                    ("Refrigerante Guaraná Antarctica 2L", 6, 3, 9.50, 5.00, 150, 4, "2026-12-31", 1),
                    
                    ("Espumante Salton Brut", 5, 5, 49.90, 28.00, 80, 4, "2029-12-31", 1),
                    ("Espumante Salton Moscatel", 5, 5, 55.00, 30.00, 65, 4, "2029-12-31", 1)
                ]

                cursor.executemany("""
                    INSERT INTO produtos 
                    (nome, id_categoria, id_fornecedor, preco_venda, preco_custo, quantidade_estoque, nota, validade, ativo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, bebidas_iniciais)
                
                conexao.commit()
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
                