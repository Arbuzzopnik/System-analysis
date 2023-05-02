import numpy as np
from numpy import linalg as LA


def normalization(array):
    temp = np.ones(len(array))
    for i in range(len(array)):
        for j in range(len(array[i])):
            temp[i] *= array[i][j]
        temp[i] = temp[i] ** (1 / len(temp))
    return temp / sum(temp)


def consistency_check(array, number_c):
    random_consistency = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    wa = LA.eigvals(np.array(array))
    lambda_max = round(max(wa.real))
    consistency_index = (lambda_max - len(array)) / (len(array) - 1)
    consistency_relation = consistency_index / random_consistency[len(array)]
    print(f'lambda_max = {lambda_max}')
    print(f'consistency_index = {consistency_index}')
    print(f'consistency_relation = {consistency_relation}')
    if consistency_relation < 0.1:
        print(f'Paired comparison matrix by C {number_c + 1} is consistency')
    else:
        print(f'Paired comparison matrix by C {number_c + 1} is inconsistency')


def get_normalized_eigenvector_c(c, c_long, rating):
    for i in range(c_long):
        for j in range(c_long):
            c[i][j] = rating[i] / rating[j]
    return normalization(c)


def get_mps(a_long, f_transpose, k):
    temp = np.zeros((a_long, a_long))
    for i in range(a_long):
        for j in range(a_long):
            temp[i][j] = f_transpose[k][i] / f_transpose[k][j]
    return temp


def get_ahp(a_long, c_long, pairwise_measurement_matrix, normalized_eigenvector_c):
    temp = a_long * [0]
    for i in range(a_long):
        for j in range(c_long):
            temp[i] += pairwise_measurement_matrix[j][i] * normalized_eigenvector_c[j]
    return temp


def get_e(a_long, c_long, pairwise_measurement_matrix, normalized_eigenvector_c):
    temp = np.zeros((a_long, a_long))
    for i in range(a_long):
        for j in range(a_long):
            for k in range(c_long):
                temp[i][j] += (pairwise_measurement_matrix[k][i] / (
                        pairwise_measurement_matrix[k][i] + pairwise_measurement_matrix[k][j])) * \
                              normalized_eigenvector_c[k]
    return temp


def get_ahp_plus(a_long, e):
    temp = np.zeros(a_long)
    for i in range(a_long):
        temp[i] = sum(e[i])
    return temp / sum(temp)


def main():
    f = np.array([[4, 7, 4, 1, 7, 6, 4, 6, 3],
                  [6, 4, 6, 5, 5, 3, 7, 5, 9],
                  [7, 9, 3, 4, 2, 3, 8, 4, 1],
                  [1, 2, 7, 5, 8, 9, 2, 7, 9],
                  [9, 5, 2, 7, 3, 1, 5, 6, 8],
                  [7, 2, 1, 3, 5, 8, 3, 3, 9]])
    rating = [3, 2, 5, 4, 9, 7, 6, 5, 8]
    a_long = len(f)
    c_long = len(f[0])
    c = np.zeros((c_long, c_long))
    f_transpose = f.transpose()
    pairwise_measurement_matrix = np.zeros((c_long, a_long))

    normalized_eigenvector_c = get_normalized_eigenvector_c(c, c_long, rating)
    print(normalized_eigenvector_c)

    for k in range(c_long):
        mps = get_mps(a_long, f_transpose, k)
        print(f'MPS C{k + 1}\n{mps}')
        consistency_check(mps, k)
        pairwise_measurement_matrix[k] = normalization(mps)
        print(f'Normalized vector:{pairwise_measurement_matrix[k]}\n')

    ahp = get_ahp(a_long, c_long, pairwise_measurement_matrix, normalized_eigenvector_c)
    print('AHP:')
    for i in range(len(ahp)):
        print(f'w[{(i + 1)}] = {ahp[i]}')

    e = get_e(a_long, c_long, pairwise_measurement_matrix, normalized_eigenvector_c)
    print(f'E\n{e}')

    ahp_plus = get_ahp_plus(a_long, e)
    print('\nAHP_plus:')
    for i in range(len(ahp_plus)):
        print(f'w[{(i + 1)}] = {ahp_plus[i]}')


if __name__ == '__main__':
    main()





