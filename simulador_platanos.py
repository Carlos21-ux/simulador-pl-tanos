
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
st.image(image, use_column_width=False, width=300)

st.title("🌿 Simulador de Plátanos")

# Menú lateral
with st.sidebar:
    st.header("Opciones Generales")
    opcion = st.radio("Selecciona un modo de simulación", ["🔢 Manual", "🎲 Montecarlo", "🌱 Vigor de la Planta"])
    st.markdown("---")
    if opcion == "🎲 Montecarlo":
        st.header("🎯 Personalizar Simulación")
        pb_range = st.slider("Rango de PB (cm)", 30, 50, (30, 50))
        pm_range = st.slider("Rango de PM (cm)", 25, 45, (25, 45))
        pa_range = st.slider("Rango de PA (cm)", 15, 35, (15, 35))
        altura_range = st.slider("Rango de Altura (m)", 2.0, 4.0, (2.0, 4.0))

def calcular(pb, pm, pa, altura):
    resultado = (pb * 0.25 + pm * 0.2 + pa * 0.15 + altura * 10) - 10
    return round(min(max(resultado, 30), 60))

def generar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Simulación de Plátanos", ln=1, align='C')

    col_names = df.columns.tolist()
    for col in col_names:
        pdf.cell(30, 10, col, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for item in row:
            pdf.cell(30, 10, str(item), border=1)
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
    pdf.cell(200, 10, txt="Diagnóstico de Vigor de Plantas", ln=1, align='C')
    pdf.ln(10)

    for idx, row in df.iterrows():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Planta {idx+1} - Estado: {row['Estado']}", ln=1)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 10, f"Grosor: {row['Grosor']} cm\nAltura Tallo: {row['Altura Tallo']} m\nHojas Sanas: {row['Hojas']}\nAltura Hijo: {row['Altura Hijo']} m\nRecomendaciones: {row['Diagnóstico']}")
        pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# Manual
if opcion == "🔢 Manual":
    st.subheader("🛠 Ingreso Manual de Datos")
    pb = st.number_input("📏 Perímetro de la base (cm):", min_value=30.0, max_value=50.0, value=40.0)
    pm = st.number_input("📏 Perímetro medio (cm):", min_value=25.0, max_value=45.0, value=35.0)
    pa = st.number_input("📏 Perímetro alto (cm):", min_value=15.0, max_value=35.0, value=25.0)
    altura = st.number_input("📏 Altura total del tronco (m):", min_value=2.0, max_value=4.0, value=3.0)

    if st.button("🌱 Calcular Plátanos"):
        pred = calcular(pb, pm, pa, altura)
        st.success(f"🌿 Estimación: {pred} plátanos 🍌")

# Montecarlo
elif opcion == "🎲 Montecarlo":
    st.subheader("🎲 Simulación por Montecarlo")
    col1, col2 = st.columns(2)

    with col1:
        n = st.number_input("🌱 Número de plantas a simular:", min_value=1, value=10)
    with col2:
        precio = st.number_input("💰 Precio por plátano (S/):", min_value=0.0, value=0.2)

    if st.button("▶️ Ejecutar Simulación"):
        data = []
        total_platanos = 0

        for _ in range(n):
            pb = round(random.uniform(*pb_range), 2)
            pm = round(random.uniform(*pm_range), 2)
            pa = round(random.uniform(*pa_range), 2)
            altura = round(random.uniform(*altura_range), 2)
            estimado = calcular(pb, pm, pa, altura)
            total_platanos += estimado
            data.append([pb, pm, pa, altura, estimado])

        df = pd.DataFrame(data, columns=["PB (cm)", "PM (cm)", "PA (cm)", "Altura (m)", "🍌 Estimación"])
        st.dataframe(df)

        fig = px.histogram(df, x="🍌 Estimación", nbins=10, title="Distribución de Plátanos Estimados")
        st.plotly_chart(fig)

        ganancia = round(total_platanos * precio, 2)
        st.success(f"🔢 Total de plátanos estimados: {total_platanos}")
        st.info(f"💰 Ganancia estimada: S/ {ganancia}")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "simulacion_platanos.csv", "text/csv")

        pdf_bytes = generar_pdf(df)
        b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="reporte_simulacion.pdf">📄 Descargar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# Vigor de la Planta
