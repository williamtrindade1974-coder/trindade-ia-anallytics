import pandas as pd
import streamlit as st

st.set_page_config(page_title="TRINDADE IA ANALYTICS", layout="wide")

st.title("🚀 TRINDADE IA ANALYTICS")

arquivo = st.file_uploader("Envie sua planilha", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.write("📊 Colunas detectadas:")
    st.write(df.columns)

    st.divider()

    # Tenta detectar colunas automaticamente
    def find_col(possiveis):
        for col in df.columns:
            for p in possiveis:
                if p.lower() in col.lower():
                    return col
        return None

    col_exec = find_col(["executado"])
    col_pend = find_col(["pendente"])
    col_improd = find_col(["improdutivo"])
    col_tecnico = find_col(["tecnico"])
    col_prod = find_col(["prod"])

    if not col_exec or not col_pend or not col_improd:
        st.error("❌ Não consegui identificar as colunas principais")
    else:
        total_exec = df[col_exec].sum()
        total_pend = df[col_pend].sum()
        total_improd = df[col_improd].sum()

        eficiencia = (total_exec / (total_exec + total_pend + total_improd)) * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Executado", total_exec)
        col2.metric("Pendente", total_pend)
        col3.metric("Improdutivo", total_improd)
        col4.metric("Eficiência", f"{eficiencia:.1f}%")

        if col_tecnico and col_prod:
            ranking = df.groupby(col_tecnico)[col_prod].sum().sort_values(ascending=False)
            st.subheader("🏆 Ranking")
            st.bar_chart(ranking)

    st.dataframe(df)
