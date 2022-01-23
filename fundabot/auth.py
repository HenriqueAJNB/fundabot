import json

from fundabot.paths import CREDENTIALS_DIR


def get_telegram_token():
    with open(CREDENTIALS_DIR / "telegram.json", "r") as file:
        credentials = json.load(file)
    return credentials["TOKEN"]
