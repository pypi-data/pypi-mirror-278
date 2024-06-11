from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from dateutil.relativedelta import relativedelta
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import month_to_bimester, month_to_quarter, month_to_semester
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.bimester import BimesterPeriod
    from dbnomics_data_model.model.periods.month import MonthPeriod
    from dbnomics_data_model.model.periods.quarter import QuarterPeriod
    from dbnomics_data_model.model.periods.semester import SemesterPeriod
    from dbnomics_data_model.model.periods.week import WeekPeriod


__all__ = ["DayPeriod"]


@dataclass(frozen=True, order=True)
class DayPeriod(Period):
    month_num: int
    day_num: int

    type_: ClassVar[PeriodType] = PeriodType.DAY

    def __post_init__(self) -> None:
        # Check that date is constructible.
        self.first_day  # noqa: B018

    @classmethod
    def from_date(cls, value: date) -> Self:
        return cls(value.year, value.month, value.day)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            day_period = cast(Self, parsers.day_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return day_period

    def __str__(self) -> str:
        return self.first_day.isoformat()

    @cached_property
    def bimester(self) -> "BimesterPeriod":
        from dbnomics_data_model.model.periods.bimester import BimesterPeriod

        bimester_num = month_to_bimester(self.month_num)
        return BimesterPeriod(self.year_num, bimester_num)

    @cached_property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, self.day_num)

    @cached_property
    def month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        return MonthPeriod(self.year_num, self.month_num)

    @cached_property
    def next(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(days=1)
        return self.from_date(new_period_first_day)

    @cached_property
    def previous(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(days=-1)
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

    @cached_property
    def week(self) -> "WeekPeriod":
        from dbnomics_data_model.model.periods.week import WeekPeriod

        return WeekPeriod.from_date(self.first_day)

    def _ordinal_difference(self, other: Self) -> int:
        return self.first_day.toordinal() - other.first_day.toordinal()
