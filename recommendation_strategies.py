# recommendation_strategies.py

from abc import ABC, abstractmethod
import random
from collections import Counter

class RecommendationStrategy(ABC):
    """
    a interface da Estratégia declara operações comuns a todas as versões
    suportadas de algum algoritmo. O Contexto usa esta interface para chamar
    o algoritmo definido pelas Estratégias Concretas
    """
    @abstractmethod
    def recommend(self, perfil, catalogo_completo, num_recomendacoes=5):
        pass

class GenreBasedStrategy(RecommendationStrategy):
    """
    implementa a recomendação baseada nos gêneros mais assistidos pelo usuário
    """
    def recommend(self, perfil, catalogo_completo, num_recomendacoes=5):
        print("Recomendações com base nos seus gêneros favoritos:\n")
        
        if not perfil.historico.historico:
            print("Você ainda não assistiu a nada. Que tal começar por estes?\n")
            sugestoes_aleatorias = random.sample(catalogo_completo.midias, min(len(catalogo_completo.midias), 3))
            for midia in sugestoes_aleatorias:
                midia.exibir_informacoes()
                print()
            return

        generos_assistidos = [midia.genero for midia in perfil.historico.historico]
        contador_generos = Counter(generos_assistidos)
        generos_recomendados = contador_generos.most_common(2)
        titulos_assistidos = {midia.titulo for midia in perfil.historico.historico}
        sugestoes_finais = []

        for genero, _ in generos_recomendados:
            sugestoes_por_genero = [
                midia for midia in catalogo_completo.midias
                if midia.genero == genero and midia.titulo not in titulos_assistidos
            ]
            random.shuffle(sugestoes_por_genero)
            sugestoes_finais.extend(sugestoes_por_genero)

        sugestoes_unicas = list(dict.fromkeys(sugestoes_finais))

        if not sugestoes_unicas:
            print("Parece que você já assistiu muito do nosso conteúdo recomendado. Impressionante!")
        else:
            for midia_sugerida in sugestoes_unicas[:num_recomendacoes]:
                midia_sugerida.exibir_informacoes()
                print()

class TrendingStrategy(RecommendationStrategy):
    """
    implementa a recomendação baseada em conteúdos populares (simulado).
    """
    def recommend(self, perfil, catalogo_completo, num_recomendacoes=5):
        print("Recomendações com base no que está em alta:\n")
        
        if not catalogo_completo.midias:
            print("O catálogo está vazio no momento.")
            return
            
        titulos_assistidos = {midia.titulo for midia in perfil.historico.historico}
        
        sugestoes_trending = [
            midia for midia in catalogo_completo.midias 
            if midia.titulo not in titulos_assistidos
        ]
        
        if not sugestoes_trending:
            print("Você já assistiu tudo o que está em alta! :)")
            return

        random.shuffle(sugestoes_trending)
        for midia_sugerida in sugestoes_trending[:num_recomendacoes]:
            midia_sugerida.exibir_informacoes()
            print()

class SurpriseMeStrategy(RecommendationStrategy):
    """
    implementa uma recomendação aleatória para descobrir novos conteúdos.
    """
    def recommend(self, perfil, catalogo_completo, num_recomendacoes=5):
        print("Surpreenda-se! Aqui estão algumas sugestões aleatórias para você:\n")

        # if not catalogo_completo.midias:
        #     print("O catálogo está vazio no momento.")
        #     return

        titulos_assistidos = {midia.titulo for midia in perfil.historico.historico}
        
        sugestoes_aleatorias = [
            midia for midia in catalogo_completo.midias 
            if midia.titulo not in titulos_assistidos
        ]

        if not sugestoes_aleatorias:
            print("Você já assistiu a todo o nosso catálogo! Parabéns!")
            return
            
        random.shuffle(sugestoes_aleatorias)
        for midia_sugerida in sugestoes_aleatorias[:num_recomendacoes]:
            midia_sugerida.exibir_informacoes()
            print()