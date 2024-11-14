from learner.client import ClientMAT


class UseCase:
    def __init__(self, client: ClientMAT) -> None:
        self.client = client

    def run(self) -> None:
        pass
