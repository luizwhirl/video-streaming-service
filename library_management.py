# library_management.py

# Content Library Management: Managing a library of streaming content, including movies and TV shows
from numpy import append
import random
from utility import limpar_tela, normalizar_texto
import time
from abc import ABC, abstractmethod
import datetime
from ads_management import realizar_exibicao_anuncio, redefinir_limite_diario
from rating_and_reviews import Avaliacoes 
import json 
from player_states import Player # Importa o novo Player
from typing import List, Dict, Any # Adicionado para type hinting

class ConjuntoMidias:
    # referente a varias midias
    def __init__(self):
        self.midias= []
    
    def buscar_por_titulo(self, titulo):
        resultados = []
        # MUDANÇA: Adicionado try...except para normalizar_texto
        try:
            titulo_normalizado = normalizar_texto(titulo)
            for midia in self.midias:
                if titulo_normalizado in normalizar_texto(midia.titulo):
                    resultados.append(midia)
        except Exception as e:
            print(f"Erro ao normalizar ou buscar título: {e}")
        return resultados if resultados else None


    def buscar_por_genero(self, genero):
        resultados = []
        # MUDANÇA: Adicionado try...except para normalizar_texto
        try:
            genero_normalizado = normalizar_texto(genero)
            for midia in self.midias:
                if genero_normalizado in normalizar_texto(midia.genero):
                    resultados.append(midia)
        except Exception as e:
            print(f"Erro ao normalizar ou buscar gênero: {e}")
        return resultados if resultados else None

    def navegar(self, quantidade=5):
        print("\n🎬 Conteúdos sugeridos para você:\n")
        if not self.midias:
            print("Nenhum conteúdo disponível para navegar.")
            return
        # MUDANÇA: Adicionado try...except para random.sample
        try:
            amostra = random.sample(self.midias, min(quantidade, len(self.midias)))
            for midia in amostra:
                midia.exibir_informacoes()
                print()
        except ValueError as e:
            print(f"Erro ao selecionar amostra para navegar: {e}")
        except Exception as e:
            print(f"Erro inesperado ao navegar: {e}")

class Midia(ABC):
    # referente a uma midia especifica
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao):
        self.id_midia = id_midia
        self.titulo = titulo
        self.genero = genero
        self.classificacao = classificacao
        self.tempo_duracao = tempo_duracao
        self.assistido = False
        self.ultima_exibicao = None
        self.recursos = [] # NOVO: Adicionado para o padrão Decorator
        
    @abstractmethod
    def exibir_informacoes(self):
        pass

    def configurar_visualizacao(self):
        # MUDANÇA: Adicionado try...except para formatação de data
        try:
            if self.assistido:
                data_formatada = self.ultima_exibicao.strftime('%d/%m/%Y %H:%M') if self.ultima_exibicao else "Data desconhecida"
                status = (
                    "✔️ Assistido "
                    f"(Última exibição: {data_formatada})"
                )
            else:
                status = "❌ Não Assistido"
        except Exception as e:
            print(f"Erro ao formatar data de visualização: {e}")
            status = "Status indisponível"
        return status


    # MÉTODO REATORADO COM O PADRÃO STATE
    def assistir(self, usuario, perfil):
        # MUDANÇA: Adicionado try...except em todo o método para falhas críticas
        try:
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

            # Atualiza o status da mídia
            self.assistido = True
            self.ultima_exibicao = datetime.datetime.now()
            perfil.ultimo_conteudo_assistido = self.titulo

            # Cria e executa o Player, que agora gerencia seus próprios estados
            player = Player(self, usuario, perfil)
            player.executar()
            
        except AttributeError as e:
            print(f"Erro ao acessar dados do usuário ou perfil durante a visualização: {e}")
        except Exception as e:
            print(f"Erro inesperado ao tentar assistir: {e}")


    def assistir_convidado(self):
        # MUDANÇA: Adicionado try...except em todo o método
        try:
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
        except Exception as e:
            print(f"Erro inesperado no modo convidado: {e}")
            time.sleep(1.5)
            limpar_tela()

