import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="TRINDADE IA ANALYTICS", layout="wide")

st.title("🚀 TRINDADE IA ANALYTICS")
st.caption("IA de Análise Operacional")

# IA
client = None
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    pass

arquivo = st.file_uploader("📂 Envie sua planilha", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.subheader("📊 Dados")
    st.dataframe(df)

    # KPIs simples
    total = df.select_dtypes(include='number').sum().sum()
    st.metric("📊 Total geral", total)

    st.divider()

    # IA
    st.subheader("🤖 Assistente Inteligente")

    pergunta = st.text_input("Faça uma pergunta sobre os dados:")

    if pergunta:
        if client:
            contexto = df.head(50).to_string()

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um analista de dados especialista em produtividade operacional."},
                    {"role": "user", "content": f"Dados:\n{contexto}\n\nPergunta: {pergunta}"}
                ]
            )

            st.success(resposta.choices[0].message.content)

        else:
            st.warning("⚠️ IA não configurada ainda (precisa da API)")
