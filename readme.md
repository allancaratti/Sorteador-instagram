# 📸 Sorteador de Instagram By DivineTech Solutions

Script em **Python** com interface **Streamlit** para extração de comentários e realização de sorteios automatizados no Instagram.  
Permite a coleta de dados de postagens públicas, exportação para **Excel** com numeração personalizada ("Número da sorte") e sorteio aleatório com efeitos visuais.

---

## 🚀 Funcionalidades
- **Modo Híbrido de Coleta**: Opção de captura anônima (rápida) ou logada (para grandes volumes).
- **Tratamento de Dados**: Filtro opcional para remover usuários duplicados (um comentário por pessoa).
- **Numeração Automática**: Gera a coluna "Número da sorte" iniciando em 1 para facilitar auditoria.
- **Sorteio Instantâneo**: Botão dedicado para escolher um vencedor aleatório com animação de balões.
- **Exportação**: Gera planilha Excel (.xlsx) pronta para conferência manual ou registro.
- **Resiliência**: Tratamento de limites do Instagram (Rate Limit) com salvamento parcial do que foi capturado.

---

## 🧰 Requisitos
- **Python 3.13.x**
- Bibliotecas:
  - `streamlit`
  - `instaloader`
  - `pandas`
  - `openpyxl`
  - `Pillow` (PIL)

---

## 📂 Estrutura do Projeto
1. **Interface**: Dashboard visual construído em Streamlit com identidade visual DivineTech.
2. **Autenticação**: Gerenciamento de sessão local para evitar bloqueios de login recorrentes.
3. **Extração**: Web scraping via Instaloader respeitando intervalos de segurança (*delays*).
4. **Memória de Sessão**: Uso de `session_state` para garantir que os dados não sejam perdidos ao clicar em botões.

---

## ▶️ Uso
1. Certifique-se de que seu logotipo está em: `\images\logo_divine.png`.

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o aplicativo:
    ```bash
    python -m streamlit run app.py
    ```

4. No navegador:
    - Insira a **URL** da postagem.
    - Escolha se deseja fazer o login (para posts com muitos comentários).
    - Clique em **Iniciar Captura**.
    - Após carregar a tabela, utilize o botão **Sortear Vencedor**.

---

## 📑 Colunas Geradas
Ao exportar para Excel, os seguintes campos são registrados:
- **Número da sorte**: ID único sequencial para o sorteio.
- **Usuário**: @handle do participante.
- **Comentário**: Texto escrito na postagem.
- **Data**: Carimbo de data/hora do comentário.

## ⚠️ Notas Importantes
- O Instagram pode aplicar bloqueios temporários de IP se houver excesso de requisições. 
- Para sorteios em perfis privados, o modo logado é obrigatório e deve ser feito com uma conta que segue o perfil.
- Este script é uma ferramenta de automação para facilitar processos de marketing técnico.

## 👨‍💻 Autor
Desenvolvido por **Allan Mauad | DivineTech Solutions** 🔗 LinkedIn: [linkedin.com/in/allancaratti](https://linkedin.com/in/allancaratti)

## 📜 Licença
Este projeto está sob Licença Proprietária.  
O uso, modificação ou distribuição sem autorização expressa do autor é proibido.