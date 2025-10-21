import pandas as pd
import numpy as np

from pandera.pandas import DataFrameSchema, Column
import pytest

@pytest.fixture
def datos_banco():
    df = pd.read_csv("data/raw/bank-additional-full.csv", sep=';')
    return df


def test_esquema(datos_banco):
    df = datos_banco
    esquema = DataFrameSchema({
        "age": Column(int, nullable=False),
        "job": Column(str, nullable=False),
        "marital": Column(str, nullable=False),
        "education": Column(str, nullable=False),
        "default": Column(str, nullable=True),
        "housing": Column(str, nullable=False),
        "loan": Column(str, nullable=False),
        "y": Column(str, nullable=False)
        # TODO: completar el resto de columnas
    })

    esquema.validate(df)