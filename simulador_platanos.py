# Se mantuvieron los imports originales y se agregaron los necesarios
import streamlit as st
import random
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import base64

# Imagen principal
image = Image.open("platano1.png")
st.image(image, use_container_width=False, width=300)

st.title("Simulador de Platanos")

with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["Manual", "Montecarlo", "Vigor de la Planta"])
    st.markdown("---")

# Función base para estimar plátanos
def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

# Eliminar tildes y emojis para PDF
def limpiar_texto(texto):
    return (
        str(texto)
        .replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        .encode("latin-1", "ignore").decode("latin-1")
    )

# Generar PDF de forma segura en Streamlit
def generar_pdf(df, total=None, ganancia=None, filename="reporte.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for col in df.columns:
        pdf.cell(40, 10, limpiar_texto(col), border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for val in row:
            pdf.cell(40, 10, limpiar_texto(val), border=1)
        pdf.ln()

    if total is not None:
        pdf.ln()
        pdf.cell(200, 10, f"Total estimado: {total} platanos", ln=True)
    if ganancia is not None:
        pdf.cell(200, 10, f"Ganancia estimada: S/ {ganancia}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)






