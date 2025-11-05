# utility.py

import os
import sys
import unicodedata
import re

def limpar_tela():
    # Limpa a tela do terminal
    # MUDANÇA: Adicionado try...except para o caso de 'os.system' falhar (ex: permissões)
    try:
        if sys.platform.startswith('win'):
            os.system('cls')
        else:
            os.system('clear')
    except OSError as e:
        print(f"Erro ao limpar a tela: {e}. Continuando...")
        # Imprime várias linhas em branco como alternativa
        print("\n" * 50)


def normalizar_texto(texto):
    # MUDANÇA: Adicionado try...except para o caso de 'texto' não ser uma string
    try:
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFKD", texto)
        texto = ''.join([c for c in texto if not unicodedata.combining(c)])
        texto = re.sub(r'\W+', '', texto)  # remove qualquer coisa que não seja letra ou número
        return texto
    except (TypeError, AttributeError):
        print(f"Erro: Tentativa de normalizar um tipo não-string ({type(texto)}).")
        return "" # Retorna string vazia como fallback
    except Exception as e:
        print(f"Erro inesperado ao normalizar texto: {e}")
        return ""