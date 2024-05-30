import random
import time

# Utility Functions
def initialize_pheromones(stock_lengths, initial_pheromone):
    return {length: initial_pheromone for length in stock_lengths}

def update_pheromones(pheromones, solutions, stock_costs, stock_lengths, alpha=1.0, decay=0.1):
    for length in pheromones.keys():
        pheromones[length] *= (1 - decay)  # Pheromone evaporation
        for solution in solutions:
            if length in solution:
                pheromones[length] += (alpha / stock_costs[stock_lengths.index(length)]) * solution[length]

def heuristic(stock_length, item, stock_costs, stock_lengths):
    index = stock_lengths.index(stock_length)
    cost = stock_costs[index]
    fit = stock_length - item
    return 1 / (1 + cost * fit)

def calculate_solution_cost(solution, stock_costs, stock_lengths):
    total_cost = 0
    for length, quantity in solution.items():
        if quantity > 0:
            index = stock_lengths.index(length)
            total_cost += quantity * stock_costs[index]
    return total_cost

# ACO Solution Construction
def construct_solution(order_lengths, order_quantities, stock_lengths, pheromones, stock_costs):
    solution = {length: 0 for length in stock_lengths}
    order = [length for length, qty in zip(order_lengths, order_quantities) for _ in range(qty)]
    for item in sorted(order, reverse=True):
        best_choice = None
        best_score = -1
        for length in stock_lengths:
            if item <= length:
                score = pheromones[length] * heuristic(length, item, stock_costs, stock_lengths)
                if score > best_score:
                    best_score = score
                    best_choice = length
        if best_choice is not None:
            solution[best_choice] += 1
    return solution

# ACO Algorithm
def novel_aco(stock_lengths, stock_costs, order_lengths, order_quantities, generations, num_ants):
    pheromones = initialize_pheromones(stock_lengths, 1.0)
    best_solution = None
    best_cost = float('inf')
    
    for _ in range(generations):
        solutions = []
        for _ in range(num_ants):
            solution = construct_solution(order_lengths, order_quantities, stock_lengths, pheromones, stock_costs)
            cost = calculate_solution_cost(solution, stock_costs, stock_lengths)
            solutions.append(solution)
            if cost < best_cost:
                best_cost = cost
                best_solution = solution
        update_pheromones(pheromones, solutions, stock_costs, stock_lengths)
    
    return best_solution, best_cost

import random
def first_fit_decreasing(order, stock_lengths, stock_costs):
    """ Apply a First-Fit Decreasing heuristic to pack pieces into stocks """
    # Create a list of items with their quantities repeated correctly
    items = []
    for length, qty in zip(order_lengths, order_quantities):
        for _ in range(qty):
            items.append(length)

    # Sort items in decreasing order of size
    items.sort(reverse=True)

    patterns = []
    costs = 0
    for item in items:
        placed = False
        for index, (pattern, stock_length) in enumerate(patterns):
            if sum(pattern) + item <= stock_length:
                pattern.append(item)
                placed = True
                break
        if not placed:
            # Find the smallest stock that can hold the item
            for stock_length, cost in sorted(zip(stock_lengths, stock_costs)):
                if item <= stock_length:
                    patterns.append(([item], stock_length))
                    costs += cost
                    break

    return patterns, costs

# GA population initialization, crossover, mutation
def crossover(parent1, parent2):
    size = min(len(parent1), len(parent2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    child1 = parent1[:cxpoint1] + parent2[cxpoint1:cxpoint2] + parent1[cxpoint2:]
    child2 = parent2[:cxpoint1] + parent1[cxpoint1:cxpoint2] + parent2[cxpoint2:]
    return child1, child2

def mutate(solution, mutation_rate=0.1):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            swap_idx = random.randint(0, len(solution) - 1)
            solution[i], solution[swap_idx] = solution[swap_idx], solution[i]
    return solution

def generate_initial_population(pop_size, order):
    population = []
    for _ in range(pop_size):
        new_order = order[:]
        random.shuffle(new_order)
        population.append(new_order)
    return population

# Genetic Algorithm
def novel_ga(stock_lengths, stock_costs, order_lengths, order_quantities, population_size, generations):
    order = [length for length, qty in zip(order_lengths, order_quantities) for _ in range(qty)]
    population = generate_initial_population(population_size, order)
    best_solution = None
    best_cost = float('inf')

    for generation in range(generations):
        new_population = []
        for individual in population:
            solution, cost = first_fit_decreasing(individual, stock_lengths, stock_costs)
            if cost < best_cost:
                best_cost = cost
                best_solution = solution
        # Assume crossover and mutation functions are defined as above
        population = [mutate(crossover(individual, random.choice(population))[0]) for individual in population]

    return best_solution, best_cost

# Example Usage
#  problem instances as dictionaries
stock_lengths=[120, 115, 110, 105, 100]
stock_costs=[12, 11.5, 11, 10.5, 10]
order_lengths=[21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67]
order_quantities=[13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17]
# Running the algorithms
aco_result = novel_aco(stock_lengths, stock_costs, order_lengths, order_quantities, generations=100, num_ants=20)
ga_result = novel_ga(stock_lengths, stock_costs, order_lengths, order_quantities, population_size=100, generations=50)

# Output results
print("ACO Result:", aco_result)
print("GA Result:", ga_result)
