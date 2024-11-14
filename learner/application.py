from learner.client import ClientMAT
from learner.settings import MAT_HOST, MAT_PORT, MAT_SECURE


class App:
    def __init__(self):
        self.client = ClientMAT(MAT_HOST, MAT_PORT, secure=MAT_SECURE)


_app: App | None = None


def get_app():
    global _app
    if _app is None:
        _app = App()
    return _app
