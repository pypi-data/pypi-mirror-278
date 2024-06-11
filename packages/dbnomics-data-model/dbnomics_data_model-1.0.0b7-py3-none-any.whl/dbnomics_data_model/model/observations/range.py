from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Range(Generic[T]):
    lowest: T
    highest: T

    def __rich__(self) -> str:
        return f"[{self.lowest} :right_arrow: {self.highest}]"

    def __str__(self) -> str:
        return f"[{self.lowest}:{self.highest}]"
