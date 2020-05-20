

import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.signal import convolve

if len(sys.argv)!=15:
    print("usage: flup.py -n <Grid size> -u <Utility Function> -t <number of tasks> -c <compCap> -i <insight> -l <leakage> -o <output_file>")
    sys.exit

# Run parameters 
n = 5 # Grid size (no. of agents = 3x3)
nTasks = 10 # No. of tasks in the environment
compCap = 10 # Computational capacity (genome size)
insight = 0.2 # Insight for certain utility functions
outfile = open("out.txt","w+") # Output file
exp_eff = 0.50 # Export efficiency

outfile.write("gen,best_sw,max_sw\n")


# GA parameters
pop_size = 100
mutation_prob = 0.1
crossover_prob = 0.75
number_of_gen = 1000

# Task to info parameters
alpha = 3.
beta = 5.

MAX_SW = ((nTasks-1.) * alpha + beta ) * compCap*n*n 

def init_Pop():
  population = np.random.randint(nTasks, size=(pop_size,n,n,compCap))
  return population

def uf(res):
  return np.sum(res)

def grid_uf(res_grid):
  ufs = np.zeros((n,n))
  for i in range(res_grid.shape[0]):
    for j in range(res_grid.shape[1]):
      ufs[i,j] = uf(res_grid[i,j])
  return ufs

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

def grid_gtrad(grid):
  res = np.zeros((n,n,nTasks))
  donate = np.zeros((n,n,nTasks))
  for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
      res[i,j],donate[i,j] = genome_to_res_and_donate(grid[i,j])
  return res,donate

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

def social_welfare(pop):
  sw_ar = np.zeros(pop.shape[0])
  for i in range(pop.shape[0]):
    sw_ar[i] = grid_sw(pop[i])
  return sw_ar

# Genetic Algorithm
def crossover(parent1, parent2):
    
    rand1 = np.random.randint(n)
    rand2 = np.random.randint(n)
    rand3 = np.random.randint(compCap)

    temp = parent1[rand1,:rand2]

    temp_2 = parent2[rand1,:rand2]

    temp1 = list(parent1[rand1,rand2,:rand3])

    temp1_2 = list(parent2[rand1,rand2,:rand3])

    temp1 = temp1 + list(parent2[rand1,rand2,rand3:])

    temp1_2 = temp1_2 + list(parent1[rand1,rand2,rand3:])

    temp1 = np.asarray([temp1])

    temp1_2 = np.asarray([temp1_2])

    temp = np.append(temp, temp1, axis = 0)

    temp_2 = np.append(temp_2, temp1_2, axis = 0)

    temp2 = parent2[rand1, rand2+1:]

    temp2_2 = parent1[rand1, rand2+1:]

    temp = np.append(temp, temp2, axis = 0)

    temp_2 = np.append(temp_2, temp2_2, axis = 0)

    temp = np.asarray([temp])

    temp_2 = np.asarray([temp_2])

#    np.vstack(list(temp))
    grid1 = np.vstack((parent1[:rand1],temp,parent2[rand1+1:]))
    
    grid2 = np.vstack((parent2[:rand1],temp_2,parent1[rand1+1:]))
    
    return [grid1, grid2]

def mutate(toAppend):
    
    a = np.random.rand(n,n,compCap)
    
    c = np.copy(toAppend)
    
    toMutate_ind = np.where(a < mutation_prob)
    
    c[toMutate_ind] = np.random.randint(low = -1*nTasks + 1, high  = nTasks, size = (c[toMutate_ind].shape))
    
    return c

def genetic_algorithm(population):
    
    fitness_arr = np.asarray(social_welfare(population)) #Returns numpy array of fitness
    
    inds = fitness_arr.argsort()[::-1] #Gives indices from max to min
    
    sortedPop = population[inds] #Sorts population based on fitness from highest to lowest
    
    fitness_arr[::-1].sort() #Sorts fitness array from max to min
    
    fitness_arr = fitness_arr/np.mean(fitness_arr) #Normalizes fitness for easier understansing
    
    prob_arr = fitness_arr / np.sum(fitness_arr)
    
    intermediate_ind = np.random.choice(len(prob_arr), pop_size, p=prob_arr)
    
    intermediates = population[intermediate_ind]
    
    temp = np.asarray(social_welfare(intermediates))
    
    newpop = []
    
    newpop.append(sortedPop[0])
    newpop.append(sortedPop[1])
    parents_ind = np.random.choice(pop_size, pop_size)
        
    for i in range(2, pop_size, 2):

        parent1 = intermediates[parents_ind[i]]
        parent2 = intermediates[parents_ind[i+1]]

        x = np.random.rand()
    
        if x < crossover_prob:
            
            grids = crossover(parent1, parent2)
            
            grid1 = grids[0]
            
            grid2 = grids[1]
            
            toAppend1 = grid1
            
            toAppend2 = grid2
            
            
        else:
            
            toAppend1 = parent1
            
            toAppend2 = parent2
            
        toAppend1 = mutate(toAppend1)
        
        toAppend2 = mutate(toAppend2)
        
        newpop.append(toAppend1)
            
        newpop.append(toAppend2)
            
    return np.asarray(newpop)

import time

start_time = time.time()

a = init_Pop()

b = genetic_algorithm(a)

best = []

for i in range(number_of_gen):
    b = genetic_algorithm(b)
    soc = np.asarray(social_welfare(b))
    best_sw = soc.max()
    best.append(best_sw)
    #outfile.write("%d,%f\n" % (i,best_sw))
    #print("%d,%f" % (i,best_sw))
    if best_sw==MAX_SW:
        print("Max SW reached, no. of generations required = %d" % i)
        outfile.write("%d,%f,%f" % (i,best_sw,max_sw))
    
outfile.close()    
    
fitness_arr = np.asarray(social_welfare(b)) #Returns numpy array of fitness

inds = fitness_arr.argsort()[::-1] #Gives indices from max to min

sortedPop = b[inds] #Sorts population based on fitness from highest to lowest
print(b[0])

print("--- %s seconds ---" % (time.time() - start_time))


#plt.plot(best)

