import numpy as np

def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:
    """
    Generate sliding windows over a 1D array.
    
    Parameters:
    input_array (list or np.ndarray): A 1D array of real numbers.
    size (int): The size (length) of each window.
    shift (int): The shift (step size) between consecutive windows. Default is 1.
    stride (int): The stride (step size) within each window. Default is 1.
    
    Returns:
    list of list or np.ndarray: A list of windows, each a list or 1D Numpy array of real numbers.
    
    Example:
    >>> window1d([1, 2, 3, 4, 5], size=3)
    [array([1, 2, 3]), array([2, 3, 4]), array([3, 4, 5])]
    """
    input_array = np.asarray(input_array)
    windows = []
    for start in range(0, len(input_array) - size + 1, shift):
        windows.append(input_array[start:start + size:stride])
    return windows
