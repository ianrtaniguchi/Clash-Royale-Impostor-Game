import random
import streamlit as st

cartas_clash = [
    "Aríete de Batalha", "Arqueiro Mágico", "Arqueiras", "Bandida", "Bárbaros",
    "Bárbaros de Elite", "Barril de Bárbaro", "Barril de Esqueletos", "Barril de Goblins",
    "Bebê Dragão", "Bola de Fogo", "Bola de Neve Gigante", "Bombardeiro",
    "Broca de Goblin", "Bruxa", "Bruxa Mãe", "Caçador", "Canhão",
    "Canhão com Rodas", "Cavaleiro", "Cavaleiro Dourado", "Cemitério", "Clone",
    "Corredor", "Domadora de Cordeiro", "Dragão Elétrico", "Dragão Infernal",
    "Duquesa das Adagas", "Eletrocutadores", "Encomenda Real", "Esqueletos",
    "Espelho", "Espírito de Cura", "Espírito de Fogo", "Espírito de Gelo",
    "Espírito Elétrico", "Exército de Esqueletos", "Executor", "Flechas", "Fênix",
    "Fornalha", "Foguete", "Fúria", "Gangue de Goblins", "Gelo", "Gigante",
    "Gigante Elétrico", "Gigante Esqueleto", "Gigante Goblin", "Gigante Real",
    "Goblins", "Goblins Lanceiros", "Golem", "Golem de Elixir", "Golem de Gelo",
    "Guardas", "Jaula de Goblin", "Lançador", "Lápide", "Lenhador", "Mago",
    "Mago de Gelo", "Mago Elétrico", "Máquina de Voar", "Mega Cavaleiro",
    "Megasservo", "Mineiro", "Mineiro Bombado", "Mini P.E.K.K.A", "Monge",
    "Morcegos", "Morteiro", "Mosqueteira", "O Tronco", "P.E.K.K.A",
    "Pequeno Príncipe", "Pescador", "Pirotécnica", "Príncipe",
    "Príncipe das Trevas", "Quebra-Muros", "Rainha Arqueira", "Raios",
    "Recrutas Reais", "Rei Esqueleto", "Relâmpago", "Servos", "Sparky",
    "Terremoto", "Tesla", "Tornado", "Torre de Bombas", "Torre Inferno",
    "Três Mosqueteiras", "Valquíria", "Veneno", "X-Besta", "Zap"
]

st.title("🕵️‍♂️ Jogo do Impostor - Clash Royale")

# Inicializar o estado da sessão do Streamlit
if "etapa" not in st.session_state:
    st.session_state.etapa = "config"
if "jogadores" not in st.session_state:
    st.session_state.jogadores = []
if "indice_atual" not in st.session_state:
    st.session_state.indice_atual = 0
if "carta_secreta" not in st.session_state:
    st.session_state.carta_secreta = ""
if "impostor" not in st.session_state:
    st.session_state.impostor = ""

# ETAPA 1: Configuração dos Jogadores
if st.session_state.etapa == "config":
    st.subheader("Configuração da Partida")
    num_jogadores = st.number_input("Número de jogadores (mínimo 3):", min_value=1, max_value=20, value=3)
    
    nomes = []
    for i in range(int(num_jogadores)):
        nome = st.text_input(f"Nome do Jogador {i+1}", key=f"jog_{i}")
        nomes.append(nome)
    
    if st.button("Iniciar Jogo"):
        # Validar se os nomes foram preenchidos
        nomes_validos = [n.strip() for n in nomes if n.strip()]
        if len(nomes_validos) < 3:
            st.error("Você precisa digitar o nome de pelo menos 3 jogadores!")
        else:
            st.session_state.jogadores = nomes_validos
            st.session_state.etapa = "sorteio"
            st.session_state.indice_atual = 0
            st.session_state.carta_secreta = random.choice(cartas_clash)
            st.session_state.impostor = random.choice(nomes_validos)
            st.rerun()

# ETAPA 2: Revelação secreta para cada jogador
elif st.session_state.etapa == "sorteio":
    idx = st.session_state.indice_atual
    jogadores = st.session_state.jogadores
    
    if idx < len(jogadores):
        jogador_atual = jogadores[idx]
        st.info"(Passe o celular/computador para: **{jogador_atual}**")
        
        # Usamos um checkbox ou botão de confirmação para revelar
        ver_carta = st.checkbox("Marque aqui apenas quando for a sua vez de ver a carta", key=f"chk_{idx}")
        
        if ver_carta:
            if jogador_atual == st.session_state.impostor:
                st.error("🚨 Você é o IMPOSTOR! Tente disfarçar.")
            else:
                st.success(f"⚔️ Sua carta secreta é: **{st.session_state.carta_secreta}**")
        
        if st.button("Próximo Jogador / Esconder"):
            st.session_state.indice_atual += 1
            st.rerun()
    else:
        st.session_state.etapa = "fim_rodada"
        st.rerun()

# ETAPA 3: Fim da rodada de revelação
elif st.session_state.etapa == "fim_rodada":
    st.success("🎉 Todos já viram suas cartas! Discutam entre si para descobrir quem é o impostor.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Jogar Outra Rodada"):
            st.session_state.etapa = "sorteio"
            st.session_state.indice_atual = 0
            st.session_state.carta_secreta = random.choice(cartas_clash)
            st.session_state.impostor = random.choice(st.session_state.jogadores)
            st.rerun()
    with col2:
        if st.button("Reiniciar Configurações"):
            st.session_state.etapa = "config"
            st.rerun()