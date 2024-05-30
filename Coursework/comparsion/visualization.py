import matplotlib.pyplot as plt# type: ignore
import seaborn as sns# type: ignore
import pandas as pd# type: ignore
import numpy as np # type: ignore

# Sample data: Mock results from ACO and GA experiments
data = {
    'Algorithm': ['ACO', 'ACO', 'ACO', 'GA', 'GA', 'GA'],
    'Stock Length': [4300, 4150, 3500, 4300, 4150, 3500],
    'Cost Efficiency': [4500, 4400, 4000, 4300, 4250, 3900],
    'Waste Minimization': [50, 45, 40, 55, 50, 45],
    'Time Efficiency (s)': [200, 190, 180, 210, 205, 195]
}

df = pd.DataFrame(data)

# Plotting Cost Efficiency
plt.figure(figsize=(10, 6))
sns.barplot(x='Stock Length', y='Cost Efficiency', hue='Algorithm', data=df)
plt.title('Cost Efficiency Comparison Between ACO and GA')
plt.ylabel('Cost Efficiency ($)')
plt.xlabel('Stock Length')
plt.legend(title='Algorithm')
plt.show()

# Plotting Waste Minimization
plt.figure(figsize=(10, 6))
sns.barplot(x='Stock Length', y='Waste Minimization', hue='Algorithm', data=df)
plt.title('Waste Minimization Comparison Between ACO and GA')
plt.ylabel('Waste Minimization (units)')
plt.xlabel('Stock Length')
plt.legend(title='Algorithm')
plt.show()

# Plotting Time Efficiency
plt.figure(figsize=(10, 6))
sns.barplot(x='Stock Length', y='Time Efficiency (s)', hue='Algorithm', data=df)
plt.title('Time Efficiency Comparison Between ACO and GA')
plt.ylabel('Time Efficiency (seconds)')
plt.xlabel('Stock Length')
plt.legend(title='Algorithm')
plt.show()
