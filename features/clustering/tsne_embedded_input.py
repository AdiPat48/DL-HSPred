import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load and preprocess your data (as you've done before)
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

# Transpose the input data
input_data = np.array(nonzero_reduced_matrix)
input_labels = np.array(updated_labels)

# Perform t-SNE
n_components = 2  # You can change this to the number of components you need
tsne = TSNE(n_components=n_components)

# Fit and transform the data using t-SNE
tsne_components = tsne.fit_transform(input_data)

# Create a DataFrame for the t-SNE components
tsne_df = pd.DataFrame(data=tsne_components, columns=['Dimension 1', 'Dimension 2'])

# Print the number of points and dimensions
num_points = len(tsne_df)
num_dimensions = tsne_df.shape[1]
print(f"Number of points: {num_points}")
print(f"Number of dimensions: {num_dimensions}")

# Create a list of colors based on binary labels (0 and 1)
point_colors = ['red' if label == 0 else 'blue' for label in input_labels]

# Plot the t-SNE Results with colored data points
plt.figure(figsize=(10, 6))
plt.scatter(tsne_df['Dimension 1'], tsne_df['Dimension 2'], c=point_colors, alpha=0.5)
plt.xlabel('Dimension 1 (t-SNE)')
plt.ylabel('Dimension 2 (t-SNE)')
plt.title('t-SNE Visualization of Transposed Embedded Input Data (Colored by Labels)')
plt.grid(True)

# Add a legend for label-color mapping
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Label 0',
               markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Label 1',
               markerfacecolor='blue', markersize=10)
]
plt.legend(handles=legend_elements)

# Save the plot as a PNG file
plt.savefig('tsne_plot_transposed.png')

# Show the plot
plt.show()
