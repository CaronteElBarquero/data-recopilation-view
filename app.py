import streamlit as st
import pandas as pd
from src.pages import patient_pages

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

st.header("Análisis de Pacientes")
patient_pages.show()

st.divider()

st.header("Análisis de Accidentes")
st.subheader("Próximamente......")

st.divider()

st.header("Análisis de Ingresos")
st.subheader("Próximamente......")


