import logging

from fundabot.paths import LOG_DIR

FORMAT = "%(asctime)s:[%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] : %(message)s"

# Enable logging
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    datefmt="%H:%M:%S",
    filename=LOG_DIR / "bot.log",
)

logger = logging.getLogger(__name__)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(FORMAT))

logger.addHandler(console)
