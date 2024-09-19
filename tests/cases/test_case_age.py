from app.models.cases import Case
from datetime import timedelta


def test_case_age():
    case = Case()
    assert case.case_age > timedelta(seconds=0)
