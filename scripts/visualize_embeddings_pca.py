# To run:
# pip3 install scikit-learn matplotlib pca

import json

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
with open('bbc_descriptions_with_embeddings.json', 'r') as f:
    data = json.load(f)

# Step 2: Extract the embeddings
embeddings = np.array([item['embedding'] for item in data.values()])
labels = [ name for name in data.keys() ]
print(labels)

# Step 3: Initialize PCA to reduce dimensionality (e.g., to 2 dimensions)
pca = PCA(n_components=2)

# Step 4: Fit and transform the embeddings
reduced_embeddings = pca.fit_transform(embeddings)

# Step 5: Print or use the reduced embeddings
print("Reduced Embeddings:\n", reduced_embeddings)

# Optional: Explained variance ratio
print("Explained Variance Ratio:", pca.explained_variance_ratio_)


plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c='blue', edgecolor='k')

# Add labels for each point
for i, label in enumerate(labels):
    plt.annotate(
        label, 
        (reduced_embeddings[i, 0], reduced_embeddings[i, 1]), 
        textcoords="offset points", 
        xytext=(0,5), 
        ha='center'
    )

plt.title('2D PCA of Embeddings')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()