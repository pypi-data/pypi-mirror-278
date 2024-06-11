import numpy as np

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Apply a 2D convolution (cross-correlation) over an input matrix with a given kernel.
    
    Parameters:
    input_matrix (np.ndarray): A 2D Numpy array of real numbers.
    kernel (np.ndarray): A 2D Numpy array of real numbers representing the convolution kernel.
    stride (int): The stride (step size) of the convolution. Default is 1.
    
    Returns:
    np.ndarray: The result of the convolution as a 2D Numpy array.
    
    Example:
    >>> input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> kernel = np.array([[1, 0], [0, -1]])
    >>> convolution2d(input_matrix, kernel)
    array([[ 1.,  1.],
           [ 1.,  1.]])
    """
    kernel_height, kernel_width = kernel.shape
    input_height, input_width = input_matrix.shape
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    output_matrix = np.zeros((output_height, output_width))
    
    for i in range(output_height):
        for j in range(output_width):
            region = input_matrix[i*stride:i*stride+kernel_height, j*stride:j*stride+kernel_width]
            conv_result = np.sum(region * kernel)
            output_matrix[i, j] = conv_result
            print(f"Region:\n{region}\nKernel:\n{kernel}\nConvolution Result: {conv_result}\n")
    
    return output_matrix
