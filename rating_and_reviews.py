# rating_and_reviews.py

# Content Rating and Reviews: Enabling users to rate and review content;
from utility import limpar_tela
import time

# SINGLETON
# essa classe agora garante que apenas uma instância dela exista em todo o sistema
# isso centraliza o gerenciamento de todas as avaliações
class Avaliacoes:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Avaliacoes, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.avaliacoes = []
        self._initialized = True

    def definir_avaliacao(self, nome_usuario, midia, nota, comentario):
        if isinstance(midia, str):
            id_conteudo = None 
            titulo_conteudo = midia
        else:
            id_conteudo = midia.id_midia
            titulo_conteudo = midia.titulo

        # verificamos se o usuário já avaliou este conteúdo
        for avaliacao in self.avaliacoes:
            if avaliacao['usuario'] == nome_usuario and avaliacao['id_conteudo'] == id_conteudo:
                print(f"{nome_usuario} já avaliou '{titulo_conteudo}'. A avaliação não será duplicada.")
                time.sleep(2)
                return

        avaliacao = {
            "usuario": nome_usuario,
            "id_conteudo": id_conteudo,
            "titulo_conteudo": titulo_conteudo,
            "nota": nota,
            "comentario": comentario
        }
        self.avaliacoes.append(avaliacao)

    def postar_avaliacao(self, usuario, midia_selecionada):
        while True:
            try:
                nota_str = input("Digite a nota (1 a 5): ")
                nota = int(nota_str)
                if not 1 <= nota <= 5:
                    print("Nota inválida. Por favor, insira um número entre 1 e 5.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        comentario = input("Digite seu comentário sobre o conteúdo: ")
        self.definir_avaliacao(usuario.nome, midia_selecionada, self.formatar_nota_estrelas(nota), comentario)
        print("Avaliação postada com sucesso!")
        time.sleep(1.5)

    def formatar_nota_estrelas(self, nota_num):
        if isinstance(nota_num, str):
            return nota_num
        return "★" * nota_num + "☆" * (5 - nota_num)

    def mostrar_avaliacoes(self):
        if not self.avaliacoes:
            print("Nenhuma avaliação foi postada ainda.")
            return

        for avaliacao in self.avaliacoes:
            print("═" * 60)
            print(f"@ {avaliacao['usuario']}")
            print(f"Conteúdo: {avaliacao['titulo_conteudo']}")
            print(f"Nota: {avaliacao['nota']}")
            print(f"Comentário: {avaliacao['comentario']}")
            print("═" * 60)

    def mostrar_avaliacoes_por_id(self, id_conteudo):
        avaliacoes_filtradas = [
            a for a in self.avaliacoes if a['id_conteudo'] == id_conteudo
        ]

        if not avaliacoes_filtradas:
            print("Este conteúdo ainda não possui avaliações.")
            return

        for avaliacao in avaliacoes_filtradas:
            print("═" * 60)
            print(f"@ {avaliacao['usuario']}")
            print(f"Nota: {avaliacao['nota']}")
            print(f"Comentário: {avaliacao['comentario']}")
            print("═" * 60)

    def obter_avaliacoes(self):
        return self.avaliacoes

def processo_para_avaliar(usuario, reviews):
    from library_management import todas_as_midias, ConjuntoMidias

    while True:
        limpar_tela()
        print("O que deseja fazer?")
        print("╔" + "═" * 50 + "╗")
        print("1. Ver todas as avaliações")
        print("2. Fazer uma avaliação")
        print("3. Voltar ao menu principal")
        print("╚" + "═" * 50 + "╝")
        opcao = input("Digite a opção desejada: ")

        if opcao == "1":
            limpar_tela()
            reviews.mostrar_avaliacoes()
            input("\nPressione Enter para continuar...")
        
        elif opcao == "2":
            limpar_tela()
            if usuario.plano.nome == "Gratuito":
                print("Usuários no plano gratuito não podem postar avaliações.")
                time.sleep(2)
                continue

            print("Selecione o perfil para fazer a avaliação:")
            if not usuario.listar_perfis():
                time.sleep(1.5)
                continue
            
            nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
            if not nome_perfil:
                continue

            perfil = usuario.obter_perfil_por_nome(nome_perfil)
            if not perfil:
                print(f"Perfil '{nome_perfil}' não encontrado.")
                time.sleep(1.5)
                continue
            
            catalogo = ConjuntoMidias()
            catalogo.midias.extend(todas_as_midias())

            titulo = input("Digite o título do conteúdo que deseja avaliar: ")
            resultados = catalogo.buscar_por_titulo(titulo)

            if not resultados:
                print("Conteúdo não encontrado.")
                time.sleep(1.5)
                continue

            print("\nConteúdos encontrados:\n")
            for idx, midia in enumerate(resultados):
                print(f"[{idx + 1}]")
                midia.exibir_informacoes()
                print()

            escolha_conteudo = input("Digite o número do conteúdo que deseja avaliar (ou pressione Enter para cancelar): ")
            if not escolha_conteudo.isdigit():
                continue
            
            indice = int(escolha_conteudo) - 1
            if 0 <= indice < len(resultados):
                conteudo_escolhido = resultados[indice]

                if conteudo_escolhido not in perfil.historico.historico:
                    print("\nVocê só pode avaliar conteúdos que já assistiu.")
                    print("Por favor, assista ao conteúdo antes de deixar uma avaliação.")
                    time.sleep(3)
                    continue

                limpar_tela()
                print(f"Avaliando: {conteudo_escolhido.titulo}")
                reviews.postar_avaliacao(usuario, conteudo_escolhido)
            else:
                print("Opção inválida.")
                time.sleep(1.5)

        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)