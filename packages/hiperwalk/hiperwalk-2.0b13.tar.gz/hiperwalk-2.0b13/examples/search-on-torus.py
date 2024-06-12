#!/usr/bin/env python
# coding: utf-8

# ## Quantum-walk-based search on the torus

# In[1]:


from sys import path
path.append('../')


# In[2]:


import hiperwalk as hpw
import numpy as np
import matplotlib.pyplot as plt


# ### Defining the graph and the QW instance

# Let set $n$ for the torus graph with $n^2$ vertices; 'torus' is an instance of the Graph class.

# In[3]:


n = 20
torus = hpw.Grid((n,n), periodic=True)
N = torus.number_of_vertices()


# The next command creates a QW on the torus, which is an instance of the Coined class.

# In[4]:


central_vertex = (n//2 , n//2)
qw = hpw.Coined(torus, shift='flipflop', coin='grover', marked= [central_vertex])


# ### Setting the initial state

# In[5]:


psi0 = qw.uniform_state()


# ### Success probability as a function of the number of steps

# In[9]:


steps = int(1.3*np.sqrt(N*np.log(N)))
states = qw.simulate(range=(0,steps,1), state=psi0)
succ_prob = qw.success_probability(states)
#plt.plot(list(range(steps)), succ_prob, marker='.')
#plt.show()


# ### Animating the quantum walk

# In[7]:


list_of_states = qw.simulate(range = (0,steps,1), state = psi0)
list_of_probs = qw.probability_distribution(list_of_states)
hpw.plot_probability_distribution(list_of_probs, graph=torus,
                                  animate=True, figsize=(9,4.5),
                                  range=(0,steps,1))


# In[ ]:




