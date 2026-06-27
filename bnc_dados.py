import mysql.connector
from connectsql import obter_conexao, fechar_execusao

def inicializar_banco():
    conexao = obter_conexao()
    if not conexao:
        return
        
    cursor = conexao.cursor()
    
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS fornecedores (id_fornecedor INTEGER PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(100) NOT NULL, pais VARCHAR(100) NOT NULL, estado VARCHAR(100) NOT NULL, cidade VARCHAR(100) NOT NULL, ativo TINYINT(1) NOT NULL DEFAULT 1)")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id_cliente INTEGER PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(150) NOT NULL, cnpj_cpf VARCHAR(18) UNIQUE NOT NULL, endereco VARCHAR(255) NOT NULL, telefone VARCHAR(20), ativo TINYINT(1) NOT NULL DEFAULT 1)")

        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id_usuario INTEGER PRIMARY KEY AUTO_INCREMENT, usuario VARCHAR(100) UNIQUE NOT NULL, senha VARCHAR(100) NOT NULL, ativo TINYINT(1) NOT NULL DEFAULT 1, cargo VARCHAR(100) NOT NULL, gmail VARCHAR(100) NOT NULL)")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS cupons (id_cupom INTEGER PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(100) UNIQUE NOT NULL, desconto DECIMAL(10,2) NOT NULL, quantidade INTEGER NOT NULL, ativo TINYINT(1) NOT NULL DEFAULT 1, qtd_used INT NOT NULL DEFAULT 0)")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS categorias (id_categoria INTEGER PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(100) UNIQUE NOT NULL, ativo TINYINT(1) NOT NULL DEFAULT 1)")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id_produto INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                id_categoria INTEGER NOT NULL,
                id_fornecedor INTEGER NOT NULL,
                preco_venda DECIMAL(10,2) NOT NULL,
                preco_custo DECIMAL(10,2) NOT NULL,
                quantidade_estoque INTEGER NOT NULL DEFAULT 0,
                nota DECIMAL(10,2) NOT NULL DEFAULT 0,
                validade DATE NOT NULL,
                ativo TINYINT(1) DEFAULT 1,
                desconto INT NOT NULL DEFAULT 0,
                min_atac INT NOT NULL DEFAULT 12,
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
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO categorias (nome) VALUES 
                    ('Vinho Tinto'), ('Vinho Branco'), ('Destilados'), 
                    ('Cervejas'), ('Espumantes'), ('Sem Álcool'), 
                    ('Energéticos'), ('Licores e Aperitivos')
                """)
                
                cursor.execute("""
                    INSERT INTO fornecedores (nome, pais, estado, cidade) VALUES 
                    ('Concha y Toro', 'Chile', 'Região Central', 'Santiago'),
                    ('Catena Zapata', 'Argentina', 'Mendoza', 'Mendoza'),
                    ('Ambev Brasil', 'Brasil', 'SP', 'São Paulo'),
                    ('Diageo', 'Reino Unido', 'Londres', 'Londres'),
                    ('Vinícola Salton', 'Brasil', 'RS', 'Bento Gonçalves'),
                    ('Red Bull GmbH', 'Áustria', 'Salzburgo', 'Fuschl am See'),
                    ('Campari Group', 'Itália', 'Lombardia', 'Milão')
                """)

                usuarios = [
                    ('Danilo', 'senha123', 1, 'Gerente de Vendas', 'danilo@distribuidora.com'),
                    ('Felipe', 'senha123', 1, 'Vendedor', 'felipe@distribuidora.com'),
                    ('Andressa', 'admin123', 1, 'Administrador', 'andressa@distribuidora.com')
                ]
                cursor.executemany("INSERT INTO usuarios (usuario, senha, ativo, cargo, gmail) VALUES (%s, %s, %s, %s, %s)", usuarios)

                clientes = [
                    ('Adega Central', '12.345.678/0001-99', 'Av. Paulista, 1000 - São Paulo, SP', '11988887777', 1),
                    ('Bar e Lanches Silva', '98.765.432/0001-11', 'Rua Augusta, 500 - São Paulo, SP', '11977776666', 1),
                    ('São Paulo Rugby Club', '11.222.333/0001-44', 'Rua do Estádio, 150 - São Paulo, SP', '11966665555', 1),
                    ('João Carlos Ferreira', '123.456.789-00', 'Rua das Flores, 45 - Osasco, SP', '11955554444', 1)
                ]
                cursor.executemany("INSERT INTO clientes (nome, cnpj_cpf, endereco, telefone, ativo) VALUES (%s, %s, %s, %s, %s)", clientes)

                cupons = [
                    ('BEMVINDO10', 10.00, 100, 1, 15),
                    ('NATAL20', 20.00, 50, 1, 0),
                    ('CLIENTEFIE', 15.00, 200, 1, 45),
                    ('QUEIMA50', 50.00, 10, 1, 8)
                ]
                cursor.executemany("INSERT INTO cupons (nome, desconto, quantidade, ativo, qtd_used) VALUES (%s, %s, %s, %s, %s)", cupons)

                produtos_iniciais = [
                    ("Heineken Long Neck 330ml", 4, 3, 7.50, 4.00, 1200, 5, "2027-01-10", 1, 0, 48, 10),
                    ("Corona Extra 330ml", 4, 3, 8.00, 4.50, 800, 5, "2027-02-20", 1, 0, 24, 8),
                    ("Campari 900ml", 8, 7, 65.90, 40.00, 150, 4, "2035-12-31", 1, 5, 12, 12),
                    ("Aperol 750ml", 8, 7, 75.00, 45.00, 200, 5, "2035-12-31", 1, 0, 6, 15),
                    ("Tequila Jose Cuervo Especial", 3, 4, 110.00, 65.00, 90, 4, "2035-12-31", 1, 10, 12, 15),
                    ("Red Bull Energy Drink 250ml", 7, 6, 8.90, 5.00, 600, 5, "2026-10-15", 1, 0, 24, 5),
                    ("Red Bull Sugar Free 250ml", 7, 6, 8.90, 5.00, 400, 4, "2026-10-15", 1, 0, 24, 5),
                    ("Alamos Malbec", 1, 2, 115.00, 65.00, 180, 5, "2032-12-31", 1, 0, 6, 10),
                    ("Concha y Toro Sauvignon Blanc", 2, 1, 60.00, 32.00, 250, 4, "2028-12-31", 1, 0, 12, 8)
                ]
                cursor.executemany("""
                    INSERT INTO produtos 
                    (nome, id_categoria, id_fornecedor, preco_venda, preco_custo, quantidade_estoque, nota, validade, ativo, desconto, min_atac, desc_atac)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, produtos_iniciais)

                vendas = [
                    (1, 2, None, 360.00, 'PIX'),
                    (3, 1, 1, 275.50, 'Cartão Crédito'),
                    (2, 3, None, 1500.00, 'Boleto')
                ]
                cursor.executemany("INSERT INTO vendas (id_cliente, id_usuario, id_cupom, valor_total, forma_pagamento) VALUES (%s, %s, %s, %s, %s)", vendas)

                itens_venda = [
                    (1, 1, 48, 7.50),
                    (2, 6, 24, 8.90),
                    (2, 4, 1, 65.90),
                    (3, 3, 12, 110.00),
                    (3, 8, 2, 115.00)
                ]
                cursor.executemany("INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)", itens_venda)
                conexao.commit()
                print("Banco de dados inicializado com sucesso!")

    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro no banco: {e}")
    finally:
        fechar_execusao(conexao, cursor)



