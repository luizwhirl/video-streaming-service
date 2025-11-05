# bookmarking_and_history.py

from utility import limpar_tela
import time

class Historico:
    def __init__(self):
        self.historico = []

    def adicionar_no_historico(self, midia):
        if midia in self.historico:
            self.historico.remove(midia)

        self.historico.insert(0, midia) # Insere no início para mostrar os mais recentes primeiro

    def exibir_historico(self):
        if self.historico == []:
            print("Seu histórico está vazio. Assista algum conteúdo primeiro.")
        else:
            print("Recém-reproduzidos:")
            for midia in self.historico:
                midia.exibir_informacoes()
                
    def limpar_historico(self):
        self.historico.clear()
        print("Seu histórico foi limpo com sucesso.")

# Recebe o objeto histórico de algum Perfil específico, a partir dele podemos ver seu historico ou limpar

def ver_historico_de_exibicao(historico):  
    historico.exibir_historico()

def limpar_historico(historico):
    historico.limpar_historico()

class Marcar:
    def __init__(self):
        self.marcados = []

    def marcar_conteudo(self, midia):
        if midia in self.marcados:  
            print("Este conteúdo já está marcado para assistir depois.")
            return
        
        if midia.assistido is False:
            self.marcados.append(midia)
            print("Conteúdo marcado com sucesso.")
        else:
            print("Você já assistiu a este conteúdo. Deseja marcar para assistir depois novamente?")
            resposta = input("Digite '1' para sim ou '2' para não: ")
            if resposta == '1':
                self.marcados.append(midia)
                print("Conteúdo marcado com sucesso.")
            else:
                print("Conteúdo não marcado.")
                
    def desmarcar_conteudo(self, midia):
        # MUDANÇA: Adicionado try...except caso a mídia não esteja na lista
        try:
            self.marcados.remove(midia)
        except ValueError:
            print(f"Erro: A mídia '{midia.titulo}' não estava na lista para desmarcar.")

    def listar_marcados(self):
        for midia in self.marcados:
            midia.exibir_informacoes()

# Função auxiliar para o bookmarking (basicamente repete a logica da função Explorar conteúdo)
def obter_catalogo_do_perfil(perfil):
    from library_management import todas_as_midias, ConjuntoMidias
    
    if perfil.catalogo is None:
        cat = ConjuntoMidias()
        midias = todas_as_midias()  # cria as instâncias UMA vez para este perfil
        if getattr(perfil, "controle_parental", False):
            # MUDANÇA: Adicionado try...except para a conversão da classificação
            midias_filtradas = []
            for m in midias:
                try:
                    classificacao_int = int(str(m.classificacao).rstrip('+'))
                    if classificacao_int <= perfil.idade_limite:
                        midias_filtradas.append(m)
                except (ValueError, TypeError):
                    # Se a classificação for 'L' (Livre) ou algo não numérico, tratamos como 0
                    if str(m.classificacao).upper() == 'L':
                         midias_filtradas.append(m)
                    else:
                        print(f"Aviso: Classificação inválida ('{m.classificacao}') para '{m.titulo}'. Tratando como restrito.")
            
            midias = midias_filtradas
            
        cat.midias.extend(midias)
        perfil.catalogo = cat
    return perfil.catalogo

def bookmarking(usuario):
    limpar_tela()
    print("Selecione um perfil:")
    continuar = usuario.listar_perfis()
    if not continuar:
        return
    nome_perfil = input("Digite o nome do perfil (ou pressione Enter para voltar): ")
    if not nome_perfil:
        return
        
    perfil = usuario.obter_perfil_por_nome(nome_perfil)  
    if perfil is None:
        print(f"Perfil '{nome_perfil}' não encontrado. Por favor, tente novamente.")
        return

    limpar_tela()
    print("╔" + "═" * 50 + "╗")
    print("O que deseja fazer?")
    print("1. Marcar conteúdo")
    print("2. Desmarcar conteúdo")
    print("3. Ver os conteúdos marcados")
    print("╚" + "═" * 50 + "╝")
    acao = input("Digite o número da ação desejada: ")

    if acao == "1":
        catalogo = obter_catalogo_do_perfil(perfil)

        while True:
            titulo = input("Digite o nome do conteúdo que deseja marcar (ou pressione Enter para cancelar):")
            if not titulo:
                break
                
            try:
                resultados = catalogo.buscar_por_titulo(titulo)
            except Exception as e:
                print(f"Ocorreu um erro ao buscar o conteúdo: {e}")
                time.sleep(1.5)
                break

            if not resultados:
                print("Nenhum conteúdo encontrado com esse título.")
                continue

            print("\nConteúdos encontrados:\n")
            for idx, midia in enumerate(resultados):
                print(f"[{idx + 1}]")
                midia.exibir_informacoes()
                print()

            escolha_conteudo = input("Digite o número do conteúdo que deseja marcar (ou pressione Enter para cancelar): ")
            if not escolha_conteudo:
                break

            # MUDANÇA: Adicionado try...except para converter a escolha em inteiro
            try:
                if escolha_conteudo.isdigit():
                    indice = int(escolha_conteudo) - 1
                    if 0 <= indice < len(resultados):
                        midia_selecionada = resultados[indice]
                        perfil.marcar.marcar_conteudo(midia_selecionada)
                        break
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida. Digite um número.")
            except ValueError:
                 print("Entrada numérica inválida.")
                 
    elif acao == "2":
        if not perfil.marcar.marcados:
            print("Nenhum conteúdo marcado.")
            return

        print("Conteúdos marcados:")
        perfil.marcar.listar_marcados()

        titulo = input("Digite o título do conteúdo que deseja desmarcar (ou pressione Enter para cancelar): ")
        if not titulo:
            return
        
        midia_para_desmarcar = None
        for midia in perfil.marcar.marcados:
            if midia.titulo.lower() == titulo.lower():
                midia_para_desmarcar = midia
                break

        if midia_para_desmarcar:
            perfil.marcar.desmarcar_conteudo(midia_para_desmarcar) # A exceção é tratada dentro do método
            print("Conteúdo desmarcado com sucesso.")
        else:
            print("Conteúdo não encontrado na lista de marcados.")
    elif acao == "3":
        if not perfil.marcar.marcados:
            print("Nenhum conteúdo marcado.")
            return

        print("Conteúdos marcados:")
        perfil.marcar.listar_marcados()