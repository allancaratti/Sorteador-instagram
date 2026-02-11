import streamlit as st
import instaloader
import pandas as pd
from PIL import Image
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sorteador DivineTech", layout="wide")

# --- MEMÓRIA DO STREAMLIT (Session State) ---
if "df_participantes" not in st.session_state:
    st.session_state.df_participantes = None

# --- CABEÇALHO COM LOGOTIPO ---
col1, col2 = st.columns([1, 5])

with col1:
    path_logo = os.path.join("images", "logo_divine.png")
    if os.path.exists(path_logo):
        logo = Image.open(path_logo)
        st.image(logo, width=120)

with col2:
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="margin-bottom: 0;">Sorteador de Instagram By DivineTech Solutions</h1>
            <h2 style="font-size: 1.2rem; color: #555; margin-top: 0;">Sorteie ganhadores através de comentários do Instagram</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("Configurações de Acesso")
modo_logado = st.sidebar.checkbox("Realizar coleta logado")
usuario_insta = st.sidebar.text_input("Usuário:", value="") if modo_logado else ""
senha_insta = st.sidebar.text_input("Senha:", type="password") if modo_logado else ""

# --- INTERFACE PRINCIPAL ---
url_post = st.text_input("URL da postagem pública:")
remover_duplicados = st.checkbox("Remover usuários duplicados")

if st.button("🚀 Iniciar Captura"):
    if not url_post:
        st.warning("Insira a URL.")
    else:
        try:
            L = instaloader.Instaloader()
            if modo_logado:
                L.login(usuario_insta, senha_insta)
            
            shortcode = url_post.split("/")[-2] if url_post.endswith("/") else url_post.split("/")[-1]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            lista = []
            with st.spinner("Coletando..."):
                for comment in post.get_comments():
                    lista.append({"Usuario": comment.owner.username, "Comentario": comment.text})
                
                df = pd.DataFrame(lista)
                if not df.empty:
                    if remover_duplicados:
                        df = df.drop_duplicates(subset=['Usuario'])
                    
                    df = df.reset_index(drop=True)
                    df.index = df.index + 1
                    df.index.name = "Número da sorte"
                    
                    # SALVA NA MEMÓRIA
                    st.session_state.df_participantes = df
                else:
                    st.error("Nenhum comentário encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")

# --- SEÇÃO DE RESULTADOS (SÓ APARECE SE TIVER DADOS NA MEMÓRIA) ---
if st.session_state.df_participantes is not None:
    df = st.session_state.df_participantes
    st.success(f"Captura concluída! {len(df)} participantes prontos.")
    st.dataframe(df, use_container_width=True)

    col_sorteio, col_download = st.columns(2)

    with col_sorteio:
        if st.button("🎰 Sortear Vencedor"):
            ganhador = df.sample(1)
            st.balloons()
            st.info(f"🏆 O VENCEDOR É O NÚMERO **{ganhador.index[0]}**: @{ganhador['Usuario'].values[0]}")

    with col_download:
        nome_arq = "participantes.xlsx"
        df.to_excel(nome_arq, index=True)
        with open(nome_arq, "rb") as f:
            st.download_button("📥 Baixar Planilha", f, file_name=nome_arq)