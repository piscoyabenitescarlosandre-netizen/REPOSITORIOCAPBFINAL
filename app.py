import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bank Marketing EDA", layout="wide")

# ==============================
# CLASE (POO)
# ==============================
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def numeric_cols(self):
        return self.df.select_dtypes(include='number').columns

    def categorical_cols(self):
        return self.df.select_dtypes(exclude='number').columns

    def summary(self):
        return self.df.describe()

    def missing(self):
        return self.df.isnull().sum()


# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("📊 Menú")
menu = st.sidebar.selectbox(
    "Navegación",
    ["Home", "Carga de Datos", "EDA", "Conclusiones"]
)

# ==============================
# HOME
# ==============================
if menu == "Home":
    st.title("📊 Bank Marketing Analysis")

    st.markdown("""
    ## 🎯 Objetivo
    Analizar los factores que influyen en la aceptación de campañas de marketing bancario.

    ## 👤 Autor
    Carlos Piscoya  

    ## 🛠 Tecnologías
    Python, Pandas, Streamlit, Seaborn

    ## 📁 Dataset
    Información de clientes y campañas bancarias.
    """)

# ==============================
# CARGA
# ==============================
elif menu == "Carga de Datos":

    st.title("📂 Carga del Dataset")
    file = st.file_uploader("Sube tu CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.session_state["df"] = df

        st.success("Archivo cargado ✅")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Vista previa")
            st.dataframe(df.head())

        with col2:
            st.subheader("Dimensiones")
            st.write(f"Filas: {df.shape[0]}")
            st.write(f"Columnas: {df.shape[1]}")

    else:
        st.warning("Sube un archivo para continuar")

# ==============================
# EDA
# ==============================
elif menu == "EDA":

    st.title("📊 Análisis Exploratorio")

    if "df" not in st.session_state:
        st.warning("Primero carga el dataset")
    else:
        df = st.session_state["df"]
        analyzer = DataAnalyzer(df)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📌 Info",
            "📊 Numéricas",
            "📊 Categóricas",
            "📈 Bivariado",
            "🎛 Dinámico",
            "🔍 Insights"
        ])

        # INFO
        with tab1:
            st.write(df.dtypes)
            st.write(analyzer.missing())
            st.write(analyzer.summary())

        # NUMERICAS
        with tab2:
            col = st.selectbox("Variable numérica", analyzer.numeric_cols())
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

            if st.checkbox("Ver correlación"):
                fig, ax = plt.subplots()
                sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        # CATEGORICAS
        with tab3:
            col = st.selectbox("Variable categórica", analyzer.categorical_cols())
            counts = df[col].value_counts()
            st.write(counts)

            fig, ax = plt.subplots()
            counts.plot(kind='bar', ax=ax)
            st.pyplot(fig)

        # BIVARIADO
        with tab4:
            tipo = st.radio("Tipo", ["Num vs Cat", "Cat vs Cat"])

            if tipo == "Num vs Cat":
                num = st.selectbox("Num", analyzer.numeric_cols())
                cat = st.selectbox("Cat", analyzer.categorical_cols())

                fig, ax = plt.subplots()
                sns.boxplot(x=df[cat], y=df[num], ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            else:
                cat1 = st.selectbox("Cat1", analyzer.categorical_cols())
                cat2 = st.selectbox("Cat2", analyzer.categorical_cols())

                cross = pd.crosstab(df[cat1], df[cat2])
                st.write(cross)
                st.bar_chart(cross)

        # DINAMICO
        with tab5:
            col = st.selectbox("Columna", df.columns)

            if df[col].dtype == "object":
                st.bar_chart(df[col].value_counts())
            else:
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax)
                st.pyplot(fig)

        # INSIGHTS
        with tab6:
            st.subheader("🔍 Insights automáticos")

            if "y" in df.columns:
                st.write("📊 Tasa de conversión")
                st.write(df["y"].value_counts(normalize=True) * 100)

                if "duration" in df.columns:
                    st.write("⏱ Duración vs resultado")
                    st.write(df.groupby("y")["duration"].mean())

                if "contact" in df.columns:
                    st.write("📞 Contacto vs conversión")
                    st.write(pd.crosstab(df["contact"], df["y"], normalize="index") * 100)

# ==============================
# CONCLUSIONES
# ==============================
elif menu == "Conclusiones":

    st.title("📌 Conclusiones")

    st.markdown("""
    1. La duración de la llamada influye directamente en la conversión.
    2. El canal de contacto impacta significativamente los resultados.
    3. La tasa de conversión es baja, confirmando el problema del negocio.
    4. Existen segmentos de clientes con mayor probabilidad de aceptación.
    5. Se recomienda optimizar la segmentación y estrategia de contacto.
    """)
