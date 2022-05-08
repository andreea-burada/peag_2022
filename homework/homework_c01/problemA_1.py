# An airline intends to extend its air fleet by purchasing three types of aircrafts, denoted by
# I, II and III respectively. The available budget is 5000 units. The three types have the following features:
# I. costs 100 units, has a range of 6.000 km and the collision avoidance system range is 30 km;
# II. costs 60 units, has a range of 4.200 km and the collision avoidance system range is 48 km;
# III. costs 50 units, has a range of 2.800 km and the collision avoidance system range is 32 km;

# Compute how many aircrafts from each type should be purchased such that
# - the budget is not exceeded
# - the mean flight range is maximized
# - the mean of the collision avoidance system range is at least 40 km.

# Solve A using the backtracking algorithm (design + source code)

# --- the backtracking approach ---

# restrictions / parameters
budget = 5000
min_collision_range = 40
no_types = 3


# declaring the class that will hold the properties of each type
class Aircraft:
    # cost = 0
    # range = 0
    # collision_range = 0

    def __init__(self):
        self.cost = 0
        self.range = 0
        self.collision_range = 0

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


# partial verification - backtracking
def possible(x, i, price):
    accepted = 1
    current_budget = 0
    for j in range(0, i + 1):
        current_budget += x[j] * price
    if current_budget > budget:
        accepted = 0
    return accepted


def add(to_test, solutions):
    collision_range_mean = 0.0
    range_max_test = 0.0
    range_max_sol = 0.0
    test_count = 0
    sol_count = 0
    for i in range(0, no_types):
        range_max_sol += solutions[i] * aircraft_type[i].range
        range_max_test += to_test[i] * aircraft_type[i].range
        collision_range_mean += to_test[i] * aircraft_type[i].collision_range
        test_count += to_test[i]
        sol_count += solutions[i]
    a = 0
    if sol_count == 0 and test_count > 0:
        a = 1
    if test_count != 0 and sol_count != 0:
        if collision_range_mean / test_count >= min_collision_range and range_max_test / test_count >= range_max_sol / sol_count:
            a = 1
    if a:
        for i in range(no_types):
            solutions[i] = to_test[i]
    return solutions


def aircraft_backtracking():
    solution = [0, 0, 0]  # an array of 3 elements which specifies how many of each aircrafts we should buy
    current = [0, 0, 0]
    max_items = [budget / aircraft_type[0].cost, budget / aircraft_type[1].cost, budget / aircraft_type[2].cost]
    i = 0
    current[i] = -1
    while i >= 0:
        under_testing = 0
        while current[i] < max_items[i] and under_testing == 0:
            current[i] += 1
            under_testing = possible(current, i, aircraft_type[i].cost)
        if under_testing == 0:
            i -= 1
        else:
            if i == no_types - 1:
                solution = add(current, solution)
            else:
                i += 1
                current[i] = -1

    return solution


def main():
    final_solution = []
    final_solution = aircraft_backtracking()
    print("Final solution\n\tAircraft type I: {} units\n\tAircraft type II: {} units\n\tAircraft type III: {} units"
          .format(final_solution[0], final_solution[1], final_solution[2]))
