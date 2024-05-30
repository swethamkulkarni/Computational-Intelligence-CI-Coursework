import random

def initialize_pheromones(stock_lengths, initial_pheromone):
    return {length: initial_pheromone for length in stock_lengths}

def update_pheromones(pheromones, solutions, stock_costs, stock_lengths, generation, max_generations, decay=0.1):
    """ Update pheromones with adaptive alpha and beta values. """
    alpha = 1 - (generation / max_generations)  # Decreases over time
    beta = 1 + (generation / max_generations)  # Increases over time

    for length in pheromones:
        pheromones[length] *= (1 - decay)  # Pheromone evaporation

    for length in stock_lengths:
        total_waste = 0
        for solution in solutions:
            items_fit = sum(item * solution[length] for item in solution if item <= length)
            waste = max(0, length * solution.get(length, 0) - items_fit)
            total_waste += waste

        if total_waste > 0:
            reward = (alpha / (total_waste + 1)) * (beta / len(solutions))
            pheromones[length] += reward

def heuristic(stock_length, item, stock_costs):
    cost = stock_costs[stock_lengths.index(stock_length)]
    fit = stock_length - item
    return 1 / (1 + cost * fit)

def local_search(solution, stock_lengths, pheromones, stock_costs):
    """ Improve solution with a more efficient local search strategy. """
    for _ in range(10):  # Perform 10 iterations of local search
        for i, length in enumerate(stock_lengths):
            for j, other_length in enumerate(stock_lengths):
                if i != j and solution[length] > 0 and solution[other_length] > 0:
                    # Try swapping elements between lengths
                    new_solution = solution.copy()
                    new_solution[length] -= 1
                    new_solution[other_length] += 1
                    new_cost = sum(new_solution[l] * stock_costs[stock_lengths.index(l)] for l in new_solution if new_solution[l] > 0)
                    current_cost = sum(solution[l] * stock_costs[stock_lengths.index(l)] for l in solution if solution[l] > 0)
                    if new_cost < current_cost:
                        solution = new_solution
    return solution

def construct_solution(order, stock_lengths, pheromones, stock_costs):
    solution = {length: 0 for length in stock_lengths}
    sorted_order = sorted(order, key=lambda x: -x)  # Descending order for better fit

    for item in sorted_order:
        best_choice = None
        best_score = -1
        for length in stock_lengths:
            if item <= length:
                score = pheromones[length] * heuristic(length, item, stock_costs)
                if score > best_score:
                    best_score = score
                    best_choice = length

        if best_choice:
            solution[best_choice] += 1
    return solution

def ant_colony_optimization(stock_lengths, stock_costs, order_lengths, order_quantities, generations, num_ants):
    order = [length for length, qty in zip(order_lengths, order_quantities) for _ in range(qty)]
    pheromones = initialize_pheromones(stock_lengths, 0.1)
    best_solution = None
    best_cost = float('inf')

    for generation in range(generations):
        solutions = []
        for _ in range(num_ants):
            solution = construct_solution(order, stock_lengths, pheromones, stock_costs)
            solution = local_search(solution, stock_lengths, pheromones, stock_costs)
            solutions.append(solution)
        update_pheromones(pheromones, solutions, stock_costs, stock_lengths, generation, generations)

        for solution in solutions:
            cost = sum(solution[length] * stock_costs[stock_lengths.index(length)] for length in solution if solution[length] > 0)
            if cost < best_cost:
                best_cost = cost
                best_solution = solution

    return best_solution, best_cost

#  problem specifics
stock_lengths = [120, 115, 110, 105, 100]
stock_costs = [12, 11.5, 11, 10.5, 10]
order_lengths = [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67]
order_quantities = [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17]

# Execute the ACO
best_solution, best_cost = ant_colony_optimization(stock_lengths, stock_costs, order_lengths, order_quantities, 100, 20)
print("Best Solution:", best_solution)
print("Best Cost:", best_cost)
