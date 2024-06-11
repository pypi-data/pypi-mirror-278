from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from dateutil.relativedelta import relativedelta
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import month_to_bimester, month_to_quarter, month_to_semester
from dbnomics_data_model.model.periods.formatters import format_month_num, format_year_num
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.bimester import BimesterPeriod
    from dbnomics_data_model.model.periods.quarter import QuarterPeriod
    from dbnomics_data_model.model.periods.semester import SemesterPeriod


__all__ = ["MonthPeriod"]


@dataclass(frozen=True, order=True)
class MonthPeriod(Period):
    month_num: int

    max_month_num: ClassVar[int] = 12
    min_month_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.MONTH

    def __post_init__(self) -> None:
        if self.month_num < self.min_month_num or self.month_num > self.max_month_num:
            msg = f"month_num must be between {self.min_month_num} and {self.max_month_num}"
            raise ValueError(msg)

    @classmethod
    def from_date(cls, value: date) -> Self:
        return cls(value.year, value.month)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            month_period = cast(Self, parsers.month_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return month_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-{format_month_num(self.month_num)}"

    @cached_property
    def bimester(self) -> "BimesterPeriod":
        from dbnomics_data_model.model.periods.bimester import BimesterPeriod

        bimester_num = month_to_bimester(self.month_num)
        return BimesterPeriod(self.year_num, bimester_num)

    @cached_property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, self.min_month_num)

    @cached_property
    def next(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(months=1)
        return self.from_date(new_period_first_day)

    @cached_property
    def previous(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(months=-1)
        return self.from_date(new_period_first_day)

    @cached_property
    def quarter(self) -> "QuarterPeriod":
        from dbnomics_data_model.model.periods.quarter import QuarterPeriod

        quarter_num = month_to_quarter(self.month_num)
        return QuarterPeriod(self.year_num, quarter_num)

    @cached_property
    def semester(self) -> "SemesterPeriod":
        from dbnomics_data_model.model.periods.semester import SemesterPeriod

        semester_num = month_to_semester(self.month_num)
        return SemesterPeriod(self.year_num, semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        return delta.years * 12 + delta.months
