import numpy as np
import scipy as sp

def numpy_matrix_power_series(A, n):
    """
    I + A + A^2/2 + A^3/3! + ... + A^n/n!
    """
    print(A)
    print('------------------------')
    U = np.eye(A.shape[0], dtype=A.dtype)
    curr_term = U.copy()
    for i in range(1, n + 1):
        curr_term = curr_term @ A / i
        U += curr_term

    return U

dim = 300
num_terms = 300
#A = np.random.random((dim, dim))
A = np.matrix([[-49.0, 24.0], [24.0, 31.0]])
print(A.max())
print(A.min())

U1 = numpy_matrix_power_series(A, num_terms)
U2 = sp.linalg.expm(A)
print(U1)
print()
print(U2)
print()
print(U1 - U2)
print(np.allclose(U1, U2))
