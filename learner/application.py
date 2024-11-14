import logging
import sys

from learner.client import ClientMAT
from learner.settings import DEBUG, MAT_HOST, MAT_PORT, MAT_SECURE
from learner.usecase import UseCase

logger = logging.getLogger(__name__)


class App:
    def __init__(self) -> None:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.DEBUG if DEBUG else logging.INFO,
            format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        client = ClientMAT(MAT_HOST, MAT_PORT, secure=MAT_SECURE)
        self.use_case = UseCase(client)

    def run(self) -> None:
        logger.info("Starting app...")
        self.use_case.run()


_app: App | None = None


def get_app() -> App:
    global _app
    if _app is None:
        _app = App()
    return _app
