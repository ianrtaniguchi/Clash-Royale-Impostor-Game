import random
import json
import string
import time
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO E INICIALIZAÇÃO DO FIREBASE
# ==========================================
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(
        cred,
        {"databaseURL": "https://impostor-multiplayer-1f7f7-default-rtdb.firebaseio.com/"},
    )

# Dicionário de Categorias (Resumido aqui, você pode colar o seu completo!)
categorias = {"Clash Royale": ["P.E.K.K.A", "Mago", "Corredor", "Tronco", "Megacavaleiro", "Princesa", "Valquíria"], "Comidas": ["Pizza", "Hambúrguer", "Sushi", "Churrasco", "Lasanha"], "Filmes": ["Vingadores", "Harry Potter", "Senhor dos Anéis", "Matrix", "Sonic 3"]}

# ==========================================
# 2. VARIÁVEIS DE SESSÃO LOCAL (MEU CELULAR)
# ==========================================
if "meu_nome" not in st.session_state:
    st.session_state.meu_nome = ""
if "codigo_sala" not in st.session_state:
    st.session_state.codigo_sala = None
if "is_host" not in st.session_state:
    st.session_state.is_host = False

st.title("🕵️‍♂️ Impostor - Multiplayer")


# ==========================================
# 3. FUNÇÕES AUXILIARES
# ==========================================
def gerar_codigo_sala():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=4))


# ==========================================
# 4. TELA INICIAL (CRIAR OU ENTRAR)
# ==========================================
if not st.session_state.codigo_sala:
    st.subheader("Bem-vindo! Identifique-se:")
    nome_input = st.text_input("Seu Nome:", max_chars=15)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Criar Nova Sala")
        categoria_escolhida = st.selectbox("Categoria:", list(categorias.keys()))
        if st.button("Criar Sala"):
            if nome_input.strip():
                codigo = gerar_codigo_sala()
                # Cria a sala no Firebase
                ref_sala = db.reference(f"salas/{codigo}")
                ref_sala.set({"status": "lobby", "categoria": categoria_escolhida, "host": nome_input, "jogadores": [nome_input.strip()], "impostor": "", "carta_secreta": ""})
                st.session_state.meu_nome = nome_input.strip()
                st.session_state.codigo_sala = codigo
                st.session_state.is_host = True
                st.rerun()
            else:
                st.error("Digite seu nome primeiro!")

    with col2:
        st.markdown("### Entrar em uma Sala")
        codigo_input = st.text_input("Código da Sala:").upper()
        if st.button("Entrar"):
            if nome_input.strip() and codigo_input:
                ref_sala = db.reference(f"salas/{codigo_input}")
                dados = ref_sala.get()

                if dados:
                    if dados["status"] == "lobby":
                        # Adiciona jogador na lista
                        jogadores_atuais = dados.get("jogadores", [])
                        if nome_input.strip() not in jogadores_atuais:
                            jogadores_atuais.append(nome_input.strip())
                            ref_sala.child("jogadores").set(jogadores_atuais)

                        st.session_state.meu_nome = nome_input.strip()
                        st.session_state.codigo_sala = codigo_input
                        st.session_state.is_host = False
                        st.rerun()
                    else:
                        st.error("Esta partida já começou!")
                else:
                    st.error("Sala não encontrada!")
            else:
                st.error("Preencha seu nome e o código da sala!")

# ==========================================
# 5. DENTRO DA SALA (LOBBY OU JOGO)
# ==========================================
else:
    # Puxa os dados atuais da sala no Firebase em tempo real
    ref_sala = db.reference(f"salas/{st.session_state.codigo_sala}")
    dados_sala = ref_sala.get()

    # Se a sala foi apagada (ex: host saiu)
    if not dados_sala:
        st.warning("A sala foi encerrada.")
        if st.button("Voltar ao Menu"):
            st.session_state.codigo_sala = None
            st.rerun()
        st.stop()

    status = dados_sala.get("status")
    jogadores = dados_sala.get("jogadores", [])

    st.success(f"Você está na sala: **{st.session_state.codigo_sala}** | Tema: {dados_sala.get('categoria')}")
    st.write(f"👤 Jogador: **{st.session_state.meu_nome}** {'(Dono da Sala 👑)' if st.session_state.is_host else ''}")

    # --- TELA DE LOBBY (AGUARDANDO) ---
    if status == "lobby":
        st.info("Aguardando os outros jogadores entrarem...")
        st.write("### Jogadores na sala:")
        for jog in jogadores:
            st.write(f"- {jog}")

        if st.session_state.is_host:
            if st.button("▶️ Iniciar Partida"):
                if len(jogadores) >= 3:
                    # Sorteia carta e impostor
                    lista_ativa = categorias[dados_sala["categoria"]]
                    carta_sorteada = random.choice(lista_ativa)
                    impostor_sorteado = random.choice(jogadores)

                    # Atualiza o Firebase para iniciar para todo mundo
                    ref_sala.update({"status": "jogando", "carta_secreta": carta_sorteada, "impostor": impostor_sorteado})
                    st.rerun()
                else:
                    st.error("É necessário pelo menos 3 jogadores para iniciar!")

    # --- TELA DO JOGO (PARTIDA INICIADA) ---
    elif status == "jogando":
        st.markdown("### A Partida Começou!")

        # Botão para revelar a carta apenas para quem estiver segurando este celular
        with st.expander("👀 CLIQUE AQUI PARA VER SUA CARTA", expanded=False):
            if st.session_state.meu_nome == dados_sala["impostor"]:
                st.error("🚨 VOCÊ É O IMPOSTOR! 🚨\n\nTente disfarçar e adivinhar a palavra!")
            else:
                st.success(f"A palavra secreta é:\n\n# {dados_sala['carta_secreta']}")

        st.write("Discutam entre si para descobrir quem é o impostor!")

        if st.session_state.is_host:
            st.markdown("---")
            if st.button("🔄 Jogar Nova Rodada"):
                ref_sala.update({"status": "lobby", "carta_secreta": "", "impostor": ""})
                st.rerun()

    # Botão de Sair da Sala
    st.markdown("---")
    if st.button("Sair da Sala"):
        # Se for o host, destrói a sala. Se for jogador, apenas sai da lista.
        if st.session_state.is_host:
            ref_sala.delete()
        else:
            if st.session_state.meu_nome in jogadores:
                jogadores.remove(st.session_state.meu_nome)
                ref_sala.child("jogadores").set(jogadores)
        st.session_state.codigo_sala = None
        st.session_state.is_host = False
        st.rerun()

    # O "Motor" do Multiplayer: Atualiza a tela automaticamente a cada 2 segundos
    # para sincronizar quem entrou na sala ou se o jogo começou.
    time.sleep(2)
    st.rerun()
