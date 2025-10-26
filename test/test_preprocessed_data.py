import pandas as pd

import pytest

@pytest.fixture
def datos_banco():
    """Fixture para cargar los datos del banco desde un archivo CSV.
    Returns:
        pd.DataFrame: DataFrame que contiene los datos del banco.
    """
    df = pd.read_csv("data/processed/bank-processed.csv", sep=',')
    return df

def test_education_mapped(datos_banco):
    valid_education = {
        "0-illiterate", "1-basic_school", "2-high_school",
        "3-professional_course", "4-university_degree"
    }

    assert datos_banco["education"].isin(valid_education).all()