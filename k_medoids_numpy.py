"""
A Numpy K-Medoids implementation

Methodology for the K-Medoids algorithm:

    Choose value for K
    Randomly select K featuresets to start as your centroids
    Calculate distance of all other featuresets to centroids
    Classify other featuresets as same as closest centroid
    Determine point within centroid that minimizes within-cluster distance function, making that
    the new centroid
    Repeat steps 3-5 until optimized (centroids no longer moving)
"""
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from k_means.make_clusters import SAMPLE_DATA
from k_means.k_means_numpy import KMeans


class KMedoids(KMeans):
    def __init__(self, k: int = 2, tol: float = 0.001, max_iter: int = 300,
                 method: str = 'euclidean'):
        super().__init__(k, tol, max_iter, method)

    def update_centroids(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        old_centroids = self.centroids.copy()
        for cluster in range(self.k):
            in_cluster = np.where(self.clusters == cluster)
            distance_matrix = self.get_distance_vec(data[in_cluster], data[in_cluster]).sum(axis=0)
            min_wcss = np.argmin(distance_matrix)
            self.centroids[cluster, :] = data[in_cluster][min_wcss]
        new_centroids = self.centroids.copy()
        return old_centroids, new_centroids

    # def within_cluster(self, centroids, data) -> float:
    #     pass

    def plot(self) -> None:
        """Plot clusters and circles medoid in red"""
        for cluster in range(self.k):
            cluster_filter = self.assignments[:, 0] == cluster
            plt.scatter(self.assignments[cluster_filter, 1],
                        self.assignments[cluster_filter, 2],
                        alpha=0.5)
        for point in self.centroids:
            plt.scatter(point[0], point[1], marker='o', edgecolors='r', facecolors='none')
        plt.show()


def main():
    """Main function"""
    kmedoids = KMedoids(k=3)
    kmedoids.fit(SAMPLE_DATA).plot()


if __name__ == '__main__':
    main()