import pandas as pd
import numpy as np
import umap
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load and preprocess your data (as you've done before)
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

input_data = np.array(nonzero_reduced_matrix)
input_labels = np.array(updated_labels)

# Perform UMAP
n_components = 2  # You can change this to the number of components you need
umap_model = umap.UMAP(n_components=n_components)

# Fit and transform the data using UMAP
umap_embedding = umap_model.fit_transform(input_data)

# Create a DataFrame for the UMAP components
umap_df = pd.DataFrame(data=umap_embedding, columns=['UMAP Dimension 1', 'UMAP Dimension 2'])

# Create a list of colors based on binary labels (0 and 1)
point_colors = ['red' if label == 0 else 'blue' for label in input_labels]

# Plot the UMAP Results with colored data points
plt.figure(figsize=(10, 6))
plt.scatter(umap_df['UMAP Dimension 1'], umap_df['UMAP Dimension 2'], c=point_colors, alpha=0.5)
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.title('UMAP Visualization of Embedded Input Data (Colored by Labels)')
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
plt.savefig('umap_plot.png')

# Show the plot
plt.show()
