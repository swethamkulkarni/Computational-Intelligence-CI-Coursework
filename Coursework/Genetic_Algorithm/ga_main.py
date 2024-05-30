#Genetic Algorithm
import random
def first_fit_decreasing(order, stock_lengths, stock_costs):
    """ Apply a First-Fit Decreasing heuristic to pack pieces into stocks """
    # Creating a list of items with their quantities repeated correctly
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
def crossover(parent1, parent2):
    """ Perform a two-point crossover between two parents """
    size = min(len(parent1), len(parent2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    child1 = parent1[:cxpoint1] + parent2[cxpoint1:cxpoint2] + parent1[cxpoint2:]
    child2 = parent2[:cxpoint1] + parent1[cxpoint1:cxpoint2] + parent2[cxpoint2:]
    return child1, child2
# Tournament selection
def tournament_selection(population, fitness_values, tournament_size=3):
    parents = []
    for _ in range(len(population)//2):
        tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
        parent1 = min(tournament, key=lambda x: x[1])[0]
        tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
        parent2 = min(tournament, key=lambda x: x[1])[0]
        parents.append(parent1)
        parents.append(parent2)
    return parents
def mutate(solution, mutation_rate=0.1):
    """ Mutate an individual by swapping two elements with a given mutation rate """
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            swap_idx = random.randint(0, len(solution) - 1)
            solution[i], solution[swap_idx] = solution[swap_idx], solution[i]
    return solution

def generate_initial_population(pop_size, order):
    """ Generate an initial population from the order """
    population = []
    for _ in range(pop_size):
        new_order = order[:]
        random.shuffle(new_order)
        population.append(new_order)
    return population
def genetic_algorithm(population_size, generations, stock_lengths, stock_costs, order_lengths, order_quantities):
    order = [length for length, qty in zip(order_lengths, order_quantities) for _ in range(qty)]
    population = generate_initial_population(population_size, order)
    best_solution = None
    best_cost = float('inf')

    for generation in range(generations):
        new_population = []
        fitness_values = []

        for individual in population:
            _, cost = first_fit_decreasing(individual, stock_lengths, stock_costs)
            fitness_values.append(cost)
            if cost < best_cost:
                best_cost = cost
                best_solution = individual

        # Tournament selection and reproduction
        population = tournament_selection(population, fitness_values, population_size)

    return best_solution, best_cost

# Define parameters
stock_lengths = [120, 115, 110, 105, 100]
stock_costs = [12, 11.5, 11, 10.5, 10]
order_lengths = [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67]
order_quantities = [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17]

# Run the genetic algorithm
best_solution, best_cost = genetic_algorithm(
    population_size=100,
    generations=50,
    stock_lengths=stock_lengths,
    stock_costs=stock_costs,
    order_lengths=order_lengths,
    order_quantities=order_quantities
)

print("Best Solution:", best_solution)
print("Best Cost:", best_cost)
