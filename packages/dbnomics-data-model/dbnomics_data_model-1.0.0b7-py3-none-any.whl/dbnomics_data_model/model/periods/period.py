from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from functools import cached_property, reduce
from typing import TYPE_CHECKING, ClassVar, Self, cast, overload

from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.year import YearPeriod


__all__ = ["Period"]


@dataclass(frozen=True, order=True)
class Period(ABC):
    year_num: int

    type_: ClassVar[PeriodType]

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            period = cast(Self, parsers.period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return period

    def __add__(self, increment: int) -> Self:
        return reduce(lambda period, _: period.next if increment > 0 else period.previous, range(abs(increment)), self)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @overload
    def __sub__(self, other: int) -> Self:
        pass

    @overload
    def __sub__(self, other: Self) -> int:
        pass

    def __sub__(self, other: int | Self) -> Self | int:
        if isinstance(other, int):
            return self + (-other)

        if self.type_ != other.type_:
            msg = f"Can't substract {type(other)!r} from {type(self)!r}"
            raise TypeError(msg)

        return self._ordinal_difference(other)

    @property
    @abstractmethod
    def first_day(self) -> date:
        pass

    @property
    @abstractmethod
    def next(self) -> Self:
        pass

    @property
    @abstractmethod
    def previous(self) -> Self:
        pass

    @cached_property
    def year(self) -> "YearPeriod":
        from dbnomics_data_model.model.periods.year import YearPeriod

        return YearPeriod(self.year_num)

    @abstractmethod
    def _ordinal_difference(self, other: Self) -> int:
        pass
