def write_to_file(grades) -> None:
    """
    Function to write our grades to a file
    :param grades: grades list
    :return: None
    """
    with open(f"grades.txt", "w") as f:
        f.write(str(grades))

