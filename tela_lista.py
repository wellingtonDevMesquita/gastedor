import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TelaLista(ctk.CTkFrame):
    def __init__(self, pai, controller):
        super().__init__(pai)
        self.controller = controller
       
        # --- Cabeçalho e Filtros (já criados antes) ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=7)
        
        self.filtro_frame = ctk.CTkFrame(self)
        self.filtro_frame.pack(fill="x", padx=20, pady=7)
        
        # Filtros de Mês e Ano (como no passo anterior)
        self.filtro_mes = ctk.CTkComboBox(self.filtro_frame, values=["Todos", "Janeiro", "Fevereiro", "Março"], command=self.filtrar)
        self.filtro_mes.pack(side="left", padx=7)
        self.filtro_ano = ctk.CTkComboBox(self.filtro_frame, values=["Todos", "2026", "2027", "2028"], command=self.filtrar)
        self.filtro_ano.pack(side="left", padx=7)
        self.container_botao = ctk.CTkFrame(self, fg_color="transparent")
        self.container_botao.pack(fill="x", padx=20)

        self.btn_new = ctk.CTkButton(self.container_botao, text="Novo", command=self.novo_item)
        self.btn_new.pack(pady=20,padx=20,side="right")
        # --- Layout de Dados ---
        # Dividimos a tela em duas partes: Lista em cima e Gráfico embaixo
        self.scroll = ctk.CTkScrollableFrame(self, height=200) # Altura menor para caber o gráfico
        self.scroll.pack(fill="both", expand=True, padx=20, pady=7)

        # Container do Gráfico
        self.graph_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.canvas = None # Armazenará o gráfico

    def filtrar(self, _=None):
        self.atualizar_lista()
    def gerar_grafico(self, dados):
        # 1. Limpar gráfico anterior e referências
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if not dados:
            return

        # 2. Agrupar preços por categoria (igual antes)
        categorias_soma = {}
        for item in dados:
          # item[2] é o preço, item[3] é a categoria (baseado na sua ordem do database.py)
            preco = item[2]
            cat = item[3]
    
            if not cat: cat = "Geral"
            categorias_soma[cat] = categorias_soma.get(cat, 0) + preco

        # Preparar dados para o Matplotlib
        nomes_cat = list(categorias_soma.keys())
        valores = list(categorias_soma.values())

        # 3. Gerar Cores Dinâmicas
        # Usamos o colormap 'Set3' que tem cores pastéis ótimas para fundos escuros.
        # Ele gera uma cor para cada índice de categoria.
        num_categorias = len(nomes_cat)
        
        # Cria uma lista de cores (RGBA) baseada na quantidade de categorias
        cmap = plt.get_cmap('Set3')
        cores_barras = [cmap(i) for i in range(num_categorias)]

        # 4. Criar a figura (estilo dark)
        # dpi=80 para um gráfico ligeiramente menor e mais nítido na tela
        fig, ax = plt.subplots(figsize=(6, 4), dpi=80) 
        fig.patch.set_facecolor('#2b2b2b') # Cor de fundo do CustomTkinter Dark
        ax.set_facecolor('#2b2b2b')
        
        # Criar as barras aplicando a lista de cores
        barras = ax.bar(nomes_cat, valores, color=cores_barras)
        
        # Adicionar rótulos de valor no topo de cada barra
        for barra in barras:
            height = barra.get_height()
            ax.annotate(f'R$ {height:.2f}',
                        xy=(barra.get_x() + barra.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', color='white', fontsize=9)

        # 5. Estilização dos Eixos e Título (essencial para tema Dark)
        ax.tick_params(axis='x', colors='white', labelsize=10)
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False) # Esconde borda superior
        ax.spines['right'].set_visible(False) # Esconde borda direita
        
        # ax.set_ylabel("Valor Total (R$)", color='white')
        ax.set_title("Gastos por Categoria (Período)", color='white', pad=15, fontdict={'fontsize': 14, 'weight': 'bold'})

        # 6. Integrar o gráfico ao CustomTkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Fecha a figura para liberar a memória do Python (RX 7600 agradece)
        plt.close(fig)



    def novo_item(self):
        self.controller.show_frame("TelaCadastro")


    def atualizar_lista(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        mes = self.filtro_mes.get()
        ano = self.filtro_ano.get()
        
        dados = self.controller.db.listar(mes, ano)
        
        # Gerar a tabela
        for item in dados:
            row = ctk.CTkFrame(self.scroll, height=35)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{item[1]} | {item[3]}").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"R$ {item[2]:.2f}", text_color="#2ecc71").pack(side="right", padx=10)

        # Atualizar o gráfico com os mesmos dados filtrados
        self.gerar_grafico(dados)