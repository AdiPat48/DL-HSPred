# import pandas as pd
# import numpy as np
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt

# # Load and preprocess your data (as you've done before)
# scaler = StandardScaler()
# df = pd.read_csv('embedded_input.csv')
# nonzero_reduced_matrix = df.iloc[:, 1:-1]
# updated_labels = df.iloc[:, -1]

# input_data = scaler.fit_transform(np.array(nonzero_reduced_matrix))
# input_labels = np.array(updated_labels)

# # Perform PCA
# n_components = 2  # You can change this to the number of components you need
# pca = PCA(n_components=n_components)

# # Fit and transform the data
# principal_components = pca.fit_transform(input_data)

# # Create a DataFrame for the Principal Components
# principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# # Create a list of colors based on binary labels (0 and 1)
# point_colors = ['red' if label == 0 else 'blue' for label in input_labels]

# # Plot the PCA Results with colored data points
# plt.figure(figsize=(10, 6))
# plt.scatter(principal_df['PC1'], principal_df['PC2'], c=point_colors, alpha=0.5)
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.title('PCA of Embedded Input Data (Colored by Labels)')
# plt.grid(True)

# # Add a legend for label-color mapping
# legend_elements = [
#     plt.Line2D([0], [0], marker='o', color='w', label='Label 0',
#                markerfacecolor='red', markersize=10),
#     plt.Line2D([0], [0], marker='o', color='w', label='Label 1',
#                markerfacecolor='blue', markersize=10)
# ]
# plt.legend(handles=legend_elements)

# plt.show()

import pandas as pd
import numpy as np
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load and preprocess your data (as you've done before)
scaler = StandardScaler()
df = pd.read_csv('embedded_input.csv')
nonzero_reduced_matrix = df.iloc[:, 1:-1]
updated_labels = df.iloc[:, -1]

input_data = np.array(nonzero_reduced_matrix)
input_labels = np.array(updated_labels)

# Perform Kernel PCA with an RBF kernel
n_components = 2  # You can change this to the number of components you need
kpca = KernelPCA(n_components=n_components, kernel='cosine')

# Fit and transform the data using Kernel PCA
principal_components = kpca.fit_transform(input_data)

# Create a DataFrame for the Principal Components
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Create a list of colors based on binary labels (0 and 1)
point_colors = ['red' if label == 0 else 'blue' for label in input_labels]

# Plot the Kernel PCA Results with colored data points
plt.figure(figsize=(10, 6))
plt.scatter(principal_df['PC1'], principal_df['PC2'], c=point_colors, alpha=0.5)
plt.xlabel('Principal Component 1 (Kernel PCA)')
plt.ylabel('Principal Component 2 (Kernel PCA)')
plt.title('Kernel PCA of Embedded Input Data (Colored by Labels)')
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
plt.savefig('kernel_pca_plot.png')

# Show the plot
plt.show()