class Filme(Midia):
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao):
        super().__init__(id_midia, titulo, genero, classificacao, tempo_duracao)

    def exibir_informacoes(self):
        # MUDANÇA: Adicionado try...except para proteger a formatação (f-string)
        try:
            print("╔" + "═" * 50 + "╗")
            print(f"║ 🎬  {self.titulo:<42}║") 
            print("╠" + "═" * 50 + "╣")
            print(f"║ ID: {self.id_midia:<44}║") 
            print(f"║ Tipo: Filme{'':<42}║")
            print(f"║ Gênero: {self.genero:<40}║")
            print(f"║ Classificação: {self.classificacao:<32}║")
            print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
            print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
            # NOVO: Bloco do Decorator
            if self.recursos:
                print("╠" + "┈" * 50 + "╣")
                for recurso in self.recursos:
                    print(f"║ ℹ️  Recurso: {recurso:<35}║")
            print("╚" + "═" * 50 + "╝")
        except Exception as e:
            print(f"Erro ao exibir informações do filme {self.titulo}: {e}")

class Serie(Midia):
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao, episodios, temporadas):
        super().__init__(id_midia, titulo, genero, classificacao, tempo_duracao)
        self.episodios = episodios
        self.temporadas = temporadas

    def exibir_informacoes(self):
        # MUDANÇA: Adicionado try...except para proteger a formatação (f-string)
        try:
            print("╔" + "═" * 50 + "╗")
            print(f"║ 📺  {self.titulo:<42}║")
            print("╠" + "═" * 50 + "╣")
            print(f"║ ID: {self.id_midia:<44}║") 
            print(f"║ Tipo: Série{'':<42}║")
            print(f"║ Gênero: {self.genero:<40}║")
            print(f"║ Classificação: {self.classificacao:<32}║")
            print(f"║ Duração média de episódios: {self.tempo_duracao} min{'':<31}║")
            print(f"║ Episódios: {self.episodios:<40}║")
            print(f"║ Temporadas: {self.temporadas:<38}║")
            print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
            # NOVO: Bloco do Decorator
            if self.recursos:
                print("╠" + "┈" * 50 + "╣")
                for recurso in self.recursos:
                    print(f"║ ℹ️  Recurso: {recurso:<35}║")
            print("╚" + "═" * 50 + "╝")
        except Exception as e:
            print(f"Erro ao exibir informações da série {self.titulo}: {e}")

class Documentario(Midia):
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao):
        super().__init__(id_midia, titulo, genero, classificacao, tempo_duracao)

    def exibir_informacoes(self):
        # MUDANÇA: Adicionado try...except para proteger a formatação (f-string)
        try:
            print("╔" + "═" * 50 + "╗")
            print(f"║ 📽️  {self.titulo:<42}║")
            print("╠" + "═" * 50 + "╣")
            print(f"║ ID: {self.id_midia:<44}║") 
            print(f"║ Tipo: Documentário{'':<42}║")
            print(f"║ Gênero: {self.genero:<40}║")
            print(f"║ Classificação: {self.classificacao:<32}║")
            print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
            print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
            # NOVO: Bloco do Decorator
            if self.recursos:
                print("╠" + "┈" * 50 + "╣")
                for recurso in self.recursos:
                    print(f"║ ℹ️  Recurso: {recurso:<35}║")
            print("╚" + "═" * 50 + "╝")
        except Exception as e:
            print(f"Erro ao exibir informações do documentário {self.titulo}: {e}")

class Novela(Midia):
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao):
        super().__init__(id_midia, titulo, genero, classificacao, tempo_duracao)

    def exibir_informacoes(self):
        # MUDANÇA: Adicionado try...except para proteger a formatação (f-string)
        try:
            print("╔" + "═" * 50 + "╗")
            print(f"║ 🌹  {self.titulo:<42}║")
            print("╠" + "═" * 50 + "╣")
            print(f"║ ID: {self.id_midia:<44}║")
            print(f"║ Tipo: Novela{'':<42}║")
            print(f"║ Gênero: {self.genero:<40}║")
            print(f"║ Classificação: {self.classificacao:<32}║")
            print(f"║ Duração: {self.tempo_duracao} min{'':<31}║")
            print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
            # NOVO: Bloco do Decorator
            if self.recursos:
                print("╠" + "┈" * 50 + "╣")
                for recurso in self.recursos:
                    print(f"║ ℹ️  Recurso: {recurso:<35}║")
            print("╚" + "═" * 50 + "╝")
        except Exception as e:
            print(f"Erro ao exibir informações da novela {self.titulo}: {e}")

