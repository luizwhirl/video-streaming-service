# player_states.py

from __future__ import annotations
from abc import ABC, abstractmethod
import time
from utility import limpar_tela
from ads_management import realizar_exibicao_anuncio
from rating_and_reviews import Avaliacoes

class Player:
    """
    O Contexto (Player) define a interface de interesse dos clientes. Ele também
    mantém uma referência a uma instância de uma subclasse de Estado, que
    representa o estado atual do Player.
    """
    _state = None

    def __init__(self, midia, usuario, perfil):
        self.midia = midia
        self.usuario = usuario
        self.perfil = perfil
        # Define o estado inicial como Pausado para mostrar o menu primeiro
        self.transicionar_para(PausedState())

    def transicionar_para(self, state: PlayerState):
        """
        O Contexto permite alterar o objeto de Estado em tempo de execução.
        """
        # MUDANÇA: Adicionado try...except para a transição de estado
        try:
            print(f"Player: Transicionando para {type(state).__name__}")
            self._state = state
            self._state.player = self
        except Exception as e:
            print(f"Erro crítico ao transicionar estado do player: {e}")
            # Se a transição falhar, tentamos parar o player
            self._state = StoppedState()
            self._state.player = self


    def executar(self):
        """
        O loop principal que executa o player.
        """
        # MUDANÇA: Adicionado try...except ao redor do loop do player
        try:
            while not isinstance(self._state, StoppedState):
                self._state.renderizar()
                self._state.lidar_com_input()
        except AttributeError as e:
            print(f"Erro: O estado do player não foi definido corretamente. {e}")
        except Exception as e:
            print(f"Erro crítico durante a execução do player: {e}")
            self.parar() # Garante que o player pare em caso de erro


    def parar(self):
        self.transicionar_para(StoppedState())


class PlayerState(ABC):
    """
    A classe base do Estado declara métodos que todos os Estados concretos
    devem implementar e também fornece uma referência de volta para o objeto
    de Contexto (Player).
    """
    @property
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, player: Player) -> None:
        self._player = player

    @abstractmethod
    def renderizar(self) -> None:
        """Renderiza a UI do estado atual."""
        pass

    @abstractmethod
    def lidar_com_input(self) -> None:
        """Processa o input do usuário para o estado atual."""
        pass


class PausedState(PlayerState):
    """
    Implementação do estado Pausado.
    """
    def renderizar(self) -> None:
        # MUDANÇA: Adicionado try...except para proteger a renderização
        try:
            limpar_tela()
            print(f"Conteúdo pausado: {self.player.midia.titulo}")
            self.player.usuario.otimizacao_banda_larga.exibir_configuracoes_qualidade()
            print("\nO que deseja fazer?")
            print("1. Continuar assistindo")
            print("2. Mudar a qualidade de reprodução")
            print("3. Ver avaliações deste conteúdo")
            print("4. Parar de assistir")
        except AttributeError as e:
            print(f"Erro ao renderizar menu de pausa (dados faltando): {e}")
        except Exception as e:
            print(f"Erro inesperado ao renderizar menu de pausa: {e}")


    def lidar_com_input(self) -> None:
        # MUDANÇA: Adicionado try...except para lidar com inputs e ações
        try:
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "1":
                self.player.transicionar_para(PlayingState())
            elif escolha == "2":
                self.player.usuario.otimizacao_banda_larga.mudar_qualidade(self.player.usuario)
            elif escolha == "3":
                limpar_tela()
                print(f"Exibindo avaliações para: {self.player.midia.titulo}\n")
                reviews_globais = Avaliacoes()
                reviews_globais.mostrar_avaliacoes_por_id(self.player.midia.id_midia)
                input("\nPressione Enter para voltar...")
            elif escolha == "4":
                self.player.parar()
            else:
                print("Opção inválida.")
                time.sleep(1)
        except AttributeError as e:
             print(f"Erro ao processar ação (dados faltando): {e}")
             time.sleep(1)
        except Exception as e:
            print(f"Erro inesperado ao processar input: {e}")
            time.sleep(1)


class PlayingState(PlayerState):
    """
    Implementação do estado Tocando (Playing).
    """
    def renderizar(self) -> None:
        # MUDANÇA: Adicionado try...except para proteger a renderização
        try:
            limpar_tela()
            titulo = self.player.midia.titulo.strip()
            titulo_centralizado = titulo.center(24)

            self.player.usuario.otimizacao_banda_larga.ajustar_qualidade(self.player.usuario)
            self.player.usuario.otimizacao_banda_larga.exibir_configuracoes_qualidade()
            
            print()
            print("░▀▄░░▄▀")
            print("▄▄▄██▄▄▄▄▄")
            print("█▒░▒░▒░█▀█ Assistindo:")
            print(f"█░▒░▒░▒█▀█ {titulo_centralizado} ")
            print("█▄▄▄▄▄▄███═════════════════════")
            print()

            if self.player.usuario.plano.nome != "Premium":
                anuncio = realizar_exibicao_anuncio(self.player.usuario)
                if anuncio:
                    # Após o anúncio, volta para o menu de pausa para não ficar em loop
                    self.player.transicionar_para(PausedState())
            else:
                print("Pressione Enter para pausar.")
        except AttributeError as e:
            print(f"Erro ao renderizar player (dados faltando): {e}")
            self.player.transicionar_para(PausedState()) # Tenta voltar para Pausa
        except Exception as e:
            print(f"Erro inesperado ao renderizar player: {e}")
            self.player.transicionar_para(PausedState()) # Tenta voltar para Pausa


    def lidar_com_input(self) -> None:
        # Em um app real, isso seria um evento. Aqui, simulamos com input().
        # Se for Premium, o input pausa. Se não, a pausa ocorre após o anúncio.
        # MUDANÇA: Adicionado try...except
        try:
            if self.player.usuario.plano.nome == "Premium":
                input() # Espera o Enter para pausar
                self.player.transicionar_para(PausedState())
            # Para planos com anúncios, a transição já é feita no método renderizar.
        except AttributeError as e:
            print(f"Erro ao verificar plano do usuário no input: {e}")
            self.player.transicionar_para(PausedState())
        except Exception as e:
            print(f"Erro inesperado no input do player: {e}")
            self.player.transicionar_para(PausedState())


class StoppedState(PlayerState):
    """
    Estado final para encerrar o player.
    """
    def renderizar(self) -> None:
        # MUDANÇA: Adicionado try...except
        try:
            print(f"\nVocê parou de assistir {self.player.midia.titulo}.")
            print("Obrigado por assistir!")
            time.sleep(1.5)
            limpar_tela()
        except AttributeError:
             print("\nObrigado por assistir!") # Fallback se 'player' ou 'midia' não existirem
             time.sleep(1.5)
             limpar_tela()
        except Exception as e:
            print(f"Erro ao encerrar o player: {e}")
            limpar_tela()


    def lidar_com_input(self) -> None:
        # Este estado não lida com input, ele apenas encerra o loop.
        pass