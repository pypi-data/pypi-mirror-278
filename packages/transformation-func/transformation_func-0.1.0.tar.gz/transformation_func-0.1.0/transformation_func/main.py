import numpy as np


def transpose2d(input_matrix: list):
    return [list(row) for row in zip(*input_matrix)]

def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1):
    if isinstance(input_array, list):
        input_array = np.array(input_array)

    windows = []
    for i in range(0, len(input_array) - size + 1, shift):
        windows.append(input_array[i:i + size:stride])

    return windows


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1):
    if input_matrix.ndim != 2 or kernel.ndim != 2:
        raise ValueError("Both input_matrix and kernel must be 2D arrays.")

    output_matrix = np.zeros((input_matrix.shape[0] - kernel.shape[0] + 1, input_matrix.shape[1] - kernel.shape[1] + 1))

    for i in range(0, output_matrix.shape[0], stride):
        for j in range(0, output_matrix.shape[1], stride):
            output_matrix[i, j] = np.sum(kernel * input_matrix[i:i + kernel.shape[0], j:j + kernel.shape[1]])

    return output_matrix


