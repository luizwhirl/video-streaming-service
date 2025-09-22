# predefinitions.py

from user_management import User, Perfil, UserBuilder 
from rating_and_reviews import Avaliacoes

# criando usuários com o userbuilder
usuario1 = UserBuilder().com_nome("João").com_email("joao@example.com").com_senha("senha123").build()
usuario2 = UserBuilder().com_nome("Maria").com_email("maria@example.com").com_senha("senha456").build()
usuario3 = UserBuilder().com_nome("José").com_email("jose@example.com").com_senha("senha789").build()
usuario4 = UserBuilder().com_nome("Teste").com_email("teste@example.com").com_senha("123456").build()
usuario5 = UserBuilder().com_nome("Otávio").com_email("otaviomenezes574@gmail.com").com_senha("senha1234").build()

# adicianado perfis a esses usuários
usuario4.adicionar_perfil("Adulto", controle_parental=False)
usuario4.adicionar_perfil("Criança", controle_parental=True)
usuario5.adicionar_perfil("Otávio", controle_parental=False)

# usando a instancia singleton para as Avaliacoes
# chamando ela aqui, garantimos que só existe uma instância dela
avaliacoes_predefinidas = Avaliacoes() 

# adicionando avaliações a essa instância única
avaliacoes_predefinidas.definir_avaliacao(usuario1.nome, "O Telefone Preto","★★★★★", "Excelente filme!")
avaliacoes_predefinidas.definir_avaliacao(usuario2.nome, "O Poderoso Chefão", "★★★★☆", "Muito bom, mas poderia ser melhor.")
avaliacoes_predefinidas.definir_avaliacao(usuario3.nome, "A Origem", "★★★☆☆", "Ok, nada especial.")
avaliacoes_predefinidas.definir_avaliacao(usuario4.nome, "Titanic", "★★☆☆☆", "Não gostei.")

usuarios_predefinidos = [
    usuario1,
    usuario2,
    usuario3,
    usuario4,
    usuario5
]

def retornar_usuarios_predefinidos():
    return usuarios_predefinidos

def retornar_avaliacoes_predefinidas():
    return avaliacoes_predefinidas