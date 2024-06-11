from typing import Final


class NullRevision:
    def __str__(self) -> str:
        return "NULL_REVISION"


NULL_REVISION: Final = NullRevision()
