
# 🎬 **Video Streaming Service**

## 🚀 **Como Executar**

Para rodar o programa, execute o arquivo principal com o comando:

```bash
python main.py
```

---

## ✨ **Funcionalidades**

- 📚 **Consultar biblioteca de conteúdo** ✅
- 👤 **Configurações de usuário** ✅
- 🤖 **Recomendações personalizadas** ☑️
- 📱 **Streaming em múltiplos dispositivos** ☑️
- ⚡ **Otimização de banda larga** ✅
- ⭐ **Marcar conteúdo e histórico de visualização** ✅
- 📝 **Revisões e avaliações de conteúdo** ☑️
- 📢 **Integração com anúncios** ✅
- 🔒 **Controle parental** ✅ 
- 👥 **Gerenciamento de usuário** ✅

## 🛡️ **Tratamento de Exceções**

Para aumentar a robustez e a estabilidade do aplicativo, diversas rotinas de tratamento de exceções foram implementadas. Elas garantem que o programa não pare inesperadamente e forneça feedback útil ao usuário.

- **Validação de Entrada do Usuário (`ValueError`)**:
  - Captura entradas numéricas inválidas (ex: letras em vez de números) em todos os menus, como na seleção de perfis (`parental_control.py`), escolha de mídias (`library_management.py`), definição de notas (`rating_and_reviews.py`) e menus de streaming (`multi_device.py`).
  - Garante que a criação de usuários (`user_management.py`) falhe graciosamente se os dados não passarem nas regras de validação (gerado pelo `UserBuilder` e capturado em `main.py` e `predefinitions.py`).

- **Erros de Leitura de Arquivo (`FileNotFoundError`, `json.JSONDecodeError`, `IOError`)**:
  - Protege o carregamento dos catálogos de mídias (`midias.json`) e anúncios (`anuncios.json`). Se um arquivo não for encontrado, estiver corrompido (JSON inválido) ou houver um erro de permissão de leitura, o sistema informará o erro e continuará executando com um catálogo vazio, em vez de parar. (Implementado em `library_management.py` e `ads_management.py`).

- **Erros de Lógica e Dados (`AttributeError`, `KeyError`, `IndexError`)**:
  - Previne falhas caso um objeto (como `usuario` ou `perfil`) não tenha um atributo esperado (ex: `usuario.plano`). Isso é comum em funções de `update` do padrão Observer (`multi_device.py`, `bandwidth_optimization.py`) e durante a renderização de estados do player (`player_states.py`).
  - Trata `KeyError` ao tentar acessar dados de um dicionário que podem não existir, como ao exibir avaliações (`rating_and_reviews.py`) ou ao definir restrições de idade (`parental_control.py`).
  - Trata `IndexError` ao tentar selecionar um anúncio de uma lista vazia (`ads_management.py`).

- **Erros de Sistema e Recursos (`OSError`, `RuntimeError`)**:
  - Captura `OSError` na função `limpar_tela()` (`utility.py`), permitindo que o programa continue mesmo se não conseguir limpar o console.
  - Captura `RuntimeError` que pode ocorrer ao iniciar uma `threading.Thread` no sistema de anúncios (`ads_management.py`).

- **Interrupção do Usuário (`KeyboardInterrupt`)**:
  - Captura `Ctrl+C` nos menus principais (`main.py`) para permitir uma saída limpa e amigável do programa, em vez de um traceback de erro.

---

## 🛠️☑️ **Refatoração**

### ⚒️ **Mudanças significativas**
- **Mudança de armazenamento**: Os anúncios e mídias disponíveis agora se encontram num .JSON à parte da lógica do programa.
- **Melhoria da lógica de recomendação**: As recomendações do sistema agora sugerem títulos similares, e não só um gênero. Além de que, para aqueles que não têm histórico de exibição, ele recomenda os mais "populares".
- **Avaliação**: O usuário, antes de fazer uma avaliação, tem que ter assistido a mídia em questão. Além disso, agora o sistema possui um ID para cada filme/série; ou seja, para cada título, há uma avaliação referente à ele. 
- **Serviço de vários dispositivos**: Assim como num sistema real de streaming, o número de aparelhos simultâneos em execução é limitado. Se o número exceder, então nao é possível iniciar uma sessão nova. (Implementação meio inutil, mas meh).
### 🧮 **Mudanças menores**
- **Transições**: O tempo de transição entre "telas" era muito grande e custoso. Esse mesmo tempo foi reduzido.
- **Cancelar ação**: Apesar do sistema já dar a possibilidade de abortar determinada ação, ele nunca informa que você pode usar o enter para cancelar uma atividade. Esses prints foram implementados. 
- **Perfil Inexistente**: O sistema agora sabe quando um perfil digitado não existe, e informa isso ao usuário.
- **Histórico por perfil**: Em alguns casos, o sistema não sabia diferenciar qual perfil havia assistido determinado conteúdo; e então dava o mesmo histório para todos os perfis. 
- **Caixas de texto**: Apenas uma correção visual. O programa agora imprime as caixas de informação de modo mais arrumado.

--- 

