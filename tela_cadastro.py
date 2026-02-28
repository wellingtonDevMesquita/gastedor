import customtkinter as ctk
from datetime import datetime

class TelaCadastro(ctk.CTkFrame):
    def __init__(self, pai, controller):
        super().__init__(pai)
        self.controller = controller # Referência à classe mãe
        mesV = ["Janeiro", "Fevereiro","Março", "Abril",
                    "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro"]
        anoV = ["2026", "2027", "2028","2029","2030"]

        categoriasV = ["Alimentação","Moradia","Serviços",
                       "Saúde","Educação","Hardware","Jogos",
                       "Transporte","Lazer","Compras","Emergência"]

        fixaV = ["NAO","SIM"]

        ctk.CTkLabel(self, text="Novo Registro", font=("Arial", 20)).pack(pady=20)
        self.filtro_frame = ctk.CTkFrame(self)
        self.filtro_frame.pack(fill="x", padx=20, pady=5)
        self.nome = ctk.CTkEntry(self, placeholder_text="Nome", width=300)
        self.nome.pack(pady=5)
        
        self.preco = ctk.CTkEntry(self, placeholder_text="Preço", width=300)
        self.preco.pack(pady=5)

        self.categoria = ctk.CTkComboBox(self, values=categoriasV)
        self.categoria.pack(pady=10)

        self.fixa = ctk.CTkComboBox(self, values=fixaV)
        self.fixa.pack(pady=10)

        self.mes = ctk.CTkComboBox(self.filtro_frame, values=mesV)
        self.mes.pack(side="left", padx=5)
        self.mes.set(mesV[(datetime.now().month)-1])
        self.ano = ctk.CTkComboBox(self.filtro_frame, values=anoV)
        self.ano.set((datetime.now().year))
        self.ano.pack(side="left", padx=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar", command=self.enviar_dados)
        self.btn_salvar.pack(pady=20)

    def enviar_dados(self):
        dados = (self.nome.get(),
                float(self.preco.get()),
                self.categoria.get(),
                self.fixa.get(),
                self.mes.get(),
                self.ano.get(),
                datetime.now().strftime("%d/%m/%Y"))
        self.controller.db.salvar(dados)
        self.controller.show_frame("TelaLista")