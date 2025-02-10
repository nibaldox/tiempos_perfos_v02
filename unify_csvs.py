import os
import glob
import pandas as pd

def main():
    # Buscar todos los archivos CSV en la carpeta 'input-data'
    csv_files = glob.glob(os.path.join("input-data", "*.csv"))
    if not csv_files:
        print("No se encontraron archivos CSV en 'input-data'.")
        return

    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
            print(f"Archivo '{file}' cargado, filas: {len(df)}.")
        except Exception as e:
            print(f"Error al leer '{file}': {e}")

    # Unificar los DataFrames asumiendo que tienen la misma estructura
    unified_df = pd.concat(dataframes, ignore_index=True)
    print(f"DataFrame unificado, total de filas: {len(unified_df)}.")
    print("Columnas:", list(unified_df.columns))

    # Guardar el DataFrame unificado en un nuevo archivo CSV
    output_path = os.path.join("input-data", "unificado.csv")
    try:
        unified_df.to_csv(output_path, index=False)
        print(f"Archivo unificado guardado como '{output_path}'.")
    except Exception as e:
        print(f"Error al guardar el archivo unificado: {e}")

if __name__ == "__main__":
    main()
