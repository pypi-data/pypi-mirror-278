import pytest
from gradebook.grade_utils import calculate_average

@pytest.mark.average
def test_that_average_grade_returns_average_of_grades_provided(some_grades):
    assert calculate_average(some_grades) == 80

