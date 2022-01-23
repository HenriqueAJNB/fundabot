import pandas as pd


def filter_divivend_yield(df: pd.DataFrame, min_div_yield: float) -> pd.DataFrame:
    """Aplica filtro para manter apenas os FI's com dividend yield acima de um determinado valor.

    Args:
        df (pd.DataFrame): Dataframe com as informações dos FII's já formatadas
        min_div_yield (float): Valor mínimo mantido em número decimal: 4% = 0.04
    """
    return df[df["dividend_yield"] >= min_div_yield]


def filter_pvp(df: pd.DataFrame, min: float, max: float) -> pd.DataFrame:
    """Filtra o kpi p/vp entre os valores especificados

    Args:
        df (pd.DataFrame): Dataframe com as informações dos FI's já formatadas
        min (float): FII's com p/vp abaixo deste valor serão eliminados
        max (float): FII's com p/vp acima deste valor serão eliminados
    """
    return df[df["p/vp"].between(min, max)]


def filter_healthy_fi(df: pd.DataFrame, min: float) -> pd.DataFrame:
    """Seleciona apenas os FI's com valor patrimonial maior que o valor mínimo.

    Args:
        df (pd.DataFrame): Dataframe com as informações dos FI's já formatadas
        min (float): FII's com patrimônio líquido abaixo deste valor serão eliminados
    """
    return df[df["patrimonio_liquido"] >= min]


def filter_liquidity(df: pd.DataFrame, min: float) -> pd.DataFrame:
    """Seleciona apenas os FI's com liquidez maior que o valor mínimo.

    Args:
        df (pd.DataFrame): Dataframe com as informações dos FI's já formatadas
        min (float): FII's com liquidez abaixo deste valor serão eliminados
    """
    return df[df["liquidez_diaria"] >= min]


def remove_negative_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove FI's com rentabilidade no mês negativa.

    Args:
        df (pd.DataFrame): Dataframe com as informações dos FI's já formatadas
    """
    return df[df["rentabilidade_mes"] > 0]
