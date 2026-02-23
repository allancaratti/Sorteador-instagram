import streamlit as st
import instaloader
import pandas as pd
from PIL import Image
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sorteador DivineTech", layout="wide")

# --- MEMÓRIA DO STREAMLIT ---
if "df_participantes" not in st.session_state:
    st.session_state.df_participantes = None

# --- CABEÇALHO ---
col1, col2 = st.columns([1, 5])
with col1:
    path_logo = os.path.join("images", "logo_divine.png")
    if os.path.exists(path_logo):
        st.image(Image.open(path_logo), width=120)

with col2:
    st.markdown("<div style='text-align: center;'><h1 style='margin-bottom: 0;'>Sorteador de Instagram By DivineTech Solutions</h1></div>", unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR ADAPTADA ---
st.sidebar.header("Configurações de Acesso")
usuario_insta = st.sidebar.text_input("Seu Usuário Instagram:", value="")
st.sidebar.info("O sistema tentará usar a sessão salva no seu computador para evitar bloqueios.")

# --- INTERFACE PRINCIPAL ---
url_post = st.text_input("URL da postagem pública:")
remover_duplicados = st.checkbox("Remover usuários duplicados", value=True)

if st.button("🚀 Iniciar Captura"):
    if not url_post or not usuario_insta:
        st.warning("Preencha a URL e o Usuário.")
    else:
        try:
            L = instaloader.Instaloader()
            
            # TENTA CARREGAR SESSÃO DO PC (Bypass de Bloqueio)
            try:
                L.load_session_from_file(usuario_insta)
                st.sidebar.success("Sessão carregada com sucesso!")
            except FileNotFoundError:
                st.sidebar.warning("Sessão local não encontrada. Rode o comando de login no terminal primeiro.")
                st.stop()

            # EXTRAÇÃO
            shortcode = url_post.split("/")[-2] if url_post.endswith("/") else url_post.split("/")[-1]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            lista = []
            container_progresso = st.empty()
            
            with st.spinner("Coletando comentários..."):
                for comment in post.get_comments():
                    lista.append({"Usuario": comment.owner.username, "Comentario": comment.text})
                    container_progresso.write(f"Participantes coletados: {len(lista)}")
                    # Pequena pausa para não ser bloqueado novamente
                    time.sleep(2.5) 
                
                df = pd.DataFrame(lista)
                if not df.empty:
                    if remover_duplicados:
                        df = df.drop_duplicates(subset=['Usuario'])
                    
                    df = df.reset_index(drop=True)
                    df.index = df.index + 1
                    df.index.name = "Número da sorte"
                    st.session_state.df_participantes = df
                else:
                    st.error("Nenhum comentário encontrado.")
                    
        except Exception as e:
            st.error(f"Erro do Instagram: {e}")

# --- SEÇÃO DE RESULTADOS ---
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
        pasta_data = "data"
        if not os.path.exists(pasta_data): os.makedirs(pasta_data)
        
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        nome_arq = f"participantes_{timestamp}.xlsx"
        caminho_completo = os.path.join(pasta_data, nome_arq)
        
        df.to_excel(caminho_completo, index=True)
        with open(caminho_completo, "rb") as f:
            st.download_button("📥 Baixar Planilha", f, file_name=nome_arq)