# main.py

import time
from user_management import User, UserBuilder 
from parental_control import select_profile_for_parental_control, select_profile_for_not_parental_control, restringir_conteudo
from utility import limpar_tela
from library_management import Explorar_Conteudo, Explorar_Conteudo_Convidado
from bookmarking_and_history import ver_historico_de_exibicao, limpar_historico, bookmarking
from rating_and_reviews import Avaliacoes, processo_para_avaliar
from predefinitions import retornar_usuarios_predefinidos, retornar_avaliacoes_predefinidas
from recommendation_strategies import GenreBasedStrategy, TrendingStrategy, SurpriseMeStrategy


# Video Streaming Service - Main Module

# MUDANÇA: Adicionado try...except ao carregar dados predefinidos
try:
    usuarios_registrados = retornar_usuarios_predefinidos()
    reviews = retornar_avaliacoes_predefinidas()
except Exception as e:
    print(f"Erro crítico ao inicializar dados predefinidos: {e}")
    print("Saindo do programa.")
    exit()


def inicializar():
    limpar_tela()
    print("╔" + "═" * 20 + "╗")
    print("║   VSTREAMING HUB   ║")
    print("╚" + "═" * 20 + "╝")

def criar_conta():
    
    while True:
        limpar_tela()
        try:
            print("Digite o nome do usuário:")
            nome = input().strip()
            
            # MUDANÇA: Adicionado 'continue' no loop 'for' para eficiência
            usuario_existe = False
            for usuario in usuarios_registrados:
                if usuario.nome == nome:
                    print("Usuário já existe. Tente novamente.")
                    time.sleep(1.5)
                    usuario_existe = True
                    break
            if usuario_existe:
                continue
            
            print("Digite seu email:")
            email = input().strip()
            
            email_existe = False
            for usuario in usuarios_registrados:
                if usuario.email == email:
                    print("Esse email já foi registrado. Tente novamente.")
                    time.sleep(1.5)
                    email_existe = True
                    break
            if email_existe:
                continue
                    
            print("Digite sua senha:")
            senha = input()
            print("Confirme sua senha:")
            senha2 = input()

            if senha != senha2:
                print("As senhas não coincidem. Tente novamente.")
                time.sleep(1.5)
                continue

            # usando agora o novo padrão builder
            builder = UserBuilder()
            novo_usuario = builder.com_nome(nome).com_email(email).com_senha(senha).build()
            
            usuarios_registrados.append(novo_usuario)
            print("Sua conta foi criada com sucesso!")
            time.sleep(1.5)
            break
            
        except ValueError as e:
            print(f"Erro: {e}")
            print("Tente novamente.")
            time.sleep(1.5)
            continue
        except Exception as e:
            print(f"Erro inesperado: {e}")
            print("Tente novamente.")
            time.sleep(1.5)
            continue

def fazer_login(usuarios_registrados):
    # MUDANÇA: Adicionado try...except para o caso de 'usuarios_registrados' estar vazio ou corrompido
    try:
        nome = input("Digite seu nome de usuário: ")
        senha = input("Digite sua senha: ")

        for usuario in usuarios_registrados:
            if usuario.login(nome, senha):
                print(f"Login bem-sucedido! Bem-vindo, {usuario.nome}.")
                time.sleep(1)
                return usuario

        print("Usuário ou senha incorretos.")
        print("1. Tentar novamente")
        print("2. Voltar ao menu inicial")
        opcao = input("Escolha uma opção (1-2):\n ")
        if opcao == "1":
            limpar_tela()
            return fazer_login(usuarios_registrados)
        elif opcao == "2":
            limpar_tela()
            return None 
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)
            limpar_tela()
            return fazer_login(usuarios_registrados)
            
    except Exception as e:
        print(f"Erro durante o processo de login: {e}")
        time.sleep(2)
        return None

