import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show(global_filters=None):
    
    df_ent = pd.read_csv("src/data/data_entries.csv")
    df_pati = pd.read_csv("src/data/data_patient.csv")
    df_substance = pd.read_csv("src/data/data_substance.csv")
    
    # Aplicar filtros globales integrados
    df_ent_filtered = df_ent.copy()
    df_pati_filtered = df_pati.copy()
    
    if global_filters and 'filtered_patient_ids' in global_filters:
        # Filtrar entradas solo de pacientes que cumplen TODOS los criterios
        df_ent_filtered = df_ent_filtered[df_ent_filtered['patient_id'].isin(global_filters['filtered_patient_ids'])]
        df_pati_filtered = df_pati_filtered[df_pati_filtered['id'].isin(global_filters['filtered_patient_ids'])]
    
    st.divider()
    
    st.subheader("Métricas de Ingresos")
    
    df_merged = pd.merge(df_ent_filtered, df_pati_filtered, left_on='patient_id', right_on='id', how='inner')
    
    
    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
    
    with col_metrics1:
        st.metric("Total de Ingresos", df_merged['patient_id'].count())
    
    with col_metrics2:
        # Días promedio de hospitalización
        avg_stay = df_merged['hospital_stay_days'].mean()
        st.metric("Días Promedio de Estancia", f"{avg_stay:.1f}" if not pd.isna(avg_stay) else "N/A")
    
    with col_metrics3:
        # Total de pacientes únicos
        unique_patients = df_merged['patient_id'].nunique()
        st.metric("Pacientes Únicos", unique_patients)
    
    with col_metrics4:
        # Reingresos (pacientes con más de un ingreso)
        reingresos = df_merged['patient_id'].value_counts()
        pacientes_con_reingresos = len(reingresos[reingresos > 1])
        st.metric("Pacientes con Reingresos", pacientes_con_reingresos)
    
    st.divider()
 
    #Seccion visual
    col5, col6 = st.columns([1.5, 2], gap="large")
    
    with col5:
        # Gráfico de barras para distribución por severidad
        st.subheader("Distribución por Severidad del Accidente")
        severity_counts = df_merged['accidentSeverity'].value_counts().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = ['#e74c3c', '#f39c12', '#27ae60', '#95a5a6']  # Rojo, Amarillo, Verde, Gris
        
        bars = ax.bar(
            range(len(severity_counts)),
            severity_counts.values,
            color=colors[:len(severity_counts)],
            edgecolor='black',
            linewidth=1.5
        )
        
        # Personalizar ejes
        ax.set_xticks(range(len(severity_counts)))
        ax.set_xticklabels(severity_counts.index, fontsize=18, weight='bold', rotation=0)
        ax.set_ylabel('Cantidad de Ingresos', fontsize=18, weight='bold')
        ax.set_xlabel('Severidad', fontsize=18, weight='bold')
        
        # Agregar valores sobre las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=20,
                weight='bold'
            )
        
        # Añadir cuadrícula
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col6:
        # Gráfico de barras para tipo de accidente
        st.subheader("Ingresos por Tipo de Accidente")
        accident_counts = df_merged['accidentType'].value_counts().sort_values(ascending=True)
        
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        # Crear gráfico de barras horizontales
        colors_gradient = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        bars = ax2.barh(
            range(len(accident_counts)),
            accident_counts.values,
            color=colors_gradient[:len(accident_counts)],
            edgecolor='black',
            linewidth=1.5
        )
        
        # Personalizar ejes
        ax2.set_yticks(range(len(accident_counts)))
        ax2.set_yticklabels(accident_counts.index, fontsize=16, weight='bold')
        ax2.set_xlabel('Cantidad de Ingresos', fontsize=18, weight='bold')
        ax2.set_ylabel('Tipo de Accidente', fontsize=18, weight='bold')
        
        # Agregar valores al final de las barras
        for i, (bar, value) in enumerate(zip(bars, accident_counts.values)):
            width = bar.get_width()
            ax2.text(
                width,
                bar.get_y() + bar.get_height()/2.,
                f' {int(value)}',
                ha='left',
                va='center',
                fontsize=18,
                weight='bold'
            )
        
        # Añadir cuadrícula
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        ax2.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig2)
    
    st.divider()
    
    # Gráfico adicional: Distribución de ingresos por género y severidad
    st.subheader("Severidad de Accidentes por Género")
    
    col7, col8 = st.columns(2, gap="large")
    
    with col7:
        st.write("**Pacientes Masculinos**")
        df_merged_m = df_merged[df_merged['sex'] == 'M']
        
        if len(df_merged_m) > 0:
            severity_m = df_merged_m['accidentSeverity'].value_counts()
            
            fig3, ax3 = plt.subplots(figsize=(18, 12))
            
            bars = ax3.bar(
                range(len(severity_m)),
                severity_m.values,
                color=['#27ae60', '#f39c12', '#e74c3c', '#95a5a6'][:len(severity_m)],
                edgecolor='black',
                linewidth=1.5
            )
            
            ax3.set_xticks(range(len(severity_m)))
            ax3.set_xticklabels(severity_m.index, fontsize=22, weight='bold', rotation=0)
            ax3.set_ylabel('Cantidad de Ingresos', fontsize=26, weight='bold')
            ax3.set_xlabel('Severidad', fontsize=26, weight='bold')
            
            # Agregar valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                ax3.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    fontsize=20,
                    weight='bold'
                )
            
            ax3.grid(axis='y', alpha=0.3, linestyle='--')
            ax3.set_axisbelow(True)
            
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            st.info("No hay datos de pacientes masculinos para los filtros seleccionados")
    
    with col8:
        st.write("**Pacientes Femeninos**")
        df_merged_f = df_merged[df_merged['sex'] == 'F']
        
        if len(df_merged_f) > 0:
            severity_f = df_merged_f['accidentSeverity'].value_counts()
            
            fig4, ax4 = plt.subplots(figsize=(18, 12))
            
            bars = ax4.bar(
                range(len(severity_f)),
                severity_f.values,
                color=['#27ae60', '#f39c12', '#e74c3c', '#95a5a6'][:len(severity_f)],
                edgecolor='black',
                linewidth=1.5
            )
            
            ax4.set_xticks(range(len(severity_f)))
            ax4.set_xticklabels(severity_f.index, fontsize=22, weight='bold', rotation=0)
            ax4.set_ylabel('Cantidad de Ingresos', fontsize=26, weight='bold')
            ax4.set_xlabel('Severidad', fontsize=26, weight='bold')
            
            # Agregar valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                ax4.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    fontsize=20,
                    weight='bold'
                )
            
            ax4.grid(axis='y', alpha=0.3, linestyle='--')
            ax4.set_axisbelow(True)
            
            plt.tight_layout()
            st.pyplot(fig4)
        else:
            st.info("No hay datos de pacientes femeninos para los filtros seleccionados")
            
    st.divider()
    
    # Insights adicionales sobre edad, género y sustancias
    st.subheader("Insights: Edad, Género y Sustancias")
    
    # Preparar datos de sustancias
    df_substance_filtered = df_substance[df_substance['patient_id'].isin(global_filters['filtered_patient_ids'])] if global_filters and 'filtered_patient_ids' in global_filters else df_substance
    
    # Unir con pacientes para obtener edad y género
    df_patient_substance = pd.merge(
        df_pati_filtered,
        df_substance_filtered,
        left_on='id',
        right_on='patient_id',
        how='inner'
    )
    
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    
    with col_insight1:
        # Edad promedio de consumidores vs no consumidores
        if len(df_patient_substance) > 0:
            age_with_substance = df_patient_substance['age'].mean()
            
            # Calcular edad de no consumidores
            all_patients_ids = set(df_pati_filtered['id'].values)
            substance_patients_ids = set(df_substance_filtered['patient_id'].dropna().values)
            non_consumers_ids = all_patients_ids - substance_patients_ids
            
            if len(non_consumers_ids) > 0:
                age_without_substance = df_pati_filtered[df_pati_filtered['id'].isin(non_consumers_ids)]['age'].mean()
                delta_text = f"vs {age_without_substance:.1f} (no consumidores)"
            else:
                delta_text = "Todos consumen"
            
            st.metric(
                "Edad Promedio: Consumidores",
                f"{age_with_substance:.1f} años",
                delta_text
            )
        else:
            st.metric("Edad Promedio: Consumidores", "N/A", "Sin datos")
    
    with col_insight2:
        # Distribución de género en consumidores
        if len(df_patient_substance) > 0:
            unique_consumers = df_patient_substance.drop_duplicates(subset=['patient_id'])
            male_count = len(unique_consumers[unique_consumers['sex'] == 'M'])
            female_count = len(unique_consumers[unique_consumers['sex'] == 'F'])
            total_consumers = male_count + female_count
            
            if total_consumers > 0:
                male_pct = (male_count / total_consumers) * 100
                
                st.metric(
                    "Consumidores: % Masculinos",
                    f"{male_pct:.1f}%",
                    f"{100-male_pct:.1f}% Femeninos"
                )
            else:
                st.metric("Consumidores por Género", "N/A", "Sin datos")
        else:
            st.metric("Consumidores por Género", "N/A", "Sin datos")
    
    with col_insight3:
        # Sustancia más común
        if len(df_substance_filtered) > 0:
            substance_counts = df_substance_filtered['substance_name'].value_counts()
            if len(substance_counts) > 0:
                most_common = substance_counts.idxmax()
                count = substance_counts.max()
                
                st.metric(
                    "Sustancia Más Común",
                    most_common,
                    f"{count} registros"
                )
            else:
                st.metric("Sustancia Más Común", "N/A", "Sin datos")
        else:
            st.metric("Sustancia Más Común", "N/A", "Sin datos")
    
    st.divider()
    
    #Heatmap
    st.subheader("🔥 Mapa de Calor: Tipo de Accidente vs Sustancia Consumida")
    
    # Preparar datos uniendo ingresos con sustancias
    df_substance_filtered = df_substance[df_substance['patient_id'].isin(global_filters['filtered_patient_ids'])] if global_filters and 'filtered_patient_ids' in global_filters else df_substance
    
    # Unir datos de ingresos con sustancias
    df_accident_substance = pd.merge(
        df_merged[['patient_id', 'accidentType', 'sex']],
        df_substance_filtered[['patient_id', 'substance_name']],
        on='patient_id',
        how='inner'
    )
    
    # Eliminar valores nulos
    df_accident_substance = df_accident_substance.dropna()
    
    if len(df_accident_substance) > 0:
        # Pestañas para seleccionar vista
        tab1, tab2, tab3 = st.tabs(["📊 General", "👨 Masculino", "👩 Femenino"])
        
        with tab1:
            st.write("**Relación entre Tipo de Accidente y Sustancia (Todos los Pacientes)**")
            
            # Crear tabla cruzada
            heatmap_data = pd.crosstab(
                df_accident_substance['accidentType'],
                df_accident_substance['substance_name']
            )
            
            # Crear heatmap
            fig_heat, ax_heat = plt.subplots(figsize=(14, 10))
            
            sns.heatmap(
                heatmap_data,
                annot=True,
                fmt='d',
                cmap='YlOrRd',
                cbar_kws={"label": "Número de Pacientes"},
                ax=ax_heat,
                linewidths=2,
                linecolor='white',
                annot_kws={'size': 14, 'weight': 'bold'}
            )
            
            ax_heat.set_title('Tipo de Accidente vs Sustancia Consumida', fontsize=20, weight='bold', pad=20)
            ax_heat.set_xlabel('Sustancia', fontsize=16, weight='bold')
            ax_heat.set_ylabel('Tipo de Accidente', fontsize=16, weight='bold')
            
            plt.xticks(rotation=45, ha='right', fontsize=14, weight='bold')
            plt.yticks(rotation=0, fontsize=14, weight='bold')
            
            plt.tight_layout()
            st.pyplot(fig_heat)
        
        with tab2:
            st.write("**Relación entre Tipo de Accidente y Sustancia (Solo Hombres)**")
            
            df_male = df_accident_substance[df_accident_substance['sex'] == 'M']
            
            if len(df_male) > 0:
                heatmap_male = pd.crosstab(
                    df_male['accidentType'],
                    df_male['substance_name']
                )
                
                fig_male, ax_male = plt.subplots(figsize=(14, 10))
                
                sns.heatmap(
                    heatmap_male,
                    annot=True,
                    fmt='d',
                    cmap='Blues',
                    cbar_kws={"label": "Número de Pacientes"},
                    ax=ax_male,
                    linewidths=2,
                    linecolor='white',
                    annot_kws={'size': 14, 'weight': 'bold'}
                )
                
                ax_male.set_title('Accidentes vs Sustancias - Hombres', fontsize=20, weight='bold', pad=20)
                ax_male.set_xlabel('Sustancia', fontsize=16, weight='bold')
                ax_male.set_ylabel('Tipo de Accidente', fontsize=16, weight='bold')
                
                plt.xticks(rotation=45, ha='right', fontsize=14, weight='bold')
                plt.yticks(rotation=0, fontsize=14, weight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_male)
            else:
                st.info("No hay datos de hombres con consumo de sustancias")
        
        with tab3:
            st.write("**Relación entre Tipo de Accidente y Sustancia (Solo Mujeres)**")
            
            df_female = df_accident_substance[df_accident_substance['sex'] == 'F']
            
            if len(df_female) > 0:
                heatmap_female = pd.crosstab(
                    df_female['accidentType'],
                    df_female['substance_name']
                )
                
                fig_female, ax_female = plt.subplots(figsize=(14, 10))
                
                sns.heatmap(
                    heatmap_female,
                    annot=True,
                    fmt='d',
                    cmap='RdPu',
                    cbar_kws={"label": "Número de Pacientes"},
                    ax=ax_female,
                    linewidths=2,
                    linecolor='white',
                    annot_kws={'size': 14, 'weight': 'bold'}
                )
                
                ax_female.set_title('Accidentes vs Sustancias - Mujeres', fontsize=20, weight='bold', pad=20)
                ax_female.set_xlabel('Sustancia', fontsize=16, weight='bold')
                ax_female.set_ylabel('Tipo de Accidente', fontsize=16, weight='bold')
                
                plt.xticks(rotation=45, ha='right', fontsize=14, weight='bold')
                plt.yticks(rotation=0, fontsize=14, weight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_female)
            else:
                st.info("No hay datos de mujeres con consumo de sustancias")
        
        # Interpretación
        with st.expander("ℹ️ Cómo interpretar estos mapas de calor"):
            st.markdown("""
            **¿Qué muestra cada celda?**
            - El **número** indica cuántos pacientes con ese tipo de accidente consumían esa sustancia
            - **Colores más oscuros** = Mayor cantidad de pacientes
            - **Colores más claros** = Menor cantidad de pacientes
            
            **Ejemplos de análisis:**
            - Si "moto-moto" + "marihuana" tiene un número alto, significa que muchos accidentes de moto están relacionados con consumo de marihuana
            - Si "auto-auto" + "alcohol" es alto, hay una fuerte relación entre accidentes de auto y alcohol
            - Puedes comparar entre géneros para ver si hay diferencias en patrones de consumo por tipo de accidente
            
            **Pestañas:**
            - 📊 **General**: Todos los pacientes
            - 👨 **Masculino**: Solo hombres (colores azules)
            - 👩 **Femenino**: Solo mujeres (colores rosa/morado)
            """)
        
        # Insights clave
        st.subheader("Combinaciones Más Comunes")
        
        # Encontrar las combinaciones más frecuentes
        top_combinations = df_accident_substance.groupby(['accidentType', 'substance_name']).size().reset_index(name='count')
        top_combinations = top_combinations.sort_values('count', ascending=False).head(5)
        
        st.write("**Top 5 Combinaciones: Tipo de Accidente + Sustancia**")
        
        for idx, row in top_combinations.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"🚗 **{row['accidentType']}**")
            with col2:
                st.write(f"💊 **{row['substance_name']}**")
            with col3:
                st.metric("Pacientes", int(row['count']))
        
        # Comparación por género
        st.divider()
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.write("**👨 Accidente más común en hombres con sustancias:**")
            male_data = df_accident_substance[df_accident_substance['sex'] == 'M']
            if len(male_data) > 0:
                most_common_male = male_data['accidentType'].value_counts().idxmax()
                count_male = male_data['accidentType'].value_counts().max()
                st.info(f"🚗 **{most_common_male}** ({count_male} casos)")
            else:
                st.info("Sin datos")
        
        with col_comp2:
            st.write("**👩 Accidente más común en mujeres con sustancias:**")
            female_data = df_accident_substance[df_accident_substance['sex'] == 'F']
            if len(female_data) > 0:
                most_common_female = female_data['accidentType'].value_counts().idxmax()
                count_female = female_data['accidentType'].value_counts().max()
                st.info(f"🚗 **{most_common_female}** ({count_female} casos)")
            else:
                st.info("Sin datos")
    else:
        st.warning("⚠️ No hay datos suficientes para generar el mapa de calor con los filtros seleccionados.")