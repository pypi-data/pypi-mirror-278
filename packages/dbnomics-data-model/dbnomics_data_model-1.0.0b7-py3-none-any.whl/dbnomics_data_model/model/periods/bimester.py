from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from dateutil.relativedelta import relativedelta
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import bimester_to_first_month, month_to_quarter, month_to_semester
from dbnomics_data_model.model.periods.formatters import format_year_num
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.month import MonthPeriod
    from dbnomics_data_model.model.periods.quarter import QuarterPeriod
    from dbnomics_data_model.model.periods.semester import SemesterPeriod


__all__ = ["BimesterPeriod"]


@dataclass(frozen=True, order=True)
class BimesterPeriod(Period):
    """A period of 2 consecutive months."""

    bimester_num: int

    def __post_init__(self) -> None:
        if self.bimester_num < self.min_bimester_num or self.bimester_num > self.max_bimester_num:
            msg = f"bimester_num must be between {self.min_bimester_num} and {self.max_bimester_num}"
            raise ValueError(msg)

    max_bimester_num: ClassVar[int] = 6
    min_bimester_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.BIMESTER

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            bimester_period = cast(Self, parsers.bimester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return bimester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-B{self.bimester_num}"

    @cached_property
    def first_day(self) -> date:
        first_month_num = bimester_to_first_month(self.bimester_num)
        return date(self.year_num, first_month_num, 1)

    @cached_property
    def first_month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        first_month_num = bimester_to_first_month(self.bimester_num)
        return MonthPeriod(self.year_num, first_month_num)

    @cached_property
    def next(self) -> Self:
        new_bimester_num = self.bimester_num + 1
        new_year_num = self.year_num
        if new_bimester_num > self.max_bimester_num:
            new_bimester_num = self.min_bimester_num
            new_year_num += 1
        return self.__class__(new_year_num, new_bimester_num)

    @cached_property
    def previous(self) -> Self:
        new_bimester_num = self.bimester_num - 1
        new_year_num = self.year_num
        if new_bimester_num < self.min_bimester_num:
            new_bimester_num = self.max_bimester_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_bimester_num)

    @cached_property
    def quarter(self) -> "QuarterPeriod":
        from dbnomics_data_model.model.periods.quarter import QuarterPeriod

        first_month_num = bimester_to_first_month(self.bimester_num)
        quarter_num = month_to_quarter(first_month_num)
        return QuarterPeriod(self.year_num, quarter_num)

    @cached_property
    def semester(self) -> "SemesterPeriod":
        from dbnomics_data_model.model.periods.semester import SemesterPeriod

        first_month_num = bimester_to_first_month(self.bimester_num)
        semester_num = month_to_semester(first_month_num)
        return SemesterPeriod(self.year_num, semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 2
