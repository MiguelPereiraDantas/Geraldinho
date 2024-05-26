import networkx as nx
from textblob import TextBlob
from anytree import Node, RenderTree, AsciiStyle, find_by_attr
from anytree.exporter import DotExporter
import tkinter as tk
from tkinter import messagebox, simpledialog

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.no = Node(nome)
        self.interacoes = []

    def adicionar_interacao(self, texto):
        self.interacoes.append(texto)

class RedeSocial:
    def __init__(self):
        self.usuarios = {}
        self.grafo = nx.Graph()

    def inserir_usuario(self, nome, nome_parente=None):
        if nome in self.usuarios:
            messagebox.showinfo("Erro", f"Usuário {nome} já existe na rede.")
            return

        novo_usuario = Usuario(nome)
        self.usuarios[nome] = novo_usuario
        self.grafo.add_node(nome)

        if nome_parente:
            if nome_parente in self.usuarios:
                novo_usuario.no.parent = self.usuarios[nome_parente].no
                self.grafo.add_edge(nome_parente, nome)
            else:
                messagebox.showinfo("Erro", f"Usuário {nome_parente} não encontrado na rede. Adicionando {nome} sem pai.")

    def remover_usuario(self, nome):
        if nome not in self.usuarios:
            messagebox.showinfo("Erro", f"Usuário {nome} não encontrado na rede.")
            return

        usuario_a_remover = self.usuarios[nome]
        if usuario_a_remover.no.is_root:
            for filho in usuario_a_remover.no.children:
                filho.parent = None
        else:
            for filho in usuario_a_remover.no.children:
                filho.parent = usuario_a_remover.no.parent

        usuario_a_remover.no.parent = None
        del self.usuarios[nome]
        self.grafo.remove_node(nome)

    def visualizar_arvore(self):
        if not self.usuarios:
            messagebox.showinfo("Erro", "A rede social está vazia.")
            return

        raiz = next((usuario.no for usuario in self.usuarios.values() if usuario.no.is_root), None)
        if raiz:
            arvore_str = ""
            for pre, fill, node in RenderTree(raiz, style=AsciiStyle()):
                arvore_str += f"{pre}{node.name}\n"
            messagebox.showinfo("Árvore de Relacionamentos", arvore_str)

    def buscar_usuario(self, nome):
        if nome not in self.usuarios:
            messagebox.showinfo("Erro", f"Usuário {nome} não encontrado na rede.")
            return

        usuario = self.usuarios[nome]
        info = f"Usuário: {usuario.nome}\n"
        if usuario.no.parent:
            info += f"Parente: {usuario.no.parent.name}\n"
        else:
            info += "Parente: Nenhum\n"
        info += f"Filhos: {[filho.name for filho in usuario.no.children]}\n"
        info += f"Interações: {usuario.interacoes}"
        messagebox.showinfo("Informações do Usuário", info)

    def exportar_arvore(self, filename='arvore_rede_social'):
        if not self.usuarios:
            messagebox.showinfo("Erro", "A rede social está vazia.")
            return

        raiz = next((usuario.no for usuario in self.usuarios.values() if usuario.no.is_root), None)
        if raiz:
            DotExporter(raiz).to_picture(f"{filename}.png")
            messagebox.showinfo("Sucesso", f"Árvore exportada para {filename}.png")

    def identificar_comunidades(self):
        comunidades = list(nx.community.label_propagation_communities(self.grafo))
        comunidades_str = ""
        for i, comunidade in enumerate(comunidades, 1):
            comunidades_str += f"Comunidade {i}: {list(comunidade)}\n"
        messagebox.showinfo("Comunidades", comunidades_str)

    def calcular_centralidade(self):
        centralidade = nx.betweenness_centrality(self.grafo)
        centralidade_str = ""
        for usuario, centralidade in centralidade.items():
            centralidade_str += f"Usuário: {usuario}, Centralidade: {centralidade:.4f}\n"
        messagebox.showinfo("Centralidade", centralidade_str)

    def adicionar_interacao(self, nome, texto):
        if nome in self.usuarios:
            self.usuarios[nome].adicionar_interacao(texto)
        else:
            messagebox.showinfo("Erro", f"Usuário {nome} não encontrado na rede.")

    def analisar_sentimentos(self):
        sentimentos_str = ""
        for usuario in self.usuarios.values():
            polaridades = [TextBlob(interacao).sentiment.polarity for interacao in usuario.interacoes]
            if polaridades:
                sentimento_medio = sum(polaridades) / len(polaridades)
                sentimentos_str += f"Usuário: {usuario.nome}, Sentimento médio: {sentimento_medio:.4f}\n"
            else:
                sentimentos_str += f"Usuário: {usuario.nome}, Sem interações para analisar\n"
        messagebox.showinfo("Análise de Sentimentos", sentimentos_str)

