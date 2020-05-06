import numpy as np
from scipy.signal import convolve

n = 2 # grid_size
nTasks = 5 
exp_eff = 0.2
compCap = 3
pop_size = 5 # GA population size (to generate fake data)
# Task to info parameters (info = task_no*alpha+beta)
alpha = 3.
beta = 5.

def init_Pop():
  # Returns a population of grids containing nxn agents each having a genome of length compCap  
  population = np.random.randint(nTasks, size=(pop_size,n,n,compCap))
  return population

test_pop = init_Pop()
print "TEST POPULATION"
print test_pop


def uf(res):
  return np.sum(res)
grid_uf = np.vectorize(uf,signature='(i)->()')

# This function returns the resource and donation vectors after processing the genome (NOTE: Zero task has no resource acquisition)
def genome_to_res_and_donate(genome):
  res = np.zeros(nTasks)
  genome_pos = genome[genome>0]


  res[genome_pos] = genome_pos*alpha+beta
  donate = np.zeros(nTasks)
  genome_neg = abs(genome[genome<0])
  donate[genome_neg] += res[genome_neg]*exp_eff
  res[genome_neg] -= res[genome_neg]*exp_eff
  return res,donate/8.
grid_gtrad = np.vectorize(genome_to_res_and_donate,signature='(i)->(nTasks),(nTasks)')


def grid_sw(grid):
  # Get resource vector for whole grid
  grid_res,grid_donate = grid_gtrad(grid)
  #print grid_donate
  grid_donate = np.pad(grid_donate,((1,1),(1,1),(0,0)),'wrap')
  # grid_res_donated contains the unpacked result of grid_donate too be added to each agent's resource reservoir
  kernel = np.array([[1.,1.,1.],[1.,0.,1.],[1.,1.,1.]])
  kernel = kernel[:,:,None] 
  grid_donated = convolve(grid_donate,kernel,mode='valid')
  #print grid_donated 
  grid_res = grid_res + grid_donated  
  return np.sum(grid_uf(grid_res))

population_sw = np.vectorize(grid_sw,signature='(i,j,k)->()')
print "Social welfare of each grid in population"
print population_sw(test_pop)



#def grid_uf(grid):
  # Takes in a grid containing genomes and returns final utility of each genome as matrix
  
  # Step 1. Create a matrix of same size as the grid but each cell contains an array of length nTasks and stores the information
  # associated with that task
#  res = np.zeros((grid.shape[0],grid.shape[1],nTasks))
  
  


#test = np.array([[ [1,3,5] , [3,4,-1] ],[ [4,3,0] , [2,-2,2] ]])
#grid_uf(test)

# Vectorization, uf converts a three dimensional matrix (a grid containing genomes) to a two dimensional matrix (a grid containing individual utilities)
#vec_uf = np.vectorize(uf,signature='(i,j,k)->(i,j)')

#def social_welfare(population):
  # Takes in a population of grids of size pop_size and returns an array of size pop_size containing social welfare of each grid
 	    
#  utilities =  vec_uf(population)
#  print utilities
#  sws = np.sum(utilities,axis=(1,2))
#  print sws

#test_2 = [[[ [1,3] , [3,4] ],[ [5,6] , [7,8] ]],[[ [1,2] , [3,4] ],[ [5,6] , [7,8] ]]]
#social_welfare(test_pop)