def menu_inicial():
    while True: 
        # MUDANÇA: Adicionado try...except para capturar interrupções (Ctrl+C)
        try:
            limpar_tela()
            print("╔══════════════════════════════╗")
            print("║ Bem-vindo ao VStreamingHub!  ║")
            print("╚══════════════════════════════╝\n")

            print("Deseja criar uma conta ou fazer login?\n")

            print("╔══════════════════════════════╗")
            print("║ 1. Criar conta               ║")
            print("║ 2. Fazer login               ║")
            print("║ 3. Continuar como convidado  ║")
            print("║ 4. Sair                      ║")
            print("╚══════════════════════════════╝")

            opcao = input("Escolha uma opção (1-4):\n ")
            if opcao == "1":
                limpar_tela()
                criar_conta()
            
            elif opcao == "2":
                limpar_tela()
                usuario_logado = fazer_login(usuarios_registrados)
                if usuario_logado:
                    menu_principal(usuario_logado)
            elif opcao == "3":
                limpar_tela()
                menu_principal_convidado()
            elif opcao == "4":
                print("Saindo do Video Streaming Service. Até logo!\n")
                exit()
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nSaindo do programa. Até logo!")
            exit()
        except Exception as e:
            print(f"Erro inesperado no menu inicial: {e}")
            time.sleep(2)


def menu_config_usuario(usuario):
    while True:
        # MUDANÇA: Adicionado try...except para proteger o menu
        try:
            limpar_tela()
            print("Configurações de usuário:\n")
            print("╔" + "═" * 50 + "╗")
            print("1. Gerenciar meus perfis\n")
            print("2. Gerenciar meu plano de assinatura\n")
            print("3. Configurações de controle parental\n")
            print("4. Voltar ao menu principal")
            print("╚" + "═" * 50 + "╝")

            opcao_usuario = input("Escolha uma opção (1-4):\n ")
            
            if opcao_usuario == "1":    
                limpar_tela()
                if usuario.listar_perfis():
                    print("\nDeseja adicionar ou remover um perfil?")
                    print("╔" + "═" * 50 + "╗")
                    print("1. Adicionar perfil")
                    print("2. Remover perfil")
                    print("3. Voltar ao menu de configurações")
                    print("╚" + "═" * 50 + "╝")
                    escolha_perfil = input("Escolha uma opção (1-3):\n ")

                    if escolha_perfil == "1":
                        limpar_tela()
                        nome_perfil = input("Digite o nome do novo perfil (ou pressione Enter para cancelar): ")
                        if nome_perfil:
                            usuario.adicionar_perfil(nome_perfil)
                        time.sleep(1.5)
                    elif escolha_perfil == "2":
                        limpar_tela()
                        print("Perfis disponíveis para remoção:")
                        usuario.listar_perfis()
                        nome_perfil = input("Digite o nome do perfil a ser removido (ou pressione Enter para cancelar): ")
                        if nome_perfil:
                            usuario.remover_perfil(nome_perfil)
                        time.sleep(1.5)
                    elif escolha_perfil == "3":
                        continue
                    else:
                        print("Opção inválida. Tente novamente.")
                else: 
                    limpar_tela()
                    # MUDANÇA: Corrigido o loop infinito, removendo a chamada recursiva
                    continue # Volta ao início do loop 'while True'
            elif opcao_usuario == "2":
                limpar_tela()
                usuario.gerenciar_plano()
            elif opcao_usuario == "3":
                limpar_tela()
                while True:
                    print("Configurações de Controle Parental:\n")
                    print("╔" + "═" * 150 + "╗")
                    print("Você pode ativar o controle parental para um perfil existente ou restringir conteúdo.\n")
                    print("Observação: Ao desativar ou mudar o tipo de restrição, as mídias já assistidas no perfil serão redefinidas para não assistidas.")
                    print("1. Ativar controle parental")
                    print("2. Desativar controle parental")
                    print("3. Restrição de conteúdo")
                    print("4. Voltar ao menu de configurações")
                    print("╚" + "═" * 150 + "╝")
                    escolha = input("Escolha uma opção (1-4):\n ")

                    if escolha == "1":
                        while True:
                            limpar_tela()
                            outro_perfil = select_profile_for_parental_control(usuario)
                            time.sleep(1.5)
                            if outro_perfil:
                                print("Deseja ativar o controle parental para outro perfil?" \
                                    "\n1. Sim\n2. Não")
                                escolha_controle = input("Escolha uma opção (1-2):\n ")

                                if escolha_controle == "1":
                                    continue  
                                elif escolha_controle == "2":
                                    break  
                                else:
                                    print("Opção inválida. Tente novamente.")
                                    time.sleep(1)
                            else:
                                break
                    elif escolha == "2":
                        limpar_tela()
                        select_profile_for_not_parental_control(usuario)
                        time.sleep(1.5)
                    elif escolha == "3":
                        limpar_tela()
                        restringir_conteudo(usuario)
                        time.sleep(1.5)
                    elif escolha == "4":
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                        time.sleep(1)
            
            elif opcao_usuario == "4":
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(1)
                
        except Exception as e:
            print(f"Erro inesperado nas configurações do usuário: {e}")
            time.sleep(2)


