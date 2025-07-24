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

st.title("🌿 Simulador de Plátanos")

with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["🔢 Manual", "🎲 Montecarlo", "🌱 Vigor de la Planta"])
    st.markdown("---")

# Función base para estimar plátanos
def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

# Generar PDF
def generar_pdf(df, total=None, ganancia=None, filename="reporte.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for i, col in enumerate(df.columns):
        pdf.cell(40, 10, str(col), border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for val in row:
            pdf.cell(40, 10, str(val), border=1)
        pdf.ln()

    if total is not None:
        pdf.ln()
        pdf.cell(200, 10, f"Total estimado: {total} plátanos", ln=True)
    if ganancia is not None:
        pdf.cell(200, 10, f"Ganancia estimada: S/ {ganancia}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">🗄️ Descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---------- MANUAL ----------
if opcion == "🔢 Manual":
    st.subheader("🔢 Ingreso Manual de Planta")
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
        df_manual = pd.DataFrame(st.session_state["plantas_manual"], columns=["PB", "PM", "PA", "Altura", "🍌 Estimado", "💰 Ganancia"])
        st.dataframe(df_manual)
        total_platanos = df_manual["🍌 Estimado"].sum()
        total_ganancia = df_manual["💰 Ganancia"].sum()
        st.success(f"🔢 Total plátanos: {total_platanos}")
        st.info(f"💰 Ganancia total estimada: S/ {total_ganancia}")
        generar_pdf(df_manual, total=total_platanos, ganancia=total_ganancia, filename="manual_resultado.pdf")

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

        df = pd.DataFrame(data, columns=["PB (cm)", "PM (cm)", "PA (cm)", "Altura (m)", "🍌 Estimación"])
        st.dataframe(df)

        ganancia = round(total_platanos * precio, 2)
        st.success(f"🔢 Total de plátanos estimados: {total_platanos}")
        st.info(f"💰 Ganancia estimada: S/ {ganancia}")

        generar_pdf(df, total=total_platanos, ganancia=ganancia, filename="montecarlo_resultado.pdf")

# ---------- VIGOR DE LA PLANTA ----------
elif opcion == "🌱 Vigor de la Planta":
    st.subheader("🌱 Evaluación del Vigor de la Planta")
    st.info("Aquí podrás ingresar las características de cada planta y analizar su vigor y salud.")

    if "plantas" not in st.session_state:
        st.session_state["plantas"] = []

    with st.form("vigor_form"):
        grosor = st.number_input("🌱 Grosor del tallo (cm)", min_value=1.0, max_value=50.0, value=30.0)
        altura_tallo = st.number_input("🌿 Altura del tallo (m)", min_value=0.5, max_value=6.0, value=2.5)
        hojas_sanas = st.number_input("🍃 Número de hojas sanas", min_value=0, max_value=30, value=10)
        altura_hijo = st.number_input("🌿 Altura del hijo (m)", min_value=0.0, max_value=4.0, value=1.5)

        col1, col2 = st.columns(2)
        with col1:
            agregar = st.form_submit_button("➕ Agregar Planta")
        with col2:
            cancelar = st.form_submit_button("❌ Cancelar")

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
                    planta["Grosor"] * 0.3 +
                    planta["AlturaTallo"] * 10 +
                    planta["HojasSanas"] * 1 +
                    planta["AlturaHijo"] * 5
                )
                if vigor > 100:
                    estado = "Saludable"
                    color = "#28a745"
                    emoji = "🟢"
                elif vigor > 75:
                    estado = "Regular"
                    color = "#ffc107"
                    emoji = "🟡"
                elif vigor > 50:
                    estado = "Débil"
                    color = "#fd7e14"
                    emoji = "🟠"
                else:
                    estado = "Crítica"
                    color = "#dc3545"
                    emoji = "🔴"

                estados[estado] += 1
                resultados.append([idx, planta["Grosor"], planta["AlturaTallo"], planta["HojasSanas"], planta["AlturaHijo"], estado])

                texto = (
                    f"{emoji} Planta {idx}:\n"
                    f"- Grosor: {planta['Grosor']} cm\n"
                    f"- Altura Tallo: {planta['AlturaTallo']} m\n"
                    f"- Hojas Sanas: {planta['HojasSanas']}\n"
                    f"- Altura Hijo: {planta['AlturaHijo']} m\n"
                    f"➡️ Estado: **{estado}**"
                )

                st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; color:white'>{texto}</div>", unsafe_allow_html=True)

            df_vigor = pd.DataFrame(resultados, columns=["#", "Grosor", "Altura Tallo", "Hojas Sanas", "Altura Hijo", "Estado"])
            fig = px.pie(
                names=list(estados.keys()),
                values=list(estados.values()),
                title="Distribución del Vigor de las Plantas",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig)
            generar_pdf(df_vigor, filename="vigor_resultado.pdf")


