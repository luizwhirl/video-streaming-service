
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

## 🧱 **Padrões criacionais**
- **Singleton**: Aplicado em ```Avaliacoes```, esse padrão garante que exista somente uma única instância dessa classe em toda a aplicação, o que funciona como um ponto de acesso global para as avaliações de conteúdo. Desse modo, qualquer parte do sistema que precisa registrar ou consultar uma avaliação vai estar interagindo com o mesmo e único repositório de dados, garantindo a consistência e integridade das informações das reviews. 
- **Factory Method**: Aqui, esse padrão foi usado na classe ```MidiaFactory``` para centralizar a criação de tipos diferentes de midias. Em vez do código do cliente decidir qual classe instanciar, ele vai somente enviar os dados para a "fábrica", que analisa o "tipo" de mídia e retorna o objeto certo. Essa prática desacopla o sistema, o que facilita a adição de novos tipos de conteúdos no futuro, já que as mudanças ficam concentradas somente na fábrica. 
- **Builder**:  Foi implementado na classe ```UserBuilder``` e serve para simplificar a criação de objetos ```User``` complexos. Ele permite construir o objeto passo a passo atráves de métodos encadeados, como ```com_nome()``` e ```com_email()```, sendo finalizada com o método ```build()```. Aqui nós separamos a lógica de construção do objeto final, o que torna a criação de novos usuários mais legível e mais organizada, especialmente quando é para se lidar com múltiplos atributos e regras de validação.
<!-- - ****: -->

---
## 👤 **Padrões comportamentais**
- **Observer**: Criei para ele um novo arquivo. Ele é um padrão ideal para situações em que uma mudança de estado em um objeto deva notificar e atualizar automaticamente outros objetos dependentes. Ele foi aplicado no sistema de gerenciamento de planos de assinatura. Quando um usuário (que é o sujeito) muda o Plano, os objetos (como o StreamingSession, por exemplo) e a BandaLarga vão ser automaticamente modificados e podem reagir às mudanças feitas.
- **Strategy**: Esse padrão permite que se possa definir uma família de algoritmos, encaplusar cada um deles e torná-los intercambiáveis. Aqui, ele era perfeito para o sistema de recomendações, já que ao invés de se ter uma única lógica de recomendação, a gente criou estratégias diferentes (baseada no gênero, tendências, ou até mesmo aleatória) que podem ser trocadas, dando mais flexibilidade ao sistema e ao usuário.
- **State**: A implementação do padrão State agora permite que um objeto (que nesse caso aqui é o player de vídeo) mude seu comportamento quando seu estado interno muda. O player vai se comportar de maneira diferente se ele está: Tocando ou pausando. Esse padrão organiza essa lógica de uma forma límpa e extensível, o que elimina a necessidade de grandes blocos de if/elif.
---

## 🎢 **Padrões estruturais**
- **Decorator**: Pelo fato do sistema ter diferentes tipos de mídias o decorator permite adicionar novas responsabilidades ou características a objetos dinamicamente, como se estivesse os embrulhando em classes decoradoras.
- **Adapter**: A função todas_as_mídias() carrega dados de um json, que tem uma estrutura específica (tipo "título", "gênero"). Esse novo padrão vai permitir que o sistema trabalhe com outras fontes de dados que possuam interfaces incompatíveis.
- **Facade**: Esse rapazinho fornece uma interface unificada e simplificada para um conjunto complexo de interfaces em um subsistema.
<!-- - ****: -->

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



