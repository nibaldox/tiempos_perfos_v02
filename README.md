# Tiempos de Perforación - Clasificador de Pozos

Este proyecto es una aplicación desarrollada en Python para procesar y clasificar datos de pozos perforados, y para visualizar dicha información de forma gráfica. La aplicación utiliza Streamlit para la interfaz de usuario, y herramientas de visualización (Plotly) para mostrar resultados de clasificación y ubicación.

## Estructura del Proyecto

El proyecto se encuentra organizado en módulos separados que facilitan el mantenimiento y escalabilidad del código:

- **streamlit_app.py**  
  Contiene la aplicación principal de Streamlit, que gestiona la interfaz de usuario, la carga de datos, el procesamiento y la visualización.

- **data_processor.py**  
  Contiene la clase `DataProcessor`, encargada de cargar, procesar y clasificar los datos de entrada (archivos CSV).
  - Convierte columnas de tiempo a formato datetime.
  - Calcula la duración en minutos entre "tiempo inicio" y "tiempo final".
  - Clasifica la dureza del pozo (roca suave, roca media, roca dura, roca muy dura) basándose en la duración.

- **visualizer.py**  
  Contiene la clase `Visualizer`, la cual genera gráficos a partir de los datos procesados.
  - `plot_location_interactive`: Genera un scatter plot interactivo para visualizar la ubicación de los pozos (basado en columnas 'este', 'norte' y 'dureza'), con colores según la dureza y la opción de mostrar el drill pattern en el hover.
  - `plot_dureza_count`: Crea un gráfico de torta interactivo con Plotly para mostrar el conteo de pozos por dureza.
  - `plot_duracion_box`: Crea un gráfico box plot interactivo para la distribución de la duración por dureza.
  - `plot_tiempo_promedio_dureza`: Crea un gráfico de torta interactivo con Plotly para el tiempo promedio de perforación por dureza.

- **logs/**  
  Carpeta (crearse manualmente si no existe) para almacenar el archivo de logging `app.log`, donde se registran eventos y errores.

- **input-data/**  
  Directorio para almacenar archivos CSV de entrada. Ejemplos:
  - `Detalle de Pozos Perforados_nov24.csv`
  - `Detalle de Pozos Perforados_oct24.csv`
  - `unificado.csv`

## Requisitos

- Python 3.x
- Bibliotecas:
  - pandas
  - plotly
  - streamlit

## Cómo Ejecutar la Aplicación

1. Asegúrate de tener instaladas las dependencias necesarias (puedes instalarlas usando pip si es necesario):

```bash
pip install pandas plotly streamlit
```

2. Coloca tus archivos CSV en el directorio **input-data/** (o en cualquier ubicación a la que apuntes durante la ejecución).
3. Ejecuta la aplicación desde la terminal:

```bash
streamlit run streamlit_app.py
```

4. Usa la interfaz de Streamlit para:
   - **Cargar CSV:** Selecciona el archivo CSV unificado para procesar y clasificar.
   - **Visualizar gráficos:** Explora los datos a través de los gráficos interactivos disponibles.
   - **Filtro por Drill Pattern:** Filtra los resultados por el valor de la columna "drill_pattern".

## Notas

- La aplicación intenta detectar el tema del navegador, pero la configuración del tema de Streamlit no se puede modificar directamente desde la aplicación.
- Asegúrate de que los nombres de las columnas del CSV sean consistentes o se estandarizan al cargarse.
- La aplicación realiza validación de columnas y manejo de errores para ayudar a identificar problemas con el archivo de entrada.
- Se actualizó el color de la categoría "roca dura" en los gráficos a un tono más brillante (#FF0000) para mejor visibilidad.

## Licencia

Este proyecto se distribuye bajo licencia MIT.
