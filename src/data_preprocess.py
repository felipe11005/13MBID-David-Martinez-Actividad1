import pandas as pd
import numpy as np


INPUT_CSV = 'data/raw/bank-additional-full.csv'
OUTPUT_CSV = 'data/processed/bank-processed.csv'


def preprocess_data(input_path=INPUT_CSV, output_path=OUTPUT_CSV):
    # Load the dataset
    df = pd.read_csv(input_path, sep=';')
    
    # Adaptar nombres de columnas
    df.columns = df.columns.str.replace(".", "_")

    # Transformar los valores 'unknown' en NaN
    df.replace('unknown', np.nan, inplace=True)

    # Se elimina la columna 'default' ya que tiene muchos valores desconocidos
    df.drop(columns=["default"], inplace=True)

    # Se hace un filtro para eliminar las filas que tienen valores nulos
    df.dropna(inplace=True)
    
    # Se hace un filtro para eliminar las filas duplicadas
    df.drop_duplicates(inplace=True)

    # Se mapea education para reunir todos los basic_school, además de poner un prefijo a modo de ranking
    education_mapper = {
        "illiterate": "0-illiterate",
        "unknown": "0-unknown",
        "basic.4y": "1-basic_school",
        "basic.6y": "1-basic_school",
        "basic.9y": "1-basic_school",
        "high.school": "2-high_school",
        "professional.course": "3-professional_course",
        "university.degree": "4-university_degree",        
    }
    df["education"] = df["education"].map(education_mapper)

    # Save the processed dataset
    df.to_csv(output_path, index=False)

    return df.shape, df["education"].unique()


if __name__ == "__main__":
    dimensiones, educations = preprocess_data()
    with open('docs/transformations.txt', 'w') as f:
        f.write("Transformaciones realizadas:\n")
        f.write("- Se reemplazaron los valores 'unknown' por NaN\n")
        f.write("- Se eliminaron las filas con valores nulos\n")
        f.write("- Se eliminaron las filas duplicadas\n")
        f.write("- Se eliminó la columna 'default' debido a la alta cantidad de valores desconocidos\n")
        f.write(f"- Cantidad de filas finales: {dimensiones[0]}\n")
        f.write(f"- Cantidad de columnas finales: {dimensiones[1]}\n")
        f.write(f"- Columna Educación: {sorted(educations)}\n")