import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show(global_filters=None):

    df_substances = pd.read_csv("src/data/data_substance.csv")
    df_patients = pd.read_csv("src/data/data_patient.csv")
    
    # Aplicar filtros globales integrados
    df_substances_filtered = df_substances.copy()
    df_patients_filtered = df_patients.copy()
    
    if global_filters and 'filtered_patient_ids' in global_filters:
        # Filtrar sustancias solo de pacientes que cumplen TODOS los criterios
        df_substances_filtered = df_substances_filtered[df_substances_filtered['patient_id'].isin(global_filters['filtered_patient_ids'])]
        df_patients_filtered = df_patients_filtered[df_patients_filtered['id'].isin(global_filters['filtered_patient_ids'])]
    
    st.divider()
    
    
    #unir dataframes sustancia(patient_id) con pacientes(id)

    st.subheader("Cantidad de Pacientes por Consumo de sustancias")

    df_merged = pd.merge(df_substances_filtered, df_patients_filtered, left_on='patient_id', right_on='id', how='inner')

    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)

    with col_metrics1:
        st.metric("Pacientes Totales", df_merged['patient_id'].nunique())
    
    with col_metrics2:
        st.metric("Pacientes Masculinos", df_merged[df_merged['sex'] == 'M']['patient_id'].nunique())

    with col_metrics3:
        st.metric("Pacientes Femeninos", df_merged[df_merged['sex'] == 'F']['patient_id'].nunique())

    #st.divider()
    
    #Sección visual
    col5, col6 = st.columns([1.5, 2], gap="large")
    
    with col5:
        # Gráfico de dona (donut chart) para distribución por género
        st.subheader("Distribución de consumo de Droga por Género")
        sex_counts = df_merged['sex'].value_counts()
        
        fig, ax = plt.subplots(figsize=(22, 22))
        colors = ['#3498db', '#e74c3c']  # Azul para M, Rojo para F
        labels = ['Masculino' if sex == 'M' else 'Femenino' for sex in sex_counts.index]
        
        wedges, texts, autotexts = ax.pie(
            sex_counts,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 26, 'weight': 'bold'},
            explode=[0.05] * len(sex_counts),
            wedgeprops=dict(width=0.5)  # Esto crea el efecto de dona
        )
        
        # Aumentar tamaño de los porcentajes y etiquetas
        for text in texts:
            text.set_fontsize(34)
            text.set_weight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(38)
            autotext.set_weight('bold')
        
        # Agregar leyenda
        ax.legend(
            wedges,
            [f'{label}: {count}' for label, count in zip(labels, sex_counts)],
            title="Género",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=26
        )
        
        ax.axis('equal')
        st.pyplot(fig)
    
    with col6:
        # Gráfico de barras agrupadas por edad y sexo
        st.subheader("Consumo de Drogas por Rango de Edad y Género")
        age_bins = [0, 18, 35, 50, 65, 100]
        age_labels = ['0-17', '18-34', '35-49', '50-64', '65+']
        df_merged['age_group'] = pd.cut(df_merged['age'], bins=age_bins, labels=age_labels, right=False)
        
        # Crear tabla cruzada para contar por edad y sexo
        age_sex_counts = pd.crosstab(df_merged['age_group'], df_merged['sex'])
        
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
            color='#3498db',
            edgecolor='black',
            linewidth=1.5
        )
        
        bars2 = ax2.bar(
            [i + width/2 for i in x],
            age_sex_counts['F'] if 'F' in age_sex_counts.columns else [0] * len(x),
            width,
            label='Femenino',
            color='#e74c3c',
            edgecolor='black',
            linewidth=1.5
        )
        
        # Personalizar ejes
        ax2.set_xticks(x)
        ax2.set_xticklabels(age_sex_counts.index, fontsize=18, weight='bold')
        ax2.set_ylabel('Cantidad de Pacientes', fontsize=18, weight='bold')
        ax2.set_xlabel('Rango de Edad', fontsize=18, weight='bold')
        
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
        ax2.legend(fontsize=18, loc='upper right')
        
        # Añadir cuadrícula para mejor lectura
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig2)
    
    st.divider()
    
    # Gráfico adicional: Distribución de frecuencias por sustancia y género
    st.subheader("Frecuencia de Consumo por Tipo de Sustancia y Género")
    
    col7, col8 = st.columns(2, gap="large")
    
    with col7:
        st.write("**Pacientes Masculinos**")
        # Filtrar solo masculinos
        df_merged_m = df_merged[df_merged['sex'] == 'M']
        
        if len(df_merged_m) > 0:
            # Crear tabla cruzada de sustancia vs frecuencia para masculinos
            substance_freq_m = pd.crosstab(
                df_merged_m['substance_name'], 
                df_merged_m['substance_freq']
            )
            
            fig3, ax3 = plt.subplots(figsize=(18, 12))
            
            # Crear gráfico de barras apiladas
            substance_freq_m.plot(
                kind='bar',
                stacked=True,
                ax=ax3,
                color=['#2ecc71', "#fba212", "#e54331", "#8c2db1"],
                edgecolor='black',
                linewidth=1.5
            )
            
            # Personalizar el gráfico
            ax3.set_xlabel('Tipo de Sustancia', fontsize=26, weight='bold')
            ax3.set_ylabel('Cantidad de Registros', fontsize=26, weight='bold')
            ax3.set_xticklabels(substance_freq_m.index, rotation=0, ha='right', fontsize=26, weight='bold')
            ax3.legend(title='Frecuencia', fontsize=18, title_fontsize=22, loc='upper right')
            ax3.grid(axis='y', alpha=0.3, linestyle='--')
            ax3.set_axisbelow(True)
            
            # Agregar valores en las secciones de las barras
            for container in ax3.containers:
                ax3.bar_label(container, label_type='center', fontsize=16, weight='bold')
            
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            st.info("No hay datos de pacientes masculinos para los filtros seleccionados")
    
    with col8:
        st.write("**Pacientes Femeninos**")
        # Filtrar solo femeninos
        df_merged_f = df_merged[df_merged['sex'] == 'F']
        
        if len(df_merged_f) > 0:
            # Crear tabla cruzada de sustancia vs frecuencia para femeninos
            substance_freq_f = pd.crosstab(
                df_merged_f['substance_name'], 
                df_merged_f['substance_freq']
            )
            
            fig4, ax4 = plt.subplots(figsize=(18, 12))
            
            # Crear gráfico de barras apiladas
            substance_freq_f.plot(
                kind='bar',
                stacked=True,
                ax=ax4,
                color=['#2ecc71', "#fba212", "#e54331", "#8c2db1"],
                edgecolor='black',
                linewidth=1.5
            )
            
            # Personalizar el gráfico
            ax4.set_xlabel('Tipo de Sustancia', fontsize=26, weight='bold')
            ax4.set_ylabel('Cantidad de Registros', fontsize=26, weight='bold')
            ax4.set_xticklabels(substance_freq_f.index, rotation=0, ha='right', fontsize=26, weight='bold')
            ax4.legend(title='Frecuencia', fontsize=18, title_fontsize=22, loc='upper right')
            ax4.grid(axis='y', alpha=0.3, linestyle='--')
            ax4.set_axisbelow(True)
            
            # Agregar valores en las secciones de las barras
            for container in ax4.containers:
                ax4.bar_label(container, label_type='center', fontsize=16, weight='bold')
            
            plt.tight_layout()
            st.pyplot(fig4)
        else:
            st.info("No hay datos de pacientes femeninos para los filtros seleccionados")
