# recommendations.py

# Personalized Recommendations: Offering personalized content recommendations based on user preferences
from collections import Counter
import random
from recommendation_strategies import GenreBasedStrategy # Importa a estratégia padrão

class Recomendacoes:
    def __init__(self, strategy=None):
        self.generos_assistidos = []
        # Define uma estratégia padrão se nenhuma for fornecida
        self._strategy = strategy or GenreBasedStrategy()

    def set_strategy(self, strategy):
        """Permite mudar a estratégia em tempo de execução."""
        self._strategy = strategy
        print(f"\nEstratégia de recomendação alterada para: {strategy.__class__.__name__}")

    def adicionar_conteudo(self, genero):
        self.generos_assistidos.append(genero)

    def recomendar_conteudo(self, usuario, perfil):
        from library_management import obter_catalogo_do_perfil
        
        if not usuario.plano.recomendacoes_personalizadas:
            print("Recomendações personalizadas estão desativadas para o plano gratuito. Faça um upgrade no seu plano!")
            return
            
        catalogo_completo = obter_catalogo_do_perfil(perfil)
        
        # Delega a tarefa de recomendação para o objeto de estratégia atual
        self._strategy.recommend(perfil, catalogo_completo)