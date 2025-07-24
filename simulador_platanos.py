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

# Exportar DataFrame a CSV descargable corregido (UTF-8 BOM + separador ;) para Excel

def exportar_csv(df, filename="reporte.csv"):
    output = BytesIO()
    try:
        df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Descargar CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error al exportar el archivo: {e}")












