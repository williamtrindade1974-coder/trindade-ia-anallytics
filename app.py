import pandas as pd
import streamlit as st

st.set_page_config(page_title="TRINDADE IA ANALYTICS", layout="wide")

st.title("🚀 TRINDADE IA ANALYTICS")
st.subheader("Dashboard Inteligente de Operações")

arquivo = st.file_uploader("📂 Envie sua planilha", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.divider()

    # Mostrar dados
    st.subheader("📊 Visualização dos Dados")
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
    col_improd = find_col(["improdutivo"])
    col_tecnico = find_col(["tecnico", "funcionario", "nome"])
    col_prod = find_col(["prod", "produção"])

    st.divider()

    # KPIs
    st.subheader("📈 Indicadores")

    if col_exec and col_pend and col_improd:
        total_exec = df[col_exec].sum()
        total_pend = df[col_pend].sum()
        total_improd = df[col_improd].sum()

        eficiencia = (total_exec / (total_exec + total_pend + total_improd)) * 100

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Executado", total_exec)
        c2.metric("Pendente", total_pend)
        c3.metric("Improdutivo", total_improd)
        c4.metric("Eficiência", f"{eficiencia:.1f}%")

    else:
        st.warning("⚠️ Não consegui identificar todas as colunas principais")

    st.divider()

    # Gráfico geral
    st.subheader("📊 Gráfico Geral")

    try:
        resumo = df.select_dtypes(include='number').sum()
        st.bar_chart(resumo)
    except:
        st.warning("Não foi possível gerar gráfico")

    # Ranking
    if col_tecnico and col_prod:
        st.divider()
        st.subheader("🏆 Ranking de Técnicos")

        ranking = df.groupby(col_tecnico)[col_prod].sum().sort_values(ascending=False)
        st.bar_chart(ranking)

        melhor = ranking.idxmax()
        pior = ranking.idxmin()

        st.success(f"🥇 Melhor desempenho: {melhor}")
        st.error(f"⚠️ Pior desempenho: {pior}")

    st.divider()

    # Insight automático
    st.subheader("🧠 Insight Inteligente")

    try:
        if total_improd > total_exec:
            st.error("Alerta: improdutividade maior que execução!")
        elif eficiencia > 80:
            st.success("Operação com alta performance 🚀")
        else:
            st.warning("Há oportunidades de melhoria na operação")
    except:
        st.info("Envie uma planilha completa para insights")
