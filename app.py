import streamlit as st
import pandas as pd
from src.pages import patient_pages, substance_page, entries_page

st.title("Sistema de Análisis de Accidentes Hospitalarios")

st.markdown("""
### Descripción del Proyecto
Este sistema ha sido desarrollado para analizar y visualizar datos extraídos del registro de accidentes 
de un hospital. Los datos recopilados permiten identificar patrones, tendencias y características 
demográficas de los pacientes involucrados en incidentes hospitalarios.

El objetivo principal es estructurar la información de accidentes de manera clara y accesible, 
facilitando la toma de decisiones para mejorar los protocolos de seguridad y prevención de riesgos 
en el entorno hospitalario.
""")

st.divider()

# FILTROS GLOBALES
st.header("🔍 Filtros Globales")
st.info("Estos filtros se aplicarán a todas las secciones de análisis")

col1, col2, col3 = st.columns(3)

with col1:
    flt_first_age = st.slider("Edad mínima", 0, 100, 0, key="global_age_min")

with col2:
    flt_second_age = st.slider("Edad máxima", 0, 100, 100, key="global_age_max")

with col3:
    flt_sex = st.selectbox("Sexo", ["Todos", "M", "F"], key="global_sex")

# Diccionario con los filtros globales
global_filters = {
    'age_min': flt_first_age,
    'age_max': flt_second_age,
    'sex': flt_sex
}

st.divider()

st.header("👥 Análisis de Pacientes")
patient_pages.show(global_filters)

st.divider()

st.header("💊 Análisis de Sustancias en Pacientes")
substance_page.show(global_filters)

st.divider()

st.header("🚑 Análisis de Ingresos")
entries_page.show(global_filters)

st.divider()

st.header("📈 Análisis de Ingresos")
st.subheader("Próximamente......")


