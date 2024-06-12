import pytest

from gradebook.grade_utils import determine_letter_grade


grade_ranges = {
    "A": range(90, 101),
    "B": range(80, 90),
    "C": range(70, 80),
    "D": range(60, 70),
    "F": range(0, 60),
}

@pytest.mark.parametrize("letter,number",
                         [(letter, number) for letter, numbers in grade_ranges.items() for number in numbers])

def test_is_letter_grade(letter, number):
    assert determine_letter_grade(number) == letter

