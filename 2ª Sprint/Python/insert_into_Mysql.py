import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Função para criar a conexão com o MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='api6sem',
            user='root',
            password='3366',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao MySQL: {e}")
        return None

def fetch_existing_ids(connection):
    """Busca IDs existentes de fábricas e clientes no banco de dados."""
    cursor = connection.cursor()
    
    cursor.execute("SELECT IDFabrica FROM fabricas")
    fabricas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT IDCliente FROM clientes")
    clientes = [row[0] for row in cursor.fetchall()]
    
    return fabricas, clientes

# Função para inserir dados da rota no banco de dados MySQL
def insert_rota(connection, data):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO rotas (Emissao, Entrega, MesBase, AnoExec, IDFabrica, IDCliente, Incoterm, Veiculo, pallets, QtdTransp, Moeda, VlrFrete, Dist) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
        connection.commit()
        messagebox.showinfo("Sucesso", "Rota cadastrada com sucesso!")
        clear_fields()  # Limpa os campos após a inserção bem-sucedida
        update_route_display()  # Atualiza a exibição dos últimos registros
    except mysql.connector.Error as e:
        messagebox.showerror("Erro ao Inserir", f"Erro ao inserir rota: {e}")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Erro inesperado: {e}")

# Função para deletar uma rota pelo ID
def delete_rota(connection, rota_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM rotas WHERE id = %s", (rota_id,))
        connection.commit()
        messagebox.showinfo("Sucesso", "Rota deletada com sucesso!")
        update_route_display()  # Atualiza a exibição após a exclusão
    except mysql.connector.Error as e:
        messagebox.showerror("Erro ao Deletar", f"Erro ao deletar rota: {e}")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Erro inesperado: {e}")

def fetch_last_routes(connection, limit=3):
    """Busca os últimos registros de rotas no banco de dados."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM rotas ORDER BY ID DESC LIMIT {limit}")
    return cursor.fetchall()

# Função para exibir as rotas (pode ser adaptada para exibir no Tkinter)
def fetch_routes(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM rotas")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Erro ao Consultar", f"Erro ao consultar rotas: {e}")
    return []

def validate_fields():
    """Verifica se todos os campos foram preenchidos."""
    if not emissao_entry.get() or not entrega_entry.get() or not mes_base_entry.get() or not ano_exec_entry.get():
        return False
    if not id_fabrica_combobox.get() or not id_cliente_combobox.get() or not incoterm_combobox.get():
        return False
    if not veiculo_entry.get() or not pallets_entry.get() or not qtd_transp_entry.get():
        return False
    if not moeda_entry.get() or not vlr_frete_entry.get() or not dist_entry.get():
        return False
    return True

# Função para limpar os campos de entrada
def clear_fields():
    emissao_entry.delete(0, tk.END)
    entrega_entry.delete(0, tk.END)
    mes_base_entry.delete(0, tk.END)
    ano_exec_entry.delete(0, tk.END)
    veiculo_entry.delete(0, tk.END)
    pallets_entry.delete(0, tk.END)
    qtd_transp_entry.delete(0, tk.END)
    moeda_entry.delete(0, tk.END)
    vlr_frete_entry.delete(0, tk.END)
    dist_entry.delete(0, tk.END)

# Função para atualizar a exibição das rotas
def update_route_display():
    """Atualiza a exibição dos últimos registros de rotas."""
    last_routes = fetch_last_routes(conn)
    route_display.delete(0, tk.END)  # Limpa o conteúdo anterior
    for route in last_routes:
        route_display.insert(tk.END, f"ID: {route[14]}, Emissão: {route[0]}, Entrega: {route[1]}, Cliente: {route[5]}")  # Adiciona cada rota

def validate_length(new_value, max_length):
    """Valida que o campo de texto não exceda um certo número de caracteres."""
    try:
        max_length = int(max_length)  # Converte max_length para inteiro
        return len(new_value) <= max_length
    except ValueError:
        return False

def validate_integer(new_value):
    """Valida que o campo aceite apenas números inteiros."""
    return new_value.isdigit() or new_value == ""

def validate_float(new_value):
    """Valida que o campo aceite apenas números flutuantes com até duas casas decimais."""
    try:
        float_value = float(new_value)
        return True
    except ValueError:
        return new_value == ""

def format_date_entry(entry):
    """Formata a entrada de data automaticamente como DD/MM/YYYY."""
    text = entry.get()
    formatted_text = text.replace("/", "")
    
    # Adiciona barras na posição correta para formatar a data como DD/MM/YYYY
    if len(formatted_text) > 2:
        formatted_text = formatted_text[:2] + "/" + formatted_text[2:]
    if len(formatted_text) > 5:
        formatted_text = formatted_text[:5] + "/" + formatted_text[5:]
    
    entry.delete(0, tk.END)
    entry.insert(0, formatted_text)

def on_emissao_change(event):
    """Callback para quando o campo Emissão é modificado. Atualiza 'MesBase' e 'AnoExec'."""
    format_date_entry(emissao_entry)  # Formata automaticamente a entrada de data

    emissao_text = emissao_entry.get()
    try:
        # Converte o texto da data para um objeto datetime usando o novo formato
        emissao_date = datetime.strptime(emissao_text, '%d/%m/%Y')
        mes_base_entry.config(state='normal')  # Ativar temporariamente para preenchimento
        ano_exec_entry.config(state='normal')  # Ativar temporariamente para preenchimento
        mes_base_entry.delete(0, tk.END)
        mes_base_entry.insert(0, emissao_date.strftime('%m'))
        ano_exec_entry.delete(0, tk.END)
        ano_exec_entry.insert(0, emissao_date.strftime('%Y'))
        mes_base_entry.config(state='readonly')  # Voltar para readonly
        ano_exec_entry.config(state='readonly')  # Voltar para readonly
    except ValueError:
        mes_base_entry.config(state='normal')
        ano_exec_entry.config(state='normal')
        mes_base_entry.delete(0, tk.END)
        ano_exec_entry.delete(0, tk.END)
        mes_base_entry.config(state='readonly')
        ano_exec_entry.config(state='readonly')

def on_entrega_change(event):
    """Callback para quando o campo Entrega é modificado."""
    format_date_entry(entrega_entry)

def delete_selected_route():
    """Deleta a rota selecionada no Listbox."""
    try:
        selected_index = route_display.curselection()[0]  # Obtém o índice do item selecionado
        selected_route = route_display.get(selected_index)  # Obtém o texto do item selecionado
        route_id = selected_route.split(",")[0].split(":")[1].strip()  # Extrai o ID da rota do texto
        delete_rota(conn, route_id)  # Chama a função para deletar o registro no banco de dados
    except IndexError:
        messagebox.showwarning("Aviso", "Nenhuma rota selecionada para deletar.")

def update_fields_based_on_incoterm(event):
    """Atualiza os campos de Veículo, Pallets e Qtd Transp com base no Incoterm selecionado."""
    incoterm_value = incoterm_combobox.get()
    if incoterm_value == "CIF":
        veiculo_entry.delete(0, tk.END)
        veiculo_entry.insert(0, "P12")
        pallets_entry.delete(0, tk.END)
        pallets_entry.insert(0, "12")
        qtd_transp_entry.delete(0, tk.END)
        qtd_transp_entry.insert(0, "1800")
    elif incoterm_value == "FOB":
        veiculo_entry.delete(0, tk.END)
        veiculo_entry.insert(0, "P24")
        pallets_entry.delete(0, tk.END)
        pallets_entry.insert(0, "24")
        qtd_transp_entry.delete(0, tk.END)
        qtd_transp_entry.insert(0, "3600")
    else:
        # Limpa os campos se a opção não for válida
        veiculo_entry.delete(0, tk.END)
        pallets_entry.delete(0, tk.END)
        qtd_transp_entry.delete(0, tk.END)

def uppercase_entry(event):
    """Converte o texto do campo para maiúsculas automaticamente."""
    current_text = moeda_entry.get()
    moeda_entry.delete(0, tk.END)
    moeda_entry.insert(0, current_text.upper())

def create_app(connection):
    """Cria a interface gráfica para cadastro de novas rotas."""
    global emissao_entry, mes_base_entry, ano_exec_entry, entrega_entry
    global id_fabrica_combobox, id_cliente_combobox, incoterm_combobox
    global veiculo_entry, pallets_entry, qtd_transp_entry, moeda_entry, vlr_frete_entry, dist_entry
    global route_display

    root = tk.Tk()
    root.title("Cadastro de Nova Rota")
    
    # Configurar estilo ttk
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10, 'bold'), background='#007ACC', foreground='white')
    style.configure('TEntry', font=('Arial', 10))
    style.configure('TCombobox', font=('Arial', 10))
    style.map('TButton', background=[('active', '#005999')])

    # Configuração responsiva
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    root.columnconfigure(2, weight=3)
    root.rowconfigure(14, weight=1)

    fabricas, clientes = fetch_existing_ids(connection)

    ttk.Label(root, text="Emissão (DD/MM/YYYY):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    emissao_entry = ttk.Entry(root)
    emissao_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    emissao_entry.bind("<KeyRelease>", on_emissao_change)

    ttk.Label(root, text="Entrega (DD/MM/YYYY):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entrega_entry = ttk.Entry(root)
    entrega_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    entrega_entry.bind("<KeyRelease>", on_entrega_change)

    ttk.Label(root, text="Mês Base:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    mes_base_entry = ttk.Entry(root, state='readonly')
    mes_base_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="Ano Exec:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    ano_exec_entry = ttk.Entry(root, state='readonly')
    ano_exec_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="ID Fábrica:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
    id_fabrica_combobox = ttk.Combobox(root, values=fabricas, state='readonly')
    id_fabrica_combobox.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="ID Cliente:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
    id_cliente_combobox = ttk.Combobox(root, values=clientes, state='readonly')
    id_cliente_combobox.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

    vcmd_length_5 = root.register(validate_length)
    vcmd_integer = root.register(validate_integer)
    vcmd_float = root.register(validate_float)

    ## Criação da Combobox para Incoterm
    ttk.Label(root, text="Incoterm:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
    incoterm_combobox = ttk.Combobox(root, values=["CIF", "FOB"], state='readonly')
    incoterm_combobox.grid(row=6, column=1, sticky='ew', padx=5, pady=5)
    incoterm_combobox.bind("<<ComboboxSelected>>", update_fields_based_on_incoterm)  # Evento de mudança

    ttk.Label(root, text="Veículo:").grid(row=7, column=0, sticky='e', padx=5, pady=5)
    veiculo_entry = ttk.Entry(root)
    veiculo_entry.grid(row=7, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="Pallets:").grid(row=8, column=0, sticky='e', padx=5, pady=5)
    pallets_entry = ttk.Entry(root, validate='key', validatecommand=(vcmd_integer, '%P'))
    pallets_entry.grid(row=8, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="Qtd Transp:").grid(row=9, column=0, sticky='e', padx=5, pady=5)
    qtd_transp_entry = ttk.Entry(root, validate='key', validatecommand=(vcmd_integer, '%P'))
    qtd_transp_entry.grid(row=9, column=1, sticky='ew', padx=5, pady=5)

    # Criação do campo "Moeda" com conversão automática para maiúsculas
    ttk.Label(root, text="Moeda:").grid(row=10, column=0, sticky='e', padx=5, pady=5)
    moeda_entry = ttk.Entry(root)
    moeda_entry.grid(row=10, column=1, sticky='ew', padx=5, pady=5)
    moeda_entry.bind("<KeyRelease>", uppercase_entry)  # Evento para transformar o texto em maiúsculas

    ttk.Label(root, text="Valor Frete:").grid(row=11, column=0, sticky='e', padx=5, pady=5)
    vlr_frete_entry = ttk.Entry(root, validate='key', validatecommand=(vcmd_float, '%P'))
    vlr_frete_entry.grid(row=11, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(root, text="Distância:").grid(row=12, column=0, sticky='e', padx=5, pady=5)
    dist_entry = ttk.Entry(root, validate='key', validatecommand=(vcmd_float, '%P'))
    dist_entry.grid(row=12, column=1, sticky='ew', padx=5, pady=5)

    def submit():
        """Coleta dados do formulário e insere no banco de dados."""
        if not validate_fields():
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        data = (
            emissao_entry.get(),
            entrega_entry.get(),
            mes_base_entry.get(),
            ano_exec_entry.get(),
            id_fabrica_combobox.get(),
            id_cliente_combobox.get(),
            incoterm_combobox.get(),  # Ajustado para pegar o valor da Combobox
            veiculo_entry.get(),
            pallets_entry.get(),
            qtd_transp_entry.get(),
            moeda_entry.get(),
            vlr_frete_entry.get(),
            dist_entry.get()
        )
        insert_rota(connection, data)

    # Configuração do estilo do botão
    style = ttk.Style()
    style.configure("SubmitButton.TButton", font=('Arial', 10, 'bold'), foreground="black")  # Define a cor do texto para preto

    # Botão "Cadastrar Rota" com o novo estilo
    submit_button = ttk.Button(root, text="Cadastrar Rota", command=submit, style="SubmitButton.TButton")
    submit_button.grid(row=13, column=0, columnspan=2, sticky='ew', padx=5, pady=10)

    # Área de exibição dos últimos registros de rotas
    route_display = tk.Listbox(root, width=70, height=15)
    route_display.grid(row=0, column=2, rowspan=14, padx=10, pady=5, sticky='nsew')
    
    # Botão para deletar rota selecionada
    style.configure("DeleteButton.TButton", font=('Arial', 10, 'bold'), foreground="black")  # Define a cor do texto para preto
    delete_button = ttk.Button(root, text="Deletar Rota", command=delete_selected_route, style="DeleteButton.TButton")
    delete_button.grid(row=14, column=2, pady=10, sticky='ew')

    update_route_display()  # Atualiza a exibição dos registros na inicialização

    root.mainloop()

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_app(conn)
        conn.close()