import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show(global_filters=None):
    df = pd.read_csv("src/data/data_patient.csv")

    df_patient = df[['patient_name', 'age', 'sex', 'id']]
    
    # Aplicar filtros globales si existen
    if global_filters and 'filtered_patient_ids' in global_filters:
        # Filtrar solo los pacientes que cumplen TODOS los criterios
        df_patient = df_patient[df_patient['id'].isin(global_filters['filtered_patient_ids'])]
    elif global_filters:
        # Filtros demográficos básicos
        df_patient = df_patient[(df_patient['age'] >= global_filters['age_min']) & 
                                (df_patient['age'] <= global_filters['age_max'])]
        
        if global_filters['sex'] != "Todos":
            df_patient = df_patient[df_patient['sex'] == global_filters['sex']]

    st.divider()
    
    # Sección de métricas
    st.subheader("Cantidad de Pacientes Según Sexo")
    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
    
    with col_metrics1:
        st.metric("Total de Pacientes", df_patient['sex'].count())
    
    with col_metrics2:
        masculinos = len(df_patient[df_patient['sex'] == 'M'])
        st.metric("Masculino", masculinos)
    
    with col_metrics3:
        femeninos = len(df_patient[df_patient['sex'] == 'F'])
        st.metric("Femenino", femeninos)
    
    #st.divider()
    
    # Sección de visualización
    col5, col6 = st.columns([1.7, 2], gap="large")
    
    with col5:
        # Gráfico de pastel (pie chart)
        st.subheader("Distribución por Género en %")
        sex_counts = df_patient['sex'].value_counts()
        
        fig, ax = plt.subplots(figsize=(22, 22))
        colors = ["#1f77b4" if sex == 'M' else "#ff7f0e" for sex in sex_counts.index]
        labels = ['Masculino' if sex == 'M' else 'Femenino' for sex in sex_counts.index]
        
        wedges, texts, autotexts = ax.pie(
            sex_counts, 
            labels=labels, 
            autopct='%1.1f%%', 
            colors=colors, 
            startangle=90,
            textprops={'fontsize': 24, 'weight': 'bold'},
            explode=[0.05] * len(sex_counts)
        )
        
        # Aumentar tamaño de los porcentajes y etiquetas
        for text in texts:
            text.set_fontsize(36)
            text.set_weight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(40)
            autotext.set_weight('bold')
        
        # Agregar leyenda con colores
        ax.legend(
            wedges, 
            [f'{label}: {count}' for label, count in zip(labels, sex_counts)],
            title="Sexo",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=28
        )
        
        ax.axis('equal')
        st.pyplot(fig)
        
    with col6:
        st.subheader("Distribución de Pacientes Agrupados por Edad")
        age_bins = [0, 18, 35, 50, 65, 100]
        age_labels = ['0-17', '18-34', '35-49', '50-64', '65+']
        df_patient['age_group'] = pd.cut(df_patient['age'], bins=age_bins, labels=age_labels, right=False)
        age_group_counts = df_patient['age_group'].value_counts().sort_values(ascending=False)
        
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        # Crear gráfico de barras con colores degradados
        bars = ax2.bar(
            range(len(age_group_counts)), 
            age_group_counts.values,
            color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
            edgecolor='black',
            linewidth=1.5
        )
        
        # Personalizar ejes
        ax2.set_xticks(range(len(age_group_counts)))
        ax2.set_xticklabels(age_group_counts.index, fontsize=16, weight='bold')
        ax2.set_ylabel('Cantidad de Pacientes', fontsize=16, weight='bold')
        ax2.set_xlabel('Grupo de Edad', fontsize=16, weight='bold')
        
        # Agregar valores sobre las barras
        for i, (bar, value) in enumerate(zip(bars, age_group_counts.values)):
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f'{int(value)}',
                ha='center', 
                va='bottom',
                fontsize=18,
                weight='bold'
            )
        
        # Añadir cuadrícula para mejor lectura
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig2)
        
        
        
