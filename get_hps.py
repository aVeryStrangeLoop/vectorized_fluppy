# Get the hyperparameters for different runs

from core import *


REPL = 5
n_ = [3,4,5]
nTasks = 10
compCap = 20 
exp_eff = 0.5
insight = 0.9
choice_of_u = 2
alpha = 3.
beta = 5.

# GA Properties
pop_size = 100
mutation_prob = 0.1
crossover_prob = 0.75
max_gen = 10000

if not os.path.exists('results_hps'):
    os.makedirs('results_hps')
hps_file = open("results_hps/hps_summary.csv","w+")
hps_file.write("# nTasks %d\n" % nTasks)
hps_file.write("# compCap %d\n" % compCap)
hps_file.write("# exp_eff %f\n" % exp_eff)
hps_file.write("# alpha %f\n" % alpha)
hps_file.write("# beta %f\n" % beta)
hps_file.write("# pop_size %d\n" % pop_size)
hps_file.write("# mut_prob %f\n" % mutation_prob)
hps_file.write("# cross_prob %f\n" % crossover_prob)
hps_file.write("grid_size,repl,th_max,best_sw,gen_req\n")

for n in n_:
    for repl in range(REPL):
        print("size = %d, repl = %d" % (n,repl))

        conf = [n,choice_of_u,nTasks,compCap,insight,exp_eff,pop_size,mutation_prob,crossover_prob,max_gen,alpha,beta]
        
        theoretical_max = (alpha*(nTasks-1)+beta)*compCap*n*n
        #theoretical_max = 1500
        print("Theoretical max = %f" % theoretical_max)
        # Generate individual files if required
        outfile = open("results_hps/best_n_"+str(n)+"_"+str(repl)+".csv","w+")
        outfile.write("# nTasks %d\n" % nTasks)
        outfile.write("# compCap %d\n" % compCap)
        outfile.write("# exp_eff %f\n" % exp_eff)
        outfile.write("# alpha %f\n" % alpha)
        outfile.write("# beta %f\n" % beta)
        outfile.write("# pop_size %d\n" % pop_size)
        outfile.write("# mut_prob %f\n" % mutation_prob)
        outfile.write("# cross_prob %f\n" % crossover_prob)
        outfile.write("generation,best_sw\n")
       
        
 
        a = init_Pop(conf)
        b = genetic_algorithm(a,conf)
        
        for i in range(max_gen):
            #print i
            b = genetic_algorithm(b,conf)
            fitness_arr = np.asarray(social_welfare(b,conf))
            inds = fitness_arr.argsort()[::-1]
            sortedPop = b[inds]
            best_sw = fitness_arr.max()
            outfile.write("%d,%f\n" % (i,best_sw))
            #print(best_sw)
            if best_sw >= theoretical_max:
                hps_file.write("%d,%d,%f,%f,%d\n" % (n,repl,theoretical_max,best_sw,i))
                break

        
hps_file.close()
