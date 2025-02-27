import logging

from prettytable import PrettyTable

from learner.client import ClientMAT
from learner.models import EquivalenceRequest, MembershipRequest

logger = logging.getLogger(__name__)


class UseCase:
    EPSILON = "ε"
    ALPHABET = ["L", "R"]

    def __init__(self, client: ClientMAT) -> None:
        self.client = client

        self.prefixes: list[str] = []
        self.non_main_prefixes: list[str] = []
        self.suffixes: list[str] = []
        self.table: list[list[bool]] = []
        self.non_main_table: list[list[bool]] = []

    def _add_prefix(self, prefix: str, is_main: bool = True) -> None:
        if is_main:
            self.prefixes.append(prefix)
        else:
            self.non_main_prefixes.append(prefix)

        row: list[bool] = []

        for suffix in self.suffixes:
            if suffix == self.EPSILON:
                suffix = ""

            request = MembershipRequest(word=f"{prefix}{suffix}")
            resp = self.client.post_membership(request).response
            if resp:
                logger.debug(f"{prefix}{suffix} is a member")
            else:
                logger.debug(f"{prefix}{suffix} is not a member")

            row.append(resp)

        if is_main:
            logger.info(f"Added main prefix: {prefix}")
            self.table.append(row)
        else:
            logger.debug(f"Added non-main prefix: {prefix}")
            self.non_main_table.append(row)

    def _add_suffix(self, suffix: str) -> None:
        self.suffixes.append(suffix)

        for i, prefix in enumerate(self.prefixes + self.non_main_prefixes):
            if prefix == self.EPSILON:
                prefix = ""

            request = MembershipRequest(word=f"{prefix}{suffix}")
            resp = self.client.post_membership(request).response
            if resp:
                logger.debug(f"{prefix}{suffix} is a member")
            else:
                logger.debug(f"{prefix}{suffix} is not a member")

            if i >= len(self.table):
                self.non_main_table[i - len(self.table)].append(resp)
            else:
                self.table[i].append(resp)

        logger.info(f"Added suffix: {suffix}")

    def _merge_tables(self) -> bool:
        changed_table = False
        new_non_main_table: list[list[bool]] = []
        new_non_main_prefixes: list[str] = []

        for i in range(len(self.non_main_table)):
            if self.non_main_table[i] not in self.table:
                changed_table = True
                logger.info(f"Moved non-main prefix: {self.non_main_prefixes[i]}")
                self.table.append(self.non_main_table[i])
                self.prefixes.append(self.non_main_prefixes[i])
            else:
                new_non_main_table.append(self.non_main_table[i])
                new_non_main_prefixes.append(self.non_main_prefixes[i])

        self.non_main_table = new_non_main_table
        self.non_main_prefixes = new_non_main_prefixes
        return changed_table

    def _extend_table(self) -> None:
        prefixes_copy = self.prefixes.copy()

        for prefix in prefixes_copy:
            for other_prefix in self.ALPHABET:
                if prefix == self.EPSILON or other_prefix == self.EPSILON:
                    continue

                if (
                    prefix + other_prefix not in self.prefixes
                    and prefix + other_prefix not in self.non_main_prefixes
                ):
                    self._add_prefix(prefix + other_prefix, is_main=False)
                else:
                    logger.debug(f"Prefix {prefix} already in table")

    def _process(self, word: str) -> None:
        suffix = ""
        for i in range(len(word) - 1, -1, -1):
            suffix = word[i] + suffix
            if suffix not in self.suffixes:
                self._add_suffix(suffix)

        was_changed = True
        while was_changed:
            was_changed = self._merge_tables()
            self._extend_table()

    def _print_table(self) -> None:
        table = PrettyTable()
        table.field_names = [""] + self.suffixes
        for i, row in enumerate(self.table):
            table.add_row([self.prefixes[i]] + [str(int(el)) for el in row])
        table.add_divider()
        for i, row in enumerate(self.non_main_table):
            table.add_row([self.non_main_prefixes[i]] + [str(int(el)) for el in row])
        logger.info("\n" + table.get_string())

    def run(self) -> None:
        logger.info("App started successfully")

        self._add_prefix(self.EPSILON)
        self._add_suffix(self.EPSILON)

        for symbol in self.ALPHABET:
            self._add_prefix(symbol, is_main=False)

        self._merge_tables()
        self._extend_table()

        while True:
            main_prefixes = " ".join(self.prefixes)
            non_main_prefixes = " ".join(self.non_main_prefixes)
            suffixes = " ".join(self.suffixes)
            table = " ".join(
                [
                    str(int(col))
                    for row in self.table + self.non_main_table
                    for col in row
                ]
            )

            resp = self.client.post_equivalence(
                EquivalenceRequest(
                    main_prefixes=main_prefixes,
                    non_main_prefixes=non_main_prefixes,
                    suffixes=suffixes,
                    table=table,
                )
            )

            if resp.type is None:
                self._print_table()
                break

            if not resp.response:
                raise Exception

            logger.info(f"Got counter response: {resp.response}")

            self._print_table()
            self._process(resp.response)

            while not self.non_main_prefixes:
                self._extend_table()
                self._merge_tables()
