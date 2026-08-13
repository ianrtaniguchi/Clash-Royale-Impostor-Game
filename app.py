import random
import json
import tempfile
import os
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# Inicializar o Firebase usando st.secrets com arquivo temporário
if not firebase_admin._apps:
    # 1. Puxa os dados dos segredos
    firebase_config = dict(st.secrets["firebase"])

    # 2. Garante que a chave esteja perfeitamente formatada (remove quebras extras no inicio/fim)
    firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n").strip()

    # 3. Cria um arquivo JSON temporário para o Firebase ler (Isso evita todos os bugs de formato)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
        json.dump(firebase_config, temp_file)
        temp_file_path = temp_file.name

    try:
        # 4. Inicializa o Firebase passando o caminho do arquivo físico temporário
        cred = credentials.Certificate(temp_file_path)
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://impostor-multiplayer-1f7f7-default-rtdb.firebaseio.com/"},
        )
    finally:
        # 5. Apaga o arquivo temporário imediatamente por segurança
        os.remove(temp_file_path)

# Referência global para a sala no Realtime Database
ref = db.reference("sala_jogo")

# Dicionário completo com várias categorias contendo muitos itens
categorias = {
    "Clash Royale": [
        "Aríete de Batalha",
        "Arqueiro Mágico",
        "Arqueiras",
        "Bandida",
        "Bárbaros",
        "Bárbaros de Elite",
        "Barril de Bárbaro",
        "Barril de Esqueletos",
        "Barril de Goblins",
        "Bebê Dragão",
        "Bola de Fogo",
        "Bola de Neve Gigante",
        "Bombardeiro",
        "Broca de Goblin",
        "Bruxa",
        "Bruxa Mãe",
        "Caçador",
        "Canhão",
        "Canhão com Rodas",
        "Cavaleiro",
        "Cavaleiro Dourado",
        "Cemitério",
        "Clone",
        "Corredor",
        "Domadora de Cordeiro",
        "Dragão Elétrico",
        "Dragão Infernal",
        "Duquesa das Adagas",
        "Eletrocutadores",
        "Encomenda Real",
        "Esqueletos",
        "Espelho",
        "Espírito de Cura",
        "Espírito de Fogo",
        "Espírito de Gelo",
        "Espírito Elétrico",
        "Exército de Esqueletos",
        "Executor",
        "Flechas",
        "Fênix",
        "Fornalha",
        "Foguete",
        "Fúria",
        "Gangue de Goblins",
        "Gelo",
        "Gigante",
        "Gigante Elétrico",
        "Gigante Esqueleto",
        "Gigante Goblin",
        "Gigante Real",
        "Goblins",
        "Goblins Lanceiros",
        "Golem",
        "Golem de Elixir",
        "Golem de Gelo",
        "Guardas",
        "Jaula de Goblin",
        "Lançador",
        "Lápide",
        "Lenhador",
        "Mago",
        "Mago de Gelo",
        "Mago Elétrico",
        "Máquina de Voar",
        "Mega Cavaleiro",
        "Megasservo",
        "Mineiro",
        "Mineiro Bombado",
        "Mini P.E.K.K.A",
        "Monge",
        "Morcegos",
        "Morteiro",
        "Mosqueteira",
        "O Tronco",
        "P.E.K.K.A",
        "Pequeno Príncipe",
        "Pescador",
        "Pirotécnica",
        "Príncipe",
        "Príncipe das Trevas",
        "Quebra-Muros",
        "Rainha Arqueira",
        "Raios",
        "Recrutas Reais",
        "Rei Esqueleto",
        "Relâmpago",
        "Servos",
        "Sparky",
        "Terremoto",
        "Tesla",
        "Tornado",
        "Torre de Bombas",
        "Torre Inferno",
        "Três Mosqueteiras",
        "Valquíria",
        "Veneno",
        "X-Besta",
        "Zap",
    ],
    "Comidas e Pratos": [
        "Pizza de Margherita",
        "Sushi de Salmão",
        "Hambúrguer Artesanal",
        "Lasanha à Bolonhesa",
        "Churrasco de Picanha",
        "Strogonoff de Frango",
        "Feijoada Completa",
        "Tacos Mexicanos",
        "Pão de Queijo Mineiro",
        "Coxinha de Frango",
        "Moqueca Capixaba",
        "Yakissoba",
        "Acarajé",
        "Hot Dog Completo",
        "Nuggets de Frango",
        "Batata Frita com Cheddar",
        "Macarrão Carbonara",
        "Risoto de Camarão",
        "Nhoque ao Sugo",
        "Esfiha de Carne",
        "Kibe Frito",
        "Pastel de Vento",
        "Pão de Alho",
        "Frango a Passarinho",
        "Salpicão de Frango",
        "Panqueca de Carne",
        "Burrito Mexicano",
        "Nacho com Guacamole",
        "Cuscuz Paulista",
        "Baião de Dois",
        "Farofa de Bacon",
        "Cartola Pernambucana",
        "Sorvete de Chocolate",
        "Pudim de Leite",
        "Brigadeiro",
        "Açaí na Tigela",
        "Petit Gateau",
    ],
    "Países do Mundo": [
        "Brasil",
        "Japão",
        "França",
        "Canadá",
        "Austrália",
        "Itália",
        "Alemanha",
        "Argentina",
        "Egito",
        "Coreia do Sul",
        "Grécia",
        "Estados Unidos",
        "Reino Unido",
        "Espanha",
        "Portugal",
        "México",
        "Rússia",
        "China",
        "Índia",
        "África do Sul",
        "Nova Zelândia",
        "Suécia",
        "Noruega",
        "Suíça",
        "Holanda",
        "Bélgica",
        "Irlanda",
        "Dinamarca",
        "Finlândia",
        "Polônia",
        "Chile",
        "Colômbia",
        "Peru",
        "Uruguai",
        "Turquia",
        "Tailândia",
        "Vietnã",
        "Filipinas",
        "Islândia",
    ],
    "Filmes e Séries": [
        "Sonic 3",
        "Vingadores: Ultimato",
        "Harry Potter",
        "O Senhor dos Anéis",
        "Interestelar",
        "Matrix",
        "Clube da Luta",
        "Breaking Bad",
        "Stranger Things",
        "Game of Thrones",
        "The Witcher",
        "Homem-Aranha",
        "Batman: O Cavaleiro das Trevas",
        "Avatar",
        "Titanic",
        "Jurassic Park",
        "Star Wars",
        "Pulp Fiction",
        "O Auto da Compadecida",
        "Peaky Blinders",
        "The Boys",
        "Attack on Titan",
        "Classroom of the Elite",
        "Death Note",
        "Naruto",
        "Dragon Ball Z",
        "One Piece",
        "Demon Slayer",
        "Arcane",
        "Toy Story",
        "Shrek",
        "Carros",
        "Divertida Mente",
        "Procurando Nemo",
    ],
    "Animais": [
        "Leão",
        "Tigre",
        "Elefante",
        "Girafa",
        "Zebra",
        "Macaco",
        "Gorila",
        "Urso Pardo",
        "Lobo",
        "Raposa",
        "Coelho",
        "Canguru",
        "Panda",
        "Koala",
        "Tartaruga",
        "Crocodilo",
        "Jacaré",
        "Cobra",
        "Águia",
        "Falcão",
        "Coruja",
        "Pinguim",
        "Golfinho",
        "Baleia Azul",
        "Tubarão Branco",
        "Polvo",
        "Cavalo-marinho",
        "Tubarão Martelo",
        "Cachorro",
        "Gato",
        "Hamster",
        "Porquinho-da-índia",
        "Cavalo",
        "Vaca",
        "Ovelha",
        "Porco",
    ],
}