class App:
    def __init__(self, root):
        self.rede = RedeSocial()

        self.root = root
        self.root.title("Rede Social")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Rede Social")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.add_user_button = tk.Button(self.frame, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.add_user_button.grid(row=1, column=0, pady=5)

        self.remove_user_button = tk.Button(self.frame, text="Remover Usuário", command=self.remover_usuario)
        self.remove_user_button.grid(row=1, column=1, pady=5)

        self.view_tree_button = tk.Button(self.frame, text="Visualizar Árvore", command=self.visualizar_arvore)
        self.view_tree_button.grid(row=2, column=0, pady=5)

        self.search_user_button = tk.Button(self.frame, text="Buscar Usuário", command=self.buscar_usuario)
        self.search_user_button.grid(row=2, column=1, pady=5)

        self.add_interaction_button = tk.Button(self.frame, text="Adicionar Interação", command=self.adicionar_interacao)
        self.add_interaction_button.grid(row=3, column=0, pady=5)

        self.export_tree_button = tk.Button(self.frame, text="Exportar Árvore", command=self.exportar_arvore)
        self.export_tree_button.grid(row=3, column=1, pady=5)

        self.identify_communities_button = tk.Button(self.frame, text="Identificar Comunidades", command=self.identificar_comunidades)
        self.identify_communities_button.grid(row=4, column=0, pady=5)

        self.calculate_centrality_button = tk.Button(self.frame, text="Calcular Centralidade", command=self.calcular_centralidade)
        self.calculate_centrality_button.grid(row=4, column=1, pady=5)

        self.analyze_sentiments_button = tk.Button(self.frame, text="Analisar Sentimentos", command=self.analisar_sentimentos)
        self.analyze_sentiments_button.grid(row=5, column=0, columnspan=2, pady=5)

    def adicionar_usuario(self):
        nome = simpledialog.askstring("Entrada", "Nome do usuário:")
        if nome:
            nome_parente = simpledialog.askstring("Entrada", "Nome do parente (ou deixe vazio):")
            self.rede.inserir_usuario(nome, nome_parente if nome_parente else None)

    def remover_usuario(self):
        nome = simpledialog.askstring("Entrada", "Nome do usuário a remover:")
        if nome:
            self.rede.remover_usuario(nome)

    def visualizar_arvore(self):
        self.rede.visualizar_arvore()

    def buscar_usuario(self):
        nome = simpledialog.askstring("Entrada", "Nome do usuário a buscar:")
        if nome:
            self.rede.buscar_usuario(nome)

    def adicionar_interacao(self):
        nome = simpledialog.askstring("Entrada", "Nome do usuário:")
        if nome:
            texto = simpledialog.askstring("Entrada", "Interação:")
            if texto:
                self.rede.adicionar_interacao(nome, texto)

    def exportar_arvore(self):
        filename = simpledialog.askstring("Entrada", "Nome do arquivo (sem extensão):")
        if filename:
            self.rede.exportar_arvore(filename)

    def identificar_comunidades(self):
        self.rede.identificar_comunidades()

    def calcular_centralidade(self):
        self.rede.calcular_centralidade()

    def analisar_sentimentos(self):
        self.rede.analisar_sentimentos()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
