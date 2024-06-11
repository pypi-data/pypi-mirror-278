from collections.abc import Generator
from enum import Enum
from typing import Any

from parsy import Parser, fail, generate, regex, seq, string, success

from dbnomics_data_model.model.periods import (
    BimesterPeriod,
    DayPeriod,
    MonthPeriod,
    Period,
    QuarterPeriod,
    SemesterPeriod,
    WeekPeriod,
    YearPeriod,
)


class PeriodCode(Enum):
    BIMESTER = "B"
    QUARTER = "Q"
    SEMESTER = "S"
    WEEK = "W"


def between(value: str, *, min_value: int, max_value: int, name: str | None = None) -> Parser:
    if name is None:
        name = "value"
    num = int(value)
    if num < min_value or num > max_value:
        return fail(f"{name} is out of bounds [{min_value!r}, {max_value!r}]: {num!r}")
    return success(num)


def to_day_num(value: str) -> Parser:
    return between(value, min_value=1, max_value=31, name="day num")


def to_month_num(value: str) -> Parser:
    return between(value, min_value=MonthPeriod.min_month_num, max_value=MonthPeriod.max_month_num, name="month num")


def to_week_num(value: str) -> Parser:
    return between(value, min_value=1, max_value=53, name="week num")


dash = string("-")


bimester_num = (
    regex(rf"[{BimesterPeriod.min_bimester_num}-{BimesterPeriod.max_bimester_num}]").map(int).desc("bimester num")
)
day_num = regex(r"[0-9]{2}").bind(to_day_num).desc("2 digit day num")
month_num = regex(r"[0-9]{2}").bind(to_month_num).desc("2 digit month num")
quarter_num = regex(rf"[{QuarterPeriod.min_quarter_num}-{QuarterPeriod.max_quarter_num}]").map(int).desc("quarter num")
semester_num = (
    regex(rf"[{SemesterPeriod.min_semester_num}-{SemesterPeriod.max_semester_num}]").map(int).desc("semester num")
)
week_num = regex(r"[0-9]{2}").bind(to_week_num).desc("2 digit week num")
year_num = regex(r"[0-9]{4}").map(int).desc("4 digit year num")


bimester_code = string(PeriodCode.BIMESTER.value)
bimester_code_and_num = bimester_code >> bimester_num

quarter_code = string(PeriodCode.QUARTER.value)
quarter_code_and_num = quarter_code >> quarter_num

semester_code = string(PeriodCode.SEMESTER.value)
semester_code_and_num = semester_code >> semester_num

week_code = string(PeriodCode.WEEK.value)
week_code_and_num = week_code >> week_num


bimester_period = seq(bimester_code_and_num, year_num).combine(BimesterPeriod)
day_period = seq(year_num << dash, month_num << dash, day_num).combine(DayPeriod)
month_period = seq(year_num << dash, month_num).combine(MonthPeriod)
quarter_period = seq(quarter_code_and_num, year_num).combine(QuarterPeriod)
semester_period = seq(semester_code_and_num, year_num).combine(SemesterPeriod)
week_period = seq(week_code_and_num, year_num).combine(WeekPeriod)
year_period = year_num.map(YearPeriod)


@generate  # type: ignore[misc]
def period() -> Generator[Parser, Any, Period]:
    year_num_value: int = yield year_num
    if (yield dash.optional()) is None:
        return YearPeriod(year_num=year_num_value)

    tagged_bimester = bimester_code_and_num.map(lambda v: (BimesterPeriod, v))
    tagged_month = month_num.map(lambda v: (MonthPeriod, v))
    tagged_quarter = quarter_code_and_num.map(lambda v: (QuarterPeriod, v))
    tagged_semester = semester_code_and_num.map(lambda v: (SemesterPeriod, v))
    tagged_week = week_code_and_num.map(lambda v: (WeekPeriod, v))

    alt_cls: type[Period]
    alt_value: int
    alt_cls, alt_value = yield tagged_bimester | tagged_month | tagged_quarter | tagged_semester | tagged_week

    if alt_cls == BimesterPeriod:
        return BimesterPeriod(bimester_num=alt_value, year_num=year_num_value)
    elif alt_cls == QuarterPeriod:
        return QuarterPeriod(quarter_num=alt_value, year_num=year_num_value)
    elif alt_cls == SemesterPeriod:
        return SemesterPeriod(semester_num=alt_value, year_num=year_num_value)
    elif alt_cls == WeekPeriod:
        return WeekPeriod(week_num=alt_value, year_num=year_num_value)

    if (yield dash.optional()) is None:
        return MonthPeriod(month_num=alt_value, year_num=year_num_value)

    day_num_value: int = yield day_num
    return DayPeriod(day_num=day_num_value, month_num=alt_value, year_num=year_num_value)
