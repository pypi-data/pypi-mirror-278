import hiperwalk as hpw

n = 10
g = hpw.Hypercube(n)
qw = hpw.Coined(g, shift='ff', coin='G',
                marked={'-I': [0, 1, 2]})

states = qw.simulate(time=(2**(n//2), 1),
                     state=qw.uniform_state())
marked_prob = qw.success_probability(states)
hpw.plot_success_probability((2**(n//2), 1), marked_prob)
