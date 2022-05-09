# Arrange m dogs and n cats (n>1) in a circle such that there are either no cats or
# at least two cats between each pair of consecutive dogs.

from dataclasses import dataclass
import numpy as np
import matplotlib.pylab as graph


# parameters
@dataclass
class Parameters:
    pop_size: int = 40
    n: int = 35      # number of cats
    m: int = 26     # number of dogs
    pets: int = 0
    max_iterations: int = 500
    crossover_probability: float = 0.8
    mutation_probability: float = 0.1


parameters = Parameters()
parameters.pets = parameters.n + parameters.m

# individual -> permutation of n + m
# if x[i] between 0 and n - 1 -> cat
# if x[i] between n and n + m -1 -> dog


# fitness/objective function
def fitness_func(individual):
    # we iterate by one the no of bad cases when we find just one cat between two dogs
    no_bad_cat_seq = 0
    for i in range(parameters.pets - 2):
        # if we find a dog we check whether the next element is a cat and the one after that is a dog
        if (parameters.n <= individual[i] < parameters.pets) and (0 <= individual[i + 1] < parameters.n) \
                and (parameters.n <= individual[i + 2] < parameters.pets):
            no_bad_cat_seq += 1
    # we check if we have an invalid case around the circle
    # case 1 -> between the last one and the first two ones
    if (parameters.n <= individual[parameters.pets - 1] < parameters.pets) and (0 <= individual[0] < parameters.n) \
            and (parameters.n <= individual[1] < parameters.pets):
        no_bad_cat_seq += 1
    # case 2 -> between the second to last, last and first one
    if (parameters.n <= individual[parameters.pets - 2] < parameters.pets) and (0 <= individual[parameters.pets - 1] < parameters.n) \
            and (parameters.n <= individual[0] < parameters.pets):
        no_bad_cat_seq += 1
    return 1 / (1 + no_bad_cat_seq)  # the solution of the GA will have fitness val = 1


# generate pop
def gen_pop():
    pop = []
    init_pop_fitness = []
    # individual - a permutation of n elements
    # we generate individual by individual
    for i in range(parameters.pop_size):
        x = np.random.permutation(parameters.pets)
        pop += [x]
        init_pop_fitness += [fitness_func(x)]
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


# PMX implementation
# crossover section (p1, p2)
def PMX(p1, p2, pos1, pos2):
    # gen. a new child with all elements -1
    new_child = -np.ones(parameters.pets, dtype=int)
    # copy the common section into the new child
    new_child[pos1:pos2 + 1] = p1[pos1:pos2 + 1]
    for i in range(pos1, pos2 + 1):
        # placing allele a
        a = p2[i]
        if a not in new_child:
            current = i
            placed = False
            while not placed:
                b = p1[current]
                # pos = where b is in p2
                [pos] = [j for j in range(parameters.pets) if p2[j] == b]
                if new_child[pos] == -1:
                    new_child[pos] = a
                    placed = True
                else:
                    current = pos
    # z = the array of alleles from p2 not yet copied in new_child
    z = [p2[i] for i in range(parameters.pets) if p2[i] not in new_child]
    # pos - the array of positions from p2 yet not copied in new_child
    pos = [i for i in range(parameters.pets) if new_child[i] == -1]
    # copying the remaining alleles
    m = len(pos)
    for i in range(m):
        new_child[pos[i]] = z[i]

    return new_child


# PMX (partially mapped crossover) crossover
# used for problems with adjacency dependence
def PMX_crossover(p1, p2):
    # generate the crossover section
    pos = np.random.randint(0, parameters.pets, 2)
    while pos[0] == pos[1]:
        pos = np.random.randint(0, parameters.n, 2)
    pos1 = np.min(pos)
    pos2 = np.max(pos)
    c1 = PMX(p1, p2, pos1, pos2)
    c2 = PMX(p2, p1, pos1, pos2)

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
            child_1, child_2 = PMX_crossover(parent_1, parent_2)
            children_pop[i] = child_1.copy()
            c1_fitness = fitness_func(child_1)
            children_fitness[i] = c1_fitness

            children_pop[i + 1] = child_2
            c2_fitness = fitness_func(child_2)
            children_fitness[i + 1] = c2_fitness

    children_pop = np.asarray(children_pop)
    children_fitness = np.asarray(children_fitness)
    return children_pop, children_fitness


# mutate individual by swap mutation
def permutation_mutation(to_mutate):
    # generating the positions for swapping
    pos = np.random.randint(0, parameters.pets, 2)
    while pos[0] == pos[1]:
        pos = np.random.randint(0, parameters.pets, 2)
    pos1 = np.min(pos)
    pos2 = np.max(pos)
    mutated = to_mutate.copy()
    mutated[pos1] = to_mutate[pos2]
    mutated[pos2] = to_mutate[pos1]

    return mutated


# population mutation
def pop_mutation(pop, pop_fitness):
    mutated_pop = pop.copy()
    mutated_pop_fitness = pop_fitness.copy()
    for i in range(parameters.pop_size):
        prob = np.random.uniform(0, 1)
        if prob <= parameters.mutation_probability:
            to_mutate = mutated_pop[i]
            mutated = permutation_mutation(to_mutate)
            mutated_pop[i] = mutated
            mutated_pop_fitness[i] = fitness_func(mutated)

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

# size = (int)(input("Population size ( > 0 ): "))
# parameters.pop_size = size
# it = (int)(input("\nMaximum number of iterations:"))
# parameters.max_iterations = it
# cp = (float)(input("\nCrossover probability (between 0 and 1):"))
# parameters.crossover_probability = cp
# mp = (float)(input("\nMutation probability (between 0 and 1):"))
# parameters.crossover_probability = mp

def GA():
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
        best_fit_history.append(np.max(next_pop_fitness))

        if next_pop_max == best_fit_history[iteration]:
            nrm += 1
        else:
            nrm = 0
        if next_pop_max == 1 or nrm == int(parameters.max_iterations / 3):
            done = True
        else:
            iteration += 1

        initial_pop = next_pop.copy()
        initial_pop_fitness = next_pop_fitness.copy()

    initial_pop_fitness = np.asarray(initial_pop_fitness)
    max_position = np.where(initial_pop_fitness == next_pop_max)
    max_individual = initial_pop[max_position[0][0]]
    max_fitness = next_pop_max

    print("We did {} iterations".format(iteration + 2))
    print("\nBest individual: ")
    print(max_individual)
    # for i in range(parameters.pets):
    #     if 0 <= max_individual[i] < parameters.n:
    #         print("cat")
    #     else:
    #         print("dog")
    print("\nBest fitness: ")
    print(np.round(max_fitness, 4))

    # graph display
    yaxis = best_fit_history.copy()
    xaxis = []
    for i in range(iteration + 2):
        xaxis += [i + 1]

    graph.title("Best Fitness Values over {0} iterations".format(iteration + 2))
    graph.xlabel("Iteration no.")
    graph.ylabel("Best fitness value of  x")
    graph.plot(xaxis, yaxis)
    graph.show()

# import problem as p
# p.GA()
