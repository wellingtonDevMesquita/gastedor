import customtkinter as ctk
from database import BancoDados
from tela_cadastro import TelaCadastro
from tela_lista import TelaLista

class FinanceiroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gastedor")
        self.geometry("1280x720")

        self.db = BancoDados()

        # Container principal onde as telas serão montadas

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        # Inicializa as telas
        for F in (TelaCadastro, TelaLista):
            page_name = F.__name__
            frame = F(pai=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame("TelaLista")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "TelaLista":
            frame.atualizar_lista() 
        frame.tkraise() # Traz a tela para a frente

if __name__ == "__main__":
    app = FinanceiroApp()
    app.mainloop()