import logging
import pandas as pd

# Configuración básica para logging
logging.basicConfig(filename="app.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

class DataProcessor:
    REQUIRED_COLUMNS = ['tiempo inicio', 'tiempo final']

    def load_and_process(self, file_path):
        logging.info(f"Iniciando carga del archivo: {file_path}")
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            logging.exception("Error leyendo el archivo")
            raise Exception(f"Error al leer el archivo: {e}")

        # Estandarizar nombres de columnas a minúsculas y sin espacios extremos.
        df.columns = [col.strip().lower() for col in df.columns]
        logging.debug(f"Columnas del archivo: {df.columns.tolist()}")

        # Validar columnas requeridas
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                logging.error(f"Falta la columna requerida: {col}")
                raise ValueError(f"El archivo no contiene la columna requerida '{col}'.")

        try:
            df['tiempo inicio'] = pd.to_datetime(df['tiempo inicio'])
            df['tiempo final'] = pd.to_datetime(df['tiempo final'])
            df['duracion'] = (df['tiempo final'] - df['tiempo inicio']).dt.total_seconds() / 60.0
        except Exception as e:
            logging.exception("Error en el cálculo de la duración")
            raise Exception(f"Error al procesar los tiempos: {e}")

        try:
            df['dureza'] = df['duracion'].apply(self.classify_duracion)
        except Exception as e:
            logging.exception("Error al clasificar la duración")
            raise Exception(f"Error al clasificar la duración: {e}")

        logging.info("Archivo procesado exitosamente.")
        return df

    def classify_duracion(self, minutos):
        if minutos < 20:
            return "roca suave"
        elif minutos < 30:
            return "roca media"
        elif minutos < 45:
            return "roca dura"
        else:
            return "roca muy dura"
