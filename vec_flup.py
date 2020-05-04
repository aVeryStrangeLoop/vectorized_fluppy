import numpy as np

n = 3

nTasks = 5

compCap = 5

pop_size = 2

def init_Pop():
  # Returns a population of grids containing nxn agents each having a genome of length compCap  
  population = np.random.randint(nTasks, size=(pop_size,n,n,compCap))

  return population
  
test_pop = init_Pop()
print test_pop

def uf(genome):
  # Utility function that gives the utility of a genome
  return np.max(genome)


def social_welfare(population):
  # Takes in a population of grids of size pop_size and returns an array of size pop_size containing social welfare of each grid
  # Algorithm
  # For each grid in population
    # For each cell, sum utilities	    
  vec_uf = np.vectorize(uf,signature='(i)->()')
  utilities =  vec_uf(population)
  print utilities
  sws = np.sum(utilities,axis=(1,2))
  print sws

#test_2 = [[[ [1,3] , [3,4] ],[ [5,6] , [7,8] ]],[[ [1,2] , [3,4] ],[ [5,6] , [7,8] ]]]

social_welfare(test_pop)

