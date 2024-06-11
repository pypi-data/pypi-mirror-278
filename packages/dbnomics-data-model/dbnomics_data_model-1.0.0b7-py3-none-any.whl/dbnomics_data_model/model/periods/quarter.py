from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from dateutil.relativedelta import relativedelta
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import month_to_semester, quarter_to_first_month
from dbnomics_data_model.model.periods.formatters import format_year_num
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.month import MonthPeriod
    from dbnomics_data_model.model.periods.semester import SemesterPeriod


__all__ = ["QuarterPeriod"]


@dataclass(frozen=True, order=True)
class QuarterPeriod(Period):
    """A period of 3 consecutive months."""

    quarter_num: int

    max_quarter_num: ClassVar[int] = 4
    min_quarter_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.QUARTER

    def __post_init__(self) -> None:
        if self.quarter_num < self.min_quarter_num or self.quarter_num > self.max_quarter_num:
            msg = f"quarter_num must be between {self.min_quarter_num} and {self.max_quarter_num}"
            raise ValueError(msg)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            quarter_period = cast(Self, parsers.quarter_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return quarter_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-Q{self.quarter_num}"

    @cached_property
    def first_day(self) -> date:
        first_month_num = quarter_to_first_month(self.quarter_num)
        return date(self.year_num, first_month_num, 1)

    @cached_property
    def first_month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        first_month_num = quarter_to_first_month(self.quarter_num)
        return MonthPeriod(self.year_num, first_month_num)

    @cached_property
    def next(self) -> Self:
        new_quarter_num = self.quarter_num + 1
        new_year_num = self.year_num
        if new_quarter_num > self.max_quarter_num:
            new_quarter_num = self.min_quarter_num
            new_year_num += 1
        return self.__class__(new_year_num, new_quarter_num)

    @cached_property
    def previous(self) -> Self:
        new_quarter_num = self.quarter_num - 1
        new_year_num = self.year_num
        if new_quarter_num < self.min_quarter_num:
            new_quarter_num = self.max_quarter_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_quarter_num)

    @cached_property
    def semester(self) -> "SemesterPeriod":
        from dbnomics_data_model.model.periods.semester import SemesterPeriod

        first_month_num = quarter_to_first_month(self.quarter_num)
        semester_num = month_to_semester(first_month_num)
        return SemesterPeriod(self.year_num, semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 3
