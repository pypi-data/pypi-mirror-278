import pytest
from gradebook.grade_utils import find_highest_grade, find_lowest_grade

@pytest.mark.hilo
@pytest.mark.highest
def test_find_highest_grade(some_grades):
    assert find_highest_grade(some_grades) == 90

@pytest.mark.hilo
@pytest.mark.lowest
def test_find_lowest_grade(some_grades):
    assert find_lowest_grade(some_grades) == 70

