import logging
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_location_interactive(df):
        # Validar columnas necesarias
        required_columns = ['este', 'norte', 'dureza']
        for col in required_columns:
            if col not in df.columns:
                logging.error(f"Falta la columna requerida: {col}")
                raise ValueError(f"El archivo no contiene la columna '{col}' necesaria para la visualización interactiva.")
        try:
            # Definir mapeo de colores desaturados para Plotly
            color_mapping = {
                "roca suave": "#98FB98",    # verde menta pastel
                "roca media": "#FFD700",    # amarillo más cercano al original
                "roca dura": "#8B0000",      # rojo más oscuro
                "roca muy dura": "#BA55D3"   # lavanda más brillante, cercano al original
            }
            # Preparar hover data para incluir drill pattern si existe
            hover_data = None
            if "drill_pattern" in df.columns:
                hover_data = ["drill_pattern", "pozo","duracion"]

            fig = px.scatter(
                df,
                x='este',
                y='norte',
                color='dureza',
                color_discrete_map=color_mapping,
                title="Ubicación Interactiva de Pozos (Este vs Norte)",
                labels={"este": "Este", "norte": "Norte", "dureza": "Dureza"},
                hover_data=hover_data
            )
            fig.update_layout(legend_title_text='Dureza')
            logging.info("Gráfica interactiva de ubicación generada correctamente.")
            return fig
        except Exception as e:
            logging.exception("Error generando gráfica interactiva de ubicación")
            raise Exception(f"Error al generar la gráfica interactiva de ubicación: {e}")

    @staticmethod
    def plot_dureza_count(df):
        try:
            # Contar la cantidad de pozos por dureza
            conteo_dureza = df['dureza'].value_counts().reset_index()
            conteo_dureza.columns = ['dureza', 'conteo']

            # Mapeo de colores desaturados para Plotly
            color_mapping = {
                "roca suave": "#98FB98",    # verde menta pastel
                "roca media": "#FFD700",    # amarillo más cercano al original
                "roca dura": "#8B0000",      # rojo pastel
                "roca muy dura": "#BA55D3"   # lavanda más brillante, cercano al original
            }
            fig = px.pie(
                conteo_dureza,
                names='dureza',
                values='conteo',
                color='dureza',
                color_discrete_map=color_mapping,
                title='Conteo de Pozos por Dureza'
            )
            logging.info("Gráfica de torta de conteo de pozos por dureza generada correctamente.")
            return fig
        except Exception as e:
            logging.exception("Error generando gráfica de torta de conteo de pozos por dureza")
            raise Exception(f"Error al generar la gráfica de torta de conteo de pozos por dureza: {e}")

    @staticmethod
    def plot_duracion_box(df):
        try:
            # Definir mapeo de colores desaturados para Plotly
            color_mapping = {
                "roca suave": "#98FB98",    # verde menta pastel
                "roca media": "#FFD700",    # amarillo más cercano al original
                "roca dura": "#FFA07A",      # rojo pastel
                "roca muy dura": "#BA55D3"   # lavanda más brillante, cercano al original
            }

            fig = px.box(
                df,
                x="dureza",
                y="duracion",
                color="dureza",
                color_discrete_map=color_mapping,
                title="Distribución de Duración por Dureza",
                labels={"duracion": "Duración (minutos)", "dureza": "Dureza"}
            )
            logging.info("Gráfico box plot de duración por dureza generado correctamente.")
            return fig
        except Exception as e:
            logging.exception("Error generando gráfico box plot")
            raise Exception(f"Error al generar el gráfico box plot: {e}")
