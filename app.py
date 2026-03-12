import streamlit as st
import pandas as pd
from src.pages import patient_pages, substance_page, entries_page

st.set_page_config(page_title="Sistema de Análisis Hospitalario", page_icon="🏥", layout="wide")

st.title("📊 Sistema de Análisis de Accidentes Hospitalarios")

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


# Advertencia sobre sesgos y limitaciones
with st.expander("⚠️ Consideraciones sobre Sesgos y Limitaciones de los Datos"):

    st.markdown(f"""
    
    **⚠️ Posibles sesgos a considerar:**
    
    1. **Sesgo de muestra pequeña:**
        - Si los números son bajos (< 30 casos por categoría), las conclusiones pueden no ser representativas
        - Las combinaciones raras pueden ser casuales, no causales
    
    2. **Sesgo de reporte:**
        - Los datos solo incluyen casos **reportados** al hospital
        - Accidentes menores o sin atención médica no están registrados
        - El consumo de sustancias puede estar **subregistrado** (pacientes que no admiten consumo)
    
    3. **Sesgo temporal:**
        - Los datos corresponden a un período específico
        - Patrones estacionales o eventos especiales pueden afectar los resultados
    
    4. **Correlación ≠ Causalidad:**
        - Una relación alta entre accidente y sustancia **NO confirma** que la sustancia causó el accidente
        - Pueden existir otros factores no medidos (hora del día, condiciones climáticas, experiencia del conductor)
    
    5. **Sesgo de género:**
        - Si hay desequilibrio significativo entre géneros (ej: 80% hombres, 20% mujeres), las comparaciones pueden ser injustas
        - Los patrones de un género pueden dominar el análisis general
    
    **💡 Recomendaciones:**
    - Interpreta los números bajos (< 5) con **extrema cautela**
    - Considera estos datos como **exploratorios**, no concluyentes
    - Complementa con estudios adicionales para validar patrones observados
    - Ten en cuenta que los datos reflejan solo una **fracción** de la realidad
    """)
        
st.divider()

# Cargar todos los datos una vez
df_patients = pd.read_csv("src/data/data_patient.csv")
df_substances = pd.read_csv("src/data/data_substance.csv")
df_entries = pd.read_csv("src/data/data_entries.csv")

# ============= FILTROS GLOBALES EN SIDEBAR (FLOTANTE) =============
st.sidebar.header("Filtros Globales Integrados")
st.sidebar.info("Estos filtros se aplicarán a TODAS las secciones y permanecerán visibles al hacer scroll")

st.sidebar.divider()

st.sidebar.subheader("📋 Filtros Demográficos")
flt_first_age = st.sidebar.slider("Edad mínima", 0, 100, 0, key="global_age_min")
flt_second_age = st.sidebar.slider("Edad máxima", 0, 100, 100, key="global_age_max")
flt_sex = st.sidebar.selectbox("Sexo", ["Todos", "M", "F"], key="global_sex")

st.sidebar.divider()

st.sidebar.subheader("💊 Filtros de Sustancias")
substance_options = ["Todas"] + sorted([x for x in df_substances['substance_name'].unique() if pd.notna(x)])
substance_filter = st.sidebar.selectbox("Tipo de Sustancia", substance_options, key="global_substance")

frequency_options = ["Todas"] + sorted([x for x in df_substances['substance_freq'].unique() if pd.notna(x)])
frequency_filter = st.sidebar.selectbox("Frecuencia de Consumo", frequency_options, key="global_frequency")

st.sidebar.divider()

st.sidebar.subheader("🚑 Filtros de Accidentes")
accident_type_options = ["Todas"] + sorted([x for x in df_entries['accidentType'].unique() if pd.notna(x)])
accident_type_filter = st.sidebar.selectbox("Tipo de Accidente", accident_type_options, key="global_accident_type")

accident_severity_options = ["Todas"] + sorted([x for x in df_entries['accidentSeverity'].unique() if pd.notna(x)])
accident_severity_filter = st.sidebar.selectbox("Gravedad del Accidente", accident_severity_options, key="global_accident_severity")

st.sidebar.divider()

# Botón para limpiar todos los filtros
if st.sidebar.button("🔄 Limpiar todos los filtros", use_container_width=True):
    st.rerun()

# ============= PROCESAMIENTO DE FILTROS CRUZADOS =============
# Empezar con todos los pacientes
filtered_patient_ids = set(df_patients['id'].values)

# Aplicar filtros demográficos
df_patients_filtered = df_patients.copy()
df_patients_filtered = df_patients_filtered[(df_patients_filtered['age'] >= flt_first_age) & 
                                            (df_patients_filtered['age'] <= flt_second_age)]
if flt_sex != "Todos":
    df_patients_filtered = df_patients_filtered[df_patients_filtered['sex'] == flt_sex]

filtered_patient_ids = filtered_patient_ids.intersection(set(df_patients_filtered['id'].values))

# Aplicar filtros de sustancias
if substance_filter != "Todas" or frequency_filter != "Todas":
    df_substances_filtered = df_substances.copy()
    
    if substance_filter != "Todas":
        df_substances_filtered = df_substances_filtered[df_substances_filtered['substance_name'] == substance_filter]
    
    if frequency_filter != "Todas":
        df_substances_filtered = df_substances_filtered[df_substances_filtered['substance_freq'] == frequency_filter]
    
    filtered_patient_ids = filtered_patient_ids.intersection(set(df_substances_filtered['patient_id'].dropna().values))

# Aplicar filtros de accidentes
if accident_type_filter != "Todas" or accident_severity_filter != "Todas":
    df_entries_filtered = df_entries.copy()
    
    if accident_type_filter != "Todas":
        df_entries_filtered = df_entries_filtered[df_entries_filtered['accidentType'] == accident_type_filter]
    
    if accident_severity_filter != "Todas":
        df_entries_filtered = df_entries_filtered[df_entries_filtered['accidentSeverity'] == accident_severity_filter]
    
    filtered_patient_ids = filtered_patient_ids.intersection(set(df_entries_filtered['patient_id'].dropna().values))

# Convertir a lista
filtered_patient_ids = list(filtered_patient_ids)

# Diccionario con los filtros globales y datos filtrados
global_filters = {
    'age_min': flt_first_age,
    'age_max': flt_second_age,
    'sex': flt_sex,
    'substance_name': substance_filter,
    'substance_freq': frequency_filter,
    'accident_type': accident_type_filter,
    'accident_severity': accident_severity_filter,
    'filtered_patient_ids': filtered_patient_ids
}

# Mostrar resumen de filtros aplicados en el sidebar
st.sidebar.divider()
st.sidebar.subheader("📊 Resumen de Filtros")
st.sidebar.metric("Pacientes filtrados", len(filtered_patient_ids))

with st.sidebar.expander("Ver detalles de filtros"):
    st.write(f"**Edad:** {flt_first_age} - {flt_second_age} años")
    st.write(f"**Sexo:** {flt_sex}")
    st.write(f"**Sustancia:** {substance_filter}")
    st.write(f"**Frecuencia:** {frequency_filter}")
    st.write(f"**Tipo de Accidente:** {accident_type_filter}")
    st.write(f"**Gravedad:** {accident_severity_filter}")

# ============= SECCIONES DE ANÁLISIS =============
st.header("👥 Análisis de Pacientes")
patient_pages.show(global_filters)

st.divider()

st.header("💊 Análisis de Sustancias en Pacientes")
substance_page.show(global_filters)

st.divider()

st.header("🚑 Análisis de Ingresos por Accidentes")
entries_page.show(global_filters)


