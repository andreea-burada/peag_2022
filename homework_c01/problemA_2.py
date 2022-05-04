# An airline intends to extend its air fleet by purchasing three types of aircrafts, denoted by
# I, II and III respectively. The available budget is 5000 units. The three types have the following features:
# I. costs 100 units, has a range of 6.000 km and the collision avoidance system range is 30 km;
# II. costs 60 units, has a range of 4.200 km and the collision avoidance system range is 48 km;
# III. costs 50 units, has a range of 2.800 km and the collision avoidance system range is 32 km;

# Compute how many aircrafts from each type should be purchased such that
# - the budget is not exceeded
# - the mean flight range is maximized
# - the mean of the collision avoidance system range is at least 40 km.

# Solve A using an EA (design)

# --- the GA approach ---

# imports
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as graph


# restrictions / parameters
@dataclass
class Parameters:
    budget: int = 5000
    min_collision_range: int = 40
    no_types: int = 3
    no_iterations: int = 250
    pop_size: int = 20
    crossover_prob: float = 0.8
    mutation_prob: float = 0.3


parameters = Parameters()


# declaring the class that will hold the properties of each type
class Aircraft:

    # def __init__(self):
    #     self.cost = 0
    #     self.range = 0
    #     self.collision_range = 0

    def __init__(self, c, r, cr):
        self.cost = c
        self.range = r
        self.collision_range = cr


# declaring the vector of aircrafts that will store the 3 types
aircraft_type = []
# for i in range(3):
#     aircraft_type[i] = Aircraft()

# initializing the three aircraft
# type I
# aircraft_type[0].cost = 100
# aircraft_type[0].range = 6000
# aircraft_type[0].collision_range = 30
aircraft_type.append(Aircraft(100, 6000, 30))

# type II
# aircraft_type[1].cost = 60
# aircraft_type[1].range = 4200
# aircraft_type[1].collision_range = 48
aircraft_type.append(Aircraft(60, 4200, 48))

# type III
# aircraft_type[2].cost = 50
# aircraft_type[2].range = 2800
# aircraft_type[2].collision_range = 32
aircraft_type.append(Aircraft(50, 2800, 32))

