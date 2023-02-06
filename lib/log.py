import os
import logging


logging.basicConfig(
    level=logging.WARNING,
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    format="%(asctime)s %(filename)s:%(lineno)d %(levelname)s "
    "- %(message)s"
)

log = logging.getLogger("main")
log.setLevel(os.environ.get("LOGLEVEL", "info").upper())
