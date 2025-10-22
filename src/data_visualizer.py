import pandas as pd
from pandas import DataFrame
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración general
sns.set(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (8, 5)

warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=UserWarning)

def save_success_rate_by_2dim(df:DataFrame, col1:str, col2:str, destination_path:str):
    df['y_numeric'] = df['y'].map({'yes':1, 'no':0})
    pivot = df.pivot_table(values='y_numeric', index=col1, columns=col2, aggfunc='mean')
    df.drop("y_numeric", axis=1, inplace = True)
    plt.figure(figsize=(7, 5))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title(f"Tasa de éxito por {col1} y {col2}")
    plt.ylabel(col1)
    plt.xlabel(col2)
    plt.savefig(f"{destination_path}/success_rate_by_{col1}_and_{col2}.png")
    plt.close()

def save_target_proprotion_by_job(df:DataFrame, destination_path:str):
    df['y_numeric'] = df['y'].map({'yes': 1, 'no': 0})

    plt.figure(figsize=(12,6))
    sns.barplot(
        data=df, 
        x='job', 
        y='y_numeric', 
        estimator='mean', 
        order=df['job'].value_counts().index
    )
    df.drop("y_numeric", axis=1, inplace = True)
    plt.xticks(rotation=45)
    plt.title("Tasa de éxito de la campaña por ocupación")
    plt.ylabel("Proporción de 'sí'")
    plt.xlabel("Ocupación")
    plt.savefig(f"{destination_path}/success_rate_by_job.png")
    plt.close()

def save_distribution_by_column(df:DataFrame, col:str, destination_path:str):
    plt.figure(figsize=(8, 4))
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(f"{destination_path}/{col}_distribution.png")
    plt.close()

def visualize_data(
    source_path:str = "data/raw/bank-additional-full.csv",
    destination_path:str = "docs/figures/"
    ):

    Path(destination_path).mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(source_path, sep=';')

    # Figure # 1 Distribución del target
    plt.figure(figsize=(8, 6))
    sns.countplot(x="y", data=df)
    plt.title("Distribución de la variable objetivo (suscripción al depósito)")
    plt.xlabel("¿Suscribió un depósito a plazo?")
    plt.ylabel("Cantidad de clientes")
    plt.savefig(f"{destination_path}/target_distribution.png")
    plt.close()

    # Figure # 2 distirbución de educación
    save_distribution_by_column(df, "education", destination_path)

    # Figure # 3 Matriz de correlación
    num_df = df.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlaciones')
    plt.savefig(f"{destination_path}/correlation_matrix.png")
    plt.close()

    # Figure # 4 distirbución de ocupación
    save_distribution_by_column(df, "job", destination_path)

    # Figure # 5 Tasa de exito por educación
    save_target_proprotion_by_job(df, destination_path)

    # Figure # 6 Tasa de exito por educación y ocupación
    save_success_rate_by_2dim(df, "education", "job", destination_path)

    # Figure # 7 Tasa de exito por medio de contacto y mes
    save_success_rate_by_2dim(df, "contact", "month", destination_path)


if __name__ == "__main__":
    visualize_data()