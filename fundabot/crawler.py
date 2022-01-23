import concurrent.futures
from functools import partial

import pandas as pd
import requests
from bs4 import BeautifulSoup

from fundabot.logs import logger
from fundabot.paths import DATA_DIR

base_url = "https://www.fundsexplorer.com.br/funds/"
req_base = requests.get(base_url)


def collect_fund_data(block, output_df):
    name = block.div.a.span.text

    block_url = base_url + name.lower()

    try:
        req_block = requests.get(block_url)
    except TimeoutError:
        logger.error(f"Timeout: {name}")
        return None

    if req_block.status_code == 200:
        soup_block = BeautifulSoup(req_block.content, "html.parser")

        price = soup_block.find("span", {"class": "price"}).text.strip()

        row = [name, price]

        indicator_values = soup_block.find_all("span", {"class": "indicator-value"})

        for value in indicator_values:
            row.append(value.text.strip())

        output_df.loc[len(output_df)] = row

        output_df.iloc[[-1], :].to_csv(
            DATA_DIR / "fund_infos.csv", sep=";", index=False, mode="a", header=False
        )

        logger.info(f"{name} --> sucesso")

    else:
        logger.warning(f"{name} retornou status {req_block.status_code}")


def crawl_funds():

    clear_fund_infos()

    soup_base = BeautifulSoup(req_base.content, "html.parser")

    infos = pd.DataFrame(
        columns=[
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
    )

    blocks = soup_base.find_all("div", {"class": "col-md-3 col-xs-12"})

    partial_collect_fund = partial(collect_fund_data, output_df=infos)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(partial_collect_fund, blocks)

    df = pd.read_csv(DATA_DIR / "fund_infos.csv", sep=";", header=None, dtype="object")

    return df


def clear_fund_infos():
    with open(DATA_DIR / "fund_infos.csv", "r+") as f:
        f.truncate(0)
        f.write(
            "nome;preco;liquidez_diaria;ultimo_rendimento;dividend_yield;patrimonio_liquido;valor_patrimonial;rentabilidade_mes;p/vp\n"
        )
