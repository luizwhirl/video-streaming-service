# rating_and_reviews.py

# Content Rating and Reviews: Enabling users to rate and review content;
from utility import limpar_tela
import time
from library_management import obter_catalogo_do_perfil

class Avaliacoes:
    def __init__(self):
        self.avaliacoes = []

    def definir_avaliacao(self, nome, conteudo, nota, comentario):
        avaliacao = {
            "usuario": nome,
            "conteudo": conteudo,
            "nota": nota,
            "comentario": comentario
        }
        self.avaliacoes.append(avaliacao)

    def postar_avaliacao(self, usuario, conteudo):
        limpar_tela()
        print(f"Postar avaliação para: {conteudo}")
        
        while True:
            try:
                nota_str = input("Digite a nota (de 1 a 5): ")
                nota = int(nota_str)
                if 1 <= nota <= 5:
                    break
                else:
                    print("Nota inválida. Por favor, insira um número entre 1 e 5.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        comentario = input("Digite seu comentário sobre o conteúdo: ")
        self.definir_avaliacao(usuario.nome, conteudo, nota, comentario)
        print("Avaliação postada com sucesso!")
        time.sleep(1.5)

    def mostrar_avaliacoes(self):
        if not self.avaliacoes:
            print("Nenhuma avaliação foi postada ainda.")
            return

        for avaliacao in self.avaliacoes:
            if isinstance(avaliacao["nota"], int):
                avaliacao["nota"] = "★" * avaliacao["nota"] + "☆" * (5 - avaliacao["nota"])
            
            print("═" * 60)
            print(f"@ {avaliacao['usuario']}")
            print(f"Conteúdo: {avaliacao['conteudo']}")
            print(f"Nota: {str(avaliacao['nota'])}")
            print(f"Comentário: {avaliacao['comentario']}")
            print("═" * 60)

    def obter_avaliacoes(self):
        return self.avaliacoes

def processo_para_avaliar(usuario, reviews):
    while True:
        limpar_tela()
        print("O que deseja fazer?")
        print("╔" + "═" * 50 + "╗")
        print("1. Ver avaliações e reviews\n")
        print("2. Fazer uma Review/Avaliação\n")
        print("3. Voltar ao menu principal")
        print("╚" + "═" * 50 + "╝")
        opcao = input("Digite a opção desejada: ")

        if opcao == "1":
            limpar_tela()
            reviews.mostrar_avaliacoes()
            input("\nPressione Enter para continuar...")
            
        elif opcao == "2":
            limpar_tela()
            # 1. verificamos se o plano do usuário permite avaliações
            if usuario.plano.nome == "Gratuito":
                print("Usuários no plano gratuito não podem postar reviews/avaliações.")
                time.sleep(2)
                continue

            # 2. pedimos para o usuário selecionar um perfil
            print("Selecione o perfil para fazer a avaliação:")
            if not usuario.listar_perfis():
                time.sleep(2)
                continue
            
            nome_perfil = input("Digite o nome do perfil (ou pressione Enter para cancelar): ")
            if not nome_perfil:
                continue
            
            perfil = usuario.obter_perfil_por_nome(nome_perfil)
            if not perfil:
                print(f"Perfil '{nome_perfil}' não encontrado.")
                time.sleep(2)
                continue

            # 3. pedimos o título do negocio
            conteudo_titulo = input("Digite o nome do conteúdo que deseja avaliar: ")
            
            # 4. verficamos se o conteúdo existe no catálogo do perfil
            catalogo = obter_catalogo_do_perfil(perfil)
            resultados_busca = catalogo.buscar_por_titulo(conteudo_titulo)
            
            if not resultados_busca:
                print("Conteúdo não encontrado na biblioteca.")
                time.sleep(2)
                continue
            
            midia_alvo = resultados_busca[0]

            # 5. i verificamos se o conteúdo está no histórico de exibição do perfil
            historico_do_perfil = perfil.historico.historico
            
            foi_assistido = any(midia.titulo == midia_alvo.titulo for midia in historico_do_perfil)
            
            if foi_assistido:
                # assistido = então pode
                reviews.postar_avaliacao(usuario, midia_alvo.titulo)
            else:
                # não assistido = então não pode
                print(f"\nVocê precisa assistir a '{midia_alvo.titulo}' no perfil '{perfil.nome_perfil}' antes de poder avaliá-lo.")
                input("Pressione Enter para continuar...")

        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)