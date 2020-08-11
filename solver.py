import numpy as np


def solve(array, i, j):
    if j > 8:
        j = 0
        i += 1

    if i > 8:
        return True
    if array[i, j] != 0:
        return solve(array, i, j + 1)
    for value in range(1, 10):
        if validCell(array, i, j, value):
            array[i, j] = value
            if solve(array, i, j + 1):
                return True

    array[i, j] = 0
    return False


def validCell(array, i, j, value):
    return value not in array[i, :] and \
           value not in array[:, j] and \
           value not in array[i // 3 * 3: i // 3 * 3 + 3, j // 3 * 3: j // 3 * 3 + 3]


def main():
    array = np.array([[0, 0, 0, 7, 0, 0, 8, 0, 0],
                      [0, 0, 4, 0, 0, 0, 6, 1, 0],
                      [3, 7, 0, 0, 0, 1, 5, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [4, 0, 9, 5, 0, 0, 0, 0, 0],
                      [0, 0, 2, 0, 0, 9, 1, 0, 3],
                      [0, 0, 0, 0, 4, 3, 2, 5, 0],
                      [0, 0, 0, 0, 0, 6, 0, 0, 0],
                      [0, 3, 0, 1, 0, 8, 0, 0, 0]])

    solve(array, 0, 0)
    print(array)


main()