class Anime(Midia):
    def __init__(self, id_midia, titulo, genero, classificacao, tempo_duracao, episodios, temporadas):
        super().__init__(id_midia, titulo, genero, classificacao, tempo_duracao)
        self.episodios = episodios
        self.temporadas = temporadas

    def exibir_informacoes(self):
        # MUDANÇA: Adicionado try...except para proteger a formatação (f-string)
        try:
            print("╔" + "═" * 50 + "╗")
            print(f"║ 🎌  {self.titulo:<42}║")
            print("╠" + "═" * 50 + "╣")
            print(f"║ ID: {self.id_midia:<44}║") 
            print(f"║ Tipo: Anime{'':<42}║")
            print(f"║ Gênero: {self.genero:<40}║")
            print(f"║ Classificação: {self.classificacao:<32}║")
            print(f"║ Duração média de episódios: {self.tempo_duracao} min{'':<31}║")
            print(f"║ Episódios: {self.episodios:<40}║")
            print(f"║ Temporadas: {self.temporadas:<38}║")
            print(f"║ Status: {self.configurar_visualizacao()} {'':<31}║")
            # NOVO: Bloco do Decorator
            if self.recursos:
                print("╠" + "┈" * 50 + "╣")
                for recurso in self.recursos:
                    print(f"║ ℹ️  Recurso: {recurso:<35}║")
            print("╚" + "═" * 50 + "╝")
        except Exception as e:
            print(f"Erro ao exibir informações do anime {self.titulo}: {e}")

# ==================================================================
# NOVO: PADRÃO DECORATOR
# ==================================================================

class MidiaDecorator(Midia, ABC):
    """
    A classe Decorator base segue a mesma interface que os outros
    componentes. O propósito principal desta classe é definir a
    interface de "embrulho" (wrapping) para todos os decoradores concretos.
    A implementação padrão da lógica de "embrulho" pode incluir um
    campo para armazenar um componente "embrulhado" e os meios
    para inicializá-lo.
    """

    def __init__(self, midia_componente: Midia):
        # O decorator "finge" ser uma Mídia, mas na verdade
        # ele apenas envolve o componente.
        self._componente = midia_componente
        # Copia os recursos do componente para que possam ser adicionados
        # MUDANÇA: Adicionado try...except para o caso de _componente não ter 'recursos'
        try:
            self.recursos = self._componente.recursos
        except AttributeError:
            self.recursos = [] # Fallback

    def __getattr__(self, name):
        """
        Delega todos os atributos e métodos não substituídos
        para o objeto componente "embrulhado".
        """
        # MUDANÇA: Adicionado try...except para delegação de atributo
        try:
            return getattr(self._componente, name)
        except AttributeError:
            raise AttributeError(f"'{type(self._componente).__name__}' e '{type(self).__name__}' não possuem o atributo '{name}'")


    @abstractmethod
    def exibir_informacoes(self):
        """
        O Decorator deve implementar a interface Midia.
        A forma mais simples é delegar ao componente.
        (Os decoradores concretos modificarão esse comportamento)
        """
        self._componente.exibir_informacoes()


class AudioDescricaoDecorator(MidiaDecorator):
    """
    Decorator Concreto que adiciona Audiodescrição.
    """
    def __init__(self, midia_componente: Midia):
        super().__init__(midia_componente)
        # A "decoração" acontece aqui:
        if "Audiodescrição" not in self.recursos:
            self.recursos.append("Audiodescrição")

    def exibir_informacoes(self):
        # Como as classes de Mídia (Filme, Serie) já foram
        # modificadas para ler 'self.recursos', este método
        # só precisa delegar a chamada. O componente fará o resto.
        self._componente.exibir_informacoes()


class DublagemDecorator(MidiaDecorator):
    """
    Decorator Concreto que adiciona Dublagem.
    """
    def __init__(self, midia_componente: Midia):
        super().__init__(midia_componente)
        # A "decoração" acontece aqui:
        if "Dublagem (PT-BR)" not in self.recursos:
            self.recursos.append("Dublagem (PT-BR)")

    def exibir_informacoes(self):
        # Delega a chamada.
        self._componente.exibir_informacoes()

# ==================================================================
# FIM DO PADRÃO DECORATOR
# ==================================================================


