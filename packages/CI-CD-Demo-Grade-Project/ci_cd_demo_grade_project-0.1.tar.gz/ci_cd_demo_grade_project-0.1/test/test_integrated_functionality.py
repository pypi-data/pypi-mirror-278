import pytest
from gradebook.grade_utils import calculate_average, determine_letter_grade

def test_letter_grade_average(some_grades):
    # calculate_average
    average = calculate_average(some_grades)

    # determine_letter_grade for the average
    average_letter_grade = determine_letter_grade(average)
    assert average_letter_grade == "B"

