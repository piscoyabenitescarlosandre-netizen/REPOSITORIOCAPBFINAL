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

    def value_counts(self, col):
        return self.df[col].value_counts()


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
    Analizar los factores que influyen en la aceptación de campañas de marketing.

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

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📌 Info",
            "📊 Numéricas",
            "📊 Categóricas",
            "📈 Bivariado",
            "🎛 Dinámico"
        ])

        # --------------------------
        # TAB 1
        # --------------------------
        with tab1:
            st.subheader("Información General")

            st.write("Tipos de datos:")
            st.write(df.dtypes)

            st.write("Valores nulos:")
            st.write(analyzer.missing())

            st.write("Estadísticas:")
            st.write(analyzer.summary())

        # --------------------------
        # TAB 2 NUMERICAS
        # --------------------------
        with tab2:
            st.subheader("Distribución Numérica")

            num_cols = analyzer.numeric_cols()
            col = st.selectbox("Selecciona variable", num_cols)

            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        # --------------------------
        # TAB 3 CATEGORICAS
        # --------------------------
        with tab3:
            st.subheader("Variables Categóricas")

            cat_cols = analyzer.categorical_cols()
            col = st.selectbox("Selecciona categórica", cat_cols)

            counts = df[col].value_counts()

            st.write(counts)

            fig, ax = plt.subplots()
            counts.plot(kind='bar', ax=ax)
            st.pyplot(fig)

        # --------------------------
        # TAB 4 BIVARIADO
        # --------------------------
        with tab4:
            st.subheader("Análisis Bivariado")

            num_cols = analyzer.numeric_cols()
            cat_cols = analyzer.categorical_cols()

            tipo = st.radio("Tipo de análisis", [
                "Numérico vs Categórico",
                "Categórico vs Categórico"
            ])

            if tipo == "Numérico vs Categórico":
                num = st.selectbox("Variable numérica", num_cols)
                cat = st.selectbox("Variable categórica", cat_cols)

                fig, ax = plt.subplots()
                sns.boxplot(x=df[cat], y=df[num], ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            else:
                cat1 = st.selectbox("Variable 1", cat_cols)
                cat2 = st.selectbox("Variable 2", cat_cols)

                cross = pd.crosstab(df[cat1], df[cat2])
                st.write(cross)

                st.bar_chart(cross)

        # --------------------------
        # TAB 5 DINAMICO
        # --------------------------
        with tab5:
            st.subheader("Análisis Dinámico")

            col = st.selectbox("Selecciona columna", df.columns)

            if df[col].dtype == "object":
                st.bar_chart(df[col].value_counts())
            else:
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax)
                st.pyplot(fig)

# ==============================
# CONCLUSIONES
# ==============================
elif menu == "Conclusiones":

    st.title("📌 Conclusiones")

    st.markdown("""
    1. La duración de la llamada influye fuertemente en la aceptación.
    2. Clientes sin créditos activos tienen mayor probabilidad de conversión.
    3. Algunos canales de contacto son más efectivos que otros.
    4. Variables económicas muestran impacto en la decisión del cliente.
    5. Segmentos específicos de clientes presentan mayor tasa de aceptación.

    💡 Recomendación:
    Optimizar estrategias de contacto y segmentación de clientes.
    """)