# FACTORY 
# essa classe centraliza a lógica de criação de objetos de mídia
# o que remove a necessidade de condicionais if/elif no código cliente
# e facilita a adição de novos tipos de mídia no futuro
class MidiaFactory:
    @staticmethod
    def criar_midia(item_data):
        # MUDANÇA: Adicionado try...except para KeyError se faltarem dados no JSON
        try:
            tipo = item_data.get("tipo")
            if tipo == "filme":
                return Filme(item_data["id"], item_data["titulo"], item_data["genero"], item_data["classificacao"], item_data["tempo_duracao"])
            elif tipo == "serie":
                return Serie(item_data["id"], item_data["titulo"], item_data["genero"], item_data["classificacao"], item_data["tempo_duracao"], item_data["episodios"], item_data["temporadas"])
            elif tipo == "documentario":
                return Documentario(item_data["id"], item_data["titulo"], item_data["genero"], item_data["classificacao"], item_data["tempo_duracao"])
            elif tipo == "novela":
                return Novela(item_data["id"], item_data["titulo"], item_data["genero"], item_data["classificacao"], item_data["tempo_duracao"])
            elif tipo == "anime":
                return Anime(item_data["id"], item_data["titulo"], item_data["genero"], item_data["classificacao"], item_data["tempo_duracao"], item_data["episodios"], item_data["temporadas"])
            else:
                # lança um erro se o tipo for desconhecido, para evitar falhas silenciosas
                raise ValueError(f"Tipo de mídia desconhecido: {tipo}")
        except KeyError as e:
            raise ValueError(f"Dados incompletos para a mídia '{item_data.get('titulo', 'N/A')}'. Falta a chave: {e}")


# ==================================================================
# NOVO: PADRÃO ADAPTER
# ==================================================================

def _carregar_dados_externos_simulados() -> List[Dict[str, Any]]:
    """
    Simula a obtenção de dados de uma API externa (ex: XML, ou JSON com
    uma estrutura diferente). Note que as chaves estão em inglês
    e são diferentes das esperadas pelo nosso sistema.
    """
    print("Carregando dados de uma fonte externa simulada...")
    return [
        {
            "ID": "e101",
            "Title": "The Art of Programming",
            "Type": "documentario",
            "Genre": "Tecnologia",
            "Rating": "L", # 'L' para "Livre"
            "Runtime": 88
        },
        {
            "ID": "e202",
            "Title": "Cyber Detectives",
            "Type": "serie",
            "Genre": "Ficção Científica",
            "Rating": "14+",
            "Runtime": 45, # Duração por episódio
            "Eps": 10,
            "Seasons": 1
        }
    ]

class ExternalMediaAdapter:
    """
    A classe Adapter "traduz" a interface de um objeto (dados externos)
    para a interface que o cliente (MidiaFactory) espera.
    """
    def __init__(self, external_data: Dict[str, Any]):
        self._external_data = external_data

    def get_dados_adaptados(self) -> Dict[str, Any]:
        """
        Realiza a "tradução" (mapeamento) dos dados externos para
        o formato interno esperado pela MidiaFactory.
        """
        # MUDANÇA: Adicionado try...except para o caso de dados externos inesperados
        try:
            dados_adaptados = {
                "id": self._external_data.get("ID"),
                "titulo": self._external_data.get("Title"),
                "tipo": self._external_data.get("Type"),
                "genero": self._external_data.get("Genre"),
                "classificacao": self._external_data.get("Rating", "L"),
                "tempo_duracao": self._external_data.get("Runtime"),
                "episodios": self._external_data.get("Eps", 0),
                "temporadas": self._external_data.get("Seasons", 0)
            }
            return dados_adaptados
        except Exception as e:
            print(f"Erro ao adaptar dados externos: {e}")
            return {} # Retorna dicionário vazio para falhar graciosamente

# ==================================================================
# FIM DO PADRÃO ADAPTER
# ==================================================================


