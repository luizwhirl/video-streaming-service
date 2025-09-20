# library_management.py

# Content Library Management: Managing a library of streaming content, including movies and TV shows
from numpy import append
import random
from utility import limpar_tela, normalizar_texto
import time
from abc import ABC, abstractmethod
import datetime
from ads_management import realizar_exibicao_anuncio, redefinir_limite_diario
import json 

class ConjuntoMidias:
    # Referente a varias midias
    def __init__(self):
        self.midias= []
    
    def buscar_por_titulo(self, titulo):
        resultados = []
        titulo = normalizar_texto(titulo)
        for midia in self.midias:
            if titulo in normalizar_texto(midia.titulo):
                resultados.append(midia)
        return resultados if resultados else None

    def buscar_por_genero(self, genero):
        resultados = []
        genero = normalizar_texto(genero)
        for midia in self.midias:
            if genero in normalizar_texto(midia.genero):
                resultados.append(midia)
        return resultados if resultados else None

    def navegar(self, quantidade=5):
        print("\n🎬 Conteúdos sugeridos para você:\n")
        if not self.midias:
            print("Nenhum conteúdo disponível para navegar.")
            return
        amostra = random.sample(self.midias, min(quantidade, len(self.midias)))
        for midia in amostra:
            midia.exibir_informacoes()
            print()

class Midia(ABC):
    # Referente a uma midia especifica
    def __init__(self, titulo, genero, classificacao, tempo_duracao):
        self.titulo = titulo
        self.genero = genero
        self.classificacao = classificacao
        self.tempo_duracao = tempo_duracao
        self.assistido = False
        self.ultima_exibicao = None
        

    @abstractmethod
    def exibir_informacoes(self):
        pass

    def configurar_visualizacao(self):
        if self.assistido:
            status = (
                "✔️ Assistido "
                f"(Última exibição: {self.ultima_exibicao.strftime('%d/%m/%Y %H:%M')})"
            )
        else:
            status = "❌ Não Assistido"
        return status

    # a função agora recebe o perfil para registrar o último conteúdo assistido
    def assistir(self, usuario, perfil):
        usuario.conteudos_vistos += 1
        if usuario.plano.limite_diario < usuario.conteudos_vistos:
            print("Limite diário de visualizações atingido. Assista um anúncio para redefinir esse limite.")
            print("Deseja assistir o anuncio? (s/n)")
            resposta = input().strip().lower()
            if resposta == "s":
                time.sleep(1)
                limpar_tela()
                redefinir_limite_diario(usuario)
                print("Limite redefinido com sucesso!")
                time.sleep(1.5)
                limpar_tela()
            else:
                return 

        while True:
            limpar_tela()
            titulo = self.titulo.strip()
            titulo_centralizado = titulo.center(24)

            # marcação de estado
            self.assistido = True
            self.ultima_exibicao = datetime.datetime.now()
            perfil.ultimo_conteudo_assistido = self.titulo  # registra o último conteúdo assistido no perfil

            # avaliação de banda antes de começar
            usuario.otimizacao_banda_larga.ajustar_qualidade(usuario)
            usuario.otimizacao_banda_larga.exibir_configuracoes_qualidade()
        
            print()

            print("░▀▄░░▄▀")
            print("▄▄▄██▄▄▄▄▄")
            print("█▒░▒░▒░█▀█ Assistindo:")
            print(f"█░▒░▒░▒█▀█ {titulo_centralizado} ")
            print("█▄▄▄▄▄▄███═════════════════════")
            print()
            # A cada alguns segundos, tentar exibir um anuncio
            if usuario.plano.nome != "Premium":
                anuncio = realizar_exibicao_anuncio(usuario)
                if anuncio is True:
                    print("Pressione Enter para continuar.")
                    continue
            else:
                input("Pressione Enter para pausar.")
                limpar_tela()

            print("Conteúdo pausado. O que deseja fazer?")
            escolha = input(
                "1. Continuar assistindo\n"
                "2. Mudar a qualidade de reprodução\n"
                "3. Parar de assistir\n"
                "Escolha uma opção: "
            ).strip()

            if escolha == "1":
                print("Retomando...")
                time.sleep(1)
                continue
            elif escolha == "2":
                usuario.otimizacao_banda_larga.mudar_qualidade(usuario)  
                
            elif escolha == "3":
                print(f"\nVocê parou de assistir {self.titulo}.")
                print("Obrigado por assistir!")
                time.sleep(1.5)
                limpar_tela()
                break
            else:
                print("Opção inválida.")


    def assistir_convidado(self):
        limpar_tela()
        titulo = self.titulo.strip()
        titulo_centralizado = titulo.center(24)
        self.assistido = True
        self.ultima_exibicao = datetime.datetime.now()

        print("░▀▄░░▄▀")
        print("▄▄▄██▄▄▄▄▄")
        print("█▒░▒░▒░█▀█ Assistindo:")
        print(f"█░▒░▒░▒█▀█ {titulo_centralizado} ")
        print("█▄▄▄▄▄▄███═════════════════════")
        print()
        print("Pressione Enter para parar de assistir.")
        input()
        print(f"\nVocê parou de assistir {self.titulo}.")
        print("Obrigado por assistir!")
        time.sleep(1.5)
        limpar_tela()

