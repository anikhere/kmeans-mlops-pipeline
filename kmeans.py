import numpy as np
class Kmeans:
    def __init__(self,k=3,max_iter=100,tol = 1e-4):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.centroid = None
    
    def _euclidian(self,a:np.array,b:np.array):
        distance = (a-b)**2
        dis = np.sum(distance)
        euclide = np.sqrt(dis)
        return euclide
    
    def fit(self,x:np.array):
        x_shape= x.shape[0]
        indices = np.random.choice(x_shape,self.k,replace=False)
        self.centroid = x[indices]
        for _ in range(self.max_iter):
           label =  self.assign(x)
           old_centroid = self.centroid.copy()
           self.update(x,label)
           movement = np.max(np.abs(self.centroid - old_centroid))
           if movement < self.tol:
              break
    
    def assign(self,X:np.array):
        labels = []
        for x in range(X.shape[0]):
            distances = []
            for cent in self.centroid:
                distances.append(self._euclidian(X[x],cent))
            label = np.argmin(distances)
            labels.append(label)
        return np.array(labels)
    
    def update(self,X:np.array,label):
        for k in range(self.k):
            mask = label == k
            point = X[mask]
            mean_val = np.mean(point,axis=0)
            self.centroid[k] = mean_val
    



