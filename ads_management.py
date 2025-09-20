# ads_management.py

# Ad Integration and Management: Managing ad placements for ad-supported content.
import random
from utility import limpar_tela
import time
import threading
import json # para carregar os anúncios do json 

class Anuncio:
    def __init__(self, nome, produto, descricao):
        self.nome = nome
        self.produto = produto
        self.descricao = descricao

class GerenciarAnuncio:
    def __init__(self): pass

    def exibir_anuncio(self, usuario, banco_ads):
        print("Pressione Enter para pausar.")
        exibido = False
        parar = threading.Event()
        threading.Thread(target=lambda: (input(), parar.set()), daemon=True).start() # Espera pelo Enter
        cont = 0
        passo = 0.5            
        alvo = 30.0          

        while not parar.is_set():
            time.sleep(passo)
            cont += passo

            if cont >= alvo:
                chances = {"Gratuito": 0.65, "Básico": 0.25} 
                mostrar = random.random() < chances.get(usuario.plano.nome, 0.0) # sorteia a chance de 'mostrar' ser true or false

                if mostrar and banco_ads:
                    ad = random.choice(banco_ads)
                    limpar_tela()
                    print("╔" + "═" * 50 + "╗")
                    print(" 📢  ANÚNCIO ESPECIAL")
                    print(f" Nome: {ad.nome:<41}")
                    print(f" Produto: {ad.produto:<38}")
                    print(f" Descrição: {ad.descricao:<35}")
                    print("╚" + "═" * 50 + "╝\n")
                    exibido = True
                    for i in range(3, 0, -1):
                        if parar.is_set(): break    
                        print(f"O anúncio termina em {i}...", end="\r", flush=True)
                        time.sleep(1)
                    print("Anúncio encerrado. Pressione Enter para continuar...")
                cont = 0.0
        return exibido

def criar_banco_de_anuncios():
    try:
        with open('anuncios.json', 'r', encoding='utf-8') as f:
            dados_anuncios = json.load(f)
        
        banco = []
        for ad_data in dados_anuncios:
            banco.append(Anuncio(ad_data['nome'], ad_data['produto'], ad_data['descricao']))
        return banco
    except FileNotFoundError:
        print("Erro: O arquivo 'anuncios.json' não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo 'anuncios.json' possui um formato inválido.")
        return []

def realizar_exibicao_anuncio(usuario):
    banco_ads = criar_banco_de_anuncios()
    anuncio = GerenciarAnuncio()
    return anuncio.exibir_anuncio(usuario, banco_ads)

def redefinir_limite_diario(usuario):
    banco_ads = criar_banco_de_anuncios()
    if not banco_ads:
        print("Não há anúncios disponíveis no momento para redefinir o limite.")
        usuario.conteudos_vistos = usuario.plano.limite_diario # Reseta para o limite sem assistir
        return

    ad = random.choice(banco_ads)
    limpar_tela()
    print("╔" + "═" * 50 + "╗")
    print(" 📢  ANÚNCIO ESPECIAL")
    print(f" Nome: {ad.nome:<41}")
    print(f" Produto: {ad.produto:<38}")
    print(f" Descrição: {ad.descricao:<35}")
    print("╚" + "═" * 50 + "╝\n")
    usuario.conteudos_vistos = 0