class Filme(Midia):
    def exibir_informacoes(self):
        print("╔" + "═" * 50 + "╗")
        print(f"║ 🎬  {self.titulo:<42}║") 
        print("╠" + "═" * 50 + "╣")
        print(f"║ Tipo: Filme{'':<42}║")
        print(f"║ Gênero: {self.genero:<40}║")
        print(f"║ Classificação: {self.classificacao:<32}║")
        print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
        print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
        print("╚" + "═" * 50 + "╝")

class Serie(Midia):
    def __init__(self, titulo, genero, classificacao, tempo_duracao, episodios, temporadas):
        super().__init__(titulo, genero, classificacao, tempo_duracao)
        self.episodios = episodios
        self.temporadas = temporadas

    def exibir_informacoes(self):
        print("╔" + "═" * 50 + "╗")
        print(f"║ 📺  {self.titulo:<42}║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Tipo: Série{'':<42}║")
        print(f"║ Gênero: {self.genero:<40}║")
        print(f"║ Classificação: {self.classificacao:<32}║")
        print(f"║ Duração média de episódios: {self.tempo_duracao} min{'':<31}║")
        print(f"║ Episódios: {self.episodios:<40}║")
        print(f"║ Temporadas: {self.temporadas:<38}║")
        print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
        print("╚" + "═" * 50 + "╝")

class Documentario(Midia):
    def exibir_informacoes(self):
        print("╔" + "═" * 50 + "╗")
        print(f"║ 📽️  {self.titulo:<42}║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Tipo: Documentário{'':<42}║")
        print(f"║ Gênero: {self.genero:<40}║")
        print(f"║ Classificação: {self.classificacao:<32}║")
        print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
        print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
        print("╚" + "═" * 50 + "╝")

class Novela(Midia):
    def exibir_informacoes(self):
        print("╔" + "═" * 50 + "╗")
        print(f"║ 🌹  {self.titulo:<42}║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Tipo: Novela{'':<42}║")
        print(f"║ Gênero: {self.genero:<40}║")
        print(f"║ Classificação: {self.classificacao:<32}║")
        print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
        print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
        print("╚" + "═" * 50 + "╝")

class Anime(Midia):
    def __init__(self, titulo, genero, classificacao, tempo_duracao, episodios, temporadas):
        super().__init__(titulo, genero, classificacao, tempo_duracao)
        self.episodios = episodios
        self.temporadas = temporadas
    def exibir_informacoes(self):
        print("╔" + "═" * 50 + "╗")
        print(f"║ 🎌  {self.titulo:<42}║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Tipo: Anime{'':<42}║")
        print(f"║ Gênero: {self.genero:<40}║")
        print(f"║ Classificação: {self.classificacao:<32}║")
        print(f"║ Duração média de episódios: {self.tempo_duracao} min{'':<31}║")
        print(f"║ Episódios: {self.episodios:<40}║")
        print(f"║ Temporadas: {self.temporadas:<38}║")
        print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
        print("╚" + "═" * 50 + "╝")

# essa função foi modificada para ler do json
def todas_as_midias():
    midias = []
    try:
        with open('midias.json', 'r', encoding='utf-8') as f:
            dados_midias = json.load(f)

        for item in dados_midias:
            tipo = item.get("tipo")
            if tipo == "filme":
                midias.append(Filme(item["titulo"], item["genero"], item["classificacao"], item["tempo_duracao"]))
            elif tipo == "serie":
                midias.append(Serie(item["titulo"], item["genero"], item["classificacao"], item["tempo_duracao"], item["episodios"], item["temporadas"]))
            elif tipo == "documentario":
                midias.append(Documentario(item["titulo"], item["genero"], item["classificacao"], item["tempo_duracao"]))
            elif tipo == "novela":
                 midias.append(Novela(item["titulo"], item["genero"], item["classificacao"], item["tempo_duracao"]))
            elif tipo == "anime":
                midias.append(Anime(item["titulo"], item["genero"], item["classificacao"], item["tempo_duracao"], item["episodios"], item["temporadas"]))
        
        return midias

    except FileNotFoundError:
        print("Erro: O arquivo 'midias.json' não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo 'midias.json' possui um formato inválido.")
        return []
    except KeyError as e:
        print(f"Erro: A chave {e} está faltando em um dos itens no arquivo 'midias.json'.")
        return []


def obter_catalogo_do_perfil(perfil) -> ConjuntoMidias:
    if perfil.catalogo is None:
        cat = ConjuntoMidias()
        midias = todas_as_midias()  # cria as instâncias UMA vez para este perfil
        if getattr(perfil, "controle_parental", False):
            midias = [m for m in midias if int(str(m.classificacao).rstrip('+')) <= perfil.idade_limite]
        cat.midias.extend(midias)
        perfil.catalogo = cat
    return perfil.catalogo

