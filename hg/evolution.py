import numpy as np
import pandas as pd
import sklearn
import pygad
import pmlb
from multiprocessing import Pool
from sklearn.model_selection import train_test_split
import time
import uuid
import pickle
import os
from collections import Counter
import randomname
from sklearn.model_selection import cross_validate
from pprint import pprint
from datetime import date
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from initialisation import initialization
from utils import save_model


WORK_DIR = Path(__file__).parent 
print(WORK_DIR)

def fitness_wrapper(solution):
    return fitness_func(solution, 0)
class PooledGA(pygad.GA):

    def cal_pop_fitness(self):
        global pool
        start_time = time.time()
        pop_fitness = pool.map(fitness_wrapper, self.population)
        # print(pop_fitness)
        pop_fitness = np.array(pop_fitness)
        end_time = time.time() - start_time
        print('fitness time (s):', end_time)
        return pop_fitness

def fitness_func(solution, solution_idx):

    # global model, task, model_params, model_params_lst, X
    # print(model_params_lst)
    # print(model_params[task])
    params = dict()
    if solution_idx:
        rand_state = solution_idx + 4576
    else:
        rand_state = 4576 
    params['random_state'] = rand_state

    for i, param in enumerate(model_params_lst):
        # print(model_params[param][solution[i]])
        params[param] = model_params[param][solution[i]] 

    gen_idx = len(model_params_lst)-1
    selected_features = list(set(solution[gen_idx:]))
    

    clf = model.set_params(**params)
    # fitness = np.mean(cross_validate(clf, X[:,selected_features], y, cv=5))
    scores = cross_validate(clf, X[:,selected_features], y, scoring=scoring, 
                            cv=5, return_train_score=True)
    fitness = np.mean(scores['test_' + fitness_metric])
    # fitness = 1.0 / (np.abs(output - 1) + 0.000001)
    save_model(clf, solution, solution_idx, fitness, scores, selected_features, gen_idx)
    return fitness

solution_fitness_gen = []
solution_idx_gen = []
solution_gen = []
def on_generation(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # solution_gen.append(solution)
    # solution_idx_gen.append(solution_idx)
    # solution_fitness_gen.append(solution_fitness)    
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))  

def evolution(X, y, models=None, task=None):

        if not models:
            models = ['DecisionTreeClassifier']
        task, model_name, model, scoring, fitness_metric = initialisation(X, y, models)
        model, model_params, model_params_lst, gene_space = prepare_params(model_name,
                                                                            model, X, 
                                                                            task)
        # print(model_params, model_params_lst) 
                                                    
        num_genes = len(gene_space)
        num_mutations_high = int(num_genes / 2)
        num_mutations_low = int(num_mutations_high / 3)
        gene_type = np.int8
        start_time = time.time()

        current_run_id = ('{random_name}-{start_time}'
                    .format(start_time=date.fromtimestamp(start_time).strftime('%d-%m-%y'),                                            
                                                    random_name = randomname.get_name()))
         
        Path(os.path.join(WORK_DIR,'/artifacts/models/{current_run_id}'.format(current_run_id=current_run_id))).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(WORK_DIR,'/artifacts/metadata/{current_run_id}'.format(current_run_id=current_run_id))).mkdir(parents=True, exist_ok=True)   
        print('Current experiment:', current_run_id)                                            
        ga_instance = PooledGA(num_generations=3,
                            fitness_func=fitness_func,
                            num_parents_mating=40,
                            parent_selection_type="tournament",
                            K_tournament=10,
                            sol_per_pop=60,
                            num_genes=num_genes,
                            gene_space=gene_space,
                            gene_type=gene_type,
                            mutation_type="adaptive",
                            mutation_num_genes=(num_mutations_high, num_mutations_low),
                            on_generation=on_generation, 
                            save_solutions=False,
                            save_best_solutions=False,
                            stop_criteria=["saturate_20"])
        with Pool(processes=4) as pool:
            ga_instance.run()

            solution, solution_fitness, solution_idx = ga_instance.best_solution()
            print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
            print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

            print("--- %s seconds ---" % (time.time() - start_time))

    

    # After the generations complete, some plots are showed that summarize how the outputs/fitness values evolve over generations.
    ga_instance.plot_result(title="Iteration vs. Fitness", linewidth=4)

    print("Number of generations passed is {generations_completed}".format(generations_completed=ga_instance.generations_completed))
    #  Saving the GA instance.
    filename = '{current_run_id}'.format(current_run_id=current_run_id) # The filename to which the instance is saved. The name is without extension.
    ga_instance.save(filename=filename)
    return current_run_id, solution, solution_fitness, solution_idx

# Loading the saved GA instance.
# loaded_ga_instance = pygad.load(filename=filename)
# loaded_ga_instance.plot_fitness()

if '__name__' == '__main__':
    evolution(X, y, models=None)
