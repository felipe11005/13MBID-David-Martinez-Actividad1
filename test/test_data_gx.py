import pandas as pd

def test_great_expectations():
    """Test para verificar que los datos cumplen con las expectativas definidas
    en un archivo de Great Expectations.

    Raises:
        AssertionError: Si alguna de las expectativas no se cumple.
    """
    # Cargar los datos
    df = pd.read_csv("data/raw/bank-additional-full.csv", sep=';')

    results = {
        "success": True,
        "expectations": [],
        "statistics": {"success_count": 0, "total_count": 0}
    }

    def add_expectation(expectation_name, condition, message=""):
        results["statistics"]["total_count"] += 1
        if condition:
            results["statistics"]["success_count"] += 1
            results["expectations"].append({
                "expectation": expectation_name,
                "success": True
            })
        else:
            results["success"] = False
            results["expectations"].append({
                "expectation": expectation_name,
                "success": False,
                "message": message
            })
    
    # Validaciones a verificar sobre los datos
    add_expectation(
        "age_range",
        df["age"].between(18, 100).all(),
        "La columna 'age' no está en el rango esperado (18-100)."
    )
    add_expectation(
        "target_values",
        df["y"].isin(["yes", "no"]).all(),
        "La columna 'y' contiene valores no válidos."
    )


    # Non negative conditions

    # Duration is in seconds, must be > 0
    add_expectation(
        "duration_positive",
        (df["duration"] > 0).all(),
        "'duration' debe ser > 0."
    )

    # Number of contacts on campaign must be > 0
    add_expectation(
        "campaign_ge_1",
        (df["campaign"] >= 1).all(),
        "'campaign' debe ser >= 1."
    )

    # pdays is in Days, it must be > 0, even 999(never contacted means > 0)
    add_expectation(
        "pdays_valid_values",
        ((df["pdays"] == 999) | (df["pdays"] >= 0)).all(),
        "'pdays' debe ser 999 (no contactado) o >= 0."
    )

    # Conditions based on coposed columns

    # If previous is >0, pdays != 999
    # It means that, if there are contact previous this campoaging, tha field
    # pdays cannot say that this person was never contacted.
    cond_prev_gt0 = (df["previous"] > 0)
    add_expectation(
        "previous_gt0_implies_pdays_not_999",
        (df.loc[cond_prev_gt0, "pdays"] != 999).all(),
        "Si 'previous' > 0, 'pdays' no debería ser 999."
    )

    