def menu_principal_convidado():
    while True:
        # MUDANÇA: Adicionado try...except para proteger o menu
        try:
            limpar_tela()
            print("Bem-vindo, convidado!\n"
                "Você pode explorar o conteúdo, porém o resto das funcionalidades estão limitadas. Crie uma conta para ter acesso completo aos nossos serviços.\n"
                "O que você gostaria de fazer?\n"
                )
            print("╔" + "═" * 50 + "╗")
            print("1. Consultar biblioteca de conteúdo\n")
            print("2. Voltar ao menu inicial")
            print("╚" + "═" * 50 + "╝")

            opcao = input("Escolha uma opção (1-2):\n ")
            if opcao == "1":
                limpar_tela()
                print("Consultando biblioteca de conteúdo...\n")
                time.sleep(1)
                limpar_tela()
                Explorar_Conteudo_Convidado()
                print("Você pode criar uma conta para acessar mais funcionalidades.\n")
                time.sleep(1.5)
            elif opcao == "2":
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(1)
        except Exception as e:
            print(f"Erro inesperado no menu de convidado: {e}")
            time.sleep(2)


def menu_principal(usuario):
    while True:
        # MUDANÇA: Adicionado try...except para proteger o menu principal
        try:
            limpar_tela()
            print(f"Bem-vindo ao Video Streaming Service, {usuario.nome}!\n"
                "O que você gostaria de fazer?\n"
                )
            print("╔" + "═" * 50 + "╗")
            print("  1. 🎬 Consultar biblioteca de conteúdo")
            print("  2. ⚙️ Configurações de usuário")
            print("  3. ⭐ Recomendações personalizadas")
            print("  4. 📺 Streaming em múltiplos dispositivos")
            print("  5. 📚 Marcar conteúdo e histórico de visualização")
            print("  6. 📝 Revisões e avaliações de conteúdo")
            print("  7. 🚪 Logout")
            print("╚" + "═" * 50 + "╝")

            opcao = input("Escolha uma opção (1-7):\n ")

            if opcao == "1":
                limpar_tela()
                print("Consultando biblioteca de conteúdo...\n")
                time.sleep(1)
                limpar_tela()
                Explorar_Conteudo(usuario)
            elif opcao == "2":
                limpar_tela()
                menu_config_usuario(usuario)

            elif opcao == "3":
                limpar_tela()
                print("Selecione o perfil para as recomendações:\n")
                booleano = usuario.listar_perfis()  
                if not booleano:
                    time.sleep(1.5)
                    continue

                nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
                if not nome_perfil:
                    continue
                    
                perfil = usuario.obter_perfil_por_nome(nome_perfil)
                if not perfil:
                    print(f"Perfil '{nome_perfil}' não encontrado.")
                    time.sleep(1.5)
                    continue
                
                # Submenu para escolher a estratégia
                while True:
                    limpar_tela()
                    print("Menu de Recomendações\n")
                    print("1. Ver Recomendações")
                    print("2. Mudar Estratégia de Recomendação")
                    print("3. Voltar")
                    escolha_rec = input("Escolha uma opção: ")

                    if escolha_rec == "1":
                        limpar_tela()
                        perfil.recomendacoes.recomendar_conteudo(usuario, perfil)
                        input("\nPressione Enter para continuar...")
                    elif escolha_rec == "2":
                        limpar_tela()
                        print("Escolha a nova estratégia de recomendação:\n")
                        print("1. Baseada em Gêneros (Padrão)")
                        print("2. Em Alta (Trending)")
                        print("3. Surpreenda-me (Aleatória)")
                        escolha_strat = input("Escolha uma opção: ")
                        if escolha_strat == "1":
                            perfil.recomendacoes.set_strategy(GenreBasedStrategy())
                        elif escolha_strat == "2":
                            perfil.recomendacoes.set_strategy(TrendingStrategy())
                        elif escolha_strat == "3":
                            perfil.recomendacoes.set_strategy(SurpriseMeStrategy())
                        else:
                            print("Opção inválida.")
                        time.sleep(1.5)
                    elif escolha_rec == "3":
                        break
                    else:
                        print("Opção inválida.")
                        time.sleep(1)


            elif opcao == "4":
                limpar_tela()
                usuario.multiplo_streaming.menu_de_streaming()

            elif opcao == "5":
                limpar_tela()
                while True:
                    print("Marcação de conteúdo e histórico de visualização:\n")
                    print("╔" + "═" * 50 + "╗")
                    print("1. Ver histórico de exibição\n")
                    print("2. Limpar histórico de exibição\n")
                    print("3. Opções de Bookmarking\n")
                    print("4. Voltar ao menu principal")
                    print("╚" + "═" * 50 + "╝")
                    opcao_historico = input("Escolha uma opção (1-4):\n ")
                    if opcao_historico == "1":
                        limpar_tela()
                        print("Selecione o perfil para acessar o histórico:\n")
                        usuario.listar_perfis()
                        nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
                        if not nome_perfil: continue
                        perfil = usuario.obter_perfil_por_nome(nome_perfil)

                        if perfil:
                            ver_historico_de_exibicao(perfil.historico)
                            input("\nPressione Enter para voltar...")
                        else:
                            print(f"Perfil '{nome_perfil}' não encontrado.")
                            time.sleep(1.5)
                    
                    elif opcao_historico == "2":
                        limpar_tela()
                        print("Selecione o perfil para acessar o histórico:\n")
                        usuario.listar_perfis()
                        nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
                        if not nome_perfil: continue
                        perfil = usuario.obter_perfil_por_nome(nome_perfil)

                        if perfil:
                            limpar_historico(perfil.historico)
                            input("Pressione Enter para continuar...")
                        else:
                            print(f"Perfil '{nome_perfil}' não encontrado.")
                            time.sleep(1.5)
                    elif opcao_historico == "3":
                        bookmarking(usuario)
                        input("Pressione Enter para continuar...")
                    elif opcao_historico == "4":
                        break
                    else:
                        print("Opção inválida.")
                        time.sleep(1)
                    limpar_tela()

            elif opcao == "6":
                processo_para_avaliar(usuario, reviews)
            elif opcao == "7":
                limpar_tela()
                print("Você escolheu sair.\n")
                print("Tem certeza de que deseja sair?\n"
                    "1. Sim\n"
                    "2. Não\n")
                opcao_logout = input("")
                if opcao_logout == "1":
                    print("Desconectando...\n")
                    time.sleep(1)
                    return 
                elif opcao_logout == "2":
                    print("Retornando ao menu principal...\n")
                    time.sleep(1)
                else:
                    print("Opção inválida. Tente novamente.")
                    time.sleep(1)
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nLogout forçado detectado. Desconectando...")
            time.sleep(1)
            return # Volta ao menu inicial
        except Exception as e:
            print(f"Erro inesperado no menu principal: {e}")
            print("Ocorreu um erro. Tentando recarregar o menu...")
            time.sleep(2)


if __name__ == "__main__":
    inicializar()
    menu_inicial()