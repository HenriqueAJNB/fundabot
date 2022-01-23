import pandas as pd
from numpy import NaN

from fundabot.paths import DATA_DIR


def str_to_float(string):
    factor_convert = {"mi": 1_000_000, "bi": 1_000_000_000}
    splited = string.split()

    if len(splited) == 3:
        _, value, multiplier_str = string.split()
        value = value.replace(".", "").replace(",", ".")
        value = float(value) * factor_convert[multiplier_str]
    elif len(splited) == 2:
        _, value = string.split()
        value = value.replace(".", "").replace(",", ".")
        value = float(value)
    return value


def format_data(df):
    df = pd.read_csv(DATA_DIR / "fund_infos.csv", sep=";", dtype="object")

    df.columns = [
        "nome",
        "preco",
        "liquidez_diaria",
        "ultimo_rendimento",
        "dividend_yield",
        "patrimonio_liquido",
        "valor_patrimonial",
        "rentabilidade_mes",
        "p/vp",
    ]

    df.replace({"N/A": NaN}, inplace=True)

    df.dropna(how="any", inplace=True)

    df["preco"] = (
        df["preco"]
        .str.replace("R$ ", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )

    df["liquidez_diaria"] = df["liquidez_diaria"].str.replace(".", "", regex=False).astype("int")

    df["ultimo_rendimento"] = (
        df["ultimo_rendimento"]
        .str.replace("R$ ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )

    df["dividend_yield"] = (
        df["dividend_yield"]
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )

    df["patrimonio_liquido"] = df["patrimonio_liquido"].apply(str_to_float)

    df["valor_patrimonial"] = (
        df["valor_patrimonial"]
        .str.replace("R$ ", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )

    df["rentabilidade_mes"] = (
        df["rentabilidade_mes"]
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )

    df["p/vp"] = (
        df["p/vp"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype("float")
    )
    return df
