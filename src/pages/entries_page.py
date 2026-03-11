import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show(global_filters=None):
    
    df_ent = pd.read_csv("src/data/data_entries.csv")
    df_pati = pd.read_csv("src/data/data_patient.csv")
    
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
        
    
    
    
    
   