# Função principal para assistir o conteúdo
def Explorar_Conteudo(usuario):
    print("Quem está assistindo?")
    continuar = usuario.listar_perfis()
    if not continuar:
        return
    nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
    if not nome_perfil:
        return
        
    perfil = usuario.obter_perfil_por_nome(nome_perfil)  
    if perfil is None:
        print(f"Perfil '{nome_perfil}' não encontrado. Por favor, tente novamente.")
        time.sleep(1.5)
        return
    print(f"Bem-vindo(a), {perfil.nome_perfil}!\n")
    time.sleep(1)

    catalogo = obter_catalogo_do_perfil(perfil)
    
    # Filtro parental
    if perfil.controle_parental:
        catalogo.midias = [m for m in catalogo.midias if int(str(m.classificacao).rstrip('+')) <= perfil.idade_limite]
    
    while True:
        print("Biblioteca de Conteúdo:")
        print("╔" + "═" * 50 + "╗")
        print("1. Buscar por Título")
        print("2. Buscar por Gênero")
        print("3. Navegar pela Biblioteca")
        print("4. Selecionar conteúdo para assistir")
        print("5. Sair")
        print("╚" + "═" * 50 + "╝")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            limpar_tela()
            titulo = input("Digite o título do conteúdo: ")
            resultados = catalogo.buscar_por_titulo(titulo)
            if resultados:
                print("\nResultados da busca por título:\n")
                for midia in resultados:
                    midia.exibir_informacoes()
            else:
                print("Nenhum conteúdo encontrado.")
            input("\nPressione Enter para continuar...")

        elif escolha == "2":
            limpar_tela()
            genero = input("Digite o gênero do conteúdo: ")
            resultados = catalogo.buscar_por_genero(genero)
            if resultados:
                print("\nResultados da busca por gênero:\n")
                for midia in resultados:
                    midia.exibir_informacoes()
            else:
                print("Nenhum conteúdo encontrado.")
            input("\nPressione Enter para continuar...")

        elif escolha == "3":
            limpar_tela()
            catalogo.navegar()
            input("\nPressione Enter para continuar...")
        elif escolha == "4":
            titulo = input("Digite o título do conteúdo que deseja assistir: ")
            resultados = catalogo.buscar_por_titulo(titulo)

            if not resultados:
                print("Conteúdo não encontrado.")
                time.sleep(1.5)
                limpar_tela()
                continue

            print("\nConteúdos encontrados:\n")
            for idx, midia in enumerate(resultados):
                print(f"[{idx + 1}]")
                midia.exibir_informacoes()
                print()

            escolha_conteudo = input("Digite o número do conteúdo que deseja assistir (ou pressione Enter para cancelar): ")
            if not escolha_conteudo:
                continue

            if escolha_conteudo.isdigit():
                indice = int(escolha_conteudo) - 1
                if 0 <= indice < len(resultados):
                    conteudo_escolhido = resultados[indice]
                    usuario.otimizacao_banda_larga.auto_ajuste = True
                    conteudo_escolhido.assistir(usuario, perfil) 
                    perfil.historico.adicionar_no_historico(conteudo_escolhido)
                    perfil.recomendacoes.adicionar_conteudo(conteudo_escolhido.genero)
                else:
                    print("Opção inválida.")
            else:
                print("Entrada inválida.")


        elif escolha == "5":
            print("Saindo da biblioteca...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)
        limpar_tela()

def Explorar_Conteudo_Convidado():
    print("Bem-vindo(a) ao modo convidado!")
    catalogo = ConjuntoMidias()
    
    for midia in todas_as_midias():
        catalogo.midias.append(midia)

    while True:
        print("Biblioteca de Conteúdo:")
        print("╔" + "═" * 50 + "╗")
        print("1. Navegar pela Biblioteca")
        print("2. Selecionar conteúdo para assistir")
        print("3. Sair")
        print("╚" + "═" * 50 + "╝")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            limpar_tela()
            # Limitar a navegação para convidados: mostrar apenas 5 conteúdos aleatórios
            catalogo.navegar(quantidade=5)

        elif escolha == "2":
            titulo = input("Digite o título do conteúdo que deseja assistir: ")
            resultados = catalogo.buscar_por_titulo(titulo)

            # Limitar resultados para convidados: mostrar no máximo 3 opções
            if not resultados:
                print("Conteúdo não encontrado.")
                time.sleep(1.5)
                limpar_tela()
                continue

            resultados_limitados = resultados[:3]

            print("\nConteúdos encontrados (máx. 3):\n")
            for idx, midia in enumerate(resultados_limitados):
                print(f"[{idx + 1}]")
                print()

            escolha_conteudo = input("Digite o número do conteúdo que deseja assistir: ")

            if escolha_conteudo.isdigit():
                indice = int(escolha_conteudo) - 1
                if 0 <= indice < len(resultados_limitados):
                    conteudo_escolhido = resultados_limitados[indice]
                    conteudo_escolhido.assistir_convidado()
                else:
                    print("Opção inválida.")
            else:
                print("Entrada inválida.")

        elif escolha == "3":
            print("Saindo da biblioteca...")
            break

        else:
            print("Opção inválida. Tente novamente.")