import sqlite3

class BancoDados:
    def __init__(self):
        self.conexao = sqlite3.connect('financeiro.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT, preco REAL, categoria TEXT, mensal TEXT, mes TEXT, ano TEXT, data TEXT
            )
        ''')
        self.conexao.commit()

    def salvar(self, dados):
        self.cursor.execute("INSERT INTO transacoes (nome, preco, categoria, mensal, mes, ano, data) VALUES (?, ?, ?, ?, ?, ?, ?)", dados)
        self.conexao.commit()
        print("Insert")

    def listar(self, mes=None, ano=None):
        # Se os filtros forem "Todos", buscamos tudo
        query = "SELECT * FROM transacoes"
        params = []
        
        if (mes and mes != "Todos") or (ano and ano != "Todos"):
            query += " WHERE "
            filtros = []
            if ano and ano != "Todos":
                filtros.append("ano LIKE ?")
                params.append(f"{ano}%")
            if mes and mes != "Todos":
                # Mapeia nome do mês para número
                print(mes)
                filtros.append("mes LIKE ?")
                params.append(f"%{mes}%")
            
            query += " AND ".join(filtros)
            
        query += " ORDER BY data DESC"
        print("Query",query)
        self.cursor.execute(query, params)
       
        return self.cursor.fetchall()

    def deletar(self, id_item):
        self.cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_item,))
        self.conexao.commit()