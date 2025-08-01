#pytest
import sys
import io

import pytest
from pytest_mock import MockerFixture

from mission2.grade import GradeFactory, NormalGrade


def test_get_grade_silver():
    grade = GradeFactory.get_grade(30)
    assert grade.name == "SILVER"

def test_get_grade_gold():
    grade = GradeFactory.get_grade(50)
    assert grade.name == "GOLD"

def test_get_grade_normal():
    grade = GradeFactory.get_grade(10)
    assert grade.name == "NORMAL"

def test_get_check_policy_NORMAL_클래스_단독사용():
    result = NormalGrade().evaluate(10)
    assert result
