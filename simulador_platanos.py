import streamlit as st
import random
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import base64

# Imagen
image = Image.open("platano1.png")
st.image(image, use_container_width=False, width=300)

st.title("Simulador de Platanos")

with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["Manual", "Montecarlo", "Vigor de la Planta"])
    st.markdown("---")

def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

def limpiar_texto(texto):
    return (
        str(texto)
        .replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        .encode("latin-1", "ignore").decode("latin-1")
    )

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

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---------------- MANUAL ----------------
if opcion == "Manual":
    st.subheader("Ingreso Manual de Planta")
    if "plantas_manual" not in st.session_state:
        st.session_state["plantas_manual"] = []

    pb = st.number_input("Perimetro de la base (cm):", min_value=30.0, max_value=50.0, value=40.0)
    pm = st.number_input("Perimetro medio (cm):", min_value=25.0, max_value=50.0, value=35.0)
    pa = st.number_input("Perimetro alto (cm):", min_value=15.0, max_value=50.0, value=25.0)
    altura = st.number_input("Altura total del tronco (m):", min_value=2.0, max_value=6.0, value=3.0)
    precio = st.number_input("Precio por platano (S/):", min_value=0.0, value=0.2)

    if st.button("Agregar Planta"):
        estimado = calcular(pb, pm, pa, altura)
        ganancia = round(estimado * precio, 2)
        st.session_state["plantas_manual"].append([pb, pm, pa, altura, estimado, ganancia])
        st.success("Planta agregada correctamente")

    if st.session_state["plantas_manual"]:
        df_manual = pd.DataFrame(
            st.session_state["plantas_manual"],
            columns=["PB", "PM", "PA", "Altura", "Estimado", "Ganancia"]
        )
        st.dataframe(df_manual)
        total_platanos = df_manual["Estimado"].sum()
        total_ganancia = df_manual["Ganancia"].sum()
        st.success(f"Total platanos: {total_platanos}")
        st.info(f"Ganancia estimada: S/ {total_ganancia}")
        generar_pdf(df_manual, total=total_platanos, ganancia=total_ganancia, filename="manual_resultado.pdf")

# ---------------- MONTECARLO ----------------
elif opcion == "Montecarlo":
    st.subheader("Simulación por Montecarlo")
    n = st.number_input("Numero de plantas a simular:", min_value=1, value=10)
    precio = st.number_input("Precio por platano (S/):", min_value=0.0, value=0.2)

    if st.button("Ejecutar Simulacion"):
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

        df = pd.DataFrame(data, columns=["PB", "PM", "PA", "Altura", "Estimacion"])
        st.dataframe(df)

        ganancia = round(total_platanos * precio, 2)
        st.success(f"Total de platanos estimados: {total_platanos}")
        st.info(f"Ganancia estimada: S/ {ganancia}")
        generar_pdf(df, total=total_platanos, ganancia=ganancia, filename="montecarlo_resultado.pdf")

# ---------------- VIGOR ----------------
elif opcion == "Vigor de la Planta":
    st.subheader("Evaluacion del Vigor de la Planta")

    if "plantas" not in st.session_state:
        st.session_state["plantas"] = []

    with st.form("vigor_form"):
        grosor = st.number_input("Grosor del tallo (cm)", min_value=1.0, max_value=50.0, value=30.0)
        altura_tallo = st.number_input("Altura del tallo (m)", min_value=0.5, max_value=6.0, value=2.5)
        hojas_sanas = st.number_input("Numero de hojas sanas", min_value=0, max_value=30, value=10)
        altura_hijo = st.number_input("Altura del hijo (m)", min_value=0.0, max_value=4.0, value=1.5)

        col1, col2 = st.columns(2)
        agregar = col1.form_submit_button("Agregar Planta")
        cancelar = col2.form_submit_button("Cancelar")

        if agregar:
            st.session_state["plantas"].append({
                "Grosor": grosor,
                "AlturaTallo": altura_tallo,
                "HojasSanas": hojas_sanas,
                "AlturaHijo": altura_hijo
            })
            st.success("Planta agregada")

        if cancelar:
            st.session_state["plantas"] = []
            st.warning("Lista reiniciada")

    if st.session_state["plantas"]:
        if st.button("Analizar Plantas"):
            resultados = []
            estados = {"Saludable": 0, "Regular": 0, "Debil": 0, "Critica": 0}

            for idx, planta in enumerate(st.session_state["plantas"], 1):
                vigor = (
                    planta["Grosor"] * 0.3 +
                    planta["AlturaTallo"] * 10 +
                    planta["HojasSanas"] * 1 +
                    planta["AlturaHijo"] * 5
                )
                if vigor > 100:
                    estado = "Saludable"
                elif vigor > 75:
                    estado = "Regular"
                elif vigor > 50:
                    estado = "Debil"
                else:
                    estado = "Critica"

                estados[estado] += 1
                resultados.append([idx, planta["Grosor"], planta["AlturaTallo"],
                                  planta["HojasSanas"], planta["AlturaHijo"], estado])

            df_vigor = pd.DataFrame(resultados, columns=["#", "Grosor", "Altura Tallo", "Hojas Sanas", "Altura Hijo", "Estado"])
            st.dataframe(df_vigor)

            fig = px.pie(
                names=list(estados.keys()),
                values=list(estados.values()),
                title="Distribucion del Vigor de las Plantas",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig)
            generar_pdf(df_vigor, filename="vigor_resultado.pdf")





