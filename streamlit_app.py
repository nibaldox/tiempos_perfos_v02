import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from visualizer import Visualizer
import plotly.express as px
from typing import Optional
from io import BytesIO

# Configuración para que la página use todo el ancho
st.set_page_config(layout="wide")

# Intenta detectar el tema del navegador
try:
    streamlit_theme = st.get_option("theme.base")
except Exception:
    streamlit_theme = "light"


@st.cache_data
def cargar_datos(uploaded_file: BytesIO) -> pd.DataFrame:
    """
    Carga y procesa los datos desde un archivo CSV.

    Args:
        uploaded_file (BytesIO): Archivo CSV subido por el usuario.

    Returns:
        pd.DataFrame: DataFrame procesado con las clasificaciones de dureza.
    """
    data_processor = DataProcessor()
    df_processed: pd.DataFrame = data_processor.load_and_process(uploaded_file)
    return df_processed


def main() -> None:
    """
    Función principal que ejecuta la aplicación Streamlit para clasificar y visualizar datos de pozos perforados.
    """
    st.title("Clasificador de Pozos - Aplicación Streamlit")

    st.markdown("""
    Esta aplicación permite cargar un archivo CSV, procesarlo y visualizar gráficos utilizando Streamlit.

    **Funcionalidades:**
    - Cargar archivo CSV y clasificar datos.
    - Visualizar gráficos en una grilla 2x2:
        - Fila 1: Box Plot y Torta.
        - Fila 2: Ubicación de Pozos (con y sin filtro).
    - Filtrar por drill pattern.
    """)

    # Aplicar estilos personalizados
    st.markdown(
        """
        <style>
        .css-1aumxhk {
            background-color: #f0f2f6;
        }
        .css-ffhzg2 {
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Subir archivo CSV
    uploaded_file: Optional[BytesIO] = st.file_uploader("Carga tu archivo CSV", type="csv")
    if uploaded_file is not None:
        try:
            # Cargar y procesar datos con caché
            df_processed: pd.DataFrame = cargar_datos(uploaded_file)
            st.success("Archivo CSV cargado y procesado exitosamente.")

            # Filtro por drill pattern
            if "drill_pattern" in df_processed.columns:
                with st.sidebar:
                    st.subheader("Filtro por Drill Pattern")
                    # Ordenar la lista de drill patterns en orden descendente
                    drill_patterns: list = sorted(df_processed["drill_pattern"].astype(str).unique(), reverse=True)
                    drill_pattern_seleccionado: list = st.multiselect("Selecciona Drill Patterns:", drill_patterns)

                    if drill_pattern_seleccionado:
                        df_filtrado: pd.DataFrame = df_processed[df_processed["drill_pattern"].isin(drill_pattern_seleccionado)]
                    else:
                        df_filtrado: pd.DataFrame = df_processed.copy()
                        st.sidebar.info("Mostrando todos los Drill Patterns.")
            else:
                df_filtrado: pd.DataFrame = df_processed.copy()
                st.sidebar.info("No se encontró la columna 'drill_pattern'. Mostrando todos los datos.")

            # Opciones de visualización
            st.sidebar.header("Opciones de Visualización")
            mostrar_box_plot: bool = st.sidebar.checkbox("Mostrar Box Plot", value=True)
            mostrar_torta: bool = st.sidebar.checkbox("Mostrar Gráfico de Torta", value=True)
            mostrar_ubicacion_equipo: bool = st.sidebar.checkbox("Mostrar Gráficos de Ubicación", value=True)

            # Crear la grilla de 2x2
            col1, col2 = st.columns(2)

            # Gráfico Box Plot (col1, fila 1)
            if mostrar_box_plot:
                with col1:
                    st.subheader("Distribución de Duración por Dureza (Box Plot)")
                    fig_box: px.Figure = Visualizer.plot_duracion_box(df_filtrado)
                    st.plotly_chart(fig_box, use_container_width=True, key="box_plot")

            # Gráfico Torta (col2, fila 1)
            if mostrar_torta:
                with col2:
                    st.subheader("Tiempo Promedio por Dureza (Torta)")
                    fig_pie: px.Figure = Visualizer.plot_dureza_count(df_filtrado)
                    st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")

            # Gráfico de Ubicación con y sin filtro (fila 2)
            if mostrar_ubicacion_equipo:
                with col1:
                    st.subheader("Ubicación de Pozos (Filtrado)")
                    fig_ubicacion_filtrado: px.Figure = Visualizer.plot_location_interactive(df_filtrado)
                    st.plotly_chart(fig_ubicacion_filtrado, use_container_width=True, key="filtered_location")

                with col2:
                    st.subheader("Ubicación de Pozos (Sin Filtrar)")
                    fig_ubicacion: px.Figure = Visualizer.plot_location_interactive(df_processed)
                    st.plotly_chart(fig_ubicacion, use_container_width=True, key="unfiltered_location")

        except ValueError as ve:
            st.error(f"Error de validación: {ve}")
        except Exception as e:
            st.error(f"Error al procesar o visualizar los datos: {e}")
    else:
        st.info("Esperando que se suba un archivo CSV.")


if __name__ == "__main__":
    main()
