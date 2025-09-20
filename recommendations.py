# recommendations.py

# Personalized Recommendations: Offering personalized content recommendations based on user preferences
from collections import Counter
import random
from library_management import obter_catalogo_do_perfil 

class Recomendacoes:
    def __init__(self):
        self.generos_assistidos = []

    def adicionar_conteudo(self, genero):
        self.generos_assistidos.append(genero)

    def recomendar_conteudo(self, usuario, perfil):
        NUM_RECOMENDACOES = 3

        if not usuario.plano.recomendacoes_personalizadas:
            print("Recomendações personalizadas estão desativadas para o plano gratuito. Faça um upgrade no seu plano!")
            return
            
        if not self.generos_assistidos:
            print("Assista a alguns conteúdos para receber recomendações personalizadas!")
            return

        # 1. encontramos o gênero mais assistido
        contador_generos = Counter(self.generos_assistidos)
        genero_recomendado = contador_generos.most_common(1)[0][0]

        print(f"Com base no seu interesse por '{genero_recomendado}', aqui estão algumas sugestões para você:\n")

        # 2. obtemos o catálogo completo e o histórico de mídias assistidas do perfil
        catalogo_completo = obter_catalogo_do_perfil(perfil)
        # Usamos um conjunto (set) para uma verificação de 'assistido' mais rápida e eficiente
        titulos_assistidos = {midia.titulo for midia in perfil.historico.historico}

        # 3. filtramos o catálogo para encontrar sugestões não assistidas do gênero recomendado
        sugestoes = [
            midia for midia in catalogo_completo.midias 
            if midia.genero == genero_recomendado and midia.titulo not in titulos_assistidos
        ]

        # 4. exbimos as as sugestões
        if not sugestoes:
            print(f"Parece que você já assistiu todo o nosso conteúdo de '{genero_recomendado}'. Impressionante!")
            print("Continue explorando outros gêneros!")
        else:
            random.shuffle(sugestoes) 
            
            for midia_sugerida in sugestoes[:NUM_RECOMENDACOES]:
                midia_sugerida.exibir_informacoes()
                print()