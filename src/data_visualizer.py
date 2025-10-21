import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración general
sns.set(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (8, 5)

warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=UserWarning)

def visualize_data(
    source_path:str = "data/raw/bank-additional-full.csv",
    destination_path:str = "docs/figures/"
    ):

    Path(destination_path).mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(source_path, sep=';')

    # Figure # 1
    plt.figure(figsize=(8, 6))
    sns.countplot(x="y", data=df)
    plt.title("Distribución de la variable objetivo (suscripción al depósito)")
    plt.xlabel("¿Suscribió un depósito a plazo?")
    plt.ylabel("Cantidad de clientes")
    plt.savefig(f"{destination_path}/target_distribution.png")
    plt.close()

    # Figure # 2
    plt.figure(figsize=(8, 4))
    col = "education"
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(f"{destination_path}/education_distribution.png")
    plt.close()

    # Figure # 3
    num_df = df.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlaciones')
    plt.savefig(f"{destination_path}/correlation_matrix.png")
    plt.close()

    # Figure # 4
    plt.figure(figsize=(8, 4))
    col = "job"
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(f"{destination_path}/job_distribution.png")
    plt.close()


if __name__ == "__main__":
    visualize_data()