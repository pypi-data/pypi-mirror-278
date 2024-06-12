def calculate_average(grades):
    """Return the average grade"""
    if not grades:
      return None
    return sum(grades) / len(grades)


def find_highest_grade(grades):
    """Return the highest grade"""
    if not grades:
        return None
    return max(grades)


def find_lowest_grade(grades):
    """Return the lowest grade"""
    if not grades:
        return None
    return min(grades)


def determine_letter_grade(grade):
    """Return the letter grade for a numeric grade."""
    if grade >= 90:
        return "A"
    elif grade >= 80:
        return "B"
    elif grade >= 70:
        return "C"
    elif grade >= 60:
        return "D"
    else:
        return "F"

