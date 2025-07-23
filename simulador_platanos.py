
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

st.title("🌿 Simulador de Plátanos")

# Menú lateral
with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["manual", "montecarlo", "vigor"])
    st.markdown("---")

def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

# Sección Manual
if opcion == "manual":
    pb = st.number_input("📏 Perímetro de la base (cm):", min_value=30.0, max_value=50.0, value=40.0)
    pm = st.number_input("📏 Perímetro medio (cm):", min_value=25.0, max_value=45.0, value=35.0)
    pa = st.number_input("📏 Perímetro alto (cm):", min_value=15.0, max_value=35.0, value=25.0)
    altura = st.number_input("📏 Altura total del tronco (m):", min_value=2.0, max_value=4.0, value=3.0)

    if st.button("🌱 Calcular Plátanos"):
        pred = calcular(pb, pm, pa, altura)
        st.success(f"🌿 Estimación: {pred} plátanos 🍌")

# Sección Montecarlo
elif opcion == "montecarlo":
    st.subheader("🎲 Simulación por Montecarlo")
    n = st.number_input("🌱 Número de plantas a simular:", min_value=1, value=10)
    precio = st.number_input("💰 Precio por plátano (S/):", min_value=0.0, value=0.2)

    if st.button("▶️ Ejecutar Simulación"):
        data = []
        total_platanos = 0

        for _ in range(n):
            pb = round(random.uniform(30, 50), 2)
            pm = round(random.uniform(25, 45), 2)
            pa = round(random.uniform(15, 35), 2)
            altura = round(random.uniform(2.0, 4.0), 2)
            estimado = calcular(pb, pm, pa, altura)
            total_platanos += estimado
            data.append([pb, pm, pa, altura, estimado])

        df = pd.DataFrame(data, columns=["PB (cm)", "PM (cm)", "PA (cm)", "Altura (m)", "🍌 Estimación"])
        st.dataframe(df)

        ganancia = round(total_platanos * precio, 2)
        st.success(f"🔢 Total de plátanos estimados: {total_platanos}")
        st.info(f"💰 Ganancia estimada: S/ {ganancia}")

# Sección Vigor de la Planta
elif opcion == "vigor":
    st.header("🌱 Evaluación del Vigor de la Planta")
    st.info("Aquí podrás ingresar las características de cada planta y analizar su vigor y salud.")

    if 'plantas' not in st.session_state:
        st.session_state['plantas'] = []

    with st.form("form_planta"):
        st.subheader("🪴 Ingreso de Datos de la Planta")
        grosor = st.slider("🌾 Grosor del tallo (cm)", min_value=1, max_value=100, value=30)
        altura_tallo = st.slider("📏 Altura del tallo (m)", min_value=0.5, max_value=4.0, value=2.0, step=0.1)
        hojas_sanas = st.number_input("🍃 Número de hojas sanas", min_value=0, max_value=30, value=10)
        altura_hijo = st.slider("🌿 Altura del hijo (m)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

        col1, col2 = st.columns(2)
        with col1:
            agregar = st.form_submit_button("➕ Agregar Planta")
        with col2:
            cancelar = st.form_submit_button("❌ Cancelar")

    if cancelar:
        st.session_state['plantas'] = []
        st.warning("Formulario reiniciado.")

    if agregar:
        st.session_state['plantas'].append({
            "Grosor": grosor,
            "AlturaTallo": altura_tallo,
            "Hojas": hojas_sanas,
            "AlturaHijo": altura_hijo
        })
        st.success("🌿 Planta registrada exitosamente")

    if st.session_state['plantas']:
        st.subheader("📋 Plantas registradas")
        df_diag = pd.DataFrame(st.session_state['plantas'])
        st.dataframe(df_diag)

        if st.button("📊 Analizar Plantas"):
            resultados = []
            clasificaciones = []
            for i, planta in enumerate(st.session_state['plantas']):
                score = planta['Grosor'] * 0.3 + planta['AlturaTallo'] * 15 + planta['Hojas'] * 1.5 + planta['AlturaHijo'] * 10
                if score >= 100:
                    estado = "🌟 Excelente"
                    color = "green"
                elif score >= 75:
                    estado = "💪 Buena"
                    color = "blue"
                elif score >= 50:
                    estado = "⚠️ Regular"
                    color = "orange"
                else:
                    estado = "❌ Débil"
                    color = "red"
                resultados.append((f"Planta #{i+1}", estado, color))
                clasificaciones.append(estado)

            st.subheader("🧾 Diagnóstico por Planta")
            for nombre, estado, color in resultados:
                st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; color:white'>
                            <strong>{nombre}</strong>: {estado}</div>", unsafe_allow_html=True)

            fig = px.pie(names=clasificaciones, title="Distribución de estados de vigor")
            st.plotly_chart(fig)

            # PDF export (puede añadirse más adelante)
            st.info("📝 Exportación a PDF estará disponible en la próxima actualización.")
