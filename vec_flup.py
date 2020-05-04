import numpy as np

n = 3
compCap = 5
pop_size = 10

def init_Pop():
  # Returns a population of grids containing nxn agents each having a genome of length compCap  
  population = np.random.randint(nTasks, size=(pop_size,n,n,compCap))

  return population
  
test_pop = init_Pop()

def uf(genome):
  # Utility function that gives the utility of a genome
  return np.sum(genome)

def social_welfare(population):
  # Takes in a population of grids of size pop_size and returns an array of size pop_size containing social welfare of each grid
  
