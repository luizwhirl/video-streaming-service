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
        NUM_RECOMENDACOES = 5

        if not usuario.plano.recomendacoes_personalizadas:
            print("Recomendações personalizadas estão desativadas para o plano gratuito. Faça um upgrade no seu plano!")
            return
            
        catalogo_completo = obter_catalogo_do_perfil(perfil)
        
        if not self.generos_assistidos:
            print("Explore nosso catálogo para começar a receber recomendações personalizadas!")
            print("Enquanto isso, que tal dar uma olhada nestes títulos?\n")
            
            if catalogo_completo.midias:
                sugestoes_aleatorias = random.sample(catalogo_completo.midias, min(len(catalogo_completo.midias), 3))
                for midia in sugestoes_aleatorias:
                    midia.exibir_informacoes()
                    print()
            return

        # 1. encontramos os 2 gêneros mais assistidos
        contador_generos = Counter(self.generos_assistidos)
        generos_recomendados = contador_generos.most_common(2)

        print("Com base no seu histórico, aqui estão algumas sugestões para você:\n")

        # 2. obtemos o histórico de mídias assistidas do perfil
        titulos_assistidos = {midia.titulo for midia in perfil.historico.historico}

        sugestoes_finais = []
        
        # 3. iteramos sobre os principais gêneros para coletar sugestões
        for genero, _ in generos_recomendados:
            sugestoes_por_genero = [
                midia for midia in catalogo_completo.midias 
                if midia.genero == genero and midia.titulo not in titulos_assistidos
            ]
            random.shuffle(sugestoes_por_genero)
            sugestoes_finais.extend(sugestoes_por_genero)

        # 4. removemos duplicatas (caso um filme se encaixe em mais de um critério futuro) e limitamos o número
        sugestoes_unicas = list(dict.fromkeys(sugestoes_finais))
        
        # 5. exibimos as sugestões
        if not sugestoes_unicas:
            print("Parece que você já assistiu muito do nosso conteúdo recomendado. Impressionante!")
            print("Continue explorando outros gêneros!")
        else:
            for midia_sugerida in sugestoes_unicas[:NUM_RECOMENDACOES]:
                midia_sugerida.exibir_informacoes()
                print()