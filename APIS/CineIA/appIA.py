import streamlit as st
import google.generativeai as genai

#Configuração da pagina
st.set_page_config(page_title="CineIA", page_icon="🎬")

#Confituração da API
CHAVE_API="CHAVE"
genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel('gemini-2.5-flash')

#INTERFACE
st.title("🎬 CineIA: Seu Próximo Filme")
st.markdown("Descubra Filmes baseados nos seus gostos pessoais e como você esta se sentindo.")

with st.sidebar:
    st.header("Preferências")
    genero = st.multiselect(
    "Gêneros favoritos:",
    ["Ação", "Drama", "Sci-Fi", "Comédia", "Terror", "Documentário"]
    )
    tempo = st.slider("Duração máxima (minutos):", 60, 240, 120)

 # Text area movido para a barra lateral para organizar melhor o layout,
    mood = st.text_area(
    "Descreva como você está se sentindo ou o que busca no filme:",
    placeholder="Ex: Quero um filme de ficção científica com reviravoltas na história."
    )

    botao_recomendar = st.button("Buscar Recomendações")

#Logica de Processamento
if botao_recomendar:
    if not mood:
        st.warning("Por favor, descreva o que você deseja assistir!")
    else:
        with st.spinner("Analisanod catálogo cinematografico..."):
            #Tratamento de generos caso o usuario não selecione nenhum
            generos_str=','.join(genero) if genero else 'qualquer gênero'

            prompt = f"""
            Você é um especialista em cinema.
            Recomende filmes para alguém que gosta de {generos_str} e que durem até {tempo} minutos.
            O usuário descreveu o clima do filme como: '{mood}'.
            Para cada filme, forneça: Título, Ano e uma frase curta do porquê combina com o pedido.
            """

            try:
                response=model.generate_content(prompt)
                st.success("Aqui estão minhas sugestões:")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao conecar com a IA: {e}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Gostei 👍"):
        with open("feedback.csv", "a", encoding="utf-8") as f:
            f.write(f"{mood},{genero},{tempo},Gostei\n")
        st.success("Obrigado pelo seu feedback positivo!")

with col2:
    if st.button("Não gostei 👎"):
        with open("feedback.csv", "a", encoding="utf-8") as f:
            f.write(f"{mood},{genero},{tempo},Não gostei\n")
        st.info("Feedback registrado. Vamos melhorar!")
        st.markdown("---")

    #Rodapé
    st.markdown("---")
    st.caption("Desenvolvido na disciplina Projeto de Banco de Dados - Sistemas de Informação - Universidade Franciscana(UFN)")
