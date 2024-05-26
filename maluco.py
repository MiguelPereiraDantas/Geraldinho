from anytree import Node, RenderTree, AsciiStyle
from anytree.exporter import DotExporter
import networkx as nx
from textblob import TextBlob

class Usuario:
    def __init__(self, nome, foto_perfil=None, biografia=None):
        self.nome = nome
        self.foto_perfil = foto_perfil
        self.biografia = biografia
        self.no = Node(nome)
        self.interacoes = []

    def adicionar_interacao(self, texto):
        self.interacoes.append(texto)

    def editar_perfil(self, nome=None, foto_perfil=None, biografia=None):
        if nome:
            self.nome = nome
        if foto_perfil:
            self.foto_perfil = foto_perfil
        if biografia:
            self.biografia = biografia

class RedeSocial:
    def __init__(self):
        self.usuarios = {}
        self.grafo = nx.Graph()

    def inserir_usuario(self, nome, nome_parente=None):
        if nome in self.usuarios:
            print(f"Usuário {nome} já existe na rede.")
            return

        novo_usuario = Usuario(nome)
        self.usuarios[nome] = novo_usuario
        self.grafo.add_node(nome)

        if nome_parente:
            if nome_parente in self.usuarios:
                novo_usuario.no.parent = self.usuarios[nome_parente].no
                self.grafo.add_edge(nome_parente, nome)
            else:
                print(f"Usuário {nome_parente} não encontrado na rede. Adicionando {nome} sem pai.")

    def remover_usuario(self, nome):
        if nome not in self.usuarios:
            print(f"Usuário {nome} não encontrado na rede.")
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
            print("A rede social está vazia.")
            return

        raiz = next((usuario.no for usuario in self.usuarios.values() if usuario.no.is_root), None)
        if raiz:
            for pre, fill, node in RenderTree(raiz, style=AsciiStyle()):
                print(f"{pre}{node.name}")

    def buscar_usuario(self, nome):
        if nome not in self.usuarios:
            print(f"Usuário {nome} não encontrado na rede.")
            return

        usuario = self.usuarios[nome]
        print(f"Usuário: {usuario.nome}")
        if usuario.no.parent:
            print(f"Parente: {usuario.no.parent.name}")
        else:
            print("Parente: Nenhum")
        print("Filhos: ", [filho.name for filho in usuario.no.children])
        print("Interações: ", usuario.interacoes)

    def exportar_arvore(self, filename='arvore_rede_social'):
        if not self.usuarios:
            print("A rede social está vazia.")
            return

        raiz = next((usuario.no for usuario in self.usuarios.values() if usuario.no.is_root), None)
        if raiz:
            DotExporter(raiz).to_picture(f"{filename}.png")
            print(f"Árvore exportada para {filename}.png")

    def identificar_comunidades(self):
        comunidades = list(nx.community.label_propagation_communities(self.grafo))
        for i, comunidade in enumerate(comunidades, 1):
            print(f"Comunidade {i}: {list(comunidade)}")

    def calcular_centralidade(self):
        centralidade = nx.betweenness_centrality(self.grafo)
        for usuario, centralidade in centralidade.items():
            print(f"Usuário: {usuario}, Centralidade: {centralidade:.4f}")

    def adicionar_interacao(self, nome, texto):
        if nome in self.usuarios:
            self.usuarios[nome].adicionar_interacao(texto)
        else:
            print(f"Usuário {nome} não encontrado na rede.")

    def analisar_sentimentos(self):
        for usuario in self.usuarios.values():
            polaridades = [TextBlob(interacao).sentiment.polarity for interacao in usuario.interacoes]
            if polaridades:
                sentimento_medio = sum(polaridades) / len(polaridades)
                print(f"Usuário: {usuario.nome}, Sentimento médio: {sentimento_medio:.4f}")
            else:
                print(f"Usuário: {usuario.nome}, Sem interações para analisar")

    def editar_perfil_usuario(self, nome):
        if nome in self.usuarios:
            usuario = self.usuarios[nome]
            novo_nome = input("Novo nome (deixe em branco para manter o atual): ")
            nova_foto_perfil = input("Nova foto de perfil (deixe em branco para manter a atual): ")
            nova_biografia = input("Nova biografia (deixe em branco para manter a atual): ")
            usuario.editar_perfil(nome=novo_nome or usuario.nome,
                                   foto_perfil=nova_foto_perfil or usuario.foto_perfil,
                                   biografia=nova_biografia or usuario.biografia)
            print("Perfil atualizado com sucesso!")
        else:
            print(f"Usuário {nome} não encontrado na rede.")

# Exemplo de uso:
rede = RedeSocial()

while True:
    print("\n1. Adicionar usuário")
    print("2. Remover usuário")
    print("3. Visualizar árvore")
    print("4. Buscar usuário")
    print("5. Adicionar interação")
    print("6. Exportar árvore")
    print("7. Identificar comunidades")
    print("8. Calcular centralidade")
    print("9. Analisar sentimentos")
    print("10. Editar perfil")
    print("0. Sair")
    
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome = input("Nome do usuário: ")
        nome_parente = input("Nome do parente (ou deixe vazio): ")
        rede.inserir_usuario(nome, nome_parente if nome_parente else None)
    elif escolha == "2":
        nome = input("Nome do usuário a remover: ")
        rede.remover_usuario(nome)
    elif escolha == "3":
        rede.visualizar_arvore()
    elif escolha == "4":
        nome = input("Nome do usuário a buscar: ")
        rede.buscar_usuario(nome)
    elif escolha == "5":
        nome = input("Nome do usuário: ")
        texto = input("Interação: ")
        rede.adicionar_interacao(nome, texto)
    elif escolha == "6":
        filename = input("Nome do arquivo")
        rede.exportar_arvore(filename)
    elif escolha == "7":
        rede.identificar_comunidades()
    elif escolha == "8":
        rede.calcular_centralidade()
    elif escolha == "9":
        rede.analisar_sentimentos()
    elif escolha == "10":
        nome = input("Nome do usuário para editar perfil: ")
        rede.editar_perfil_usuario(nome)
    elif escolha == "0":
        break
    else:
        print("Opção inválida. Tente novamente.")
