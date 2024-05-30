import random
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



# Defining a function to run each algorithm multiple times
def run_algorithm(algorithm, params, runs=30):
    results = []
    for _ in range(runs):
        start_time = time.time()
        solution, cost = algorithm(**params)
        end_time = time.time()
        results.append({
            'cost': cost,
            'time': end_time - start_time,
            'solution': solution
        })
    return results

# Defining problem instances
problem_params = {
    "stock_lengths": [120, 115, 110, 105, 100],
    "stock_costs": [12, 11.5, 11, 10.5, 10],
    "order_lengths": [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67],
    "order_quantities": [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17]
}

# Compare ACO and GA
aco_results = run_algorithm(novel_aco, {**problem_params, "generations": 100, "num_ants": 20})
ga_results = run_algorithm(novel_ga, {**problem_params, "population_size": 100, "generations": 50})

# Converting results to DataFrame
aco_df = pd.DataFrame(aco_results)
ga_df = pd.DataFrame(ga_results)

# Statistical Analysis
aco_mean_cost = np.mean(aco_df['cost'])
ga_mean_cost = np.mean(ga_df['cost'])
aco_mean_time = np.mean(aco_df['time'])
ga_mean_time = np.mean(ga_df['time'])

print(f"ACO Mean Cost: {aco_mean_cost} vs GA Mean Cost: {ga_mean_cost}")
print(f"ACO Mean Time: {aco_mean_time}s vs GA Mean Time: {ga_mean_time}s")

# Visualization
plt.figure(figsize=(12, 6))
sns.histplot(aco_df['cost'], color='blue', label='ACO Cost', kde=True)
sns.histplot(ga_df['cost'], color='red', label='GA Cost', kde=True)
plt.legend()
plt.title('Cost Distribution Comparison')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(aco_df['time'], color='blue', label='ACO Time', kde=True)
sns.histplot(ga_df['time'], color='red', label='GA Time', kde=True)
plt.legend()
plt.title('Time Distribution Comparison')
plt.show()

# Decision on Winning Solution
if aco_mean_cost < ga_mean_cost:
    print("ACO is the winning solution based on lower average cost.")
elif ga_mean_cost < aco_mean_cost:
    print("GA is the winning solution based on lower average cost.")
else:
    print("Both algorithms perform similarly in cost. Comparing based on time efficiency...")
    if aco_mean_time < ga_mean_time:
        print("ACO is also more time efficient.")
    else:
        print("GA is more time efficient.")