st.title("🕵️‍♂️ Jogo do Impostor - Multiplayer Firebase")

# Sincronizar estado inicial com o Firebase se existir
dados_remotos = ref.get()

# Inicializar o estado da sessão do Streamlit
if "etapa" not in st.session_state:
    if dados_remotos and "etapa" in dados_remotos:
        st.session_state.etapa = dados_remotos["etapa"]
        st.session_state.jogadores = dados_remotos.get("jogadores", [])
        st.session_state.indice_atual = dados_remotos.get("indice_atual", 0)
        st.session_state.carta_secreta = dados_remotos.get("carta_secreta", "")
        st.session_state.impostor = dados_remotos.get("impostor", "")
        st.session_state.categoria_escolhida = dados_remotos.get("categoria_escolhida", "Clash Royale")
    else:
        st.session_state.etapa = "menu"
        st.session_state.jogadores = []
        st.session_state.indice_atual = 0
        st.session_state.carta_secreta = ""
        st.session_state.impostor = ""
        st.session_state.categoria_escolhida = "Clash Royale"


def atualizar_firebase():
    """Salva o estado atual no Firebase para sincronizar com os outros jogadores"""
    ref.set(
        {
            "etapa": st.session_state.etapa,
            "jogadores": st.session_state.jogadores,
            "indice_atual": st.session_state.indice_atual,
            "carta_secreta": st.session_state.carta_secreta,
            "impostor": st.session_state.impostor,
            "categoria_escolhida": st.session_state.categoria_escolhida,
        }
    )


