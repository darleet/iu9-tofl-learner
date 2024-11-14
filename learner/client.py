import requests

from learner.models import (
    EquivalenceRequest,
    EquivalenceResponse,
    MembershipRequest,
    MembershipResponse,
)


class ClientMAT:
    def __init__(self, host: str, port: int, secure: bool = False):
        self.host = host
        self.port = port
        self.schema = "https" if secure else "http"

    def post_membership(self, request: MembershipRequest) -> MembershipResponse:
        resp = requests.post(
            f"{self.schema}://{self.host}:{self.port}/checkWord",
            json=request.model_dump(),
        )
        return MembershipResponse(**resp.json())

    def post_equivalence(self, request: EquivalenceRequest) -> EquivalenceResponse:
        resp = requests.post(
            f"{self.schema}://{self.host}:{self.port}/checkTable",
            json=request.model_dump(),
        )
        return EquivalenceResponse(**resp.json())
