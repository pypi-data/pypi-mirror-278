from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.month import MonthPeriod


__all__ = ["YearPeriod"]


@dataclass(frozen=True, order=True)
class YearPeriod(Period):
    type_: ClassVar[PeriodType] = PeriodType.YEAR

    def __post_init__(self) -> None:
        # Check that date is constructible.
        self.first_day  # noqa: B018

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            year_period = cast(Self, parsers.year_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return year_period

    def __str__(self) -> str:
        return str(self.year_num)

    @cached_property
    def first_day(self) -> date:
        return date(self.year_num, 1, 1)

    @cached_property
    def first_month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        return MonthPeriod(self.year_num, month_num=1)

    @cached_property
    def next(self) -> Self:
        return self.__class__(self.year_num + 1)

    @cached_property
    def previous(self) -> Self:
        return self.__class__(self.year_num - 1)

    def _ordinal_difference(self, other: Self) -> int:
        return self.year_num - other.year_num
