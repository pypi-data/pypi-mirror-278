import pytest

from gradebook.save_grades import write_to_file

# first we pass the mocker in
def test_write_grades_to_file(mocker):
    """
    Function to test writing grades to a file
    """

    # mock the 'open' function call to return a file object
    # using a builtin from unittest
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    # now we can call our function that writes to a file
    write_to_file([50,75,100])

    # assert that the 'open' function was called with the expected arguments
    mock_file.assert_called_once_with("grades.txt", "w")

    # assert that the file was written to with the expected text
    mock_file().write.assert_called_once_with(str([50,75,100]))

