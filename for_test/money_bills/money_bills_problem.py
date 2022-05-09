# Utilizați un algoritm genetic pentru a rezolva problema: pentru plata unei sume S se pot folosi bancnote cu n valori nominale distincte (v[i], i=1,…,n).
# NU este disponibila bancnota cu valoare 1. Pentru fiecare valoare nominala este disponibila o cantitate limitata de bancnote (c[i], i=1,…,n).
# Găsiți o modalitate de plata care folosește numărul minim de bancnote. Este utilizat un algoritm genetic.

# imports
from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as graph


# parameters
@dataclass
class Parameters:
    pop_size: int = 100
    n: int = 7
    max_iterations: int = 500
    to_pay: int = 50  # sum we have to pay
    bill_values: list = field(default_factory=lambda: [])
    max_bill_amounts: list = field(default_factory=lambda: [])
    crossover_probability: float = 0.8
    mutation_probability: float = 0.1
    # bill_value_txt : str = "bill_values.txt"
    # bill_amounts_txt: str = "bill_amounts.txt"


parameters = Parameters()

parameters.bill_values = [2, 3, 5, 7, 10, 11, 13]
# parameters.bill_values = np.genfromtxt(parameters.bill_value_txt)

parameters.max_bill_amounts = [8, 11, 2, 3, 5, 7, 4]


# parameters.max_bill_amounts = np.genfromtxt(parameters.bill_amounts_txt)


# cost function
# cost_v to avoid having the same variable name in two functions
def cost_func(individ):
    cost_v = 0
    for i in range(parameters.n):
        cost_v += individ[i]
    return cost_v


# fitness function
def fitness_func(individ):
    cost = cost_func(individ)
    return 1 / (1 + cost)


# check feasibility
def isFeasible(individ):
    value_sum = 0
    for i in range(parameters.n):
        value_sum += individ[i] * parameters.bill_values[i]
    if value_sum != parameters.to_pay:
        return False  # non feasible individual
    return True  # feasible individual


# generating the initial population and the array of fitness values
def gen_pop():
    pop = []
    init_pop_fitness = []
    # individual
    # an array of length parameters.n where individual[i] represents the amount of parameters.bill_values[i] bills used
    # we generate individual by individual
    # when generating a new individual, we make sure that the values comply to the restriction (x[i] < parameters.max_bill_amounts[i])
    for i in range(parameters.pop_size):
        x = []
        wasAccepted = False
        # we generate the individual until we get a feasible individual
        while wasAccepted == False:
            # we generate element by element in the individual
            x_fitness = 0
            for j in range(parameters.n):
                current_value = np.random.randint(0, parameters.max_bill_amounts[j] + 1)
                x += [current_value]
            # after we have an individual, we check if it is feasible
            if isFeasible(x) == True:
                wasAccepted = True
                pop += [x]  # we add x to the population
                x_fitness = fitness_func(x)
                init_pop_fitness += [x_fitness]
            else:
                x = []
    pop = np.asarray(pop)
    init_pop_fitness = np.asarray(init_pop_fitness)
    return pop, init_pop_fitness


# fps (fitness proportional selection)
def fps(pop_fitness_ar):
    fps_array = np.zeros(parameters.pop_size)
    fitness_sum = np.sum(pop_fitness_ar)
    for i in range(parameters.pop_size):
        fps_array[i] = pop_fitness_ar[i] / fitness_sum
    fps_qualities = fps_array.copy()
    for i in range(1, parameters.pop_size):
        fps_qualities[i] = fps_qualities[i - 1] + fps_array[i]
    return fps_qualities


# sigma scaling for fps
def sigma_fps(pop_fitness_ar):
    mean_val = np.mean(pop_fitness_ar)
    std_deviation = np.std(pop_fitness_ar)
    new_qual = [max(0, pop_fitness_ar[i] - (mean_val - 2 * std_deviation)) for i in range(parameters.pop_size)]
    if np.sum(new_qual) == 0:
        fps_qualities = fps(pop_fitness_ar)
    else:
        fps_qualities = fps(new_qual)
    return fps_qualities


# SUS (stochastic universal sampling) selection
# pop_fitness_ar - the array of fitness values of the population
def SUS_selection(pop, pop_fitness_ar):
    selected_pop = pop.copy()
    selected_pop_fitness = np.zeros(parameters.pop_size)
    fps_qualities = sigma_fps(pop_fitness_ar)
    r = np.random.uniform(0, 1 / parameters.pop_size)
    k = 0
    i = 0
    while k < parameters.pop_size:
        while r < fps_qualities[i]:
            selected_pop[k][:] = pop[i][:]
            selected_pop_fitness[k] = pop_fitness_ar[i]
            r = r + 1 / parameters.pop_size
            k += 1
        i += 1
    return selected_pop, selected_pop_fitness


# uniform crossover function
def uniform_crossover(p1, p2):
    c1 = p1.copy()
    c2 = p2.copy()
    for i in range(parameters.n):
        doWeSwitch = np.random.randint(0, 2)
        if doWeSwitch == 1:
            c1[i] = p2[i]
            c2[i] = p1[i]
    return c1, c2