def todas_as_midias():
    midias = []
    
    # --- FONTE DE DADOS 1: JSON (Sistema Interno) ---
    try:
        with open('midias.json', 'r', encoding='utf-8') as f:
            dados_midias = json.load(f)

        print("Carregando mídias do 'midias.json'...")
        for item in dados_midias:
            try:
                # 1. Cria a mídia usando a Factory
                midia_obj = MidiaFactory.criar_midia(item)
                
                # 2. NOVO: Aplica o padrão Decorator (Exemplo)
                if item["id"] == "f001": # Ex: O Poderoso Chefão
                    midia_obj = AudioDescricaoDecorator(midia_obj)
                
                if item["id"] == "s001": # Ex: Stranger Things
                    midia_obj = DublagemDecorator(midia_obj)
                    midia_obj = AudioDescricaoDecorator(midia_obj) # Pode empilhar decoradores

                midias.append(midia_obj)
            
            except (ValueError, KeyError) as e:
                print(f"Erro ao processar item de mídia: {item.get('titulo', 'sem título')}. Detalhes: {e}")
    
    except FileNotFoundError:
        print("Erro: O arquivo 'midias.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("Erro: O arquivo 'midias.json' possui um formato inválido.")
    # MUDANÇA: Adicionada captura genérica para erros de I/O ou permissão
    except IOError as e:
        print(f"Erro de I/O ao ler 'midias.json': {e}")
    except Exception as e:
        print(f"Erro inesperado ao carregar mídias internas: {e}")

    
    # --- FONTE DE DADOS 2: API Externa (Padrão Adapter) ---
    # MUDANÇA: Adicionado try...except para o carregamento e processamento de dados externos
    try:
        dados_externos = _carregar_dados_externos_simulados()
        for item_externo in dados_externos:
            try:
                # 1. Adapta a interface externa para a nossa interface
                adapter = ExternalMediaAdapter(item_externo)
                dados_adaptados = adapter.get_dados_adaptados()
                
                if not dados_adaptados: # Verifica se a adaptação falhou
                    continue
                    
                # 2. Usa a MESMA Factory com os dados adaptados
                midia_obj_externa = MidiaFactory.criar_midia(dados_adaptados)
                
                # 3. (Opcional) Podemos decorar mídias externas também
                if midia_obj_externa.id_midia == "e101":
                    midia_obj_externa = DublagemDecorator(midia_obj_externa)

                midias.append(midia_obj_externa)
            
            except (ValueError, KeyError) as e:
                print(f"Erro ao processar item de mídia externa: {item_externo.get('Title', 'sem título')}. Detalhes: {e}")
    except Exception as e:
        print(f"Falha crítica ao carregar dados externos simulados: {e}")


    print("\nCatálogo completo carregado.")
    time.sleep(0.5) # Pausa rápida para ver as mensagens de carregamento
    return midias


def obter_catalogo_do_perfil(perfil) -> ConjuntoMidias:
    if perfil.catalogo is None:
        cat = ConjuntoMidias()
        midias = todas_as_midias()  # cria as instâncias UMA vez para este perfil
        if getattr(perfil, "controle_parental", False):
            # MUDANÇA: Adicionado try...except para a lógica de filtragem parental
            midias_filtradas = []
            for m in midias:
                try:
                    # Tenta converter classificacao para int (removendo '+')
                    classificacao_int = int(str(m.classificacao).rstrip('+'))
                    if classificacao_int <= perfil.idade_limite:
                        midias_filtradas.append(m)
                except (ValueError, TypeError):
                    # Se for 'L' (Livre) ou '10' (que já é string), trata
                    if str(m.classificacao).upper() == 'L':
                        midias_filtradas.append(m) # Livre é sempre permitido
                    elif str(m.classificacao).isdigit(): # Caso '10', '12'
                         if int(m.classificacao) <= perfil.idade_limite:
                             midias_filtradas.append(m)
                    else:
                        print(f"Aviso: Classificação inválida ('{m.classificacao}') para '{m.titulo}'. Tratando como restrito.")
            
            midias = midias_filtradas
            
        cat.midias.extend(midias)
        perfil.catalogo = cat
    return perfil.catalogo


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
            
            # MUDANÇA: Adicionado try...except para converter a escolha em inteiro
            try:
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
                    print("Entrada inválida. Digite um número.")
            except ValueError:
                print("Entrada numérica inválida.")
            except Exception as e:
                print(f"Erro ao tentar assistir conteúdo: {e}")


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
            catalogo.navegar(quantidade=5)

        elif escolha == "2":
            titulo = input("Digite o título do conteúdo que deseja assistir: ")
            resultados = catalogo.buscar_por_titulo(titulo)
            
            if not resultados:
                print("Conteúdo não encontrado.")
                time.sleep(1.5)
                limpar_tela()
                continue

            resultados_limitados = resultados[:3]

            print("\nConteúdos encontrados (máx. 3):\n")
            for idx, midia in enumerate(resultados_limitados):
                print(f"[{idx + 1}]")
                midia.exibir_informacoes()
                print()

            escolha_conteudo = input("Digite o número do conteúdo que deseja assistir: ")

            # MUDANÇA: Adicionado try...except para converter a escolha em inteiro
            try:
                if escolha_conteudo.isdigit():
                    indice = int(escolha_conteudo) - 1
                    if 0 <= indice < len(resultados_limitados):
                        conteudo_escolhido = resultados_limitados[indice]
                        conteudo_escolhido.assistir_convidado()
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")
            except ValueError:
                print("Entrada numérica inválida.")
            except Exception as e:
                print(f"Erro ao tentar assistir conteúdo como convidado: {e}")

        elif escolha == "3":
            print("Saindo da biblioteca...")
            break

        else:
            print("Opção inválida. Tente novamente.")