# Botão para buscar atualizações manuais do servidor
if st.button("🔄 Sincronizar / Atualizar Tela"):
    st.rerun()

# ETAPA 0: Menu de Seleção de Categoria
if st.session_state.etapa == "menu":
    st.subheader("🎯 Escolha a Categoria do Jogo")
    categoria_selecionada = st.selectbox("Selecione o tema:", list(categorias.keys()))

    if st.button("Avançar para Configuração"):
        st.session_state.categoria_escolhida = categoria_selecionada
        st.session_state.etapa = "config"
        atualizar_firebase()
        st.rerun()

# ETAPA 1: Configuração dos Jogadores
elif st.session_state.etapa == "config":
    st.subheader(f"Configuração da Partida (Tema: {st.session_state.categoria_escolhida})")

    if st.button("⬅️ Voltar e trocar de categoria"):
        st.session_state.etapa = "menu"
        atualizar_firebase()
        st.rerun()

    num_jogadores = st.number_input("Número de jogadores (mínimo 3):", min_value=3, max_value=20, value=3)

    nomes = []
    for i in range(int(num_jogadores)):
        nome = st.text_input(f"Nome do Jogador {i+1}", key=f"jog_{i}")
        nomes.append(nome)

    if st.button("Iniciar Jogo"):
        nomes_validos = [n.strip() for n in nomes if n.strip()]
        if len(nomes_validos) < 3:
            st.error("Você precisa digitar o nome de pelo menos 3 jogadores!")
        else:
            st.session_state.jogadores = nomes_validos
            st.session_state.etapa = "sorteio"
            st.session_state.indice_atual = 0

            lista_ativa = categorias[st.session_state.categoria_escolhida]
            st.session_state.carta_secreta = random.choice(lista_ativa)
            st.session_state.impostor = random.choice(nomes_validos)

            atualizar_firebase()
            st.rerun()

# ETAPA 2: Revelação secreta para cada jogador
elif st.session_state.etapa == "sorteio":
    idx = st.session_state.indice_atual
    jogadores = st.session_state.jogadores

    if idx < len(jogadores):
        jogador_atual = jogadores[idx]
        st.info(f"Passe o celular/computador para: **{jogador_atual}**")

        ver_carta = st.checkbox("Marque aqui apenas quando for a sua vez de ver a carta", key=f"chk_{idx}")

        if ver_carta:
            if jogador_atual == st.session_state.impostor:
                st.error("🚨 Você é o IMPOSTOR! Tente disfarçar.")
            else:
                st.success(f"📂 Categoria: **{st.session_state.categoria_escolhida}**\n\n⚔️" f" Sua palavra secreta é: **{st.session_state.carta_secreta}**")

        if st.button("Próximo Jogador / Esconder"):
            st.session_state.indice_atual += 1
            atualizar_firebase()
            st.rerun()
    else:
        st.session_state.etapa = "fim_rodada"
        atualizar_firebase()
        st.rerun()

# ETAPA 3: Fim da rodada de revelação
elif st.session_state.etapa == "fim_rodada":
    st.success("🎉 Todos já viram suas cartas! Discutam entre si para descobrir quem é" f" o impostor. (O impostor era: **{st.session_state.impostor}**)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Jogar Outra Rodada"):
            st.session_state.etapa = "sorteio"
            st.session_state.indice_atual = 0
            lista_ativa = categorias[st.session_state.categoria_escolhida]
            st.session_state.carta_secreta = random.choice(lista_ativa)
            st.session_state.impostor = random.choice(st.session_state.jogadores)
            atualizar_firebase()
            st.rerun()
    with col2:
        if st.button("Trocar Categoria / Reiniciar"):
            st.session_state.etapa = "menu"
            atualizar_firebase()
            st.rerun()