# population crossover
def crossover_pop(pop, pop_fitness):
    children_pop = pop.copy()
    children_fitness = pop_fitness.copy()
    for i in range(0, parameters.pop_size - 1, 2):
        parent_1 = pop[i]
        parent_2 = pop[i + 1]
        r = np.random.uniform(0, 1)
        if r <= parameters.crossover_probability:
            child_1, child_2 = uniform_crossover(parent_1, parent_2)
            # we check if child 1 is feasible
            isC1Good = isFeasible(child_1)
            if isC1Good:
                c1_fitness = fitness_func(child_1)
                child_1 = list(child_1)
                children_pop[i] = child_1.copy()
                children_fitness[i] = c1_fitness
            # we check if child 2 is feasible
            isC2Good = isFeasible(child_2)
            if isC2Good:
                c2_fitness = fitness_func(child_2)
                child_2 = list(child_2)
                children_pop[i + 1] = child_2.copy()
                children_fitness[i + 1] = c2_fitness

    children_pop = np.asarray(children_pop)
    # children_fitness = np.asarray(children_fitness)
    return children_pop, children_fitness


# creep mutation
def creep_mutation(to_mutate, lower_bound, higher_bound):
    prob = np.random.randint(0, 2)
    if prob == 1:
        sign = 1
    else:
        sign = -1

    mutated = to_mutate + sign
    if mutated > higher_bound:
        mutated = higher_bound
    if mutated < lower_bound:
        mutated = lower_bound

    return mutated


# population mutation
def pop_mutation(pop, pop_fitness):
    mutated_pop = pop.copy()
    mutated_pop_fitness = pop_fitness.copy()
    for i in range(parameters.pop_size):
        possible_mutant = pop[i].copy()
        for j in range(parameters.n):
            prob = np.random.uniform(0, 1)
            if prob <= parameters.mutation_probability:
                possible_mutant[j] = creep_mutation(possible_mutant[j], 0, parameters.max_bill_amounts[j])
        isGood = isFeasible(possible_mutant)
        if isGood:
            mutant_fitness = fitness_func(possible_mutant)
            possible_mutant = list(possible_mutant)
            mutated_pop[i] = possible_mutant.copy()
            mutated_pop_fitness[i] = mutant_fitness

    return mutated_pop, mutated_pop_fitness


# elitism for future generation
def elitism(pop_p, pop_p_fitness, pop_c, pop_c_fitness):
    better_pop = pop_c.copy()
    better_pop_fitness = pop_c_fitness.copy()
    max_child = np.max(pop_c_fitness)
    max_parent = np.max(pop_p_fitness)
    if max_parent > max_child:
        p1 = np.where(pop_p_fitness == max_parent)
        imax = p1[0][0]
        to_replace = np.random.randint(parameters.pop_size)
        better_pop[to_replace] = pop_p[imax].copy()
        better_pop_fitness[to_replace] = max_parent

    return better_pop, better_pop_fitness


# ----------- the GA ------------
def GA():
    # size = (int)(input("Population size ( > 0 ): "))
    # parameters.pop_size = size
    # it = (int)(input("\nMaximum number of iterations:"))
    # parameters.max_iterations = it
    # cp = (float)(input("\nCrossover probability (between 0 and 1):"))
    # parameters.crossover_probability = cp
    # mp = (float)(input("\nMutation probability (between 0 and 1):"))
    # parameters.crossover_probability = mp

    next_pop_max = -1

    initial_pop, initial_pop_fitness = gen_pop()
    best_fit_history = [np.max(initial_pop_fitness)]
    iteration = 0
    done = False
    nrm = 1
    while iteration < parameters.max_iterations and not done:
        parent_pop, parent_fitness = SUS_selection(initial_pop, initial_pop_fitness)
        children_pop, children_fitness = crossover_pop(parent_pop, parent_fitness)
        mutated_children_pop, mutated_children_fitness = pop_mutation(children_pop, children_fitness)
        next_pop, next_pop_fitness = elitism(initial_pop, initial_pop_fitness, mutated_children_pop,
                                             mutated_children_fitness)

        next_pop_min = np.min(next_pop_fitness)
        next_pop_max = np.max(next_pop_fitness)

        if next_pop_max == best_fit_history[iteration]:
            nrm += 1
        else:
            nrm = 0
        if next_pop_max == next_pop_min or nrm == int(parameters.max_iterations / 3):
            done = True
        else:
            iteration += 1

        best_fit_history.append(np.max(next_pop_fitness))
        initial_pop = next_pop.copy()
        initial_pop_fitness = next_pop_fitness.copy()

    initial_pop_fitness = np.asarray(initial_pop_fitness)
    max_position = np.where(initial_pop_fitness == next_pop_max)
    max_individual = initial_pop[max_position[0][0]]
    max_fitness = next_pop_max

    print("We did {} iterations".format(iteration + 2))
    print("\nBest individual: ")
    print(max_individual)
    print("\nBest fitness: ")
    print(np.round(max_fitness, 4))

    # graph display
    yaxis = best_fit_history.copy()
    xaxis = []
    for i in range(iteration + 2):
        xaxis += [i + 1]

# import money_bills_problem as b
# b.GA()