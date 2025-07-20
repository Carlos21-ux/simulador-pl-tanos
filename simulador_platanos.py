
import streamlit as st
import random
import pandas as pd
from PIL import Image

# Imagen
image = Image.open("platano1.png")
st.image(image, use_column_width=False, width=300)

st.title("🌿 Simulador de Plátanos")

opcion = st.radio("Selecciona un modo de simulación", ["🔢 Manual", "🎲 Montecarlo"])

def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

if opcion == "🔢 Manual":
    pb = st.number_input("📏 Perímetro de la base (cm):", min_value=30.0, max_value=50.0, value=40.0)
    pm = st.number_input("📏 Perímetro medio (cm):", min_value=25.0, max_value=45.0, value=35.0)
    pa = st.number_input("📏 Perímetro alto (cm):", min_value=15.0, max_value=35.0, value=25.0)
    altura = st.number_input("📏 Altura total del tronco (m):", min_value=2.0, max_value=4.0, value=3.0)

    if st.button("🌱 Calcular Plátanos"):
        pred = calcular(pb, pm, pa, altura)
        st.success(f"🌿 Estimación: {pred} plátanos 🍌")

else:
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
