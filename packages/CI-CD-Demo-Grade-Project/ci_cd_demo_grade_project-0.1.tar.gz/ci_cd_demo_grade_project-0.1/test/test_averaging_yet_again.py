import pytest
from gradebook.grade_utils import calculate_average

@pytest.mark.average
def test_that_average_of_nothing_still_does_what_is_expected():
    assert calculate_average(None) is None

