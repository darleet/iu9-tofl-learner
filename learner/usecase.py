import logging

from learner.client import ClientMAT
from learner.models import MembershipRequest

logger = logging.getLogger(__name__)


class UseCase:
    EPSILON = "ε"
    L = "L"
    R = "R"

    def __init__(self, client: ClientMAT) -> None:
        self.client = client

        self.prefixes: list[str] = []
        self.non_main_prefixes: list[str] = []
        self.suffixes: list[str] = []
        self.table: list[list[bool]] = []
        self.non_main_table: list[list[bool]] = []

    def _add_prefix(self, prefix: str, main: bool = True) -> None:
        self.prefixes.append(prefix)
        row: list[bool] = []

        for suffix in self.suffixes:
            request = MembershipRequest(word=f"{prefix}{suffix}")
            resp = self.client.post_membership(request).response
            if resp:
                logger.info(f"{prefix}{suffix} is a member")
            else:
                logger.info(f"{prefix}{suffix} is not a member")
            row.append(resp)

        if main:
            logger.info(f"Added main prefix: {prefix}")
            self.table.append(row)
        else:
            logger.info(f"Added non-main prefix: {prefix}")
            self.non_main_table.append(row)

    def _add_suffix(self, suffix: str) -> None:
        self.suffixes.append(suffix)

        for i, prefix in enumerate(self.prefixes + self.non_main_prefixes):
            request = MembershipRequest(word=f"{prefix}{suffix}")
            resp = self.client.post_membership(request).response
            if resp:
                logger.info(f"{prefix}{suffix} is a member")
            else:
                logger.info(f"{prefix}{suffix} is not a member")
            self.table[i].append(resp)

        logger.info(f"Added suffix: {suffix}")

    def run(self) -> None:
        logger.info("App started successfully")

        self._add_prefix(self.EPSILON)
        self._add_prefix(self.L)
        self._add_prefix(self.R)
        self._add_suffix(self.EPSILON)
