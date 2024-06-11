def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix.
    
    Parameters:
    input_matrix (list of list of float): A 2D matrix represented as a list of lists of real numbers.

    Returns:
    list of list of float: The transposed 2D matrix.
    
    Example:
    >>> transpose2d([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(row) for row in zip(*input_matrix)]
