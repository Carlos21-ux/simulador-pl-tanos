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

# ---------- MANUAL ----------
if opcion == "🔢 Manual":
    st.subheader("Ingreso Manual de Planta")
    if "plantas_manual" not in st.session_state:
        st.session_state["plantas_manual"] = []

    pb = st.number_input("📏 Perímetro de la base (cm):", min_value=30.0, max_value=50.0, value=40.0)
    pm = st.number_input("📏 Perímetro medio (cm):", min_value=25.0, max_value=50.0, value=35.0)
    pa = st.number_input("📏 Perímetro alto (cm):", min_value=15.0, max_value=50.0, value=25.0)
    altura = st.number_input("📏 Altura total del tronco (m):", min_value=2.0, max_value=6.0, value=3.0)
    precio = st.number_input("💰 Precio por plátano (S/):", min_value=0.0, value=0.2)

    if st.button("➕ Agregar Planta"):
        estimado = calcular(pb, pm, pa, altura)
        ganancia = round(estimado * precio, 2)
        st.session_state["plantas_manual"].append([pb, pm, pa, altura, estimado, ganancia])
        st.success("🌿 Planta agregada correctamente")

    if st.session_state["plantas_manual"]:
        df_manual = pd.DataFrame(
            st.session_state["plantas_manual"],
            columns=["PB", "PM", "PA", "Altura", "🍌 Estimado", "💰 Ganancia"]
        )
        st.dataframe(df_manual)
        total_platanos = df_manual["🍌 Estimado"].sum()
        total_ganancia = df_manual["💰 Ganancia"].sum()
        st.success(f"🔢 Total plátanos: {total_platanos}")
        st.info(f"💰 Ganancia estimada: S/ {total_ganancia}")
        exportar_csv(df_manual, prefix="manual_resultado")

# ---------- MONTECARLO ----------
elif opcion == "🎲 Montecarlo":
    st.subheader("🎲 Simulación por Montecarlo")
    n = st.number_input("🌱 Número de plantas a simular:", min_value=1, value=10)
    precio = st.number_input("💰 Precio por plátano (S/):", min_value=0.0, value=0.2)

    if st.button("▶️ Ejecutar Simulación"):
        data = []
        total_platanos = 0

        for _ in range(n):
            pb = round(random.uniform(30, 50), 2)
            pm = round(random.uniform(25, 50), 2)
            pa = round(random.uniform(15, 50), 2)
            altura = round(random.uniform(2.0, 6.0), 2)
            estimado = calcular(pb, pm, pa, altura)
            total_platanos += estimado
            data.append([pb, pm, pa, altura, estimado])

        df = pd.DataFrame(data, columns=["PB", "PM", "PA", "Altura", "🍌 Estimación"])
        st.dataframe(df)

        ganancia = round(total_platanos * precio, 2)
        st.success(f"🔢 Total de plátanos estimados: {total_platanos}")
        st.info(f"💰 Ganancia estimada: S/ {ganancia}")

        df["💰 Ganancia"] = df["🍌 Estimación"] * precio
        exportar_csv(df, prefix="montecarlo_resultado")
















