import pytest
from gradebook.grade_utils import calculate_average

@pytest.fixture
def no_grades():
    return []

@pytest.mark.average
def test_that_average_of_no_grades_still_works(no_grades):
    assert calculate_average(no_grades) is None

