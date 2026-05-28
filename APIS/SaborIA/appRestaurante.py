import streamlit as st
import google.generativeai as genai
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SaborIA", page_icon="🍽️", layout="centered")

# Substitua pela sua chave real
CHAVE_API = "CHAVE" 
genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel('gemini-3.5-flash')

# --- INTERFACE ---
st.title("🍽️ SaborIA: Onde Comer Hoje?")
st.markdown("Descubra os melhores restaurantes na sua cidade!")

with st.sidebar:
    st.header("Suas Preferências")
    cidade = st.text_input("Qual a sua cidade?", value="Santa Maria - RS")
    
    culinaria = st.multiselect(
        "Tipos de culinária:",
        ["Brasileira", "Italiana", "Japonesa", "Lanches/Burgers", "Pizza", "Saudável/Vegana", "Doces/Café"]
    )
    
    orcamento = st.slider("Orçamento máximo por pessoa (R$):", 20, 200, 80)

    mood = st.text_area(
        "Descreva o clima do local ou a comida:",
        placeholder="Ex: Lugar animado para ir com amigos comer um hambúrguer."
    )

    botao_recomendar = st.button("Buscar Restaurantes")

# --- LÓGICA DE PROCESSAMENTO ---
if botao_recomendar:
    if not mood or not cidade:
        st.warning("Por favor, preencha sua cidade e o que você deseja comer!")
    else:
        with st.spinner(f"Buscando restaurantes reais em {cidade}..."):
            
            culinaria_str = ', '.join(culinaria) if culinaria else 'qualquer tipo de comida'

            # Prompt ajustado: removido termo_imagem e adicionado campo emoji
            prompt = f"""
           Você é um guia gastronômico estritamente factual.
            Liste até 3 restaurantes REAIS e famosos que realmente existem na cidade de {cidade} para alguém que gosta de {culinaria_str}.
            O clima desejado é: '{mood}'. Orçamento máximo: R$ {orcamento}.
            
            REGRA VITAL 1: NÃO INVENTE NOMES. Só recomende locais que você tem certeza absoluta que existem em {cidade}.
            REGRA VITAL 2: Se você não tiver certeza ou não encontrar locais na região, retorne um restaurante com o nome "Nenhuma opção segura encontrada", explique o motivo na área "motivo" e use o emoji ⚠️.
            
            Retorne EXCLUSIVAMENTE um array JSON válido, sem texto antes ou depois, neste exato formato:
            [
              {{
                "nome": "Nome do Restaurante",
                "prato": "Sugestão de prato",
                "motivo": "Por que combina (1 frase)",
                "emoji": "Um único emoji (ex: 🍔, 🍣, 🍕, ou ⚠️)"
              }}
            ]
            """

            try:
                response = model.generate_content(prompt)
                
                # Tratamento para limpar a resposta e extrair apenas o JSON
                texto_resposta = response.text.strip()
                if texto_resposta.startswith("```json"):
                    texto_resposta = texto_resposta[7:]
                if texto_resposta.endswith("```"):
                    texto_resposta = texto_resposta[:-3]
                    
                restaurantes = json.loads(texto_resposta)
                
                st.success("Encontrei estas opções deliciosas:")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Renderização do Layout em Blocos apenas com Emoji e Texto
                for rest in restaurantes:
                    with st.container(border=True):
                        st.subheader(f"{rest.get('emoji', '🍽️')} {rest['nome']}")
                        st.write(f"🍲 **Prato:** {rest['prato']}")
                        st.write(f"💡 **Por que ir:** {rest['motivo']}")
                            
            except json.JSONDecodeError:
                st.error("A IA teve dificuldade em formatar os dados. Por favor, clique em buscar novamente!")
            except Exception as e:
                st.error(f"Erro ao conectar: {e}")

# --- SISTEMA DE FEEDBACK ---
st.markdown("---")
st.write("O que achou das recomendações?")
col1, col2 = st.columns(2)

with col1:
    if st.button("Gostei 👍", use_container_width=True):
        st.success("Feedback salvo!")

with col2:
    if st.button("Não gostei 👎", use_container_width=True):
        st.info("Vamos melhorar!")