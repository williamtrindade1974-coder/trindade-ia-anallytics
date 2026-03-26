import pandas as pd
import streamlit as st

st.set_page_config(page_title="TRINDADE IA ANALYTICS", layout="wide")

st.title("🚀 TRINDADE IA ANALYTICS")
st.caption("Dashboard Inteligente de Produtividade")

arquivo = st.file_uploader("📂 Envie sua planilha", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.subheader("📊 Dados carregados")
    st.dataframe(df)

    # Detectar colunas automaticamente
    def find_col(possiveis):
        for col in df.columns:
            for p in possiveis:
                if p.lower() in col.lower():
                    return col
        return None

    col_exec = find_col(["executado"])
    col_pend = find_col(["pendente"])
    col_improd = find_col(["improd"])
    col_tecnico = find_col(["tecnico"])
    col_prod = find_col(["prod"])

    st.divider()

    if col_exec and col_pend and col_improd:
        total_exec = df[col_exec].sum()
        total_pend = df[col_pend].sum()
        total_improd = df[col_improd].sum()

        eficiencia = (total_exec / (total_exec + total_pend + total_improd)) * 100

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("✅ Executado", total_exec)
        col2.metric("⏳ Pendente", total_pend)
        col3.metric("⚠️ Improdutivo", total_improd)
        col4.metric("📈 Eficiência", f"{eficiencia:.1f}%")

        st.divider()

        st.subheader("📊 Distribuição")
        chart_data = pd.DataFrame({
            "Categoria": ["Executado", "Pendente", "Improdutivo"],
            "Valores": [total_exec, total_pend, total_improd]
        }).set_index("Categoria")

        st.bar_chart(chart_data)

    else:
        st.warning("⚠️ Não consegui identificar todas as colunas principais")

    # Ranking
    if col_tecnico and col_prod:
        st.divider()
        st.subheader("🏆 Ranking de Técnicos")

        ranking = df.groupby(col_tecnico)[col_prod].sum().sort_values(ascending=False)

        st.bar_chart(ranking)

        st.success("🔥 Destaque: " + str(ranking.index[0]))
