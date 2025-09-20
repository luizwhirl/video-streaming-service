
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

## 🛠️☑️ **Refatoração**

### ⚒️ **Mudanças significativas**
- **Mudança de armazenamento**: Os anúncios e mídias disponíveis agora se encontram num .JSON à parte da lógica do programa.
- **Melhoria da lógica de recomendação**: As recomendações do sistema agora sugerem títulos similares, e não só um gênero. Além de que, para aqueles que não têm histórico de exibição, ele recomenda os mais "populares".
- **Avaliação**: O usuário, antes de fazer uma avaliação, tem que ter assistido a mídia em questão. Além disso, agora o sistema possui um ID para cada filme/série; ou seja, para cada título, há uma avaliação referente à ele. 
- **Serviço de vários dispositivos**: Assim como num sistema real de streaming, o número de aparelhos simultâneos em execução é limitado. Se o número exceder, então nao é possível iniciar uma sessão nova. (Implementação meio inutil, mas meh).
<!-- - ****: 
- ****: 
- ****: 
- ****:  -->

### 🧮 **Mudanças menores**
- **Transições**: O tempo de transição entre "telas" era muito grande e custoso. Esse mesmo tempo foi reduzido.
- **Cancelar ação**: Apesar do sistema já dar a possibilidade de abortar determinada ação, ele nunca informa que você pode usar o enter para cancelar uma atividade. Esses prints foram implementados. 
- **Perfil Inexistente**: O sistema agora sabe quando um perfil digitado não existe, e informa isso ao usuário.
- **Histórico por perfil**: Em alguns casos, o sistema não sabia diferenciar qual perfil havia assistido determinado conteúdo; e então dava o mesmo histório para todos os perfis. 
- **Caixas de texto**: Apenas uma correção visual. O programa agora imprime as caixas de informação de modo mais arrumado.

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



