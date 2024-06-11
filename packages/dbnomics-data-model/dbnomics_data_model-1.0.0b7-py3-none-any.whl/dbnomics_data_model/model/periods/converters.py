# ruff: noqa: PLR2004


def bimester_to_first_month(bimester_num: int) -> int:
    return bimester_num * 2 - 1


def month_to_bimester(month_num: int) -> int:
    return (month_num - 1) // 2 + 1


def month_to_quarter(month_num: int) -> int:
    return (month_num - 1) // 3 + 1


def month_to_semester(month_num: int) -> int:
    return 1 if month_num <= 6 else 2


def quarter_to_first_month(quarter_num: int) -> int:
    return quarter_num * 3 - 2


def semester_to_first_month(semester_num: int) -> int:
    return semester_num * 6 - 5