## 🧱 **Padrões criacionais**
- **Singleton**: Aplicado na classe `Avaliacoes` (`rating_and_reviews.py`), esse padrão garante que exista somente uma única instância dessa classe em toda a aplicação, o que funciona como um ponto de acesso global para as avaliações de conteúdo. Desse modo, qualquer parte do sistema que precisa registrar ou consultar uma avaliação vai estar interagindo com o mesmo e único repositório de dados, garantindo a consistência e integridade das informações das reviews. 
- **Factory Method**: Usado na classe `MidiaFactory` (`library_management.py`) para centralizar a criação de tipos diferentes de midias (`Filme`, `Serie`, `Documentario`, etc.). Em vez do código do cliente decidir qual classe instanciar, ele vai somente enviar os dados para a "fábrica", que analisa o "tipo" de mídia e retorna o objeto certo. Essa prática desacopla o sistema, o que facilita a adição de novos tipos de conteúdos no futuro, já que as mudanças ficam concentradas somente na fábrica. 
- **Builder**: Implementado na classe `UserBuilder` (`user_management.py`) para simplificar a criação de objetos `User` complexos. Ele permite construir o objeto passo a passo atráves de métodos encadeados, como `com_nome()` e `com_email()`, sendo finalizada com o método `build()`. Aqui nós separamos a lógica de construção do objeto final, o que torna a criação de novos usuários mais legível e mais organizada, especialmente quando é para se lidar com múltiplos atributos e regras de validação.
---
## 👤 **Padrões comportamentais**
- **Observer**: Usado para notificar mudanças de estado. A classe `User` (`user_management.py`) atua como o `Subject` (Sujeito). As classes `StreamingSession` (`multi_device.py`) e `BandaLarga` (`bandwidth_optimization.py`) atuam como `Observers` (Observadores). Quando um usuário muda seu plano de assinatura (ex: de "Gratuito" para "Premium"), o `User` notifica seus observadores, que reagem automaticamente para atualizar o limite de telas ou as configurações de qualidade de vídeo.
- **Strategy**: Permite definir uma família de algoritmos e torná-los intercambiáveis. É usado pelo sistema de recomendações. A classe `Recomendacoes` (`recommendations.py`) é o "Contexto" que mantém uma referência a uma estratégia. As classes `GenreBasedStrategy`, `TrendingStrategy`, e `SurpriseMeStrategy` (`recommendation_strategies.py`) são as estratégias concretas, permitindo ao usuário alterar o tipo de recomendação que deseja receber em tempo de execução.
- **State**: Permite que um objeto altere seu comportamento quando seu estado interno muda. Implementado no player de vídeo (`player_states.py`). A classe `Player` é o "Contexto" que delega o comportamento para objetos de estado concretos (`PausedState`, `PlayingState`, `StoppedState`), que implementam a interface comum `PlayerState`. Isso elimina grandes blocos condicionais no player e organiza a lógica de "play", "pause" e "stop" de forma limpa.
---

## 🎢 **Padrões estruturais**
- **Decorator**: Permite adicionar novas responsabilidades a objetos dinamicamente. Usado para adicionar recursos extras às mídias (`library_management.py`). As classes `AudioDescricaoDecorator` e `DublagemDecorator` "embrulham" um objeto `Midia` (como `Filme` ou `Serie`) para adicionar novos recursos (como "Audiodescrição") sem alterar a classe original da mídia.
- **Adapter**: Permite que interfaces incompatíveis trabalhem juntas. Usado em `library_management.py` com a classe `ExternalMediaAdapter`. Ela "traduz" dados de uma fonte externa simulada (que usa chaves como "Title" e "Runtime") para o formato que a `MidiaFactory` interna espera (com chaves como "titulo" e "tempo_duracao"), permitindo que o sistema carregue mídias de diferentes fontes de forma transparente.
- **Facade**: Fornece uma interface unificada e simplificada para um conjunto complexo de interfaces em um subsistema. Funções como `Explorar_Conteudo` (`library_management.py`) e os menus em `main.py` atuam como Facades, escondendo a complexidade de buscar no catálogo, lidar com perfis, iniciar o player e registrar no histórico, tudo através de uma simples interface de menu.
---
## 🏗️ **Estrutura de Projeto**

### 🏛️ **Classes:**

- **User**: Template para ministrar, administrar e utilizar diferentes usuários.
- **Perfil**: Template para diferentes perfis em cada usuário distinto.
- **ConjuntoMidias**: Template onde teremos todos os tipos de mídia possíveis e a partir delas realizar funções como explorar o conteúdo.
- **Midia**: Template que terá diversas outras subclasses referentes ao tipo de mídia, além de funções básicas como exibir informações de tal mídia.

  **Subclasses de Mídia:**
  - **Filme**: Para mídias que são filmes.
  - **Documentario**: Para mídias que são documentários.
  - **Serie**: Para mídias que são séries.
  - **Anime**: Para mídias que são animes.
  - **Novela**: Para mídias que são novelas.
  - **Historico**: Realiza o controle do histórico de exibição, permitindo funcionalidades como limpar histórico ou acessá-lo para cada perfil (vai ser um objeto de um atributo da classe Perfil).

- **Recomendacoes**: Template para sugerir conteúdos específicos baseado no gênero assistido pelo perfil (vai ser um objeto de um atributo da classe Perfil).
- **Anuncio**: Template para fazer a organização e manuntenção de anúncios na plataforma de acordo com o plano 
- **Marcar**: Template para marcar conteúdos específicos para assistir mais tarde e influenciar na recomendação do usuário
- **Plano**: Template para melhorar o gerenciamento de plano com pagamentos e ser utilizado no user_management, além de influenciar na parte dos anúncios devido ao plano escolhido com regras pre-estabelecidas;
- **Devices**: Template para a organização de streaming em multiplataforma;
- **BandaLarga**: Template para a manuntenção da banda larga e a qualidade da transmissão enquanto a pessoa assiste;
- **Avaliacoes**: Template para avaliações e reviews sobre um certo conteúdo em uma mini-rede social;
