from fundabot.business_rules import (
    filter_divivend_yield,
    filter_healthy_fi,
    filter_liquidity,
    filter_pvp,
    remove_negative_returns,
)
from fundabot.crawler import crawl_funds
from fundabot.preprocess import format_data


def select_funds():

    fi_raw = crawl_funds()

    fi_formated = format_data(fi_raw)

    fi_selected = (
        fi_formated.pipe(filter_divivend_yield, 0.05)
        .pipe(filter_pvp, 0.4, 1.1)
        .pipe(filter_healthy_fi, 500_000)
        .pipe(filter_liquidity, 100_000)
        .pipe(remove_negative_returns)
    )

    return fi_selected


if __name__ == "__main__":
    select_funds()
