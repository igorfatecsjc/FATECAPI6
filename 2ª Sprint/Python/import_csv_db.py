import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
import sqlite3  # Importa a biblioteca sqlite3 para manipulação do banco de dados SQLite

def create_connection(db_file):
    """
    Cria uma conexão com o banco de dados SQLite.
    
    :param db_file: Nome do arquivo do banco de dados SQLite
    :return: Conexão com o banco de dados ou None se houver erro
    """
    try:
        connection = sqlite3.connect(db_file)  # Tenta conectar ao banco de dados SQLite
        print("Conexão com o banco de dados SQLite estabelecida.")
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        return None

def create_tables(connection):
    """
    Cria as tabelas necessárias no banco de dados se elas não existirem.
    
    :param connection: Conexão com o banco de dados SQLite
    """
    try:
        cursor = connection.cursor()  # Cria um cursor para executar comandos SQL

        # Cria a tabela 'fabricas' para armazenar informações sobre fábricas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fabricas (
            IDFabrica INTEGER PRIMARY KEY,
            MUN TEXT,
            MUNMIN TEXT,
            SGUF TEXT,
            LAT REAL,
            LONG REAL
        );
        """)

        # Cria a tabela 'clientes' para armazenar informações sobre clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            IDCliente INTEGER PRIMARY KEY,
            MUN TEXT,
            LAT REAL,
            LONG REAL
        );
        """)

        # Cria a tabela 'rotas' para armazenar informações sobre rotas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rotas (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Emissao TEXT,
            Entrega TEXT,
            MesBase INTEGER,
            AnoExec INTEGER,
            IDFabrica INTEGER,
            IDCliente INTEGER,
            Incoterm TEXT,
            Veiculo TEXT,
            pallets INTEGER,
            QtdTransp INTEGER,
            Moeda TEXT,
            VlrFrete REAL,
            Dist REAL,
            FOREIGN KEY (IDFabrica) REFERENCES fabricas(IDFabrica),
            FOREIGN KEY (IDCliente) REFERENCES clientes(IDCliente)
        );
        """)

        print("Tabelas criadas ou já existentes.")
    except sqlite3.Error as e:
        print(f"Erro ao criar as tabelas: {e}")

def clean_column_names(df):
    """
    Limpa os nomes das colunas do DataFrame para remover caracteres indesejados.
    
    :param df: DataFrame pandas
    :return: DataFrame com nomes de colunas limpos
    """
    df.columns = df.columns.str.strip()  # Remove espaços em branco ao redor dos nomes das colunas
    df.columns = df.columns.str.replace(';', '')  # Remove ponto e vírgula dos nomes das colunas
    df.columns = df.columns.str.replace('"', '')  # Remove aspas duplas dos nomes das colunas
    return df

def insert_data_from_csv(connection):
    """
    Insere dados dos arquivos CSV para as tabelas do banco de dados.
    
    :param connection: Conexão com o banco de dados SQLite
    """
    cursor = connection.cursor()  # Cria um cursor para executar comandos SQL

    # Leitura dos arquivos CSV com codificação UTF-8
    df_fabricas = pd.read_csv(r'csv\\Fabricas.csv', encoding='utf-8', delimiter=';')
    df_clientes = pd.read_csv(r'csv\\Clientes.csv', encoding='utf-8', delimiter=';')
    df_rotas = pd.read_csv(r'csv\\Rotas.csv', encoding='utf-8', delimiter=';')

    # Limpa os nomes das colunas para garantir que estão corretos
    df_fabricas = clean_column_names(df_fabricas)
    df_clientes = clean_column_names(df_clientes)
    df_rotas = clean_column_names(df_rotas)

    # Exibe os nomes das colunas e o tamanho dos DataFrames para depuração
    print("Colunas em df_fabricas:", df_fabricas.columns)
    print("Colunas em df_clientes:", df_clientes.columns)
    print("Colunas em df_rotas:", df_rotas.columns)
    print(f"Tamanho do DataFrame df_rotas: {len(df_rotas)} registros")

    try:
        # Insere os dados na tabela 'fabricas'
        for _, row in df_fabricas.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO fabricas (IDFabrica, MUN, MUNMIN, SGUF, LAT, LONG) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['IDFabrica'], row['MUN'], row['MUNMIN'], row['SGUF'], row['LAT'], row['LONG']))
        
        # Insere os dados na tabela 'clientes'
        for _, row in df_clientes.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO clientes (IDCliente, MUN, LAT, LONG) 
                VALUES (?, ?, ?, ?)
            """, (row['IDCliente'], row['MUN'], row['LAT'], row['LONG']))

        # Insere os dados na tabela 'rotas'
        for _, row in df_rotas.iterrows():
            cursor.execute("""
                INSERT INTO rotas (Emissao, Entrega, MesBase, AnoExec, IDFabrica, IDCliente, Incoterm, Veiculo, pallets, QtdTransp, Moeda, VlrFrete, Dist) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (row['Emissao'], row['Entrega'], row['MesBase'], row['AnoExec'], row['IDFabrica'], row['IDCliente'], 
                  row['Incoterm'], row['Veiculo'], row['pallets'], row['QtdTransp'], row['Moeda'], row['VlrFrete'], row['Dist']))

        connection.commit()  # Confirma as mudanças no banco de dados
        print("Dados inseridos com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    # Define o nome do arquivo do banco de dados SQLite
    database = "seu_banco.db"
    
    # Cria uma conexão com o banco de dados
    conn = create_connection(database)
    if conn:
        # Cria as tabelas no banco de dados
        create_tables(conn)
        
        # Insere os dados dos arquivos CSV no banco de dados
        insert_data_from_csv(conn)
        
        # Fecha a conexão com o banco de dados
        conn.close()
