from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from dateutil.relativedelta import relativedelta
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import semester_to_first_month
from dbnomics_data_model.model.periods.formatters import format_year_num
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.month import MonthPeriod


__all__ = ["SemesterPeriod"]


@dataclass(frozen=True, order=True)
class SemesterPeriod(Period):
    """A period of 6 consecutive months."""

    semester_num: int

    max_semester_num: ClassVar[int] = 2
    min_semester_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.SEMESTER

    def __post_init__(self) -> None:
        if self.semester_num < self.min_semester_num or self.semester_num > self.max_semester_num:
            msg = f"semester_num must be between {self.min_semester_num} and {self.max_semester_num}"
            raise ValueError(msg)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            semester_period = cast(Self, parsers.semester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return semester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-S{self.semester_num}"

    @cached_property
    def first_day(self) -> date:
        first_month_num = semester_to_first_month(self.semester_num)
        return date(self.year_num, first_month_num, 1)

    @cached_property
    def first_month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        first_month_num = semester_to_first_month(self.semester_num)
        return MonthPeriod(self.year_num, first_month_num)

    @cached_property
    def next(self) -> Self:
        new_semester_num = self.semester_num + 1
        new_year_num = self.year_num
        if new_semester_num > self.max_semester_num:
            new_semester_num = self.min_semester_num
            new_year_num += 1
        return self.__class__(new_year_num, new_semester_num)

    @cached_property
    def previous(self) -> Self:
        new_semester_num = self.semester_num - 1
        new_year_num = self.year_num
        if new_semester_num < self.min_semester_num:
            new_semester_num = self.max_semester_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 6
