import matplotlib.pyplot as plt

# Algorithms to compare
algorithms = [
    "YourAlgorithm", 
    "NMF", 
    "SVD", 
    "KNNBasic", 
    "SlopeOne"
]

# RMSE and MAE values for each algorithm
rmse_values = [0.89, 0.92, 0.87, 0.94, 0.91]
mae_values = [0.68, 0.71, 0.65, 0.72, 0.70]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(algorithms, rmse_values, marker='o', label='RMSE', color='green')
plt.plot(algorithms, mae_values, marker='o', label='MAE', color='blue')

# Add labels, title, and legend
plt.title('Comparison of Algorithms on RMSE and MAE')
plt.xlabel('Algorithms')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Save and display the plot
output_path = "algorithm_comparison.png"
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Graph saved as: {output_path}")
