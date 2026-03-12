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
        st.subheader("Distribución de Pacientes por Género")
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
        st.subheader("Distribución de Pacientes Agrupados por Edad y Género")
        age_bins = [0, 18, 35, 50, 65, 100]
        age_labels = ['0-17', '18-34', '35-49', '50-64', '65+']
        df_patient_copy = df_patient.copy()
        
        # Crear columna age_group con categorías ordenadas
        df_patient_copy['age_group'] = pd.cut(df_patient_copy['age'], bins=age_bins, labels=age_labels, right=False, ordered=True)
        
        # Crear tabla cruzada para contar por edad y sexo
        age_sex_counts = pd.crosstab(df_patient_copy['age_group'], df_patient_copy['sex'])
        
        # Reindexar con el orden correcto de las etiquetas
        age_sex_counts = age_sex_counts.reindex(age_labels, fill_value=0)
        
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        # Posiciones de las barras
        x = range(len(age_sex_counts.index))
        width = 0.35
        
        # Crear barras agrupadas
        bars1 = ax2.bar(
            [i - width/2 for i in x],
            age_sex_counts['M'] if 'M' in age_sex_counts.columns else [0] * len(x),
            width,
            label='Masculino',
            color='#1f77b4',
            edgecolor='black',
            linewidth=1.5
        )
        
        bars2 = ax2.bar(
            [i + width/2 for i in x],
            age_sex_counts['F'] if 'F' in age_sex_counts.columns else [0] * len(x),
            width,
            label='Femenino',
            color='#ff7f0e',
            edgecolor='black',
            linewidth=1.5
        )
        
        # Personalizar ejes
        ax2.set_xticks(x)
        ax2.set_xticklabels(age_sex_counts.index, fontsize=16, weight='bold')
        ax2.set_ylabel('Cantidad de Pacientes', fontsize=16, weight='bold')
        ax2.set_xlabel('Grupo de Edad', fontsize=16, weight='bold')
        
        # Agregar valores sobre las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax2.text(
                        bar.get_x() + bar.get_width()/2.,
                        height,
                        f'{int(height)}',
                        ha='center',
                        va='bottom',
                        fontsize=14,
                        weight='bold'
                    )
        
        # Añadir leyenda
        ax2.legend(fontsize=16, loc='upper right')
        
        # Añadir cuadrícula para mejor lectura
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig2)
        
        
        
