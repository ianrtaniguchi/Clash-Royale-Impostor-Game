
# Clash Royale Impostor Game

**Clash Royale Impostor** é um jogo de dedução social multiplayer inspirado em *Among Us* e *Spyfall*, mas com a temática de **Clash Royale**. Os jogadores entram em uma sala e, a cada rodada, uma carta do Clash Royale é sorteada. A maioria dos jogadores vê a carta real, mas um jogador (o Impostor) vê apenas uma dica vaga. O objetivo é descobrir quem é o impostor através de perguntas e respostas, enquanto o impostor tenta se misturar.

## 🎮 Como Jogar

1.  **Login:** Digite seu nome e um ID de sala (ex: `1234`) na tela inicial. Todos os amigos devem usar o mesmo ID de sala.
2.  **Lobby:** Aguarde todos os jogadores entrarem na sala. O jogo requer no mínimo **3 jogadores**.
3.  **Início da Rodada:** Qualquer jogador pode clicar em "SORTEAR CARTA".
4.  **O Jogo:**
      * **Crewmates (Não-Impostores):** A tela ficará azul. Vocês verão a **Imagem** e o **Nome** da carta sorteada.
      * **Impostor:** A tela ficará vermelha. Você verá apenas uma **Dica** (ex: "7 de elixir, tanque"). Você *não* sabe qual é a carta.
5.  **Dedução:** Os jogadores devem conversar e fazer perguntas sobre a carta para tentar identificar quem não sabe do que se trata (o Impostor). O Impostor deve mentir e fingir que sabe qual é a carta baseando-se na dica.
6.  **Próxima Rodada:** Clique em "PRÓXIMA RODADA" para sortear novos papéis e uma nova carta.

## 🚀 Funcionalidades

  * **Sistema de Salas:** Crie ou entre em salas privadas para jogar com amigos.
  * **Multiplayer em Tempo Real:** Sincronização instantânea de estado de jogo, jogadores e sorteios usando **Firebase Realtime Database**.
  * **Papéis Dinâmicos:** Sorteio aleatório de Impostor e Cartas a cada rodada.
  * **Banco de Dados de Cartas:** Integração com um JSON contendo cartas do Clash Royale, suas cores, dicas e imagens.
  * **Interface Responsiva:** Design adaptado para dispositivos móveis e desktop (CSS Dark Mode).

## 🛠️ Tecnologias Utilizadas

  * **HTML5** - Estrutura semântica.
  * **CSS3** - Estilização e responsividade.
  * **JavaScript (Vanilla)** - Lógica do jogo e manipulação do DOM.
  * **Firebase Realtime Database** - Backend para gerenciamento de salas e estados em tempo real.

## 📦 Como Rodar o Projeto

1.  Clone este repositório:
    ```bash
    git clone https://github.com/ianrtaniguchi/clash-royale-impostor-game.git
    ```
2.  Navegue até a pasta do projeto.
3.  Abra o arquivo `index.html` em seu navegador preferido.

> **Nota:** O projeto utiliza uma configuração do Firebase exposta no `index.html`. Para produção ou uso contínuo, recomenda-se criar seu próprio projeto no [Firebase Console](https://console.firebase.google.com/), substituir as credenciais na variável `firebaseConfig` dentro do arquivo `index.html` e importar o arquivo `BD.json` para o seu Realtime Database.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.

Copyright (c) 2025 **Ian Riki Taniguchi**
