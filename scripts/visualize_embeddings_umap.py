# To run:
# pip3 install scikit-learn matplotlib umap-learn

import json
import numpy as np
import matplotlib.pyplot as plt
import umap

# Step 1: Load the JSON file
with open('bbc_descriptions_with_embeddings.json', 'r') as f:
    data = json.load(f)

# Step 2: Extract the embeddings and optionally labels
embeddings = np.array([item['embedding'] for item in data.values()])
labels = [ name for name in data.keys() ]

# Step 3: Initialize UMAP to reduce dimensionality (e.g., to 2 dimensions)
umap_model = umap.UMAP(n_components=2, random_state=42)

# Step 4: Fit and transform the embeddings
reduced_embeddings = umap_model.fit_transform(embeddings)

# Step 5: Plot the reduced embeddings with labels
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

plt.title('2D UMAP of Embeddings')
plt.xlabel('UMAP Component 1')
plt.ylabel('UMAP Component 2')
plt.grid(True)
plt.show()