from sys import path
path.append('../..')
import hiperwalk as hpw
import numpy as np
import scipy as sp
H = np.matrix([[-49,24],[24,31]])
g = hpw.WeightedGraph(-1j*H)
qw = hpw.ContinuousTime(g, gamma=1, time=1, terms=300)
U1 = qw.get_evolution()
U2 = sp.linalg.expm(H)

print(U1)
print()
print(U2)

print(np.allclose(U1, U2))
