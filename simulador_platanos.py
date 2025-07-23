
import streamlit as st
import random
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import base64
import unicodedata

# Imagen
image = Image.open("platano1.png")
st.image(image, use_column_width=False, width=300)

st.title("🌿 Simulador de Plátanos")

# Menú lateral
with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["manual", "montecarlo", "vigor"])
    st.markdown("---")
    if opcion == "montecarlo":
        st.header("🎯 Personalizar Simulación")
        pb_range = st.slider("Rango de PB (cm)", 30, 50, (30, 50))
        pm_range = st.slider("Rango de PM (cm)", 25, 45, (25, 45))
        pa_range = st.slider("Rango de PA (cm)", 15, 35, (15, 35))
        altura_range = st.slider("Rango de Altura (m)", 2.0, 4.0, (2.0, 4.0))

def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

def limpiar_texto(texto):
    return unicodedata.normalize("NFKD", texto).encode("latin-1", "ignore").decode("latin-1")

def generar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Simulacion de Platanos", ln=1, align='C')

    col_names = df.columns.tolist()
    for col in col_names:
        pdf.cell(30, 10, limpiar_texto(col), border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for item in row:
            pdf.cell(30, 10, limpiar_texto(str(item)), border=1)
        pdf.ln()

    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generar_pdf_diagnostico(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Diagnostico de Vigor de Plantas", ln=1, align='C')
    pdf.ln(10)

    for idx, row in df.iterrows():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, limpiar_texto(f"Planta {idx+1} - Estado: {row['Estado']}"), ln=1)
        pdf.set_font("Arial", '', 11)
        texto = f"Grosor: {row['Grosor']} cm\nAltura Tallo: {row['Altura Tallo']} m\nHojas Sanas: {row['Hojas']}\nAltura Hijo: {row['Altura Hijo']} m\nRecomendaciones: {row['Diagnóstico']}"
        pdf.multi_cell(0, 10, limpiar_texto(texto))
        pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
