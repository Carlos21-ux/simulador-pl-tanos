# Se mantuvieron los imports originales y se agregaron los necesarios
import streamlit as st
import random
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime

# Imagen principal
image = Image.open("platano1.png")
st.image(image, use_container_width=False, width=300)

st.title("🌿 Simulador de Plátanos")

with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["🔢 Manual", "🎲 Montecarlo", "🌱 Vigor de la Planta"])
    st.markdown("---")

# Función base para estimar plátanos
def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

# Exportar DataFrame a CSV descargable corregido (UTF-8 BOM + separador ;) para Excel

def exportar_csv(df, prefix="reporte"):
    output = BytesIO()
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.csv"
        df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Descargar CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error al exportar el archivo: {e}")

# Modificación puntual para ajustar límite de grosor y hojas, y bajar exigencia de salud
if opcion == "🌱 Vigor de la Planta":
    st.subheader("🌱 Evaluación del Vigor de la Planta")
    st.info("Aquí podrás ingresar las características de cada planta y analizar su vigor y salud.")

    if "plantas" not in st.session_state:
        st.session_state["plantas"] = []

    with st.form("vigor_form"):
        grosor = st.number_input("🌱 Grosor del tallo (cm)", min_value=1.0, max_value=50.0, value=30.0)
        altura_tallo = st.number_input("🌿 Altura del tallo (m)", min_value=0.5, max_value=6.0, value=2.5)
        hojas_sanas = st.number_input("🍃 Número de hojas sanas", min_value=0, max_value=50, value=10)
        altura_hijo = st.number_input("🌿 Altura del hijo (m)", min_value=0.0, max_value=4.0, value=1.5)

        col1, col2 = st.columns(2)
        agregar = col1.form_submit_button("➕ Agregar Planta")
        cancelar = col2.form_submit_button("❌ Cancelar")

        if agregar:
            st.session_state["plantas"].append({
                "Grosor": grosor,
                "AlturaTallo": altura_tallo,
                "HojasSanas": hojas_sanas,
                "AlturaHijo": altura_hijo
            })
            st.success("🌱 Planta agregada")

        if cancelar:
            st.session_state["plantas"] = []
            st.warning("🚫 Lista de plantas reiniciada")

    if st.session_state["plantas"]:
        if st.button("📊 Analizar Plantas"):
            resultados = []
            estados = {"Saludable": 0, "Regular": 0, "Débil": 0, "Crítica": 0}

            for idx, planta in enumerate(st.session_state["plantas"], 1):
                vigor = (
                    planta["Grosor"] * 0.4 +
                    planta["AlturaTallo"] * 10 +
                    planta["HojasSanas"] * 1 +
                    planta["AlturaHijo"] * 5
                )
                if vigor > 75:
                    estado = "Saludable"
                    emoji = "🟢"
                elif vigor > 55:
                    estado = "Regular"
                    emoji = "🟡"
                elif vigor > 35:
                    estado = "Débil"
                    emoji = "🟠"
                else:
                    estado = "Crítica"
                    emoji = "🔴"

                estados[estado] += 1
                resultados.append([idx, planta["Grosor"], planta["AlturaTallo"], planta["HojasSanas"], planta["AlturaHijo"], f"{emoji} {estado}"])

            df_vigor = pd.DataFrame(resultados, columns=["#", "Grosor", "Altura Tallo", "Hojas Sanas", "Altura Hijo", "Estado"])
            st.dataframe(df_vigor)

            fig = px.pie(
                names=list(estados.keys()),
                values=list(estados.values()),
                title="Distribución del Vigor de las Plantas",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig)
            exportar_csv(df_vigor, prefix="vigor_resultado")

            st.markdown("---")
            st.markdown("### 📋 Resumen de diagnóstico")
            for estado, cantidad in estados.items():
                st.markdown(f"**{estado}:** {cantidad} plantas")

