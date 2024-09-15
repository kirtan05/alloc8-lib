import matplotlib.pyplot as plt
#from spherecluster import SphericalKMeans
import numpy as np
from sklearn.cluster import KMeans
'''
points = np.array([[5, 3], [10, 15], [15, 12], [24, 10], [30, 45], [85, 70], [71, 80], [60, 78], [55, 52],[80, 91]])

xs = points[:,0] # Selects all xs from the array
ys = points[:,1]  # Selects all ys from the array
plt.title("10 Stores Coordinates")
plt.scatter(x=xs, y=ys)

#skm = SphericalKMeans(n_clusters=K)
#skm.fit(X)


# The random_state needs to be the same number to get reproducible results
kmeans = KMeans(n_clusters=2,n_init="auto").fit(points) 
kmeans.labels_

'''

from sklearn.cluster import KMeans
import numpy as np
X = np.array([[1, 2], [1, 4], [1, 0],
              [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)
kmeans.labels_
kmeans.predict([[0, 0], [12, 3]])
kmeans.cluster_centers_