# bandwidth_optimization.py

# Bandwidth Optimization: Adapting streaming quality based on user bandwidth
# Nesse caso, estou simulando uma rede instável visto que para fazer isso diretamente teria que importar outras bibliotecas não nativas do python, como o speedtest
import random
from observer import Observer, Subject

class BandaLarga(Observer):
    def __init__(self):
        self.velocidade_mbps = None
        self.qualidade_video = "720p" # Qualidade padrão
        self.auto_ajuste = True # Configurado para ajuste automático

    def update(self, usuario: Subject) -> None:
        """
        Recebe notificação quando o plano do usuário muda e ajusta as capacidades.
        """
        # MUDANÇA: Adicionado try...except para acessar atributos do usuário
        try:
            print(f"\n[Notificação de Banda Larga]: O plano do usuário {usuario.nome} foi atualizado para '{usuario.plano.nome}'. As configurações de qualidade foram reavaliadas.")
        except AttributeError as e:
            print(f"[Notificação de Banda Larga]: Erro ao ler atualização do usuário: {e}")

    def detectar_velocidade(self):
        return round(random.uniform(0.5, 300), 2) # Retorna um valor aleatório de velocidade de internet
    
    def ajustar_qualidade(self, usuario):
        if self.auto_ajuste is True:
            self.velocidade_mbps = self.detectar_velocidade()
            
            # MUDANÇA: Adicionado try...except para o caso de 'usuario.plano.nome' falhar
            try:
                if self.velocidade_mbps < 0.7:
                    print("Mudando para 144p devido à baixa velocidade.")
                    self.qualidade_video = "144p"
                elif self.velocidade_mbps < 1.5:
                    print("Mudando para 240p devido à baixa velocidade.")
                    self.qualidade_video = "240p"
                elif self.velocidade_mbps < 3:
                    print("Mudando para 360p devido à baixa velocidade.")
                    self.qualidade_video = "360p"
                elif self.velocidade_mbps < 5:
                    print("Mudando para 480p devido à baixa velocidade.")
                    self.qualidade_video = "480p"
                elif self.velocidade_mbps < 10:
                    print("Mudando para 720p devido à média velocidade.")
                    self.qualidade_video = "720p"
                elif self.velocidade_mbps < 25:
                    print("Mudando para 1080p devido à alta velocidade.")
                    self.qualidade_video = "1080p"
                else:
                    if usuario.plano.nome == "Premium":
                        print("Conexão excelente! Mudando para 4K.")
                        self.qualidade_video = "4K"
                    else:
                        print("Conexão excelente! Mudando para 1080p.")
                        self.qualidade_video = "1080p"
            except AttributeError as e:
                print(f"Erro ao verificar plano do usuário para ajuste de qualidade: {e}")
                print("Mantendo qualidade 1080p como padrão de alta velocidade.")
                self.qualidade_video = "1080p" # Fallback seguro

    def mudar_qualidade(self, usuario):
        # Mudar manualmente para a qualidade que eu quiser. Se tentar mudar para resoluções altas com conexão ruim, haverá travamentos
        
        # MUDANÇA: Bloco try...except melhorado para cobrir AttributeError e outros erros
        try: 
            self.auto_ajuste = False

            qualidades_validas = ["144p", "240p", "360p", "480p", "720p", "1080p"]
            qualidades_validas_premium = ["144p", "240p", "360p", "480p", "720p", "1080p", "4K"]

            if usuario.plano.nome == "Premium":
                usuario.plano.alta_definicao = True
                print("As qualidades válidas são:", ", ".join(qualidades_validas_premium))
                print("Digite a qualidade desejada para confirmar a mudança manual:")
                nova_qualidade = input()
                if nova_qualidade in qualidades_validas_premium:
                    self.qualidade_video = nova_qualidade
                else:
                    print("Qualidade inválida. Escolha entre: 144p, 240p, 360p, 480p, 720p, 1080p, 4K.")

            else:
                usuario.plano.alta_definicao = False
                print("As qualidades válidas são:", ", ".join(qualidades_validas))
                print("Digite a qualidade desejada para confirmar a mudança manual:")
                nova_qualidade = input()
                if nova_qualidade in qualidades_validas:
                    self.qualidade_video = nova_qualidade
                else:
                    print("Qualidade inválida. Escolha entre: 144p, 240p, 360p, 480p, 720p, 1080p.")
        
        except AttributeError as e:
            print(f"Erro ao acessar dados do plano do usuário: {e}")
        except Exception as e:
            print(f"Erro inesperado ao mudar qualidade: {e}")
            print("Qualidade inválida! Continua na configuração anterior.")

    def exibir_configuracoes_qualidade(self):
        print(f"Qualidade de vídeo: {self.qualidade_video}")
        print(f"Ajuste automático: {'Ativado' if self.auto_ajuste else 'Desativado'}")
        print(f"Velocidade da conexão: {self.velocidade_mbps} Mbps")