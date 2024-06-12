import hiperwalk as hpw
import numpy as np

n = 12
g = hpw.Hypercube(n)
N = g.number_of_vertices()

marked = [0]
num_marked = len(marked)
qw = hpw.Coined(g)
qw.set_marked({'-I': marked})

t_opt = int(np.pi/np.sqrt(8) * np.sqrt(N/len(qw.get_marked())))

states = qw.simulate(range=2*int(t_opt), state=qw.uniform_state())
p_succ = qw.success_probability(states)

hpw.plot_success_probability(2*int(t_opt), p_succ)
