from kmeans import Kmeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
X, _ = make_blobs(n_samples=100, centers=3, random_state=42)
model = Kmeans(max_iter=100,k=3,tol=0.0001)
model.fit(x=X)
labels = model.assign(X=X)
print(f'the centroid received are {model.centroid}')

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(model.centroid[:, 0], model.centroid[:, 1], 
            c='red', marker='X', s=200)
plt.title("KMeans From Scratch")
plt.savefig("results.png")
print("Plot saved as results.png")
