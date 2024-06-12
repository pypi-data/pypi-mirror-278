from sys import path
path.append('..')
import hiperwalk as hpw
import numpy as np

g = hpw.Hypercube(3)
adj = g.adjacency_matrix()
indices = np.array(adj.indices, copy=True)
indptr = np.array(adj.indptr, copy=True)
print(adj.indices)
print(adj.indptr)
# print(adj.todense())

adj[0, 1] = 2
adj[1, 0] = 2
adj[1, 3] = 3
adj[3, 1] = 3

mg = hpw.Hypercube(3, weights=adj)
# madj = g.adjacency_matrix()
madj = mg.adjacency_matrix()

print()
print(adj.todense())
print(id(adj))
print()
print(madj.todense())
print(id(madj))
print()
print(id(g._adj_matrix))
print(id(mg._adj_matrix))
# print((adj - madj).todense())
# print(madj.indices)
# print(madj.indptr)
# 
# print(np.alltrue(indices == madj.indices))
# print(np.alltrue(indptr == madj.indptr))