max_units = [parameters.budget // aircraft_type[0].cost,
             parameters.budget // aircraft_type[1].cost,
             parameters.budget // aircraft_type[2].cost]


# checking the feasibility of an individual and calculating the objective function
def check(to_check):
    total_range = 0
    total_cost = 0
    for i in range(parameters.no_types):
        total_range = total_range + to_check[i] * aircraft_type[i].range
        total_cost = total_cost + to_check[i] * aircraft_type[i].cost
    return total_cost <= parameters.budget, total_range


# initial population
def generate():
    current = []
    obj_func_value = 0
    # population list
    pop = []
    # generating individual by individual
    for i in range(parameters.pop_size):
        done = False
        while not done:
            # generate current candidate
            current = np.random.randint(0, max(max_units), parameters.no_types)
            done, obj_func_value = check(
                current)  # obj_func_value is the range value of the individual - objective function value
        # when we exit the while -> we found a feasible candidate
        current = list(current)
        # add range total value at the end of the list (obj. func. value)
        current += [obj_func_value]
        # add the individual to the population
        pop += [current]
    return pop


# uniform crossover between p1 and p2
def uniform_crossover(p1, p2):
    # copying the parents into the children
    c1 = p1.copy()
    c2 = p2.copy()
    # crossover
    alpha = np.random.randint(0, 2, parameters.no_types)
    for i in range(parameters.no_types):
        if alpha[i] == 1:
            c1[i] = p2[i]
            c2[i] = p1[i]
    return c1, c2


# applying uniform crossover on the population
def pop_crossover(pop):
    children_pop = []
    # we choose 2 by 2
    for i in range(0, parameters.pop_size - 1, 2):
        # parent selection
        p1 = pop[i]
        p2 = pop[i + 1]
        # generate random probability
        alpha = np.random.uniform(0, 1)
        if alpha <= parameters.crossover_prob:
            # crossing over p1 and p2 - uniform
            # we take the first 3 elements of each parent because the 4th is the cost
            c1, c2 = uniform_crossover(p1[:parameters.no_types], p2[:parameters.no_types])
            # we check c1
            isGood, total_cost_c1 = check(c1)
            if isGood:
                c1 += [total_cost_c1]
            else:
                c1 = p1.copy()
            # we check c2
            isGood, total_cost_c2 = check(c2)
            if isGood:
                c2 += [total_cost_c2]
            else:
                c2 = p2.copy()
        else:
            # asexual recombination
            c1 = p1.copy()
            c2 = p2.copy()

        # we add the children to the new population
        children_pop += [c1]
        children_pop += [c2]
    return children_pop


# uniform mutation - array of real numbers
def uniform_mutation(first, last):
    new = int(np.random.uniform(first, last))
    return new


# mutating the children population
def pop_mutation(children_pop):
    mutated_pop = children_pop.copy()
    for i in range(parameters.pop_size):
        # we make a copy of individual i from children_pop
        current = children_pop[i][:parameters.no_types].copy()
        alpha = np.random.uniform(0, 2, parameters.no_types)
        for j in range(parameters.no_types):
            if alpha[j] <= parameters.mutation_prob:
                # the mutation
                current[j] = uniform_mutation(0, max_units[j])
        # we check if the mutated individual is feasible
        isGood, total_cost = check(current)
        if isGood:
            current += [total_cost]
            mutated_pop[i] = current.copy()

    return mutated_pop


# select the best individual from the population and return its position in the population
def pop_selection(pop):
    max_range = -1
    chosen = []
    pos = -1
    for i in range(parameters.pop_size):
        current = pop[i][:parameters.no_types]
        total_range = 0
        total_col_range = 0
        total_cost = 0
        for j in range(parameters.no_types):
            total_range += current[j] * aircraft_type[j].range
            total_col_range += current[j] * aircraft_type[j].collision_range
            total_cost += current[j] * aircraft_type[j].cost
        if total_range > max_range and total_col_range > 0:
                if total_col_range / (current[0] + current[1] + current[2]) > parameters.min_collision_range:
                    max_range = total_range
                    chosen = current.copy()
                    pos = i
    return chosen, pos, max_range


def elitism(pop, children_pop):
    new_pop = children_pop.copy()
    best_child, pos_child, child_range = pop_selection(children_pop)
    best_parent, pos_parent, parent_range = pop_selection(pop)
    # we check if the best parent is better than the best child
    parent_range_mean = parent_range / (best_parent[0] + best_parent[1] + best_parent[2])
    child_range_mean = child_range / (best_child[0] + best_child[1] + best_child[2])
    if parent_range_mean > child_range_mean:
        # we get rid of a random child and keep the parent
        rand_pos = np.random.randint(0, parameters.pop_size)
        new_pop[rand_pos] = best_parent
    return new_pop


# choose the best option from the population
def best_individual(pop):
    max_range = -1
    best_ind_cost = 0
    best_col_range = 0
    chosen = []
    for i in range(parameters.pop_size):
        current = pop[i][:parameters.no_types]
        total_range = 0
        total_col_range = 0
        total_cost = 0
        for j in range(parameters.no_types):
            total_range += current[j] * aircraft_type[j].range
            total_col_range += current[j] * aircraft_type[j].collision_range
            total_cost += current[j] * aircraft_type[j].cost
        if total_range > max_range and (
                total_col_range / (current[0] + current[1] + current[2]) > parameters.min_collision_range):
            max_range = total_range
            chosen = current.copy()
            best_ind_cost = total_cost
            best_col_range = total_col_range
    return chosen, max_range, best_ind_cost, best_col_range


# running the EA for a certain number of iterations
pop = generate()
for i in range (parameters.no_iterations):

    current_best, rangeC, cost, col_range = best_individual(pop)
    new_pop = pop_crossover(pop)
    new_pop = pop_mutation(new_pop)
    pop = elitism(pop, new_pop)
    if (i + 1) % 10 == 0:
        print("Iteration number {}".format(i + 1))
        print("\tBest individual of iteration {}: {}\t  Cost: {}\t Range: {}\tCol. range: {}\n".format(i + 1, current_best[:parameters.no_types], cost, rangeC, col_range))


# testing code
# test_pop = generate()
# print(test_pop)
# test_pop_2 = pop_crossover(test_pop)
# print(test_pop_2)
# test_pop_2 = pop_mutation(test_pop_2)
# print(test_pop_2)
