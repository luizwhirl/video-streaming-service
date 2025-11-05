#multi_device.py

# Multi-Device Streaming: Enabling content streaming across various devices;

from utility import limpar_tela
import time
import random
from observer import Observer, Subject

class Device:
    def __init__(self, nome, tipo, identificador):
        self.nome = nome
        self.tipo = tipo
        self.identificador = identificador
        self.streaming_content = None # mudei isso aqui para que possamos controlar o que está sendo transmitido

    def __str__(self):
        status = f"Transmitindo: {self.streaming_content}" if self.streaming_content else "Disponível"
        return f"{self.nome} ({self.tipo}) - ID: {self.identificador} [{status}]"

    def exibir_informacoes(self):
        print(f"Dispositivo: {self.nome}")
        print(f"Tipo: {self.tipo}")
        print(f"ID: {self.identificador}")
        if self.streaming_content:
            print(f"Status: Transmitindo '{self.streaming_content}'")
        else:
            print("Status: Disponível")

class StreamingSession(Observer):
    def __init__(self, usuario):
        self.usuario = usuario
        self.dispositivos = [] 

    def update(self, usuario: Subject) -> None:
        """
        Recebe notificação quando o plano do usuário muda para reavaliar o limite de telas.
        """
        # MUDANÇA: Adicionado try...except para acessar atributos do usuário
        try:
            novo_limite = usuario.plano.maximo_telas_simultaneas
            print(f"\n[Notificação de Streaming]: O plano de {usuario.nome} foi atualizado. Novo limite de telas simultâneas: {novo_limite}.")
            sessoes_ativas = self.get_sessoes_ativas()
            if sessoes_ativas > novo_limite:
                print(f"AVISO: Você está excedendo o novo limite de telas. Ativas: {sessoes_ativas}, Limite: {novo_limite}.")
        except AttributeError as e:
            print(f"[Notificação de Streaming]: Erro ao ler atualização do usuário: {e}")


    # vamos contar quantas telas estão ativas
    def get_sessoes_ativas(self):
        return sum(1 for d in self.dispositivos if d.streaming_content is not None)

    def adicionar_dispositivo(self):
        # MUDANÇA: Adicionado try...except para geração de ID (improvável, mas seguro)
        try:
            nome = input("Digite o nome do dispositivo (ex: TV da Sala): ")
            tipo = input("Digite o tipo do dispositivo (ex: Smart TV): ")
            device_id = random.randint(1000, 9999)

            while any(d.identificador == device_id for d in self.dispositivos):
                device_id = random.randint(1000, 9999)

            dispositivo = Device(nome, tipo, device_id)
            self.dispositivos.append(dispositivo)
            print(f"Dispositivo '{dispositivo.nome}' adicionado.")
        except Exception as e:
            print(f"Erro ao adicionar dispositivo: {e}")

    # aqui a lógica foi refeita para simular streaming simultâneo
    def iniciar_sessao(self):
        # MUDANÇA: Adicionado try...except para todo o processo
        try:
            sessoes_ativas = self.get_sessoes_ativas()
            limite_telas = self.usuario.plano.maximo_telas_simultaneas

            print(f"Telas em uso: {sessoes_ativas} de {limite_telas}")

            if sessoes_ativas >= limite_telas:
                print("Limite de telas simultâneas atingido para o seu plano!")
                input("Pressione Enter para continuar...")
                return

            dispositivos_disponiveis = [d for d in self.dispositivos if not d.streaming_content]
            if not dispositivos_disponiveis:
                print("Todos os seus dispositivos já estão em uso.")
                input("Pressione Enter para continuar...")
                return

            print("\nDispositivos disponíveis:")
            for i, device in enumerate(dispositivos_disponiveis):
                print(f"{i + 1}. {device.nome} ({device.tipo})")

            escolha = input("Escolha o dispositivo para iniciar a transmissão (ou Enter para cancelar): ")
            if not escolha:
                return
                
            if not escolha.isdigit():
                 print("Entrada inválida. Digite um número.")
                 time.sleep(1)
                 return

            indice_escolha = int(escolha) - 1
            if not (0 <= indice_escolha < len(dispositivos_disponiveis)):
                print("Opção inválida.")
                time.sleep(1)
                return
            
            dispositivo_escolhido = dispositivos_disponiveis[indice_escolha]
            
            # simula a escolha de um conteúdo para assistir
            midia = input("Digite o nome do filme/série para assistir neste dispositivo: ")
            if not midia:
                print("Nenhum conteúdo selecionado.")
                return

            dispositivo_escolhido.streaming_content = midia
            print(f"\nIniciando a transmissão de '{midia}' em '{dispositivo_escolhido.nome}'.")
            print(f"Telas em uso: {self.get_sessoes_ativas()} de {limite_telas}")
            input("Pressione Enter para continuar...")
            
        except ValueError:
            print("Entrada numérica inválida.")
            time.sleep(1)
        except AttributeError as e:
            print(f"Erro ao ler dados do plano do usuário: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"Erro inesperado ao iniciar sessão: {e}")
            time.sleep(1)


    # a  lógicaaqui foi refeita para encerrar um stream específico
    def encerrar_sessao(self):
        # MUDANÇA: Adicionado try...except para todo o processo
        try:
            dispositivos_ativos = [d for d in self.dispositivos if d.streaming_content]
            if not dispositivos_ativos:
                print("Nenhuma transmissão ativa para encerrar.")
                input("Pressione Enter para continuar...")
                return

            print("\nSelecione a transmissão para encerrar:")
            for i, device in enumerate(dispositivos_ativos):
                print(f"{i + 1}. {device.nome} (assistindo '{device.streaming_content}')")
            
            escolha = input("Qual transmissão deseja encerrar? (ou Enter para cancelar): ")
            if not escolha:
                return
                
            if not escolha.isdigit():
                 print("Entrada inválida. Digite um número.")
                 time.sleep(1)
                 return
                 
            indice_escolha = int(escolha) - 1
            if not (0 <= indice_escolha < len(dispositivos_ativos)):
                print("Opção inválida.")
                time.sleep(1)
                return

            dispositivo_a_parar = dispositivos_ativos[indice_escolha]
            print(f"\nEncerrando a transmissão em '{dispositivo_a_parar.nome}'.")
            dispositivo_a_parar.streaming_content = None
            print(f"Dispositivo agora está disponível. Telas em uso: {self.get_sessoes_ativas()}")
            input("Pressione Enter para continuar...")
            
        except ValueError:
            print("Entrada numérica inválida.")
            time.sleep(1)
        except Exception as e:
            print(f"Erro inesperado ao encerrar sessão: {e}")
            time.sleep(1)


    def remover_dispositivo(self):
        if not self.dispositivos:
            print("Nenhum dispositivo para remover.")
            return

        self.listar_dispositivos()
        try:
            dispositivo_id_str = input("Digite o ID do dispositivo a ser removido (ou pressione Enter para cancelar): ")
            if not dispositivo_id_str:
                return
            dispositivo_id = int(dispositivo_id_str)
            dispositivo = next((d for d in self.dispositivos if d.identificador == dispositivo_id), None)
            if dispositivo:
                self.dispositivos.remove(dispositivo)
                print(f"Dispositivo '{dispositivo.nome}' removido.")
            else:
                print("ID de dispositivo não encontrado.")
        except ValueError:
            print("ID de dispositivo inválido. Deve ser um número.")

    def listar_dispositivos(self):
        if not self.dispositivos:
            print("Nenhum dispositivo cadastrado.")
            return

        print("Dispositivos conectados:\n")
        for dispositivo in self.dispositivos:
            dispositivo.exibir_informacoes()
            print()

    def menu_de_streaming(self):
        while True:
            # MUDANÇA: Adicionado try...except para proteger o menu
            try:
                limpar_tela()
                sessoes_ativas = self.get_sessoes_ativas()
                limite_telas = self.usuario.plano.maximo_telas_simultaneas
                
                print(f"\nConfigurações de Streaming ({sessoes_ativas}/{limite_telas} telas em uso):")
                print("╔" + "═" * 50 + "╗")
                print("1. Iniciar Transmissão em um Dispositivo")
                print("2. Encerrar Transmissão")
                print("3. Adicionar Dispositivo")
                print("4. Remover Dispositivo")
                print("5. Listar Dispositivos")
                print("6. Sair")
                print("╚" + "═" * 50 + "╝")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    self.iniciar_sessao()
                elif opcao == "2":
                    self.encerrar_sessao()
                elif opcao == "3":
                    self.adicionar_dispositivo()
                    time.sleep(1.5)
                elif opcao == "4":
                    self.remover_dispositivo()
                    time.sleep(1.5)
                elif opcao == "5":
                    limpar_tela()
                    self.listar_dispositivos()
                    input("Pressione Enter para continuar...")
                elif opcao == "6":
                    print("Saindo do menu de streaming.")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    time.sleep(1)
            except AttributeError as e:
                print(f"Erro ao ler dados do plano do usuário: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Erro inesperado no menu de streaming: {e}")
                time.sleep(2)