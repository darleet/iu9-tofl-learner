from learner.client import ClientMAT
from learner.settings import MAT_HOST, MAT_PORT, MAT_SECURE
from learner.usecase import UseCase


class App:
    def __init__(self) -> None:
        client = ClientMAT(MAT_HOST, MAT_PORT, secure=MAT_SECURE)
        self.use_case = UseCase(client)

    def run(self) -> None:
        self.use_case.run()


_app: App | None = None


def get_app() -> App:
    global _app
    if _app is None:
        _app = App()
    return _app
