import pandas as pd
import streamlit as st

st.title("🚀 TRINDADE IA ANALYTICS")

arquivo = st.file_uploader("📂 Envie sua planilha", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.write("📊 Colunas da planilha:")
    st.write(df.columns)

    st.dataframe(df)

    # Tentativa segura
    try:
        total = df.select_dtypes(include='number').sum().sum()
        st.success(f"📊 Soma total dos dados numéricos: {total}")
    except:
        st.warning("Não foi possível calcular automaticamente")
