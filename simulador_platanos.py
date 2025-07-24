# Se mantuvieron los imports originales y se agregaron los necesarios
import streamlit as st
import random
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
import base64

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

# Exportar DataFrame a Excel descargable
def exportar_excel(df, filename="reporte.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
        workbook = writer.book
        worksheet = writer.sheets['Resultados']
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Descargar Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

# Agregado contenido para opción Manual
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
        exportar_excel(df_manual, filename="manual_resultado.xlsx")