elif opcion == "🌱 Vigor de la Planta":
    st.subheader("🧪 Evaluación del Vigor de la Planta")
    if 'plantas' not in st.session_state:
        st.session_state.plantas = []

    with st.form("planta_form"):
        col1, col2 = st.columns(2)
        with col1:
            grosor = st.number_input("📏 Grosor del tallo (cm):", min_value=5.0, max_value=25.0, value=12.0)
            hojas = st.number_input("🌿 Número de hojas sanas:", min_value=0, max_value=30, value=10)
        with col2:
            altura_tallo = st.number_input("📏 Altura del tallo (m):", min_value=0.5, max_value=4.0, value=2.0)
            altura_hijo = st.number_input("🌱 Altura del hijo (m):", min_value=0.0, max_value=3.0, value=1.0)

        agregar = st.form_submit_button("➕ Agregar Planta")
        cancelar = st.form_submit_button("❌ Cancelar")

        if agregar:
            st.session_state.plantas.append({
                "Grosor": grosor,
                "Altura Tallo": altura_tallo,
                "Hojas": hojas,
                "Altura Hijo": altura_hijo
            })
        if cancelar:
            st.session_state.plantas = []
            st.info("Plantas eliminadas.")

    if st.session_state.plantas:
        df_vigor = pd.DataFrame(st.session_state.plantas)
        st.dataframe(df_vigor)

        if st.button("📊 Analizar Plantas"):
            diagnosticos = []
            estado_counts = {"Óptima": 0, "Media": 0, "Débil": 0, "Crítica": 0}

            for p in st.session_state.plantas:
                score = p['Grosor'] * 1.5 + p['Altura Tallo'] * 2 + p['Hojas'] * 1.2 + p['Altura Hijo'] * 1

                if score >= 80:
                    estado = "Óptima"
                    icono = "✅"
                    color = "#D4EDDA"
                    recomendaciones = "🌟 Planta en excelentes condiciones. Mantener riego y nutrición."
                elif score >= 60:
                    estado = "Media"
                    icono = "ℹ️"
                    color = "#FFF3CD"
                    recomendaciones = "🧪 Planta saludable, pero revisar nutrición foliar."
                elif score >= 40:
                    estado = "Débil"
                    icono = "⚠️"
                    color = "#F8D7DA"
                    recomendaciones = "⚠️ Mejorar riego, aplicar fertilizantes orgánicos."
                else:
                    estado = "Crítica"
                    icono = "🚨"
                    color = "#F5C6CB"
                    recomendaciones = "🚨 Atención urgente: revisar raíz, suelo, aplicar bioestimulantes."

                estado_counts[estado] += 1
                diagnosticos.append({**p, "Estado": estado, "Diagnóstico": recomendaciones, "Icono": icono, "Color": color})

            df_diag = pd.DataFrame(diagnosticos)

            for i, row in df_diag.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div style='background-color:{row['Color']}; padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <h4>{row['Icono']} Planta {i+1} - Estado: {row['Estado']}</h4>
                            <ul>
                                <li>📏 Grosor del tallo: {row['Grosor']} cm</li>
                                <li>🌿 Hojas sanas: {row['Hojas']}</li>
                                <li>📏 Altura del tallo: {row['Altura Tallo']} m</li>
                                <li>🌱 Altura del hijo: {row['Altura Hijo']} m</li>
                                <li>🩺 Diagnóstico: {row['Diagnóstico']}</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

            fig = px.pie(names=list(estado_counts.keys()), values=list(estado_counts.values()),
                         title="Distribución del Vigor de Plantas", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig)

            pdf_diag = generar_pdf_diagnostico(df_diag)
            b64_pdf_diag = base64.b64encode(pdf_diag).decode('utf-8')
            href_diag = f'<a href="data:application/octet-stream;base64,{b64_pdf_diag}" download="diagnostico_vigor.pdf">📄 Descargar Diagnóstico en PDF</a>'
            st.markdown(href_diag, unsafe_allow_html=True)
            st.success("✅ Diagnóstico completo generado.")
