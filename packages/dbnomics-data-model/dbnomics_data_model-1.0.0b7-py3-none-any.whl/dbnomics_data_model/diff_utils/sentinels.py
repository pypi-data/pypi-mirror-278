from typing import Final


class Missing:
    def __rich__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "-"


MISSING: Final = Missing()
